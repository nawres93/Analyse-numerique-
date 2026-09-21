import asyncio

from app.database.mongodb import connect_to_mongo, close_mongo_connection, get_database


# Exercice pour interpolation_facile : interpolation linéaire entre 2 points.
# L'étudiant doit tracer la droite passant par (0,20) et (10,35) sur Desmos,
# puis on vérifie la valeur qu'il obtient à x=4 (attendu : y=26, cf. l'exercice
# du cours facile).
EXERCISE_FACILE = {
    "_id": "ex_interpolation_facile",
    "course_id": "interpolation_facile",
    "type": "desmos",
    "instructions": (
        "Un capteur donne : à t=0s, T=20°C ; à t=10s, T=35°C. "
        "Trace la droite d'interpolation linéaire passant par ces deux points sur "
        "Desmos, puis lis la valeur de T à t=4s et t=7s."
    ),
    "given_points": [[0, 20], [10, 35]],
    "check_points": [[4, 26], [7, 30.5]],
    "tolerance": 0.5,
}


async def seed():
    await connect_to_mongo()
    db = get_database()

    await db.exercises.delete_many({"course_id": "interpolation_facile"})
    await db.exercises.insert_one(EXERCISE_FACILE)
    print("Exercice 'interpolation_facile' inséré.")

    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(seed())
