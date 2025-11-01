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

## Prompt utilisateur supprimé ici, il sera affiché uniquement avant la génération de réponse

# Paramètres réglables (curseurs)
st.header("Paramètres du Modèle")
temperature = st.slider("Température", 0.0, 2.0, 1.0, 0.1, label_visibility="collapsed")
top_p = st.slider("Top P", 0.0, 1.0, 0.9, 0.1, label_visibility="collapsed")
max_tokens = st.slider("Max Tokens", 10, 500, 50, 10, label_visibility="collapsed")

# Interface de chat
st.header("Chat")
if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.markdown(f'''<div style="font-size:1.25em;font-weight:500;border-radius:14px;border:2px solid #6366f1;background:#f3f3f7;padding:18px 22px 14px 22px;margin:12px 0;color:#232336;box-shadow:0 2px 12px #6366f133;">{message["content"]}</div>''', unsafe_allow_html=True)
        elif message["role"] == "user":
            st.markdown(f'''<div style="font-size:1.15em;font-weight:500;border-radius:14px;border:2px solid #22c55e;background:#e7ffe7;padding:16px 20px 12px 20px;margin:12px 0;color:#1e2e1e;box-shadow:0 2px 12px #22c55e33;">{message["content"]}</div>''', unsafe_allow_html=True)
        else:
            st.markdown(message["content"])

if prompt := st.chat_input("Votre message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f'''<div style="font-size:1.15em;font-weight:500;border-radius:14px;border:2px solid #22c55e;background:#e7ffe7;padding:16px 20px 12px 20px;margin:12px 0;color:#1e2e1e;box-shadow:0 2px 12px #22c55e33;">{prompt}</div>''', unsafe_allow_html=True)

    with st.chat_message("assistant"):
        response = get_chat_response(model_name, prompt, system_prompt, "", {"temperature": temperature, "top_p": top_p, "max_tokens": max_tokens})
        st.markdown(f'''<div style="font-size:1.25em;font-weight:500;border-radius:14px;border:2px solid #6366f1;background:#f3f3f7;padding:18px 22px 14px 22px;margin:12px 0;color:#232336;box-shadow:0 2px 12px #6366f133;">{response}</div>''', unsafe_allow_html=True)
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
        
        st.subheader("📜 Dialogue actuel")
        # Conversion des retours à la ligne en HTML
        dialogue_html = dialogue_text.replace('\n', '<br>')
        st.markdown(f'''
        <div style="
            font-size: 1.1em;
            line-height: 1.6;
            background: #2a2d3a;
            color: #e8e9f3;
            border-radius: 10px;
            padding: 20px;
            border-left: 4px solid #6366f1;
            margin: 10px 0;
            max-height: 300px;
            overflow-y: auto;
            font-family: monospace;
        ">
        {dialogue_html}
        </div>
        ''', unsafe_allow_html=True)

        speakers = get_speakers(parse_dialogue(selected_file_path))
        if speakers:
            character = st.selectbox("Choisir le personnage à faire parler :", speakers)

            # Choix du prompt utilisateur uniquement
            user_prompt_options = list(prompts.get("user_prompts", {}).keys())
            selected_user = st.selectbox("Prompt utilisateur pour cette génération :", ["Aucun"] + user_prompt_options)
            if selected_user != "Aucun":
                default_user = prompts["user_prompts"][selected_user]
            else:
                default_user = f"Répondez en tant que {{character}} de façon naturelle et cohérente avec le contexte du dialogue."
            local_user_prompt = st.text_area("Prompt utilisateur (éditable - utilisez {character} pour le nom du personnage):", value=default_user, height=80)
            
            # Remplacer {character} par le nom du personnage choisi
            final_user_prompt = local_user_prompt.replace("{character}", character)

            if st.button("Générer une réponse"):
                dialogue_lines = parse_dialogue(selected_file_path)
                response = generate_dialogue_response(model_name, character, dialogue_lines, system_prompt, final_user_prompt, {"temperature": temperature, "top_p": top_p, "max_tokens": max_tokens})
                st.subheader(f"**{character}**")
                st.markdown(f'''<div style="font-size:1.25em;font-weight:500;border-radius:14px;border:2px solid #f59e42;background:#fff7e7;padding:18px 22px 14px 22px;margin:12px 0;color:#332a1e;box-shadow:0 2px 12px #f59e4233;">{response[0]}</div>''', unsafe_allow_html=True)
                st.write(f"*Instruction : {response[1]}*")

            num_responses = st.slider("Nombre de réponses à générer :", 1, 5, 3)
            if st.button("Générer plusieurs réponses"):
                dialogue_lines = parse_dialogue(selected_file_path)
                responses = generate_multiple_responses(model_name, character, dialogue_lines, system_prompt, final_user_prompt, {"temperature": temperature, "top_p": top_p, "max_tokens": max_tokens}, num_responses=num_responses)
                for i, resp in enumerate(responses, 1):
                    st.subheader(f"**Option {i} : {character}**")
                    st.markdown(f'''<div style="font-size:1.25em;font-weight:500;border-radius:14px;border:2px solid #f59e42;background:#fff7e7;padding:18px 22px 14px 22px;margin:12px 0;color:#332a1e;box-shadow:0 2px 12px #f59e4233;">{resp}</div>''', unsafe_allow_html=True)
else:
    st.write("Aucun fichier de dialogue trouvé dans dialogues_text/")