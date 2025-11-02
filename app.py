
import streamlit as st
from ollama_utils import get_available_models, get_chat_response, get_file_path, load_prompts, list_log_files, parse_dialogue, get_speakers, generate_dialogue_response, generate_multiple_responses
from pathlib import Path
import toml


# Charger les prompts
prompts = load_prompts()

# Gestion multi-dossiers
config_path = Path("config.toml")
if config_path.exists():
    config = toml.load(config_path)
    dialogue_dirs = config.get("dialogue_dirs", {}).get("dirs", ["dialogues_text"])
    active_dir = config.get("dialogue_dirs", {}).get("active", dialogue_dirs[0])
else:
    dialogue_dirs = ["dialogues_text"]
    active_dir = "dialogues_text"

st.header("Dossiers de dialogues")
selected_dir = st.selectbox("Choisir le dossier de dialogues :", dialogue_dirs, index=dialogue_dirs.index(active_dir) if active_dir in dialogue_dirs else 0, key="selectbox_dossier")
if st.button("Définir comme dossier actif"):
    config["dialogue_dirs"]["active"] = selected_dir
    with open(config_path, "w", encoding="utf-8") as f:
        toml.dump(config, f)
    st.success(f"Dossier actif sauvegardé : {selected_dir}")

# Ajout d'un nouveau dossier

# Création du dialogue (en haut)
st.header("Génération de Dialogues")


