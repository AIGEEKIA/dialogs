# Ollama - Exécution locale de modèles de langage

## Qu'est-ce qu'Ollama ?

Ollama est une plateforme open-source qui permet d'exécuter des modèles de langage (LLM) localement sur votre machine. Contrairement aux APIs cloud comme OpenAI ou Anthropic, Ollama offre :

- **Confidentialité totale** : Vos données restent sur votre machine
- **Pas de coûts** : Utilisation gratuite après téléchargement initial
- **Hors ligne** : Fonctionne sans connexion internet
- **Performance optimisée** : Modèles quantifiés pour un usage efficace

## Installation et premiers pas

### Installation

```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Télécharger depuis https://ollama.ai/download
```

### Téléchargement d'un modèle

```bash
# Modèle de base (recommandé pour débuter)
ollama pull llama2

# Autres modèles populaires
ollama pull mistral
ollama pull codellama
ollama pull llama2:13b
ollama pull llama2:70b
```

### Vérification de l'installation

```bash
ollama list  # Voir les modèles installés
ollama serve # Démarrer le serveur (optionnel)
```

## Architecture et fonctionnement

Ollama fonctionne comme un serveur local qui expose une API REST similaire à OpenAI. Les modèles sont automatiquement quantifiés et optimisés pour votre matériel.

### API REST

```bash
# Test rapide
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Bonjour, comment allez-vous ?"
}'
```

### Intégration Python

```python
import requests

response = requests.post('http://localhost:11434/api/generate', json={
    'model': 'llama2',
    'prompt': 'Expliquez ce qu\'est l\'intelligence artificielle'
})

print(response.json()['response'])
```

## Créer un chatbot Streamlit avec Ollama

### Application minimale (chatbot simple)

Voici le code le plus simple possible pour créer un chatbot Streamlit avec Ollama :

```python
import streamlit as st
import requests

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"

st.title("🤖 Chatbot Ollama")

# Sélection du modèle
models = ["llama2", "mistral", "codellama"]  # Modèles disponibles
selected_model = st.selectbox("Choisir un modèle :", models)

# Zone de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input utilisateur
if prompt := st.chat_input("Votre message..."):
    # Ajouter le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Générer la réponse
    with st.chat_message("assistant"):
        with st.spinner("Réflexion..."):
            try:
                response = requests.post(OLLAMA_URL, json={
                    "model": selected_model,
                    "prompt": prompt,
                    "stream": False
                })

                if response.status_code == 200:
                    result = response.json()
                    reply = result.get("response", "Erreur dans la réponse")
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                else:
                    st.error(f"Erreur HTTP: {response.status_code}")

            except Exception as e:
                st.error(f"Erreur de connexion: {e}")
                st.info("Vérifiez qu'Ollama est démarré : `ollama serve`")
```

### Fonctionnalités de cette application

- ✅ **Sélection de modèle** : Liste déroulante pour choisir le LLM
- ✅ **Interface chat** : Messages alternés utilisateur/assistant
- ✅ **Historique** : Conservation des messages pendant la session
- ✅ **Gestion d'erreurs** : Messages informatifs en cas de problème
- ✅ **Interface moderne** : Utilise les nouveaux composants Streamlit

### Améliorations possibles

#### 1. Liste dynamique des modèles

```python
def get_available_models():
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            return [model["name"] for model in models]
    except:
        return ["llama2"]  # Modèle par défaut

# Dans l'interface
models = get_available_models()
selected_model = st.selectbox("Choisir un modèle :", models)
```

#### 2. Paramètres avancés

```python
st.sidebar.header("Paramètres")

temperature = st.sidebar.slider("Température", 0.0, 2.0, 0.7)
max_tokens = st.sidebar.slider("Tokens max", 50, 2000, 500)

# Dans la requête
response = requests.post(OLLAMA_URL, json={
    "model": selected_model,
    "prompt": prompt,
    "options": {
        "temperature": temperature,
        "num_predict": max_tokens
    }
})
```

#### 3. Streaming en temps réel

```python
# Pour un affichage progressif
response = requests.post(OLLAMA_URL, json={
    "model": selected_model,
    "prompt": prompt,
    "stream": True
}, stream=True)

placeholder = st.empty()
full_response = ""

for line in response.iter_lines():
    if line:
        chunk = json.loads(line.decode('utf-8'))
        if chunk.get("done"):
            break
        token = chunk.get("response", "")
        full_response += token
        placeholder.markdown(full_response + "▌")

placeholder.markdown(full_response)
```

## Modèles recommandés

### Pour le chat général

- **llama2** : Modèle équilibré, bon pour la conversation
- **mistral** : Excellent pour le raisonnement, plus concis
- **vicuna** : Spécialisé dans les conversations naturelles

### Pour la programmation

- **codellama** : Expert en code, génération et explication
- **deepseek-coder** : Spécialisé dans les langages de programmation

### Pour l'analyse de données

- **llama2:13b** : Bonne capacité d'analyse
- **mistral** : Bon pour les tâches structurées

## Dépannage courant

### "Connection refused"

```bash
# Vérifier qu'Ollama tourne
ollama serve

# Ou vérifier le port
netstat -an | grep 11434
```

### "Model not found"

```bash
# Lister les modèles disponibles
ollama list

# Télécharger un modèle
ollama pull llama2
```

### Performance lente

- Utilisez des modèles plus petits (`llama2:7b` au lieu de `llama2:70b`)
- Activez l'accélération GPU si disponible
- Fermez les autres applications gourmandes en RAM

## Ressources et communauté

### Documentation officielle

- [Site web Ollama](https://ollama.ai/)
- [Modèles disponibles](https://ollama.ai/library)
- [Guide d'installation](https://github.com/jmorganca/ollama)

### Communauté

- **Discord Ollama** : Support et discussions
- **Reddit r/ollama** : Partage d'expériences
- **GitHub Issues** : Signalement de bugs

### Alternatives

- **LM Studio** : Interface graphique pour modèles locaux
- **GPT4All** : Alternative open-source
- **LocalAI** : API compatible OpenAI pour modèles locaux

Ollama démocratise l'accès aux LLM en permettant leur exécution locale, offrant confidentialité et contrôle total sur vos données tout en maintenant des performances impressionnantes.
