import asyncio
import redis.asyncio as aioredis
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ares.config import get_settings

router = APIRouter()

@router.websocket("/runs/{run_id}/stream")
async def stream_run_status(websocket: WebSocket, run_id: str):
    await websocket.accept()
    
    settings = get_settings()
    
    try:
        redis_client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        pubsub = redis_client.pubsub()
        channel = f"agent_run_{run_id}"
        await pubsub.subscribe(channel)
    except Exception as e:
        await websocket.close(code=1011, reason="Failed to connect to Redis")
        return

    async def reader(ps, ws: WebSocket):
        try:
            async for message in ps.listen():
                if message["type"] == "message":
                    await ws.send_text(message["data"])
        except Exception:
            pass

    # Start the task to read from Redis and push to the WebSocket
    task = asyncio.create_task(reader(pubsub, websocket))

    try:
        # Keep connection open and wait for client to disconnect
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        task.cancel()
        await pubsub.unsubscribe(channel)
        await redis_client.aclose()