# Sélection et affichage du dialogue dans le dossier actif
dialogue_files = list_log_files(selected_dir)
if dialogue_files:
    file_names = [Path(f).name for f in dialogue_files]
    
    # Initialiser selected_file_name dans session_state si pas déjà fait
    if 'selected_file_name' not in st.session_state:
        st.session_state.selected_file_name = file_names[0] if file_names else None
    
    # S'assurer que le fichier sélectionné existe encore dans la liste
    if st.session_state.selected_file_name not in file_names:
        st.session_state.selected_file_name = file_names[0] if file_names else None
    
    def update_file_selection():
        st.session_state.selected_file_name = st.session_state.main_file_selector
        
    selected_file_name = st.selectbox("Choisir un fichier de dialogue :", file_names, 
                                    index=file_names.index(st.session_state.selected_file_name) if st.session_state.selected_file_name in file_names else 0,
                                    key="main_file_selector", on_change=update_file_selection)
    st.session_state.selected_file_name = selected_file_name
    
    selected_file_path = next(f for f in dialogue_files if Path(f).name == st.session_state.selected_file_name)
    # ...existing code...


    speakers = get_speakers(parse_dialogue(selected_file_path))
    if speakers:

            # Ajout de la configuration du prompt système
            st.subheader("Prompt Système")
            system_prompt_options = list(prompts.get("system_prompts", {}).keys())
            # Sélectionne le premier prompt système de la liste comme défaut
            if system_prompt_options:
                selected_system = st.selectbox(
                    "Prompt système prédéfini :",
                    system_prompt_options,
                    index=0,
                    key=f"selectbox_system_{selected_file_name}"
                )
                default_system = prompts["system_prompts"].get(selected_system, "")
            else:
                selected_system = st.selectbox(
                    "Prompt système prédéfini :",
                    ["Aucun"],
                    index=0,
                    key=f"selectbox_system_{selected_file_name}"
                )
                default_system = ""
            # Affiche le texte du prompt sélectionné dans le text_area
            system_prompt = st.text_area("Prompt système (éditable)", value=default_system, height=100, key=f"textarea_system_{selected_file_name}")

            # Réglages juste sous le prompt système
            st.markdown("**Réglages du modèle**")
            temperature = st.slider("Température", 0.0, 2.0, 1.0, 0.1, key=f"slider_temp_{st.session_state.selected_file_name}")
            top_p = st.slider("Top P", 0.0, 1.0, 0.9, 0.1, key=f"slider_top_p_{st.session_state.selected_file_name}")
            max_tokens = st.slider("Max Tokens", 10, 500, 50, 10, key=f"slider_max_tokens_{st.session_state.selected_file_name}")
            models = get_available_models()
            model_name = st.selectbox("Choisissez un modèle Ollama :", models, key=f"selectbox_model_{st.session_state.selected_file_name}")

            # Rechoix du fichier de dialogue après le modèle
            dialogue_files = list_log_files(selected_dir)
            if dialogue_files:
                file_names = [Path(f).name for f in dialogue_files]
                
                selected_file_name_secondary = st.selectbox("Changer de fichier de dialogue :", file_names, 
                                                index=file_names.index(st.session_state.selected_file_name) if st.session_state.selected_file_name in file_names else 0, 
                                                key="secondary_file_selector")
                
                # Si le fichier a changé via le deuxième selectbox, mettre à jour
                if selected_file_name_secondary != st.session_state.selected_file_name:
                    st.session_state.selected_file_name = selected_file_name_secondary
                    selected_file_path = next(f for f in dialogue_files if Path(f).name == selected_file_name_secondary)
                    speakers = get_speakers(parse_dialogue(selected_file_path))
            
            # Choix du personnage (mis à jour avec les nouveaux speakers)
            character = st.selectbox("Choisir le personnage à faire parler :", speakers, key=f"selectbox_character_{st.session_state.selected_file_name}")
            if speakers and character not in speakers:
                character = speakers[0]  # Sélectionner le premier speaker si l'ancien n'existe plus
            
            # Affichage du dialogue juste sous le choix du personnage
            
            # Affichage du dialogue juste sous le choix du personnage
            with open(selected_file_path, "r", encoding="utf-8") as f:
                dialogue_text = f.read()
            # Nettoie les lignes vides tout en gardant l'ordre normal
            dialogue_lines = dialogue_text.split('\n')
            dialogue_lines = [line for line in dialogue_lines if line.strip()]
            dialogue_text = '\n'.join(dialogue_lines)
            st.subheader("📜 Dialogue actuel")
            dialogue_html = dialogue_text.replace('\n', '<br>')
            
            # Utilise CSS pour forcer le scroll en bas
            st.markdown("""
            <style>
            .dialogue-container {
                font-size: 1.1em;
                line-height: 1.6;
                background: #232336;
                color: #e8e9f3;
                border-radius: 10px;
                padding: 20px;
                border-left: 4px solid #6366f1;
                margin: 10px 0;
                max-height: 300px;
                overflow-y: auto;
                font-family: monospace;
                display: flex;
                flex-direction: column-reverse;
            }
            .dialogue-content {
                display: flex;
                flex-direction: column;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown(f'''
            <div class="dialogue-container">
                <div class="dialogue-content">
                    {dialogue_html}
                </div>
            </div>
            ''', unsafe_allow_html=True)

            # Prompt utilisateur après le personnage
            user_prompt_options = list(prompts.get("user_prompts", {}).keys())
            # Sélectionne le premier prompt utilisateur comme défaut
            if user_prompt_options:
                selected_user = st.selectbox(
                    "Prompt utilisateur pour cette génération :",
                    user_prompt_options,
                    index=0,
                    key=f"selectbox_user_{selected_file_name}"
                )
                default_user = prompts["user_prompts"][selected_user]
            else:
                selected_user = st.selectbox(
                    "Prompt utilisateur pour cette génération :",
                    ["Aucun"],
                    index=0,
                    key=f"selectbox_user_{selected_file_name}"
                )
                default_user = f"Répondez en tant que {{character}} de façon naturelle et cohérente avec le contexte du dialogue."
            # Affiche le texte du prompt sélectionné dans le text_area
            local_user_prompt = st.text_area("Prompt utilisateur (éditable - utilisez {character} pour le nom du personnage):", value=default_user, height=80, key=f"textarea_user_{selected_file_name}")
            final_user_prompt = local_user_prompt.replace("{character}", character)

            if st.button("Générer une réponse", key=f"gen_response_{selected_file_name}_{character}"):
                # Rafraîchit le dialogue en arrière-plan avant la génération
                with open(selected_file_path, "r", encoding="utf-8") as f:
                    dialogue_text = f.read()
                dialogue_lines = parse_dialogue(selected_file_path)
                response = generate_dialogue_response(model_name, character, dialogue_lines, system_prompt, final_user_prompt, {"temperature": temperature, "top_p": top_p, "max_tokens": max_tokens})
                
                # Affiche seulement la réponse du personnage
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
