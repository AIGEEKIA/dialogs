# 🤗 Chatbot Psychologue

Un assistant IA spécialisé en psychologie utilisant RAG (Retrieval-Augmented Generation) avec des données locales.

## ⚠️ AVERTISSEMENTS IMPORTANTS

### 🚨 **CE PROJET EST UN EXEMPLE ÉDUCATIF UNIQUEMENT**

**Ce chatbot est un exemple technique de RAG (Retrieval-Augmented Generation) appliqué à la psychologie.** Il n'est en aucun cas destiné à fournir des conseils médicaux, psychologiques ou thérapeutiques.

### 🩺 **LIMITATIONS CRITIQUES**
- ❌ **PAS un diagnostic médical** : Ne peut pas diagnostiquer de troubles mentaux
- ❌ **PAS un traitement** : Ne peut pas remplacer une thérapie professionnelle
- ❌ **PAS un avis médical** : Les réponses sont génériques et informatives uniquement
- ❌ **PAS une urgence** : En cas de détresse psychologique, contactez immédiatement un professionnel

### 🎯 **CE QUE C'EST VRAIMENT**
- ✅ **Exemple de RAG** : Démonstration technique d'intelligence artificielle locale
- ✅ **Outil éducatif** : Présentation de concepts psychologiques de base
- ✅ **Support temporaire** : Écoute empathique non-professionnelle
- ✅ **Orientation** : Guide vers les ressources d'aide appropriées

### 🔄 **ADAPTABLE À D'AUTRES DOMAINES**
Ce code peut être facilement adapté à d'autres domaines :
- 📚 **Éducation** : Chatbot pédagogique avec base de connaissances scolaire
- 💼 **Ressources humaines** : Assistant RH avec politiques d'entreprise
- 🏥 **Santé générale** : Information sur la prévention (mais JAMAIS de diagnostic)
- 📖 **Documentation** : Assistant recherche dans des bases documentaires

### 🚨 **PRÉCAUTIONS ABSOLUES**
1. **Ne prenez PAS ce chatbot comme substitut à une aide thérapeutique ou médicale**
2. **En cas de détresse psychologique** : Contactez un professionnel de santé
3. **Pour tout problème médical** : Consultez un médecin qualifié
4. **Les réponses sont génériques** : Elles ne tiennent pas compte de votre situation personnelle
5. **L'IA ne remplace pas l'humain** : L'empathie et l'expertise humaine sont irremplaçables

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