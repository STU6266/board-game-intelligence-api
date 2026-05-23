from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories import report_repository
from app.schemas.report import (
    FamilyFriendlyGameResponse,
    LowComplexityHighRatingGameResponse,
)
from app.services.report_service import (
    build_family_friendly_report,
    build_low_complexity_high_rating_report,
)

router = APIRouter(prefix="/reports")


@router.get("/family-friendly", response_model=list[FamilyFriendlyGameResponse])
def get_family_friendly_games(db: Session = Depends(get_db)):
    games = report_repository.get_games_for_reports(db)

    return build_family_friendly_report(games)


@router.get(
    "/low-complexity-high-rating",
    response_model=list[LowComplexityHighRatingGameResponse],
)
def get_low_complexity_high_rating_games(db: Session = Depends(get_db)):
    games = report_repository.get_games_for_reports(db)

    return build_low_complexity_high_rating_report(games)