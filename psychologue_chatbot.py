import streamlit as st
import os
from pathlib import Path
import re
from typing import List, Dict, Tuple
import json
from datetime import datetime

# Import Ollama utilities (version simplifiée)
try:
    from ollama_utils_simple import get_available_models, get_chat_response
except ImportError:
    st.error("Erreur: Impossible d'importer ollama_utils_simple. Assurez-vous que le fichier existe.")
    st.stop()

class PsychologueChatbot:
    def __init__(self, data_dir: str = "psychologie_data"):
        self.data_dir = Path(data_dir)
        self.knowledge_base = self.load_knowledge_base()

    def load_knowledge_base(self) -> Dict[str, str]:
        """Charge la base de connaissances depuis les fichiers Markdown"""
        knowledge = {}

        if not self.data_dir.exists():
            return knowledge

        for file_path in self.data_dir.glob("*.md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Extraire le titre du fichier
                    title = file_path.stem.replace('_', ' ').title()
                    knowledge[title] = content
            except Exception as e:
                st.warning(f"Erreur lors du chargement de {file_path}: {e}")

        return knowledge

    def search_knowledge(self, query: str, max_results: int = 3) -> List[Tuple[str, str, float]]:
        """Recherche dans la base de connaissances avec scoring de pertinence"""
        results = []

        # Tokenization simple de la requête
        query_words = set(re.findall(r'\b\w+\b', query.lower()))

        for title, content in self.knowledge_base.items():
            # Recherche dans le titre
            title_score = len(query_words.intersection(set(re.findall(r'\b\w+\b', title.lower()))))

            # Recherche dans le contenu
            content_words = set(re.findall(r'\b\w+\b', content.lower()))
            content_score = len(query_words.intersection(content_words))

            # Score total (titre plus important)
            total_score = title_score * 2 + content_score

            if total_score > 0:
                # Extraire un extrait pertinent autour des mots-clés trouvés
                excerpt = self.extract_relevant_excerpt(content, query_words)
                results.append((title, excerpt, total_score))

        # Trier par score décroissant et limiter les résultats
        results.sort(key=lambda x: x[2], reverse=True)
        return results[:max_results]

    def extract_relevant_excerpt(self, content: str, query_words: set, context_chars: int = 200) -> str:
        """Extrait un passage pertinent du contenu autour des mots-clés"""
        content_lower = content.lower()

        # Trouver la première occurrence d'un mot-clé
        best_pos = len(content)
        for word in query_words:
            pos = content_lower.find(word)
            if pos != -1 and pos < best_pos:
                best_pos = pos

        if best_pos == len(content):
            # Aucun mot-clé trouvé, retourner le début du contenu
            return content[:context_chars] + "..."

        # Extraire autour de la position trouvée
        start = max(0, best_pos - context_chars // 2)
        end = min(len(content), best_pos + context_chars // 2)

        excerpt = content[start:end]
        if start > 0:
            excerpt = "..." + excerpt
        if end < len(content):
            excerpt = excerpt + "..."

        return excerpt

    def generate_response(self, user_message: str, model_name: str, conversation_history: List[Dict] = None) -> str:
        """Génère une réponse en utilisant RAG + LLM"""

        # Recherche dans la base de connaissances
        relevant_docs = self.search_knowledge(user_message)

        # Construire le contexte avec les documents pertinents
        context = ""
        if relevant_docs:
            context = "\n\n".join([
                f"📚 Information pertinente - {title}:\n{excerpt}"
                for title, excerpt, score in relevant_docs
            ])

        # Prompt système pour le psychologue
        system_prompt = """Tu es un psychologue clinicien empathique et professionnel.
Tu dois :
- Écouter activement et montrer de l'empathie
- Utiliser les connaissances psychologiques fournies quand c'est pertinent
- Éviter de donner des diagnostics médicaux définitifs
- Encourager l'utilisateur à consulter un professionnel si nécessaire
- Répondre en français de manière naturelle et bienveillante
- Ne jamais remplacer un suivi thérapeutique professionnel

Connaissances disponibles :
{context}

Si tu n'as pas assez d'informations spécifiques, utilise tes connaissances générales en psychologie."""

        # Historique de conversation
        if conversation_history is None:
            conversation_history = []

        # Ajouter le message utilisateur à l'historique
        conversation_history.append({"role": "user", "content": user_message})

        # Construire le prompt avec contexte
        full_prompt = f"""Contexte psychologique pertinent :
{context}

Question de l'utilisateur : {user_message}

Réponds en tant que psychologue professionnel, utilisant les informations ci-dessus si elles sont pertinentes."""

        try:
            # Utiliser Ollama pour générer la réponse
            response = get_chat_response(
                model_name=model_name,
                user_message=full_prompt,
                system_prompt=system_prompt
            )

            # Ajouter la réponse à l'historique
            conversation_history.append({"role": "assistant", "content": response})

            return response

        except Exception as e:
            return f"Erreur lors de la génération de la réponse : {e}"

def main():
    st.set_page_config(
        page_title="Chatbot Psychologue 🤗",
        page_icon="🧠",
        layout="wide"
    )

    st.title("🧠 Chatbot Psychologue")
    st.markdown("*Un assistant IA pour l'écoute et le soutien psychologique*")

    # AVERTISSEMENT CRITIQUE
    st.error("🚨 **AVERTISSEMENT CRITIQUE** 🚨")
    st.markdown("""
    **CE CHATBOT EST UN EXEMPLE TECHNIQUE DE RAG UNIQUEMENT**

    - ❌ **PAS de diagnostic médical** : Ne peut pas diagnostiquer de troubles mentaux
    - ❌ **PAS de traitement** : Ne remplace pas une thérapie professionnelle
    - ❌ **PAS d'urgence** : En cas de détresse, contactez immédiatement un professionnel

    ✅ **C'est un exemple éducatif** qui peut être adapté à d'autres domaines (éducation, RH, documentation)
    """)

    # Initialiser le chatbot
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = PsychologueChatbot()

    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    if 'current_model' not in st.session_state:
        st.session_state.current_model = None

    # Sidebar pour la configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Sélection du modèle
        models = get_available_models()
        if models:
            selected_model = st.selectbox(
                "Modèle Ollama :",
                models,
                index=models.index(st.session_state.current_model) if st.session_state.current_model in models else 0
            )
            st.session_state.current_model = selected_model
        else:
            st.error("Aucun modèle Ollama disponible. Lancez Ollama et installez un modèle.")
            return

        # Informations sur la base de connaissances
        st.header("📚 Base de connaissances")
        num_docs = len(st.session_state.chatbot.knowledge_base)
        st.info(f"{num_docs} documents chargés")

        if st.button("🔄 Recharger la base"):
            st.session_state.chatbot = PsychologueChatbot()
            st.success("Base de connaissances rechargée !")

        # Bouton pour effacer l'historique
        if st.button("🗑️ Effacer la conversation"):
            st.session_state.conversation_history = []
            st.success("Conversation effacée !")

    # Zone principale de chat
    st.header("💬 Discussion")

    # Afficher l'historique des messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.conversation_history:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
            else:
                with st.chat_message("assistant"):
                    st.write(message["content"])

    # Input pour nouveau message
    if prompt := st.chat_input("Partagez ce qui vous préoccupe..."):
        if not st.session_state.current_model:
            st.error("Veuillez sélectionner un modèle dans la sidebar.")
            return

        # Ajouter le message utilisateur
        with chat_container:
            with st.chat_message("user"):
                st.write(prompt)

        # Générer la réponse
        with chat_container:
            with st.chat_message("assistant"):
                with st.spinner("Le psychologue réfléchit..."):
                    response = st.session_state.chatbot.generate_response(
                        prompt,
                        st.session_state.current_model,
                        st.session_state.conversation_history
                    )
                st.write(response)

        # Ajouter à l'historique
        st.session_state.conversation_history.append({"role": "user", "content": prompt})
        st.session_state.conversation_history.append({"role": "assistant", "content": response})

        # Scroll automatique vers le bas
        st.rerun()

    # Footer avec disclaimer renforcé
    st.markdown("---")
    st.error("🚨 **RAPPEL CRITIQUE** 🚨")
    st.markdown("""
    **CE CHATBOT EST UN EXEMPLE TECHNIQUE DE RAG - PAS UN OUTIL MÉDICAL**

    - 🩺 **Jamais de diagnostic** : L'IA ne peut pas remplacer un professionnel de santé
    - 💊 **Jamais de traitement** : Les réponses sont informatives uniquement
    - 🚑 **En cas d'urgence** : Contactez immédiatement les services appropriés

    **Ressources d'aide professionnelles :**
    - 🇫🇷 **SAMU** : 15 (urgences médicales)
    - 🇫🇷 **SOS Médecins** : 3624
    - 🇫🇷 **SOS Amitié** : 09 72 39 40 50 (écoute 24h/24)
    - 🇫🇷 **Fil Santé Jeunes** : 0 800 235 236 (3-25 ans)
    - 🌐 **Votre médecin traitant** ou **psychologue**

    *Ce projet est un exemple éducatif qui peut être adapté à d'autres domaines.*
    """)

if __name__ == "__main__":
    main()