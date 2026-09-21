import asyncio

from app.database.mongodb import connect_to_mongo, close_mongo_connection, get_database


FINAL_QUIZ_MOYEN = {
    "_id": "quiz_interpolation_moyen_final",
    "quiz_type": "final",
    "module_id": "interpolation",
    "course_id": "interpolation_moyen",
    "questions": [
        {
            "question": "D'après le théorème de Weierstrass, toute fonction continue sur [a,b] peut être :",
            "options": [
                "Approchée par un polynôme, d'aussi près qu'on veut",
                "Dérivée en tout point",
                "Représentée par une série de Fourier uniquement",
                "Interpolée par une seule droite",
            ],
            "correct": 0,
            "notion": "weierstrass",
            "weight": 1,
        },
        {
            "question": "Le polynôme de Taylor approxime une fonction :",
            "options": [
                "Sur tout un intervalle, aussi bien partout",
                "Seulement au voisinage d'un point précis",
                "Uniquement pour les fonctions polynomiales",
                "Sans jamais diverger",
            ],
            "correct": 1,
            "notion": "taylor_vs_interpolation",
            "weight": 1,
        },
        {
            "question": "Le polynôme caractéristique de Lagrange ℓᵢ(x) est de degré :",
            "options": ["1", "n", "n+1", "0"],
            "correct": 1,
            "notion": "lagrange_polynomes",
            "weight": 1,
        },
        {
            "question": "L'erreur d'interpolation Eₙ(x) = f(x) - Πₙf(x) fait intervenir :",
            "options": [
                "f^(n+1)(ξ) et le polynôme nodal ωₙ₊₁(x)",
                "Seulement le nombre de points",
                "La dérivée première de f uniquement",
                "Rien, elle est toujours nulle",
            ],
            "correct": 0,
            "notion": "erreur_interpolation",
            "weight": 2,
        },
        {
            "question": "L'avantage de la forme de Newton avec différences divisées est :",
            "options": [
                "Elle donne un polynôme différent de Lagrange",
                "Ajouter un point coûte moins cher qu'avec Lagrange",
                "Elle nécessite moins de points",
                "Elle élimine toute erreur d'interpolation",
            ],
            "correct": 1,
            "notion": "newton_forme",
            "weight": 1,
        },
    ],
    "scoring": {"pass_threshold": 5},  # 5/6 pondéré (poids total = 6)
}

FINAL_QUIZ_DIFFICILE = {
    "_id": "quiz_interpolation_difficile_final",
    "quiz_type": "final",
    "module_id": "interpolation",
    "course_id": "interpolation_difficile",
    "questions": [
        {
            "question": "Dans la formule de Newton, δⁿy[x₀,...,xₙ] est appelée :",
            "options": [
                "Différence divisée d'ordre n",
                "Erreur d'interpolation",
                "Polynôme nodal",
                "Constante de Lebesgue",
            ],
            "correct": 0,
            "notion": "differences_divisees",
            "weight": 1,
        },
        {
            "question": "Une propriété clé des différences divisées est qu'elles sont :",
            "options": [
                "Toujours positives",
                "Symétriques par permutation des nœuds",
                "Nulles pour les polynômes de degré 2",
                "Dépendantes de l'ordre des points",
            ],
            "correct": 1,
            "notion": "differences_divisees",
            "weight": 1,
        },
        {
            "question": "Les points de Chebyshev sont utilisés pour :",
            "options": [
                "Minimiser l'amplification des erreurs et éviter le phénomène de Runge",
                "Accélérer uniquement le calcul numérique",
                "Remplacer la méthode de Newton",
                "Rendre f dérivable",
            ],
            "correct": 0,
            "notion": "points_chebyshev",
            "weight": 2,
        },
        {
            "question": "Le phénomène de Runge apparaît typiquement quand :",
            "options": [
                "On utilise trop peu de points",
                "On augmente le degré sur des points équidistants",
                "La fonction est un polynôme",
                "On utilise une spline",
            ],
            "correct": 1,
            "notion": "phenomene_runge",
            "weight": 2,
        },
        {
            "question": "Une spline cubique est, par construction :",
            "options": [
                "Un polynôme unique de haut degré",
                "2 fois continûment différentiable, degré 3 par morceaux",
                "Discontinue entre chaque intervalle",
                "Toujours de degré 5",
            ],
            "correct": 1,
            "notion": "splines",
            "weight": 1,
        },
    ],
    "scoring": {"pass_threshold": 6},  # poids total = 7, seuil 6/7
}


async def seed():
    await connect_to_mongo()
    db = get_database()

    for quiz in [FINAL_QUIZ_MOYEN, FINAL_QUIZ_DIFFICILE]:
        await db.quizzes.delete_many({"_id": quiz["_id"]})
        await db.quizzes.insert_one(quiz)
        print(f"Quiz final '{quiz['course_id']}' inséré.")

    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(seed())
