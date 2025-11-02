from ollama import list as get_models, chat
from pathlib import Path
import os
import toml
import random
import time
import uuid
import re

def clean_response(response_text, character_name):
    """Nettoie la réponse pour enlever le nom du personnage et les guillemets."""
    # Enlever le nom du personnage au début
    patterns_to_remove = [
        f"^{character_name}\\s*:\\s*",  # "Enseignant: "
        f"^{character_name}\\s+",       # "Enseignant "
        f"^\\*\\*{character_name}\\*\\*\\s*:\\s*",  # "**Enseignant**: "
    ]
    
    cleaned = response_text.strip()
    
    for pattern in patterns_to_remove:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
    
    # Enlever les guillemets en début et fin
    cleaned = cleaned.strip('"\'""''')
    
    # Enlever les guillemets qui entourent tout le texte
    if (cleaned.startswith('"') and cleaned.endswith('"')) or (cleaned.startswith("'") and cleaned.endswith("'")):
        cleaned = cleaned[1:-1]
    
    return cleaned.strip()

def get_available_models():
    """Retourne la liste des modèles Ollama disponibles."""
    try:
        models = get_models()
        # Gérer le cas où models est un objet avec attribut models ou un dictionnaire
        if hasattr(models, 'models'):
            return [model.model for model in models.models]
        elif isinstance(models, dict) and 'models' in models:
            return [model['model'] if isinstance(model, dict) else model.model for model in models['models']]
        else:
            return ["llama2-uncensored:latest"]  # Modèle par défaut
    except Exception as e:
        print(f"Erreur de connexion à Ollama: {e}")
        return ["llama2-uncensored:latest"]  # Modèle par défaut si Ollama n'est pas disponible

def load_prompts():
    """Charge les prompts depuis prompts.toml."""
    prompts_path = Path(__file__).parent / "prompts.toml"
    if prompts_path.exists():
        return toml.load(prompts_path)
    return {"system_prompts": {}, "user_prompts": {}}

def get_chat_response(model_name, user_message, system_prompt="", user_prompt="", options=None):
    """Retourne la réponse du modèle choisi avec prompts système et utilisateur, et options."""
    try:
        messages = []
        if system_prompt:
            messages.append({'role': 'system', 'content': system_prompt})
        messages.append({'role': 'user', 'content': user_prompt + "\n\n" + user_message if user_prompt else user_message})
        
        response = chat(
            model=model_name,
            messages=messages,
            options=options or {}
        )
        return response['message']['content']
    except Exception as e:
        return f"Erreur: Impossible de contacter Ollama. Veuillez vérifier que le serveur Ollama est en cours d'exécution. Détails: {e}"

def generate_dialogue_response(model_name, character, dialogue, system_prompt="", user_prompt="", options=None, context_lines=5, generation_count=0):
    """Génère une réponse pour le personnage dans le dialogue, en utilisant le contexte récent."""
    # Prendre les dernières context_lines messages
    recent_context = dialogue[-context_lines:] if len(dialogue) > context_lines else dialogue
    context_text = "\n".join(f"{speaker}: {msg}" for speaker, msg in recent_context)

    # Instruction aléatoire pour plus de variété
    random_instruction = random.choice([
        "Réponds de manière naturelle et immersive.",
        "Continue l'histoire de façon engageante.",
        "Réagis comme le personnage le ferait.",
        "Apporte de la tension ou de l'humour.",
        "Développe la réponse de manière détaillée.",
        "Sois créatif dans ta réponse."
    ])

    # Ajout d'un identifiant unique pour invalider le cache
    unique_id = f"\nUnique ID: {uuid.uuid4()}-{time.time()}"
    prompt = f"Dialogue récent:\n{context_text}\n\n{random_instruction}\nRépondez en tant que {character} de façon naturelle et cohérente. {user_prompt}\n\nIMPORTANT: Répondez UNIQUEMENT avec les paroles directes de {character}, sans écrire son nom, sans guillemets, sans préfixe. Juste le contenu de ce qu'il dit.{unique_id}"

    messages = []
    if system_prompt:
        messages.append({'role': 'system', 'content': f"{system_prompt}\n\nRègle stricte: Vous êtes {character}. Ne jamais inclure le nom du personnage dans votre réponse. Répondez directement avec les paroles."})
    messages.append({'role': 'user', 'content': prompt})

    # Options avec graine aléatoire et désactivation explicite du cache
    final_options = options.copy() if options else {}
    final_options['seed'] = random.randint(0, 1000000)
    # Randomize temperature slightly for more variety
    base_temp = final_options.get('temperature', 1.0)
    final_options['temperature'] = base_temp + random.uniform(-0.2, 0.2)

    # Journalisation des messages pour débogage
    print("Messages envoyés à Ollama:", messages)

    try:
        response = chat(
            model=model_name,
            messages=messages,
            options=final_options
        )
        # Post-traitement pour nettoyer la réponse
        cleaned_response = clean_response(response['message']['content'], character)
        return cleaned_response, random_instruction
    except Exception as e:
        return f"Erreur: Impossible de contacter Ollama. Veuillez vérifier que le serveur Ollama est en cours d'exécution. Détails: {e}", random_instruction

