from fastapi import APIRouter, HTTPException
from app.schemas.agents_schemas import (
    RefinementRequest, SearchRequest, SugerenceRequest, 
    ConstructionRequest, QueryGraphRequest, 
    ErrorResponse, SuccessResponse
)
from app.run import (
    run_refinement, run_search, run_sugerence, 
    run_construction, query_graph
)

router = APIRouter()

@router.post("/run-refinement", response_model=SuccessResponse)
async def refinement_endpoint(request: RefinementRequest):
    result = run_refinement(request.topic)
    if not result:
        raise HTTPException(status_code=400, detail="Refinement process failed")
    return SuccessResponse(data=result)

@router.post("/run-search", response_model=SuccessResponse)
async def search_endpoint(request: SearchRequest):
    result = run_search(
        request.queries,
        max_results=request.max_results,
        sort_by=request.sort_by
    )
    if not result:
        raise HTTPException(status_code=400, detail="Search process failed")
    return SuccessResponse(data=result)

@router.post("/run-sugerence", response_model=SuccessResponse)
async def sugerence_endpoint(request: SugerenceRequest):
    result = run_sugerence(request.papers)
    if not result:
        raise HTTPException(status_code=400, detail="Sugerence process failed")
    return SuccessResponse(data=result)

@router.post("/run-construction", response_model=SuccessResponse)
async def construction_endpoint(request: ConstructionRequest):
    result = run_construction(request.papers)
    if not result:
        raise HTTPException(status_code=400, detail="Construction process failed")
    return SuccessResponse(data={"message": "Operation completed successfully"})

@router.post("/query-graph", response_model=SuccessResponse)
async def query_graph_endpoint(request: QueryGraphRequest):
    result = query_graph(request.topic)
    if not result:
        raise HTTPException(status_code=400, detail="Query graph process failed")
    return SuccessResponse(data=result)


