# EPITA C++

Exercices : `hello_friends`, `timer`, `war`.

## Lancer les tests en local

```sh
./check.sh                  # tout
./check.sh style            # coding style seulement
./check.sh hello_friends    # un exercice
.venv/bin/pytest tests/style -k timer -v                # style d'un exercice
.venv/bin/clang-format -i hello_friends/hello_friends.cc
```

Prérequis : `python3` (avec `venv`), `g++`, `clang++`, `valgrind`.

## Structure

- `.clang-format`, `.clang-tidy` : règles de style (clang-format 18.1.8 épinglé)
- `tests/exercises.py` : par exercice, fichiers à rendre, headers autorisés, constructions interdites
- `tests/style/` : tests généraux, appliqués à tous les fichiers à rendre existants
- `tests/<exercice>/` : tests ciblés (ignorés tant que l'exercice n'est pas écrit)
- `.github/workflows/ci.yml` : 1 job style + 1 job par exercice
