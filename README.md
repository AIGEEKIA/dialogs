# 🤗 Chatbot Psychologue

Un assistant IA spécialisé en psychologie utilisant RAG (Retrieval-Augmented Generation) avec des données locales.

## 🎯 Objectif

Créer un chatbot psychologue qui :
- Utilise des connaissances spécialisées en psychologie stockées localement
- Respecte la confidentialité des données (tout reste local)
- Fournit un soutien empathique et informatif
- Oriente vers des professionnels quand nécessaire

## 🏗️ Architecture

### RAG (Retrieval-Augmented Generation)
- **Base de connaissances locale** : Documents Markdown avec concepts psychologiques
- **Recherche sémantique** : Recherche par mots-clés dans les documents
- **Génération augmentée** : LLM enrichi avec contexte pertinent
- **Confidentialité** : Aucune donnée ne quitte votre machine

### Structure des fichiers
```
psychologie_data/
├── connaissances_base.md    # Concepts fondamentaux de psychologie
└── [autres documents...]

psychologue_chatbot.py       # Application Streamlit principale
start_psychologue.bat        # Script de démarrage
```

## 🚀 Démarrage rapide

### Prérequis
- Python 3.8+
- Ollama installé avec un modèle (ex: llama2, mistral)

### Installation
```bash
# Cloner le repository
git clone <repository-url>
cd chatbot_streamlit

# Créer l'environnement virtuel
python -m venv .venv
.venv\Scripts\activate  # Windows
# ou
source .venv/bin/activate  # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt
```

### Lancement
```bash
# Double-clic sur start_psychologue.bat
# ou en ligne de commande :
streamlit run psychologue_chatbot.py --server.port 8501
```

## 📚 Base de connaissances

### Contenu actuel
- **Anxiété** : Symptômes, causes, gestion
- **Dépression** : Signes, traitement, prévention
- **Stress** : Eustress vs distress, gestion
- **Troubles du sommeil** : Impact sur la santé mentale
- **Thérapies** : TCC, relaxation, méditation
- **Émotions** : Intelligence émotionnelle, régulation
- **Santé mentale** : Burnout, réseaux sociaux
- **Psychologie positive** : Flow, gratitude, résilience

### Extension
Ajoutez vos propres documents dans `psychologie_data/` :
- Format Markdown (.md)
- Structure avec titres et sous-titres
- Contenu validé par des sources fiables

## 🔧 Fonctionnalités

### Interface utilisateur
- 💬 Chat en temps réel
- 📚 Recherche dans la base de connaissances
- ⚙️ Configuration du modèle Ollama
- 🗑️ Gestion de l'historique
- 🔄 Rechargement de la base

### Moteur RAG
- Recherche par mots-clés
- Scoring de pertinence
- Extraction d'extraits contextuels
- Génération enrichie par le contexte

## ⚠️ Disclaimer important

**Ce chatbot n'est PAS :**
- ❌ Un diagnostic médical
- ❌ Un traitement thérapeutique
- ❌ Un substitut à un professionnel de santé

**Il est :**
- ✅ Un outil d'information générale
- ✅ Un soutien empathique temporaire
- ✅ Une orientation vers des ressources professionnelles

## 🔒 Confidentialité et sécurité

- 🔐 **Données locales** : Rien ne quitte votre machine
- 🛡️ **Aucune collecte** : Pas de tracking ou analytics
- 🔒 **Stockage sécurisé** : Conversations en mémoire session uniquement

## 🚀 Évolutions possibles

### Court terme
- [ ] Ajout de plus de documents spécialisés
- [ ] Amélioration de l'algorithme de recherche
- [ ] Interface plus intuitive

### Moyen terme
- [ ] Support multimodal (images, audio)
- [ ] Intégration avec des bases de données médicales
- [ ] Mode "urgence" avec ressources d'aide

### Long terme
- [ ] Framework RAG plus sophistiqué (comme ApeRAG)
- [ ] Apprentissage continu des interactions
- [ ] Personnalisation par profil utilisateur

## 🤝 Contribution

Pour contribuer :
1. Fork le repository
2. Créer une branche feature
3. Ajouter/modifier du contenu dans `psychologie_data/`
4. Tester les changements
5. Pull request

## 📞 Support

En cas de détresse psychologique réelle :
- 🚨 **SAMU** : 15 (France)
- 🏥 **SOS Médecins** : 3624
- 💙 **SOS Amitié** : 09 72 39 40 50
- 🌐 **Fil Santé Jeunes** : 0 800 235 236

---

*Ce projet est développé avec ❤️ pour aider et informer, pas pour remplacer les professionnels de santé.*