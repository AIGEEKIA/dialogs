import streamlit as st
from ollama_utils import get_available_models, get_chat_response, get_file_path, load_prompts, list_log_files, parse_dialogue, get_speakers, generate_dialogue_response, generate_multiple_responses
from pathlib import Path
import random

st.set_page_config(page_title="Chatbot Ollama", layout="centered")
st.title("Chatbot Ollama")

# Charger les prompts
prompts = load_prompts()

# Sélection du modèle
models = get_available_models()
default_model = "llama2-uncensored:latest"
if default_model in models:
    default_index = models.index(default_model)
else:
    default_index = 0
model_name = st.selectbox("Choisissez un modèle Ollama :", models, index=default_index)

# Gestion des prompts
st.header("Configuration des Prompts")

# Prompt système
st.subheader("Prompt Système")
system_prompt_options = list(prompts.get("system_prompts", {}).keys())
default_system_index = 0  # "Aucun"
if "neutre" in system_prompt_options:
    default_system_index = system_prompt_options.index("neutre") + 1
selected_system = st.selectbox("Prompt système prédéfini :", ["Aucun"] + system_prompt_options, index=default_system_index)
if selected_system != "Aucun":
    default_system = prompts["system_prompts"][selected_system]
else:
    default_system = ""
system_prompt = st.text_area("Prompt système (éditable) :", value=default_system, height=100)

# Prompt utilisateur
st.subheader("Prompt Utilisateur")
user_prompt_options = list(prompts.get("user_prompts", {}).keys())
default_user_index = 0  # "Aucun"
if "default" in user_prompt_options:
    default_user_index = user_prompt_options.index("default") + 1
selected_user = st.selectbox("Prompt utilisateur prédéfini :", ["Aucun"] + user_prompt_options, index=default_user_index)
if selected_user != "Aucun":
    default_user = prompts["user_prompts"][selected_user]
else:
    default_user = ""
user_prompt = st.text_area("Prompt utilisateur (éditable) :", value=default_user, height=100)

# Paramètres réglables (curseurs)
st.header("Paramètres du Modèle")
temperature = st.slider("Température", 0.0, 2.0, 1.0, 0.1, label_visibility="collapsed")
top_p = st.slider("Top P", 0.0, 1.0, 0.9, 0.1, label_visibility="collapsed")
max_tokens = st.slider("Max Tokens", 10, 1000, 200, 10, label_visibility="collapsed")

# Interface de chat
st.header("Chat")
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Votre message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = get_chat_response(model_name, prompt, system_prompt, user_prompt, {"temperature": temperature, "top_p": top_p, "max_tokens": max_tokens})
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Section génération de dialogues
st.header("Génération de Dialogues")
dialogue_files = list_log_files("dialogues_text")
if dialogue_files:
    # Extraire juste le nom du fichier pour l'affichage
    file_names = [Path(f).name for f in dialogue_files]
    selected_file_name = st.selectbox("Choisir un fichier de dialogue :", file_names)
    if selected_file_name:
        # Trouver le chemin complet correspondant
        selected_file_path = next(f for f in dialogue_files if Path(f).name == selected_file_name)
        
        with open(selected_file_path, "r", encoding="utf-8") as f:
            dialogue_text = f.read()
        st.text_area("Dialogue actuel :", value=dialogue_text, height=200, disabled=True)

        speakers = get_speakers(parse_dialogue(selected_file_path))
        if speakers:
            character = st.selectbox("Choisir le personnage à faire parler :", speakers)
            if st.button("Générer une réponse"):
                dialogue_lines = parse_dialogue(selected_file_path)
                response = generate_dialogue_response(model_name, character, dialogue_lines, system_prompt, user_prompt, {"temperature": temperature, "top_p": top_p, "max_tokens": max_tokens})
                st.write(f"**{character} :** {response[0]}")
                st.write(f"*Instruction : {response[1]}*")

            num_responses = st.slider("Nombre de réponses à générer :", 1, 5, 3)
            if st.button("Générer plusieurs réponses"):
                dialogue_lines = parse_dialogue(selected_file_path)
                responses = generate_multiple_responses(model_name, character, dialogue_lines, system_prompt, user_prompt, {"temperature": temperature, "top_p": top_p, "max_tokens": max_tokens}, num_responses=num_responses)
                for i, resp in enumerate(responses, 1):
                    st.write(f"**Option {i} : {character} :** {resp}")
else:
    st.write("Aucun fichier de dialogue trouvé dans dialogues_text/")