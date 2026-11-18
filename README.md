# EPITA C++

| Dossier | Exercices |
|---|---|
| `cpp_1/` | hello_friends, queue, timer |
| `cpp_2/` | hola_amigos, stack, war |

## Lancer les tests en local

```sh
./check.sh                       # tout
./check.sh style                 # coding style seulement
./check.sh cpp_1/hello_friends   # un exercice
.venv/bin/clang-format -i cpp_1/hello_friends/hello_friends.cc
```

Prérequis : `python3`, `g++`, `clang++`, `valgrind`, `cmake`.

## Structure

- `.clang-format`, `.clang-tidy` : règles de style (clang-format 18.1.8 épinglé)
- `tests/exercises.py` : par exercice, fichiers à rendre, headers autorisés, constructions interdites
- `tests/style/` : tests généraux, appliqués à tous les fichiers à rendre existants
- `tests/cpp_N/<exercice>/` : tests ciblés (ignorés tant que l'exercice n'est pas écrit)
- `tests/greeter_suite.py` : suite partagée hello_friends / hola_amigos
- `.github/workflows/ci.yml` : 1 job style + 1 job par exercice
