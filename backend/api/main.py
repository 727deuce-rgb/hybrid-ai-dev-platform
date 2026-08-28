#!/usr/bin/env python3
"""
DRACO-4 Backend API
Production-ready FastAPI server for hybrid AI development platform
"""

from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import asyncio
import json
from datetime import datetime
import uvicorn

# Import DRACO-4 orchestrator
import sys
sys.path.insert(0, '../draco-4/core')
from draco4_orchestrator import DRACO4Orchestrator, TaskMessage, NeuralPattern

app = FastAPI(
    title="DRACO-4 Hybrid AI Platform",
    description="Production orchestration engine with multi-agent support",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global orchestrator instance
orchestrator: Optional[DRACO4Orchestrator] = None


class TaskRequest(BaseModel):
    """Task request schema"""
    task_id: str
    target_agent: str
    payload: Dict[str, Any]
    pattern: str
    priority: int = 5
    requires_response: bool = True


class AgentStatusResponse(BaseModel):
    """Agent status response schema"""
    agent_id: str
    role: str
    pattern: str
    metrics: Dict[str, Any]
    queue_size: int
    task_history_size: int


@app.on_event("startup")
async def startup_event():
    """Initialize DRACO-4 orchestrator on startup"""
    global orchestrator
    orchestrator = DRACO4Orchestrator()
    await orchestrator.initialize()
    print("\n=== DRACO-4 Backend API Started ===")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Orchestrator Status: {'Active' if orchestrator.initialized else 'Inactive'}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("\nDRACO-4 Backend API shutting down...")


# ============================================================================
# SYSTEM ENDPOINTS
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "orchestrator": "active" if orchestrator and orchestrator.initialized else "inactive"
    }


@app.get("/api/system/status")
async def get_system_status():
    """Get complete system status"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    return orchestrator.get_system_status()


# ============================================================================
# AGENT ENDPOINTS
# ============================================================================

@app.get("/api/agents")
async def list_agents():
    """List all agents"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    return {
        "agents": list(orchestrator.agents.keys()),
        "count": len(orchestrator.agents)
    }


@app.get("/api/agents/{agent_id}")
async def get_agent_status(agent_id: str):
    """Get specific agent status"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    agent = orchestrator.agents.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    
    return agent.get_status()


# ============================================================================
# TASK ROUTING ENDPOINTS
# ============================================================================

@app.post("/api/tasks/route")
async def route_task(request: TaskRequest):
    """Route a single task to appropriate agent"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    try:
        # Convert pattern string to enum
        pattern = NeuralPattern[request.pattern.upper()]
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Unknown pattern: {request.pattern}")
    
    msg = TaskMessage(
        task_id=request.task_id,
        source_agent="api",
        target_agent=request.target_agent,
        payload=request.payload,
        pattern=pattern,
        timestamp=datetime.now().timestamp(),
        priority=request.priority,
        requires_response=request.requires_response
    )
    
    result = await orchestrator.route_message(msg)
    return result


@app.post("/api/tasks/broadcast")
async def broadcast_task(request: TaskRequest):
    """Broadcast task to all pillar agents"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    try:
        pattern = NeuralPattern[request.pattern.upper()]
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Unknown pattern: {request.pattern}")
    
    msg = TaskMessage(
        task_id=request.task_id,
        source_agent="api",
        target_agent="all_pillars",
        payload=request.payload,
        pattern=pattern,
        timestamp=datetime.now().timestamp(),
        priority=request.priority,
        requires_response=request.requires_response
    )
    
    results = await orchestrator.broadcast_to_pillars(msg)
    return {
        "broadcast_id": request.task_id,
        "results": results,
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# MINI-STACK APPLICATION ENDPOINTS
# ============================================================================

@app.get("/api/apps")
async def list_apps():
    """List all mini-stack applications"""
    return {
        "apps": [
            {
                "id": "app_1",
                "name": "Perceptron Decision Engine",
                "pattern": "monad",
                "nodes": 1,
                "params": 12
            },
            {
                "id": "app_2",
                "name": "Comparative Analyzer",
                "pattern": "dyad",
                "nodes": 2,
                "params": 256
            },
            {
                "id": "app_3",
                "name": "Triangle Validator",
                "pattern": "triad",
                "nodes": 3,
                "params": 1024
            },
            {
                "id": "app_4",
                "name": "DRACO-4 Hub",
                "pattern": "tetrad",
                "nodes": 4,
                "params": 4096
            },
            {
                "id": "app_5",
                "name": "Pentagon Expander",
                "pattern": "pentad",
                "nodes": 5,
                "params": 8192
            }
        ],
        "total": 5
    }


@app.post("/api/apps/{app_id}/execute")
async def execute_app(app_id: str, payload: Dict[str, Any]):
    """Execute specific mini-stack application"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    # Route to appropriate pillar based on app
    app_routing = {
        "app_1": ("pillar_north", NeuralPattern.PERCEPTRON),
        "app_2": ("pillar_north", NeuralPattern.FEED_FORWARD),
        "app_3": ("pillar_east", NeuralPattern.RECURRENT),
        "app_4": ("draco_leader", NeuralPattern.LSTM),
        "app_5": ("pillar_west", NeuralPattern.AUTOENCODER),
    }
    
    if app_id not in app_routing:
        raise HTTPException(status_code=404, detail=f"Application {app_id} not found")
    
    target_agent, pattern = app_routing[app_id]
    
    msg = TaskMessage(
        task_id=f"{app_id}_{datetime.now().timestamp()}",
        source_agent="api",
        target_agent=target_agent,
        payload=payload,
        pattern=pattern,
        timestamp=datetime.now().timestamp()
    )
    
    result = await orchestrator.route_message(msg)
    return {
        "app_id": app_id,
        "execution_result": result,
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# METRICS & ANALYTICS ENDPOINTS
# ============================================================================

@app.get("/api/metrics/summary")
async def get_metrics_summary():
    """Get overall system metrics"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    status = orchestrator.get_system_status()
    total_tasks = sum(
        agent['metrics']['tasks_processed']
        for agent in status['agents'].values()
    )
    avg_response_time = sum(
        agent['metrics']['avg_response_time_ms']
        for agent in status['agents'].values()
    ) / len(status['agents'])
    
    return {
        "total_tasks_processed": total_tasks,
        "avg_response_time_ms": avg_response_time,
        "active_agents": status['total_agents'],
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/metrics/agents")
async def get_agent_metrics():
    """Get metrics for all agents"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    status = orchestrator.get_system_status()
    return {
        "agents": {
            agent_id: agent['metrics']
            for agent_id, agent in status['agents'].items()
        },
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# WEBSOCKET ENDPOINTS (Real-time Updates)
# ============================================================================

active_connections: List[WebSocket] = []


@app.websocket("/ws/status")
async def websocket_status(websocket: WebSocket):
    """WebSocket endpoint for real-time system status"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # Send status every 2 seconds
            if orchestrator:
                status = orchestrator.get_system_status()
                await websocket.send_json(status)
            await asyncio.sleep(2)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        active_connections.remove(websocket)


# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with API documentation"""
    return {
        "name": "DRACO-4 Hybrid AI Development Platform",
        "version": "1.0.0",
        "description": "Enterprise orchestration engine with multi-agent support",
        "endpoints": {
            "health": "/health",
            "system_status": "/api/system/status",
            "agents_list": "/api/agents",
            "task_routing": "/api/tasks/route",
            "apps_list": "/api/apps",
            "metrics": "/api/metrics/summary"
        },
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
