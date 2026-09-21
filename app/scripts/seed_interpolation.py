import asyncio

from app.database.mongodb import connect_to_mongo, close_mongo_connection, get_database


# ---------------------------------------------------------------------------
# Contenu HTML — niveau FACILE (source: Chapitr2.pdf — L.BAZIZ)
# ---------------------------------------------------------------------------
CONTENT_FACILE = """
<h2>2.1 Introduction</h2>
<p>L'interpolation consiste à connecter des points de données discrets de manière à
obtenir des estimations raisonnables entre les points donnés, ou de remplacer une
fonction par une autre plus simple mais qui coïncide avec la première en un nombre
fini de points donnés au départ.</p>
<p>Les points discrets peuvent être reliés par une ligne simple (interpolation
linéaire), ou par un polynôme (interpolation polynomiale).</p>
<p>Soit \\( f \\) une application de \\( \\mathbb{R} \\) dans \\( \\mathbb{R} \\), dont on
connaît \\( (n+1) \\) points \\( (x_i, f(x_i)) \\) pour \\( i = 0, \\dots, n \\). Le but de
l'interpolation est de déterminer une fonction \\( P \\) simple à calculer, telle que :
\\[ P(x_i) = f(x_i), \\quad i = 0, \\dots, n. \\]
Les points \\( (x_i, f(x_i)) \\) sont appelés <strong>points d'interpolation</strong>.</p>

<h2>2.2 Unicité du polynôme d'interpolation</h2>
<p><strong>Théorème 1 :</strong> Une condition nécessaire et suffisante pour qu'il existe
un polynôme d'interpolation \\( P_n \\) unique est que les points d'interpolation
\\( x_i \\) soient tous distincts.</p>

<h2>2.3 Interpolation de Lagrange</h2>
<h3>2.3.1 Polynôme de Lagrange</h3>
<p>On appelle polynôme de Lagrange de degré \\( n \\) basé sur les points
d'interpolation \\( (x_i, f(x_i)) \\), le polynôme unique d'ordre \\( n \\) qui passe
exactement par ces \\( (n+1) \\) points. Il est donné par :
\\[ P_n(x) = \\sum_{k=0}^{n} L_k(x)\\, f(x_k) \\]
où \\( L_k(x) \\) est le polynôme élémentaire de Lagrange :
\\[ L_k(x) = \\prod_{\\substack{i=0 \\\\ i \\ne k}}^{n} \\frac{x - x_i}{x_k - x_i} \\]
avec la propriété \\( L_k(x_i) = 1 \\) si \\( i = k \\), et \\( 0 \\) sinon.</p>

<h4>Exemple</h4>
<table>
<tr><th>x_i</th><td>0</td><td>1</td><td>2</td><td>3</td></tr>
<tr><th>y_i</th><td>1</td><td>4</td><td>8</td><td>14</td></tr>
</table>
<p>Le polynôme de Lagrange déterminé par ces points est :
\\[ P_3(x) = \\frac{1}{3}x^3 + \\dots \\]
(construit en sommant les 4 termes \\( L_k(x) \\cdot f(x_k) \\) — détail complet dans le
support imprimé).</p>

<h3>2.3.2 L'erreur d'interpolation</h3>
<p><strong>Théorème 2 :</strong> Soit \\( f \\in C^{n+1}[a,b] \\) et \\( P_n(x) \\) le
polynôme d'interpolation de \\( f \\) sur les points \\( (x_i, f(x_i)) \\). L'erreur
d'interpolation est bornée par :
\\[ |E(x)| \\le \\frac{M \\prod_{i=0}^{n} |x - x_i|}{(n+1)!}, \\quad
M = \\max_{\\xi \\in [a,b]} |f^{(n+1)}(\\xi)| \\]</p>

<h4>Exemple</h4>
<p>Pour \\( f(x) = \\dfrac{1}{x} \\), avec les points \\( x_i = 2, 2.5, 4 \\)
(\\( y_i = 0.5, 0.4, 0.25 \\)), on obtient
\\( P_2(x) = \\frac{1}{20}x^2 - \\frac{51}{120}x + \\frac{23}{20} \\).
En \\( x = 3 \\) : \\( P_2(3) = 0.325 \\), alors que \\( f(3) = 0.333 \\), soit une erreur
réelle de \\( 0.006 \\) — à comparer à la borne théorique \\( 0.015 \\) (avec
\\( M = \\max |f''(x)| = 2 \\)).</p>

<h2>2.4 Interpolation de Newton</h2>
<p>Le polynôme d'interpolation par la méthode de Newton s'écrit :
\\[ P_n(x) = a_0 + a_1(x-x_0) + a_2(x-x_0)(x-x_1) + \\dots +
a_n(x-x_0)(x-x_1)\\cdots(x-x_{n-1}) \\]
Les coefficients \\( a_k \\) sont calculés par la méthode des <strong>différences
divisées</strong> :
\\[ \\Delta y_i = \\frac{y_{i+1} - y_i}{x_{i+1} - x_i}, \\qquad
\\Delta^2 y_i = \\frac{\\Delta y_{i+1} - \\Delta y_i}{x_{i+2} - x_i} \\]
et ainsi de suite pour les ordres supérieurs, organisées dans un tableau triangulaire.</p>

<h4>Exemple (n=2)</h4>
<p>Points : \\( (0,1), (2,5), (4,17) \\).</p>
<table>
<tr><th>x</th><th>y</th><th>Δy</th><th>Δ²y</th></tr>
<tr><td>0</td><td>1</td><td></td><td></td></tr>
<tr><td>2</td><td>5</td><td>2</td><td></td></tr>
<tr><td>4</td><td>17</td><td>6</td><td>1</td></tr>
</table>
<p>D'où \\( P_2(x) = 1 + 2x + x(x-2) = 1 + x^2 \\).</p>
"""


