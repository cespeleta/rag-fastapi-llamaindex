"""API health router definition."""

from fastapi import APIRouter, status

from app.api.v1.schemas import HealthCheckResponseStatus

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheckResponseStatus,
    include_in_schema=False,
)
def get_health() -> HealthCheckResponseStatus:
    """Perform a Health Check.

    This endpoint can primarily be used by Docker to ensure a robust container
    orchestration and management is in place.

    Returns:
        HealthCheckResponseStatus: Returns a JSON response with the health status
    """
    return HealthCheckResponseStatus(status="OK")
