"""
Sécurité des mots de passe avec Argon2.

Pourquoi Argon2 et pas bcrypt ou du SHA256 ?
---------------------------------------------
- On ne stocke JAMAIS un mot de passe en clair, ni même un simple hash SHA256
  (trop rapide à calculer -> attaques par force brute faciles avec un GPU).
- Argon2 est l'algorithme recommandé par l'OWASP en 2024/2025. Il a gagné la
  "Password Hashing Competition" et est volontairement lent + gourmand en
  mémoire, ce qui rend les attaques par force brute très coûteuses.
- pwdlib est la librairie moderne recommandée (successeur de passlib, qui
  n'est plus activement maintenu).
"""

from pwdlib import PasswordHash

# PasswordHash.recommended() utilise Argon2id avec des paramètres sûrs par défaut
password_hasher = PasswordHash.recommended()


def hash_password(plain_password: str) -> str:
    """Transforme un mot de passe en clair en un hash sécurisé à stocker en base."""
    return password_hasher.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie qu'un mot de passe en clair correspond au hash stocké en base."""
    return password_hasher.verify(plain_password, hashed_password)
