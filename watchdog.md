# Watchdog (Python)

## Qu'est-ce que Watchdog ?
Watchdog est une bibliothèque Python qui surveille les fichiers et dossiers en temps réel. Elle détecte automatiquement les modifications (création, suppression, édition) et peut déclencher des actions personnalisées.

## Usages courants
- Rechargement automatique d'une application (ex : Streamlit) dès qu'un fichier change.
- Développement rapide : pas besoin de relancer manuellement l'application.
- Automatisation de tâches (ex : scripts, tests, synchronisation) à chaque modification.

## Exemple d'utilisation
```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f'Fichier modifié : {event.src_path}')

observer = Observer()
observer.schedule(MyHandler(), path='.', recursive=True)
observer.start()
```

## Avantages
- Gain de temps en développement.
- Surveillance fiable et en temps réel.
- Facile à intégrer dans des workflows automatisés.

## Utilisation pour le développement Python en live

### Applications pratiques

- **Rechargement automatique d'applications web** (Streamlit, Flask, FastAPI)
- **Test automatique** : relancer les tests à chaque modification
- **Validation de code** : vérifier la syntaxe ou exécuter des linters automatiquement
- **Synchronisation de fichiers** : copier automatiquement les changements vers un serveur
- **Build automatique** : recompiler à chaque modification

### Exemple concret avec Streamlit

```bash
watchmedo shell-command --patterns="*.py" --recursive --command="streamlit run app.py" .
```

Cette commande surveille tous les fichiers `.py` et relance automatiquement Streamlit à chaque modification, permettant un développement fluide sans interruption.

### Pour le débogage

- **Logs automatiques** : enregistrer les changements pour tracer les bugs
- **Tests ciblés** : exécuter seulement les tests affectés par les modifications
- **Validation en temps réel** : vérifier la conformité du code automatiquement

## Documentation

- [Documentation officielle Watchdog](https://python-watchdog.readthedocs.io/)