# ---------------------------------------------------------------------------
# Contenu HTML — niveau MOYEN (source: cours-interp.pdf)
# ---------------------------------------------------------------------------
CONTENT_MOYEN = """
<h2>Objectif</h2>
<p>Approcher une fonction dont on ne connaît les valeurs qu'en certains points —
soit parce qu'une fonction connue analytiquement est difficile à évaluer,
différencier ou intégrer par ordinateur, soit parce qu'on dispose d'un nombre fini
de valeurs obtenues expérimentalement (étalonnage, relevés de mesures...).</p>

<h3>Pourquoi une approximation polynomiale ?</h3>
<p>Toute fonction continue peut être approchée par un polynôme :</p>
<blockquote><strong>Théorème (approximation de Weierstrass) :</strong> Supposons que
\\( f \\) est définie et continue sur \\( [a,b] \\). Pour tout \\( \\varepsilon > 0 \\), il
existe un polynôme \\( P(x) \\) tel que \\( |f(x) - P(x)| < \\varepsilon \\) pour tout
\\( x \\in [a,b] \\).</blockquote>
<p>Les calculs de dérivées et d'intégrales de polynômes sont par ailleurs bien plus
simples que ceux de fonctions générales.</p>

<h2>Polynôme de Taylor vs interpolation</h2>
<p>Le polynôme de Taylor de degré \\( n \\) en \\( a \\) approxime \\( f \\) seulement au
<strong>voisinage</strong> de \\( a \\). Exemple pour \\( f(x) = \\dfrac{1}{x} \\) au point
\\( 1 \\), en approximant \\( f(3) = 1/3 \\) :</p>
<table>
<tr><th>n</th><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td></tr>
<tr><th>P_n(3)</th><td>1</td><td>-1</td><td>3</td><td>-5</td><td>11</td><td>-21</td><td>43</td><td>-85</td></tr>
</table>
<p>Le polynôme de Taylor <strong>diverge</strong> ici en s'éloignant de \\( a=1 \\) — d'où
l'intérêt de l'interpolation, qui donne une approximation sur tout un intervalle en
utilisant directement plusieurs points connus de la fonction.</p>

<h2>Formulation générale</h2>
<p>Étant donnés \\( (n+1) \\) couples \\( (x_i, y_i) \\), on cherche une fonction
\\( \\Phi(x) \\) telle que \\( \\Phi(x_i) = y_i \\). On dit que \\( \\Phi \\)
<strong>interpole</strong> \\( \\{y_i\\} \\) aux <strong>nœuds</strong> \\( \\{x_i\\} \\).</p>
<ul>
<li>Si \\( \\Phi \\) est un polynôme → interpolation polynomiale.</li>
<li>Si \\( \\Phi \\) est polynomiale par morceaux → interpolation par splines.</li>
<li>Si \\( \\Phi \\) est un polynôme trigonométrique → interpolation trigonométrique.</li>
</ul>
<blockquote><strong>Théorème (existence et unicité) :</strong> Étant donné \\( (n+1) \\)
points distincts \\( x_0, \\dots, x_n \\) et \\( (n+1) \\) valeurs \\( y_0, \\dots, y_n \\),
il existe un unique polynôme \\( \\Pi_n \\) de degré \\( \\le n \\) tel que
\\( \\Pi_n(x_i) = y_i \\).</blockquote>

<h2>Comment trouver ce polynôme ?</h2>
<p>La méthode générale (résoudre le système linéaire des coefficients) est coûteuse
et souvent mal conditionnée. On préfère des méthodes ad hoc :</p>
<ul>
<li><strong>Méthode de Lagrange</strong></li>
<li><strong>Méthode de Newton</strong> — donne le même polynôme que Lagrange, mais à
coût de calcul moindre, notamment pour ajouter un point.</li>
<li>Méthode de Hermite (utilise aussi les dérivées)</li>
</ul>

<h2>Polynômes caractéristiques de Lagrange</h2>
\\[ \\ell_i(x) = \\prod_{j=0, j \\ne i}^{n} \\frac{x - x_j}{x_i - x_j} \\]
<p>Ces polynômes sont de degré \\( n \\), et vérifient \\( \\ell_i(x_i) = 1 \\),
\\( \\ell_i(x_j) = 0 \\) pour \\( j \\ne i \\). Ils forment une base de l'ensemble des
polynômes de degré \\( \\le n \\), d'où :
\\[ \\Pi_n(x) = \\sum_{i=0}^{n} y_i\\, \\ell_i(x) \\]</p>

<h2>Erreur d'interpolation</h2>
<blockquote><strong>Théorème :</strong> Si \\( f \\in C^{n+1}(I_x) \\), où \\( I_x \\) est le
plus petit intervalle contenant les nœuds et le point \\( x \\), alors :
\\[ E_n(x) = f(x) - \\Pi_n f(x) = \\frac{f^{(n+1)}(\\xi)}{(n+1)!}\\, \\omega_{n+1}(x),
\\quad \\xi \\in I_x \\]
où \\( \\omega_{n+1}(x) = (x-x_0)(x-x_1)\\cdots(x-x_n) \\) est le polynôme
nodal.</blockquote>

<h2>Forme de Newton</h2>
<p>On écrit \\( \\Pi_n(x) = \\Pi_{n-1}(x) + q_n(x) \\), où
\\( q_n(x) = a_n\\, \\omega_n(x) \\) et \\( a_n = f[x_0, \\dots, x_n] \\) est la
<strong>n-ème différence divisée de Newton</strong>, avec la formule de récurrence :
\\[ f[x_0,\\dots,x_n] = \\frac{f[x_1,\\dots,x_n] - f[x_0,\\dots,x_{n-1}]}{x_n - x_0} \\]
D'où :
\\[ \\Pi_n f(x) = \\sum_{k=0}^{n} \\omega_k(x)\\, f[x_0,\\dots,x_k] \\]</p>
<p>Le tableau des différences divisées se construit en triangle : pour \\( n+1 \\)
points, il faut \\( n(n+1) \\) additions et \\( n(n+1)/2 \\) divisions. Avantage clé sur
Lagrange : pour passer de \\( \\Pi_n \\) à \\( \\Pi_{n+1} \\) (ajout d'un point), il suffit
de \\( (n+1) \\) divisions et \\( 2(n+1) \\) additions supplémentaires, sans tout
recalculer.</p>

<h2>Exemple d'application</h2>
<p>Une voiture accélère depuis 60 km/h, avec vitesse mesurée régulièrement :</p>
<table>
<tr><th>t [s]</th><td>0.0</td><td>0.7</td><td>1.4</td><td>2.1</td><td>2.8</td></tr>
<tr><th>v [km/h]</th><td>60</td><td>72.4</td><td>81.5</td><td>87.2</td><td>95.9</td></tr>
</table>
<p>Question type : à l'aide d'un polynôme d'interpolation de degré \\( \\le 2 \\), estimer
la vitesse à \\( t = 1.2s \\), puis donner l'expression analytique de l'erreur commise
et son ordre de grandeur.</p>
"""


