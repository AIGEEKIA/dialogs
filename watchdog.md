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

## Documentation
- https://python-watchdog.readthedocs.io/
