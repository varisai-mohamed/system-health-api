from fastapi import FastAPI
from fastapi.responses import FileResponse

import asyncio

from app.services.dag_builder import DagBuilder
from app.services.bfs_traversal import BFSTraversal
from app.services.health_checker import HealthChecker
from app.services.health_aggregator import HealthAggregator

from app.validators.dag_validator import DagValidator
from app.utils.logger import logger

from app.models.component import HealthCheckRequest
from app.models.health_response import ( 
    HealthResponse 
)
from app.services.graph_visualizer import GraphVisualizer

from app.exceptions.exception_handler import (
    register_exception_handlers
)


app = FastAPI(
    title="System Health Check API",
    version="1.0.0"
)

register_exception_handlers(app)


@app.get("/")
async def root():
    return {"message": "System Health Check API"}


@app.get("/health")
async def health():
    return {"status": "UP"}


@app.post(
        "/api/v1/system/health",
        response_model= HealthResponse
)
async def check_health(request: HealthCheckRequest):

    logger.info("System health check request received")
    
    DagValidator.validate(request)
    logger.info("Validation successful")


    graph = DagBuilder.build_graph(
        request.components
    )

    root_nodes = [
        component.id
        for component in request.components
        if not component.dependencies
    ]

    bfs_order = BFSTraversal.traverse(
        graph,
        root_nodes
    )

    logger.info(
        f"BFS order: {bfs_order}"
    )

    tasks = [
        HealthChecker.check_component(node)
        for node in bfs_order
    ]

    results = await asyncio.gather(*tasks)

    results = HealthAggregator.propagate_failures(
        request.components,
        results
    )

    overall_status = (
        HealthAggregator.calculate_system_health(results)
    )

    summary = (
        HealthAggregator.build_summary(results)
    )

    image_path = GraphVisualizer.generate_graph(
        request.components,
        results
    )

    logger.info("Health check completed")

    return HealthResponse(
        overall_status= overall_status,
        summary= summary,
        components= results,
        graph_file= image_path
    )
    

@app.post("/api/v1/system/graph")
async def generate_graph(request: HealthCheckRequest):

    logger.info("System health check request received")
    
    DagValidator.validate(request)
    logger.info("Validation successful")


    graph = DagBuilder.build_graph(
        request.components
    )

    root_nodes = [
        component.id
        for component in request.components
        if not component.dependencies
    ]

    bfs_order = BFSTraversal.traverse(
        graph,
        root_nodes
    )

    logger.info(
        f"BFS order: {bfs_order}"
    )

    tasks = [
        HealthChecker.check_component(node)
        for node in bfs_order
    ]

    results = await asyncio.gather(*tasks)

    results = HealthAggregator.propagate_failures(
        request.components,
        results
    )

    image_path = GraphVisualizer.generate_graph(
        request.components,
        results
    )

    logger.info("Health graph completed")

    return FileResponse(
        path= image_path,
        media_type= "image/png",
        filename= image_path.split("/")[-1]
    )
    