# ---------------------------------------------------------------------------
# Contenu HTML — niveau DIFFICILE (source: chap2.pdf — sections II.1-II.5, II.10-II.11)
# Note: II.6-II.9 (DFT/FFT/DCT/JPEG) volontairement exclues — hors périmètre
# "interpolation" du module.
# ---------------------------------------------------------------------------
CONTENT_DIFFICILE = """
<h2>II.1 Différences divisées et formule de Newton</h2>
<p>Étant donnés les \\( n+1 \\) points \\( (x_0,y_0), \\dots, (x_n,y_n) \\) où les
\\( x_i \\) sont distincts, on cherche un polynôme \\( p(x) \\) de degré \\( n \\) tel que
\\( p(x_i) = y_i \\).</p>
<p><strong>Définition (différences divisées) :</strong>
\\[ y[x_i] := y_i, \\qquad
\\delta y[x_i,x_j] := \\frac{y[x_j]-y[x_i]}{x_j-x_i}, \\qquad
\\delta^n y[x_{i_0},\\dots,x_{i_n}] :=
\\frac{\\delta^{n-1}y[x_{i_1},\\dots,x_{i_n}] - \\delta^{n-1}y[x_{i_0},\\dots,x_{i_{n-1}}]}{x_{i_n}-x_{i_0}} \\]</p>
<p><strong>Théorème (formule de Newton) :</strong> Le polynôme d'interpolation de degré
\\( n \\) passant par les \\( n+1 \\) points est unique et donné par :
\\[ p(x) = y[x_0] + (x-x_0)\\,\\delta y[x_0,x_1] + (x-x_0)(x-x_1)\\,\\delta^2 y[x_0,x_1,x_2]
+ \\dots + (x-x_0)\\cdots(x-x_{n-1})\\,\\delta^n y[x_0,\\dots,x_n] \\]</p>
<p><em>Remarque :</em> l'ordre des \\( x_i \\) n'a aucune importance pour la formule de
Newton — permuter les données donne le même polynôme, car \\( \\delta^n y \\) est une
fonction symétrique de ses arguments. Pour diminuer l'influence des erreurs
d'arrondi, il est recommandé d'ordonner les \\( x_i \\) en prenant d'abord les valeurs
au milieu, puis celles aux extrémités.</p>

<h2>II.2 Erreur de l'interpolation</h2>
<p><strong>Lemme :</strong> Soit \\( f \\) \\( n \\)-fois différentiable et
\\( y_i = f(x_i) \\). Alors il existe \\( \\xi \\in (\\min x_i, \\max x_i) \\) tel que
\\( \\delta^n y[x_0,\\dots,x_n] = \\dfrac{f^{(n)}(\\xi)}{n!} \\).</p>
<p><strong>Théorème :</strong> Soit \\( f: [a,b] \\to \\mathbb{R} \\) \\( (n+1) \\)-fois
différentiable et \\( p(x) \\) le polynôme d'interpolation de degré \\( n \\). Pour
\\( x \\in [a,b] \\), il existe \\( \\xi \\) tel que :
\\[ f(x) - p(x) = (x-x_0)\\cdots(x-x_n)\\, \\frac{f^{(n+1)}(\\xi)}{(n+1)!} \\]</p>
<p><em>Exemple :</em> pour \\( \\sin x \\) avec 7 points, l'erreur est bornée par
\\( |p(x)-\\sin x| \\le 0.035 \\) en \\( x=4 \\). Pour \\( f(x) = 1/(1+x^2) \\) avec les
mêmes points, l'erreur peut être <strong>4392 fois plus grande</strong> — l'erreur
dépend fortement de la fonction interpolée, pas seulement du nombre de points.</p>

<h2>II.3 Polynômes de Chebyshev</h2>
<p>L'erreur d'interpolation est un produit de la dérivée \\( (n+1) \\)-ème de \\( f \\) et
de l'expression \\( (x-x_0)\\cdots(x-x_n) \\), qui ne dépend que du choix des points.
Problème : pour un \\( n \\) donné, quelle division de \\( [a,b] \\) minimise
\\( L = \\max_{x\\in[a,b]} |(x-x_0)\\cdots(x-x_n)| \\) ?</p>
<p><strong>Définition :</strong> \\( T_n(x) = \\cos(n \\arccos x) \\) pour
\\( x \\in [-1,1] \\). Propriétés : \\( T_{n+1}(x) = 2x T_n(x) - T_{n-1}(x) \\),
\\( |T_n(x)| \\le 1 \\), les \\( T_n \\) sont orthogonaux par rapport au poids
\\( 1/\\sqrt{1-x^2} \\).</p>
<p><strong>Théorème :</strong> L'expression \\( L \\) est minimale si et seulement si les
points sont les <strong>points de Chebyshev</strong> :
\\[ x_k = \\frac{a+b}{2} + \\frac{b-a}{2}\\cos\\!\\left(\\frac{(2k+1)\\pi}{2n+2}\\right),
\\quad k=0,\\dots,n \\]</p>

<h2>II.4 Convergence — le phénomène de Runge</h2>
<p>Pour \\( f(x) = 1/(1+25x^2) \\) sur \\( [-1,1] \\), augmenter le degré \\( n \\) avec des
points <strong>équidistants</strong> n'améliore pas la précision près des bords —
au contraire, l'erreur explose (phénomène de Runge, 1901).</p>
<p><strong>Théorème (Runge, 1901) :</strong> Si \\( f(z) \\) n'a pas de singularité dans
une certaine région liée à la fonction \\( G(z) \\), alors le polynôme d'interpolation
converge vers \\( f(x) \\) seulement sur un sous-intervalle \\( (-\\beta, \\beta) \\).</p>
<p>Avec les <strong>points de Chebyshev</strong>, ce phénomène disparaît : on observe une
convergence uniforme sur tout l'intervalle \\( [-1,1] \\).</p>

<h2>II.5 Influence des erreurs d'arrondi</h2>
<p>La constante de Lebesgue \\( \\Lambda_n = \\max_{x \\in [a,b]} \\sum_{i=0}^{n}
|\\ell_i(x)| \\) mesure l'amplification de l'erreur dans les données.</p>
<ul>
<li>Points équidistants : \\( \\Lambda_n \\approx \\dfrac{2^{n+1}}{e \\cdot n \\cdot \\log n} \\)
— croissance <strong>exponentielle</strong> (\\( \\Lambda_{40} \\approx 10^{10} \\)).</li>
<li>Points de Chebyshev : \\( \\Lambda_n \\approx \\dfrac{2}{\\pi}\\log n \\) — croissance
seulement <strong>logarithmique</strong>.</li>
</ul>
<p>D'où l'intérêt pratique majeur des points de Chebyshev pour l'interpolation à haut
degré.</p>

<h2>II.10 Interpolation par fonctions spline</h2>
<p>Une <strong>spline</strong> est une fonction \\( s: [a,b] \\to \\mathbb{R} \\), 2 fois
continûment différentiable, polynôme de degré 3 sur chaque sous-intervalle
\\( [x_{i-1}, x_i] \\), et telle que \\( s(x_i) = y_i \\).</p>
<p>Trois types de conditions aux extrémités :</p>
<ul>
<li><strong>Spline naturel :</strong> \\( s''(a) = 0 \\) et \\( s''(b) = 0 \\).</li>
<li><strong>Spline scellé :</strong> pentes données \\( s'(a) = p_0 \\), \\( s'(b) = p_n \\).</li>
<li><strong>Spline périodique :</strong> \\( s'(a)=s'(b) \\) et \\( s''(a)=s''(b) \\).</li>
</ul>
<p>La spline minimise l'énergie \\( \\int_a^b (s''(x))^2\\, dx \\) parmi toutes les
fonctions satisfaisant les mêmes conditions — d'où son interprétation physique
("languette élastique" forcée de passer par les points).</p>
<p>La construction ramène à un <strong>système linéaire tridiagonal</strong> en les
pentes \\( p_0, \\dots, p_n \\), toujours inversible, résolu efficacement par
élimination.</p>

<h2>II.11 L'erreur du spline</h2>
<p><strong>Théorème (erreur du spline scellé) :</strong> Pour \\( f \\) de classe
\\( C^4 \\), le spline scellé \\( s(x) \\) sur une division de pas maximal \\( h \\)
vérifie :
\\[ |f(x) - s(x)| \\le \\frac{5}{384}\\, h^4 \\max_{\\xi \\in [a,b]} |f^{(4)}(\\xi)| \\]</p>
<p>Contrairement au polynôme d'interpolation de haut degré, l'erreur du spline reste
bien contrôlée même pour de nombreux points — c'est pourquoi les splines évitent le
phénomène de Runge.</p>
"""


COURSES = [
    {
        "_id": "interpolation_facile",
        "module_id": "interpolation",
        "level": "facile",
        "title": "Interpolation — niveau facile",
        "content_html": CONTENT_FACILE,
        "video_url": "",
        "order": 1,
    },
    {
        "_id": "interpolation_moyen",
        "module_id": "interpolation",
        "level": "moyen",
        "title": "Interpolation — niveau moyen",
        "content_html": CONTENT_MOYEN,
        "video_url": "",
        "order": 2,
    },
    {
        "_id": "interpolation_difficile",
        "module_id": "interpolation",
        "level": "difficile",
        "title": "Interpolation — niveau difficile",
        "content_html": CONTENT_DIFFICILE,
        "video_url": "",
        "order": 3,
    },
]


async def seed():
    await connect_to_mongo()
    db = get_database()

    await db.courses.delete_many({"module_id": "interpolation"})
    await db.courses.insert_many(COURSES)
    print(f"{len(COURSES)} cours interpolation insérés (facile / moyen / difficile).")

    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(seed())
