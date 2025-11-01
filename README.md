# 🤖 Chatbot Streamlit avec Ollama

Une application web interactive pour converser avec des modèles Ollama, avec support pour les prompts personnalisés et la génération de dialogues.

## ✨ Fonctionnalités

- **Chat interactif** avec les modèles Ollama
- **Prompts personnalisables** (système et utilisateur)
- **Paramètres ajustables** (température, top_p, max_tokens)
- **Génération de dialogues** pour des personnages spécifiques
- **Interface intuitive** avec Streamlit

## 🚀 Installation

1. **Cloner le repository**
```bash
git clone <url-du-repo>
cd chatbot_streamlit
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Installer Ollama**
- Télécharger depuis [ollama.ai](https://ollama.ai)
- Installer au moins un modèle : `ollama pull llama2-uncensored`

## 📱 Utilisation

1. **Lancer l'application**
```bash
streamlit run app.py
```

2. **Ouvrir dans le navigateur**
- Aller sur http://localhost:8501

3. **Configurer**
- Choisir un modèle Ollama
- Sélectionner des prompts prédéfinis ou créer les vôtres
- Ajuster les paramètres selon vos besoins

## 📁 Structure du projet

```
chatbot_streamlit/
├── app.py              # Application Streamlit principale
├── ollama_utils.py     # Fonctions utilitaires Ollama
├── prompts.toml        # Configuration des prompts
├── requirements.txt    # Dépendances Python
├── dialogues_text/     # Fichiers de dialogue (optionnel)
└── README.md          # Documentation
```

## ⚙️ Configuration

### Prompts disponibles

**Prompts Système :**
- `neutre` : Assistant utile et neutre
- `creatif` : Assistant créatif et imaginatif  
- `strict` : Assistant strict et factuel

**Prompts Utilisateur :**
- `default` : Réponses claires et concises
- `detaille` : Réponses détaillées et complètes
- `amusant` : Réponses amusantes et légères

### Personnalisation

Modifiez `prompts.toml` pour ajouter vos propres prompts :

```toml
[system_prompts]
expert = "Vous êtes un expert technique..."

[user_prompts]
educatif = "Expliquez comme si vous enseigniez..."
```

## 🛠️ Technologies utilisées

- **Streamlit** : Interface web
- **Ollama** : Modèles de langage locaux
- **Python** : Langage principal
- **TOML** : Configuration des prompts

## 📝 Licence

MIT License

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou proposer une pull request.