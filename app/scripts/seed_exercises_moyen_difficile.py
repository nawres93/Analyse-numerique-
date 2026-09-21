import asyncio

from app.database.mongodb import connect_to_mongo, close_mongo_connection, get_database


EXERCISE_MOYEN = {
    "_id": "ex_interpolation_moyen",
    "course_id": "interpolation_moyen",
    "type": "desmos",
    "instructions": (
        "On interpole les points (-2, 10), (-1, 4) et (1, 6) par un polynôme de "
        "Lagrange de degré 2. Explore la courbe sur Desmos (tu peux taper la formule "
        "toi-même si besoin), puis lis la valeur du polynôme à x=0 et x=0.5."
    ),
    "given_points": [[-2, 10], [-1, 4], [1, 6]],
    "check_points": [[0, 2.667], [0.5, 3.75]],
    "tolerance": 0.3,
}

EXERCISE_DIFFICILE = {
    "_id": "ex_interpolation_difficile",
    "course_id": "interpolation_difficile",
    "type": "desmos",
    "instructions": (
        "On interpole les points (0, -1), (2, 1) et (4, 6) par la formule de Newton "
        "(différences divisées). Trace toi-même la parabole correspondante sur Desmos "
        "(tape son équation), puis lis la valeur à x=1 et x=3."
    ),
    "given_points": [[0, -1], [2, 1], [4, 6]],
    "check_points": [[1, -0.375], [3, 3.125]],
    "tolerance": 0.5,
}


async def seed():
    await connect_to_mongo()
    db = get_database()

    for exercise in [EXERCISE_MOYEN, EXERCISE_DIFFICILE]:
        await db.exercises.delete_many({"course_id": exercise["course_id"]})
        await db.exercises.insert_one(exercise)
        print(f"Exercice '{exercise['course_id']}' inséré.")

    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(seed())
