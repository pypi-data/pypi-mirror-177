from typing import List

from fastapi import APIRouter, Query, Request
from pydantic import Required

from ...db.utils import get_all_meeting_points
from ...models.municipality import MuncipalityWithDistance, Municipality
from ...services.search_meeting_points import search_close_meeting_points

router = APIRouter()


@router.get(
    "/MeetingPointsFromPosition",
    response_model=List[MuncipalityWithDistance],
    responses={
        200: {
            "description": "Meeting Points successfully found",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "201",
                            "name": "Mairie ANNEXE LILLE-SECLIN",
                            "longitude": 3.0348016639327,
                            "latitude": 50.549140395451,
                            "public_entry_address": "89 RUE ROGER BOUVRY 59113 SECLIN",
                            "zip_code": "59113",
                            "city_name": "SECLIN",
                            "website": "http://www.ville-seclin.fr",
                            "city_logo": "https://www.ville-seclin.fr/images/logo-ville-seclin/logo_ville_de_seclin.png",
                            "distance_km": 1.56,
                        }
                    ]
                }
            },
        }
    },
)
def meeting_points_from_position(
    request: Request,
    longitude: float = Query(default=Required, example=2.352222),
    latitude: float = Query(default=Required, example=48.856613),
    radius_km: int = Query(default=20, enum=[20, 40, 60]),
) -> List[MuncipalityWithDistance]:
    """
    Search Meeting Point from position.
    """
    all_points: List[Municipality] = get_all_meeting_points()
    meeting_points: List[MuncipalityWithDistance] = search_close_meeting_points(
        all_points, latitude, longitude, radius_km
    )
    return meeting_points
