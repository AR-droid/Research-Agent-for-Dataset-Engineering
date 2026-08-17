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

@router.websocket("/demo-run")
async def demo_run(websocket: WebSocket):
    await websocket.accept()
    
    try:
        data = await websocket.receive_json()
        objective = data.get("objective")
        if not objective:
            await websocket.send_json({"type": "ERROR", "message": "No objective provided"})
            await websocket.close()
            return
            
        await websocket.send_json({
            "type": "LOG", 
            "stage": "01",
            "message": "Initializing Research Planner..."
        })
        
        from ares.agents.agents import ResearchPlanner, ResearchDiscovery
        from ares.agents.schemas import ResearchPlannerInput, ResearchDiscoveryInput
        from ares.agents.tools.research_tools import search_sources, retrieve_source
        
        # 1. PLANNER
        planner = ResearchPlanner()
        planner_input = ResearchPlannerInput(objective=objective)
        
        await websocket.send_json({"type": "LOG", "stage": "01", "message": f"Formulating plan for: {objective}"})
        
        try:
            plan = planner.execute(planner_input)
            await websocket.send_json({
                "type": "LOG", 
                "stage": "01", 
                "message": "Plan formulated successfully."
            })
            await websocket.send_json({
                "type": "PLAN",
                "data": plan.model_dump()
            })
        except Exception as e:
            await websocket.send_json({"type": "ERROR", "message": f"Planner failed: {str(e)}"})
            await websocket.close()
            return
            
        # 2. DISCOVERY
        await websocket.send_json({"type": "LOG", "stage": "02", "message": "Initializing Discovery Agent..."})
        discovery = ResearchDiscovery()
        task = plan.tasks[0] if plan.tasks else "Search for relevant papers"
        
        await websocket.send_json({"type": "LOG", "stage": "02", "message": f"Task: {task}"})
        
        discovery_input = ResearchDiscoveryInput(
            task=task,
            queries=[f"{objective} 2024", f"{objective} research"]
        )
        
        try:
            discovery_output = discovery.execute(discovery_input)
            query = discovery_input.queries[0]
            await websocket.send_json({"type": "LOG", "stage": "02", "message": f"Searching DuckDuckGo for: {query}"})
            
            # Wait a tiny bit to simulate processing visually
            await asyncio.sleep(1)
            results = search_sources(query, max_results=2)
            
            for r in results:
                await websocket.send_json({"type": "LOG", "stage": "02", "message": f"Found: {r['title']}"})
                
            scraped_content = ""
            if results:
                url_to_scrape = results[0]['url']
                await websocket.send_json({"type": "LOG", "stage": "02", "message": f"Scraping content from {url_to_scrape}..."})
                scraped_content = retrieve_source(url_to_scrape)
                await websocket.send_json({"type": "LOG", "stage": "02", "message": f"Scraped {len(scraped_content)} characters."})
            else:
                await websocket.send_json({"type": "LOG", "stage": "02", "message": "DuckDuckGo returned no results."})
                
            # 3. RESULTS
            await websocket.send_json({"type": "LOG", "stage": "03", "message": "Synthesizing Results..."})
            await asyncio.sleep(1)
            
            await websocket.send_json({
                "type": "RESULTS",
                "sources": results,
                "content_snippet": scraped_content[:500] if scraped_content else "No content scraped."
            })
            
        except Exception as e:
            await websocket.send_json({"type": "ERROR", "message": f"Discovery failed: {str(e)}"})
            
        await websocket.close()
        
    except WebSocketDisconnect:
        pass
    except Exception as e:
        if websocket.client_state.name == "CONNECTED":
            await websocket.send_json({"type": "ERROR", "message": str(e)})
            await websocket.close()
