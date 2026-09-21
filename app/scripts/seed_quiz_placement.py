import asyncio

from app.database.mongodb import connect_to_mongo, close_mongo_connection, get_database


PLACEMENT_QUIZ = {
    "_id": "quiz_interpolation_placement",
    "quiz_type": "placement",
    "module_id": "interpolation",
    "course_id": None,
    "questions": [
        # --- niveau facile (notions de base) ---
        {
            "question": "L'interpolation consiste à :",
            "options": [
                "Trouver une fonction qui passe exactement par des points donnés",
                "Calculer la moyenne d'une série de valeurs",
                "Résoudre une équation différentielle",
                "Trouver les racines d'un polynôme",
            ],
            "correct": 0,
            "notion": "definition_interpolation",
            "weight": 1,
        },
        {
            "question": "Pour n+1 points distincts donnés, combien existe-t-il de polynômes d'interpolation de degré ≤ n ?",
            "options": ["Aucun", "Exactement un", "Exactement deux", "Une infinité"],
            "correct": 1,
            "notion": "unicite_polynome",
            "weight": 1,
        },
        {
            "question": "Le polynôme caractéristique de Lagrange ℓᵢ(x) vérifie :",
            "options": [
                "ℓᵢ(xᵢ) = 0 et ℓᵢ(xⱼ) = 1 pour j≠i",
                "ℓᵢ(xᵢ) = 1 et ℓᵢ(xⱼ) = 0 pour j≠i",
                "ℓᵢ(x) = 1 pour tout x",
                "ℓᵢ(xᵢ) dépend de f(xᵢ)",
            ],
            "correct": 1,
            "notion": "lagrange_base",
            "weight": 1,
        },
        # --- niveau moyen (Newton, erreur) ---
        {
            "question": "Quel est l'avantage principal de la méthode de Newton (différences divisées) sur Lagrange ?",
            "options": [
                "Elle donne un polynôme de degré inférieur",
                "Elle permet d'ajouter un point sans tout recalculer",
                "Elle ne nécessite pas de points distincts",
                "Elle est toujours exacte, sans erreur",
            ],
            "correct": 1,
            "notion": "newton_differences_divisees",
            "weight": 1,
        },
        {
            "question": "L'erreur d'interpolation E(x) = f(x) - Pₙ(x) dépend de :",
            "options": [
                "Uniquement du nombre de points utilisés",
                "Uniquement de l'intervalle [a,b]",
                "De la dérivée (n+1)-ème de f et de la position des nœuds",
                "Rien, l'erreur est toujours nulle",
            ],
            "correct": 2,
            "notion": "erreur_interpolation",
            "weight": 2,
        },
        {
            "question": "Étant donné f(0)=1, f(2)=5, f(4)=17, quelle est la valeur de la différence divisée f[x₀,x₁] ?",
            "options": ["1", "2", "4", "8"],
            "correct": 1,
            "notion": "calcul_differences_divisees",
            "weight": 2,
        },
        # --- niveau difficile (Chebyshev, Runge, splines) ---
        {
            "question": "Le phénomène de Runge se manifeste quand :",
            "options": [
                "On utilise trop peu de points",
                "On interpole à haut degré sur des points équidistants, causant des oscillations aux bords",
                "La fonction à interpoler n'est pas continue",
                "On utilise une spline au lieu d'un polynôme",
            ],
            "correct": 1,
            "notion": "phenomene_runge",
            "weight": 2,
        },
        {
            "question": "Les points de Chebyshev sont utilisés pour :",
            "options": [
                "Accélérer le calcul du polynôme",
                "Minimiser l'amplification des erreurs et éviter le phénomène de Runge",
                "Remplacer la méthode de Newton",
                "Garantir que f soit dérivable",
            ],
            "correct": 1,
            "notion": "points_chebyshev",
            "weight": 2,
        },
        {
            "question": "Une spline cubique est, par définition, une fonction qui est :",
            "options": [
                "Un polynôme unique de haut degré sur tout l'intervalle",
                "2 fois continûment différentiable, polynôme de degré 3 par morceaux",
                "Discontinue entre chaque point",
                "Toujours de degré 2",
            ],
            "correct": 1,
            "notion": "definition_spline",
            "weight": 2,
        },
    ],
    # score max = 1+1+1+1+2+2+2+2+2 = 14
    "scoring": {
        "faible_max": 5,   # 0-5 points  -> facile
        "moyen_max": 9,    # 6-9 points  -> moyen
                            # 10-14       -> difficile
    },
}


async def seed():
    await connect_to_mongo()
    db = get_database()

    await db.quizzes.delete_many({"_id": "quiz_interpolation_placement"})
    await db.quizzes.insert_one(PLACEMENT_QUIZ)
    print("Quiz de placement 'interpolation' inséré (9 questions, score max 14).")

    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(seed())

