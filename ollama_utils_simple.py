"""
Utilitaires Ollama pour le Chatbot Psychologue
Version simplifiée et autonome pour le projet chatbot-RAG
"""

from ollama import list as get_models, chat

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