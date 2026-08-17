import asyncio
import json
import logging
from uuid import UUID
from datetime import datetime, timezone

import redis.asyncio as aioredis
from sqlalchemy import select

from ares.worker.celery_app import celery_app
from ares.domain.enums import AgentRunStatus, AgentStage
from ares.db.engine import async_session_maker
from ares.db.tables import AgentRun
from ares.config import get_settings

logger = logging.getLogger(__name__)

async def _publish_status(redis_client, run_id: str, status: str, stage: str | None = None) -> None:
    message = json.dumps({"run_id": run_id, "status": status, "stage": stage})
    await redis_client.publish(f"agent_run_{run_id}", message)
    logger.info(f"Published to agent_run_{run_id}: {message}")

async def _execute_workflow_async(run_id_str: str) -> None:
    """Async implementation of the workflow state machine."""
    logger.info(f"Starting workflow for run_id: {run_id_str}")
    run_id = UUID(run_id_str)
    settings = get_settings()
    redis_client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    
    try:
        async with async_session_maker() as session:
            stmt = select(AgentRun).where(AgentRun.id == run_id)
            result = await session.execute(stmt)
            agent_run = result.scalar_one_or_none()
            
            if not agent_run:
                logger.error(f"AgentRun {run_id} not found.")
                return

            if agent_run.status == AgentRunStatus.CANCELLED:
                logger.info(f"AgentRun {run_id} was cancelled before starting.")
                return
            
            agent_run.status = AgentRunStatus.RUNNING
            agent_run.started_at = datetime.now(timezone.utc)
            await session.commit()
            await _publish_status(redis_client, run_id_str, agent_run.status, agent_run.current_stage)

            stages = [
                AgentStage.PLANNING,
                AgentStage.PLAN_REVIEW,
                AgentStage.DISCOVERING,
                AgentStage.ACQUIRING,
                AgentStage.PROCESSING,
                AgentStage.EXTRACTING,
                AgentStage.VALIDATING,
                AgentStage.DEDUPLICATING,
                AgentStage.CONFLICT_RESOLUTION,
                AgentStage.REVIEW,
                AgentStage.PUBLISHING,
            ]
            
            start_idx = 0
            if agent_run.current_stage in stages:
                start_idx = stages.index(agent_run.current_stage)

            for stage in stages[start_idx:]:
                # Check cancellation
                await session.refresh(agent_run)
                if agent_run.status == AgentRunStatus.CANCELLED:
                    logger.info(f"Run {run_id} cancelled at stage {stage}")
                    return

                # If paused, stop processing and wait for resume
                if agent_run.status == AgentRunStatus.PAUSED:
                    logger.info(f"Run {run_id} paused at stage {stage}")
                    return
                
                # Check if review is required
                if stage in (AgentStage.PLAN_REVIEW, AgentStage.REVIEW):
                    agent_run.status = AgentRunStatus.REQUIRES_REVIEW
                    agent_run.current_stage = stage
                    await session.commit()
                    await _publish_status(redis_client, run_id_str, agent_run.status, stage)
                    # Stop workflow, wait for approve endpoint to resume
                    return

                agent_run.current_stage = stage
                agent_run.status = AgentRunStatus.RUNNING
                await session.commit()
                await _publish_status(redis_client, run_id_str, agent_run.status, stage)
                
                # Simulate work
                await asyncio.sleep(2)
                
            agent_run.current_stage = AgentStage.COMPLETED
            agent_run.status = AgentRunStatus.COMPLETED
            agent_run.completed_at = datetime.now(timezone.utc)
            await session.commit()
            await _publish_status(redis_client, run_id_str, agent_run.status, agent_run.current_stage)

    except Exception as e:
        logger.error(f"Workflow error for {run_id}: {e}")
        async with async_session_maker() as session:
            stmt = select(AgentRun).where(AgentRun.id == run_id)
            result = await session.execute(stmt)
            agent_run = result.scalar_one_or_none()
            if agent_run:
                agent_run.status = AgentRunStatus.FAILED
                agent_run.error_details = str(e)
                await session.commit()
                await _publish_status(redis_client, run_id_str, agent_run.status, agent_run.current_stage)
        raise e
    finally:
        await redis_client.aclose()

@celery_app.task(bind=True, name="ares.worker.tasks.execute_workflow")
def execute_workflow(self, run_id: str) -> dict:
    """
    Celery task that acts as a state machine for an AgentRun.
    """
    try:
        asyncio.run(_execute_workflow_async(run_id))
        return {"status": "success", "run_id": run_id}
    except Exception as e:
        logger.error(f"Error executing workflow for {run_id}: {e}")
        raise e