def generate_multiple_responses(model_name, character, dialogue, system_prompt="", user_prompt="", options=None, context_lines=5, generation_count=0, num_responses=3):
    """Génère plusieurs réponses pour le personnage dans le dialogue."""
    responses = []
    for _ in range(num_responses):
        # Prendre les dernières context_lines messages
        recent_context = dialogue[-context_lines:] if len(dialogue) > context_lines else dialogue
        context_text = "\n".join(f"{speaker}: {msg}" for speaker, msg in recent_context)

        # Instruction aléatoire pour plus de variété
        random_instruction = random.choice([
            "Réponds de manière naturelle et immersive.",
            "Continue l'histoire de façon engageante.",
            "Réagis comme le personnage le ferait.",
            "Apporte de la tension ou de l'humour.",
            "Développe la réponse de manière détaillée.",
            "Sois créatif dans ta réponse."
        ])

        # Ajout d'un identifiant unique pour invalider le cache
        unique_id = f"\nUnique ID: {uuid.uuid4()}-{time.time()}"
        prompt = f"Dialogue récent:\n{context_text}\n\n{random_instruction}\nRépondez en tant que {character} de façon naturelle et cohérente. {user_prompt}\n\nIMPORTANT: Répondez UNIQUEMENT avec les paroles directes de {character}, sans écrire son nom, sans guillemets, sans préfixe. Juste le contenu de ce qu'il dit.{unique_id}"

        messages = []
        if system_prompt:
            messages.append({'role': 'system', 'content': f"{system_prompt}\n\nRègle stricte: Vous êtes {character}. Ne jamais inclure le nom du personnage dans votre réponse. Répondez directement avec les paroles."})
        messages.append({'role': 'user', 'content': prompt})

        # Options avec graine aléatoire et désactivation explicite du cache
        final_options = options.copy() if options else {}
        final_options['seed'] = random.randint(0, 1000000)
        final_options['disable_cache'] = True  # Désactivation explicite du cache si supporté

        # Appel au modèle
        try:
            response = chat(
                model=model_name,
                messages=messages,
                options=final_options
            )
            # Post-traitement pour nettoyer la réponse
            cleaned_response = clean_response(response['message']['content'], character)
            responses.append(cleaned_response)
        except Exception as e:
            responses.append(f"Erreur: Impossible de contacter Ollama. Veuillez vérifier que le serveur Ollama est en cours d'exécution. Détails: {e}")

    return responses

def list_log_files(folder_path):
    """Liste les fichiers .txt dans le dossier, triés par date de modification (plus récent en premier)."""
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        return []
    txt_files = [f for f in folder.iterdir() if f.is_file() and f.suffix == '.txt']
    txt_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)  # Plus récent en premier
    return [str(f) for f in txt_files]

def parse_dialogue(file_path):
    """Parse le fichier de dialogue en liste de (speaker, message)."""
    dialogue = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if ': ' in line:
                speaker, message = line.split(': ', 1)
                dialogue.append((speaker, message))
    return dialogue

def get_speakers(dialogue_data):
    """Retourne la liste des speakers uniques dans le dialogue.
    dialogue_data peut être soit une liste de tuples (speaker, message) 
    soit un chemin de fichier à parser."""
    if isinstance(dialogue_data, str):
        # Si c'est un chemin de fichier, le parser d'abord
        dialogue_data = parse_dialogue(dialogue_data)
    return list(set(speaker for speaker, _ in dialogue_data))

# Exemple d'utilisation de Path pour un fichier (à adapter selon besoin)
def get_file_path(filename):
    """Retourne le chemin absolu d'un fichier dans le dossier du projet."""
    base_dir = Path(__file__).parent.resolve()
    return str(base_dir / filename)
