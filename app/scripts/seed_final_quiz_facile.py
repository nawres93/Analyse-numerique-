import asyncio

from app.database.mongodb import connect_to_mongo, close_mongo_connection, get_database


FINAL_QUIZ_FACILE = {
    "_id": "quiz_interpolation_facile_final",
    "quiz_type": "final",
    "module_id": "interpolation",
    "course_id": "interpolation_facile",
    "questions": [
        {
            "question": "Pour f(0)=10 et f(2)=20, l'interpolation linéaire donne f(1) = ?",
            "options": ["10", "15", "20", "30"],
            "correct": 1,
            "notion": "interpolation_lineaire",
            "weight": 1,
        },
        {
            "question": "Pour n+1 points distincts, il existe :",
            "options": [
                "Plusieurs polynômes d'interpolation possibles de degré n",
                "Un unique polynôme d'interpolation de degré ≤ n",
                "Un unique polynôme de degré exactement n+1",
                "Aucun polynôme si les points ne sont pas équidistants",
            ],
            "correct": 1,
            "notion": "unicite_polynome",
            "weight": 1,
        },
        {
            "question": "Le polynôme caractéristique de Lagrange ℓᵢ(x) vaut 1 en x=xᵢ et 0 en :",
            "options": [
                "Tous les autres points x_j (j≠i)",
                "Aucun autre point",
                "x=0 uniquement",
                "Le point milieu de l'intervalle",
            ],
            "correct": 0,
            "notion": "lagrange_base",
            "weight": 1,
        },
        {
            "question": "L'avantage principal de la méthode de Newton sur Lagrange est :",
            "options": [
                "Elle est plus précise",
                "Elle permet d'ajouter un point sans tout recalculer",
                "Elle donne un polynôme différent",
                "Elle fonctionne même avec des points identiques",
            ],
            "correct": 1,
            "notion": "newton_differences_divisees",
            "weight": 1,
        },
        {
            "question": "Avec les points (1,2) et (3,8), quelle est la pente utilisée pour l'interpolation linéaire ?",
            "options": ["2", "3", "6", "8"],
            "correct": 1,
            "notion": "interpolation_lineaire",
            "weight": 1,
        },
    ],
    "scoring": {
        "pass_threshold": 4,   # sur 5 : il faut au moins 4/5 pour passer
    },
}


async def seed():
    await connect_to_mongo()
    db = get_database()

    await db.quizzes.delete_many({"_id": "quiz_interpolation_facile_final"})
    await db.quizzes.insert_one(FINAL_QUIZ_FACILE)
    print("Quiz final 'interpolation_facile' inséré (5 questions, seuil 4/5).")

    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(seed())
