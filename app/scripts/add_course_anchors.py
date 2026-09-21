import asyncio

from app.database.mongodb import connect_to_mongo, close_mongo_connection, get_database


# Pour chaque cours, mapping : texte exact du titre existant -> notion (utilisée comme ancre id)
ANCHORS = {
    "interpolation_facile": {
        "<h2>2.1 Introduction</h2>": '<h2 id="interpolation_lineaire">2.1 Introduction</h2>',
        "<h2>2.2 Unicité du polynôme d'interpolation</h2>": '<h2 id="unicite_polynome">2.2 Unicité du polynôme d\'interpolation</h2>',
        "<h3>2.3.1 Polynôme de Lagrange</h3>": '<h3 id="lagrange_base">2.3.1 Polynôme de Lagrange</h3>',
        "<h2>2.4 Interpolation de Newton</h2>": '<h2 id="newton_differences_divisees">2.4 Interpolation de Newton</h2>',
    },
    "interpolation_moyen": {
        "<h3>Pourquoi une approximation polynomiale ?</h3>": '<h3 id="weierstrass">Pourquoi une approximation polynomiale ?</h3>',
        "<h2>Polynôme de Taylor vs interpolation</h2>": '<h2 id="taylor_vs_interpolation">Polynôme de Taylor vs interpolation</h2>',
        "<h2>Polynômes caractéristiques de Lagrange</h2>": '<h2 id="lagrange_polynomes">Polynômes caractéristiques de Lagrange</h2>',
        "<h2>Erreur d'interpolation</h2>": '<h2 id="erreur_interpolation">Erreur d\'interpolation</h2>',
        "<h2>Forme de Newton</h2>": '<h2 id="newton_forme">Forme de Newton</h2>',
    },
    "interpolation_difficile": {
        "<h2>II.1 Différences divisées et formule de Newton</h2>": '<h2 id="differences_divisees">II.1 Différences divisées et formule de Newton</h2>',
        "<h2>II.3 Polynômes de Chebyshev</h2>": '<h2 id="points_chebyshev">II.3 Polynômes de Chebyshev</h2>',
        "<h2>II.4 Convergence — le phénomène de Runge</h2>": '<h2 id="phenomene_runge">II.4 Convergence — le phénomène de Runge</h2>',
        "<h2>II.10 Interpolation par fonctions spline</h2>": '<h2 id="splines">II.10 Interpolation par fonctions spline</h2>',
    },
}


async def add_anchors():
    await connect_to_mongo()
    db = get_database()

    for course_id, replacements in ANCHORS.items():
        course = await db.courses.find_one({"_id": course_id})
        if course is None:
            print(f"Cours '{course_id}' introuvable, ignoré.")
            continue

        content = course["content_html"]
        count = 0
        for old, new in replacements.items():
            if old in content:
                content = content.replace(old, new)
                count += 1
            else:
                print(f"  ⚠ Titre non trouvé dans '{course_id}' : {old[:50]}...")

        await db.courses.update_one(
            {"_id": course_id}, {"$set": {"content_html": content}}
        )
        print(f"'{course_id}' : {count}/{len(replacements)} ancre(s) ajoutée(s).")

    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(add_anchors())
