from app.database.mongodb import get_database
from app.schemas.exercise_schema import ExercisePublic, ExerciseResult


async def get_exercise_for_course(course_id: str) -> ExercisePublic:
    db = get_database()
    exercise = await db.exercises.find_one({"course_id": course_id})
    if exercise is None:
        raise ValueError(f"Aucun exercice trouvé pour le cours '{course_id}'")

    check_x = [point[0] for point in exercise["check_points"]]

    return ExercisePublic(
        id=exercise["_id"],
        course_id=exercise["course_id"],
        type=exercise["type"],
        instructions=exercise["instructions"],
        given_points=exercise["given_points"],
        check_x=check_x,
    )


async def submit_exercise(
    course_id: str, student_id: str, submitted_points: list[list[float]]
) -> ExerciseResult:
    db = get_database()
    exercise = await db.exercises.find_one({"course_id": course_id})
    if exercise is None:
        raise ValueError(f"Aucun exercice trouvé pour le cours '{course_id}'")

    check_points = exercise["check_points"]
    tolerance = exercise["tolerance"]

    if len(submitted_points) != len(check_points):
        raise ValueError(
            f"{len(check_points)} points attendus, {len(submitted_points)} reçus"
        )

    details = []
    all_ok = True
    for (expected_x, expected_y), (given_x, given_y) in zip(check_points, submitted_points):
        ok = abs(given_y - expected_y) <= tolerance
        all_ok = all_ok and ok
        details.append({
            "x": expected_x,
            "expected_y": expected_y,
            "given_y": given_y,
            "ok": ok,
        })

    course = await db.courses.find_one({"_id": course_id})
    module_id = course["module_id"] if course else None

    if module_id:
        await db.student_progress.update_one(
            {"student_id": student_id},
            {"$set": {f"modules.{module_id}.exercise_done": all_ok}},
            upsert=True,
        )

    return ExerciseResult(success=all_ok, details=details)
