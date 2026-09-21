from fastapi import APIRouter, Depends, HTTPException

from app.schemas.quiz import QuizPublic, QuizSubmission, PlacementResult, FinalQuizResult
from app.schemas.learning_course import CourseContentPublic
from app.schemas.exercise_schema import ExercisePublic, ExerciseSubmission, ExerciseResult
from app.services import placement_service, course_content_service, exercise_service, final_quiz_service
from app.dependencies.auth import get_current_user

router = APIRouter(tags=["learning"])


@router.get("/modules/{module_id}/placement-quiz", response_model=QuizPublic)
async def get_placement_quiz(module_id: str):
    try:
        return await placement_service.get_placement_quiz(module_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/modules/{module_id}/placement-quiz/submit", response_model=PlacementResult)
async def submit_placement_quiz(
    module_id: str,
    submission: QuizSubmission,
    current_user: dict = Depends(get_current_user),
):
    try:
        return await placement_service.submit_placement_quiz(
            module_id, str(current_user["_id"]), submission.answers
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/courses/{course_id}", response_model=CourseContentPublic)
async def get_course_content(
    course_id: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        return await course_content_service.get_course_content(course_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/courses/{course_id}/exercise", response_model=ExercisePublic)
async def get_exercise(
    course_id: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        return await exercise_service.get_exercise_for_course(course_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/courses/{course_id}/exercise/submit", response_model=ExerciseResult)
async def submit_exercise(
    course_id: str,
    submission: ExerciseSubmission,
    current_user: dict = Depends(get_current_user),
):
    try:
        return await exercise_service.submit_exercise(
            course_id, str(current_user["_id"]), submission.submitted_points
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/courses/{course_id}/final-quiz", response_model=QuizPublic)
async def get_final_quiz(course_id: str):
    try:
        return await final_quiz_service.get_final_quiz(course_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/courses/{course_id}/final-quiz/submit", response_model=FinalQuizResult)
async def submit_final_quiz(
    course_id: str,
    submission: QuizSubmission,
    current_user: dict = Depends(get_current_user),
):
    try:
        return await final_quiz_service.submit_final_quiz(
            course_id, str(current_user["_id"]), submission.answers
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
