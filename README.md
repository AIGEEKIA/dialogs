# 🎭 Assistant de Dialogues avec Ollama

Une application de surveillance de dialogues qui utilise l'IA pour assister à la gestion des réponses dans des conversations. L'application surveille un dossier de fichiers de dialogue et permet de générer des réponses contextuelles pour différents personnages avec un contrôle précis du comportement du LLM.

## 🎯 Objectif Principal

Cette application est conçue pour **assister les créateurs de contenu, scénaristes, auteurs et développeurs de chatbots** dans la gestion et la continuation de dialogues complexes. Elle surveille un dossier de fichiers de dialogue et offre une interface intelligente pour :

- 👥 **Choisir le personnage** qui doit répondre
- 🎨 **Contrôler le comportement du LLM** (créatif, strict, neutre)
- 📝 **Personnaliser les prompts** système et utilisateur
- ⚡ **Générer plusieurs options** de réponses
- 🔄 **Surveillance automatique** des fichiers de dialogue

## ✨ Fonctionnalités

### 🎭 Gestion Intelligente des Dialogues
- **Surveillance de dossier** : Détection automatique des nouveaux dialogues
- **Sélection de personnages** : Choix du personnage qui doit répondre
- **Analyse contextuelle** : Compréhension du ton et du style de chaque personnage
- **Génération multiple** : Plusieurs options de réponses pour choisir la meilleure

### 🎨 Contrôle du Comportement IA
- **Prompts système personnalisables** : Définir la personnalité de l'IA
- **Prompts utilisateur adaptatifs** : Contrôler le style de réponse
- **Paramètres fins** : Température, top_p, max_tokens pour un contrôle précis
- **Modèles multiples** : Support de tous les modèles Ollama

### 💬 Interface Chat Intégrée
- **Chat en temps réel** avec les modèles Ollama
- **Historique des conversations** maintenu
- **Test rapide** des prompts et paramètres

## 🏗️ Justification des Choix Techniques

### Pourquoi Streamlit ?
- ✅ **Prototypage rapide** : Interface web en quelques lignes
- ✅ **Réactivité** : Rechargement automatique lors des modifications
- ✅ **Widgets intuitifs** : Sliders, selectbox, text_area prêts à l'emploi
- ✅ **Déploiement simple** : Un seul fichier `streamlit run app.py`

### Pourquoi Ollama ?
- ✅ **Local et privé** : Pas de données envoyées vers des API externes
- ✅ **Performance** : Modèles optimisés pour le matériel local
- ✅ **Flexibilité** : Support de nombreux modèles (Llama, Mistral, etc.)
- ✅ **Coût zéro** : Pas d'abonnement ou de coûts par token

### Pourquoi Watchdog ?
- ✅ **Surveillance en temps réel** : Détection automatique des modifications
- ✅ **Efficacité** : Pas besoin de polling constant
- ✅ **Cross-platform** : Fonctionne sur Windows, macOS, Linux
- ✅ **Intégration Streamlit** : Rechargement automatique lors des changements

### Pourquoi TOML pour la configuration ?
- ✅ **Lisibilité** : Format human-friendly
- ✅ **Structure** : Organisation claire des prompts
- ✅ **Édition facile** : Modification rapide sans redémarrage
- ✅ **Standard** : Format moderne et bien supporté

## 🎬 Cas d'Usage Concrets

### 📚 Création de Contenu
- **Scénaristes** : Développer des dialogues naturels entre personnages
- **Auteurs** : Maintenir la cohérence des voix de personnages dans un roman
- **Game Designers** : Créer des dialogues de PNJ adaptatifs

### 🤖 Développement de Chatbots
- **Entraînement de personnalités** : Tester différents comportements IA
- **Validation de réponses** : Générer plusieurs options pour A/B testing
- **Affinement de prompts** : Optimiser les instructions pour des cas spécifiques

### 🎓 Éducation et Formation
- **Simulations pédagogiques** : Créer des dialogues éducatifs interactifs
- **Formation en communication** : Pratiquer différents styles conversationnels
- **Analyse comportementale** : Étudier les patterns de dialogue

## 🔄 Workflow Typique

1. **📁 Préparation** : Placer les fichiers de dialogue dans `dialogues_text/`
2. **🎯 Configuration** : Choisir le modèle et ajuster les prompts
3. **👤 Sélection** : Choisir le personnage qui doit répondre
4. **🎨 Génération** : Créer plusieurs options de réponses
5. **✅ Validation** : Sélectionner la meilleure réponse
6. **📝 Intégration** : Copier la réponse dans le dialogue original

## 🎛️ Contrôle Granulaire du LLM

### Niveaux de Contrôle

#### 🏗️ **Niveau Architecture** (Prompts Système)
```toml
[system_prompts]
creatif = "Vous êtes un assistant créatif qui privilégie l'originalité"
analytique = "Vous êtes un assistant factuel et méthodique"
empathique = "Vous êtes un assistant bienveillant et à l'écoute"
```

#### 🎯 **Niveau Comportement** (Prompts Utilisateur)
```toml
[user_prompts]
concis = "Répondez en une phrase maximum"
detaille = "Développez votre réponse avec des exemples"
dramatique = "Ajoutez de la tension émotionnelle"
```

#### ⚙️ **Niveau Technique** (Paramètres)
- **Température** (0.0-2.0) : Créativité vs Cohérence
- **Top P** (0.0-1.0) : Diversité du vocabulaire
- **Max Tokens** (10-1000) : Longueur des réponses

### Combinaisons Recommandées

| Cas d'Usage | Système | Utilisateur | Température | Top P |
|-------------|---------|-------------|-------------|--------|
| **Dialogue naturel** | `neutre` | `default` | 0.7 | 0.9 |
| **Créativité littéraire** | `creatif` | `detaille` | 1.2 | 0.95 |
| **Consistance technique** | `strict` | `concis` | 0.3 | 0.8 |
| **Émotion dramatique** | `empathique` | `dramatique` | 0.9 | 0.9 |

## 🛠️ Prérequis

### 1. Ollama
```bash
# Télécharger et installer Ollama depuis https://ollama.ai
# Puis installer au moins un modèle :
ollama pull llama2-uncensored:latest
ollama pull mistral:7b
```

### 2. Python 3.8+
```bash
python --version  # Vérifier la version
```

## �🚀 Installation

### 1. Cloner le repository

```bash
git clone https://github.com/votre-username/chatbot-streamlit-ollama.git
cd chatbot_streamlit
```

### 2. Créer un environnement virtuel (recommandé)

```bash
# Créer l'environnement
python -m venv .venv

# Activer l'environnement
# Sur Windows :
.venv\Scripts\activate
# Sur macOS/Linux :
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Vérifier l'installation d'Ollama

```bash
ollama list  # Voir les modèles installés
ollama serve  # Démarrer le serveur Ollama (si pas déjà démarré)
```

## 📱 Utilisation

### Démarrage rapide

```bash
# S'assurer qu'Ollama tourne
ollama serve

# Dans un autre terminal, lancer l'app
streamlit run app.py
```

### Développement avec watchdog

Pour le développement, Streamlit inclut déjà le rechargement automatique :

```bash
streamlit run app.py --server.runOnSave=true
```

### Accès à l'application

- **Local** : <http://localhost:8501>
- **Réseau** : <http://votre-ip:8501>

## 📁 Structure du projet

```
chatbot_streamlit/
├── app.py                 # 🎯 Application Streamlit principale
├── ollama_utils.py        # 🔧 Fonctions utilitaires Ollama
├── prompts.toml          # ⚙️ Configuration des prompts
├── requirements.txt      # 📦 Dépendances Python
├── dialogues_text/       # 💬 Fichiers de dialogue (optionnel)
│   ├── dialogue1.txt
│   ├── dialogue2.txt
│   └── ...
├── .gitignore           # 🚫 Fichiers ignorés par Git
├── .venv/               # 🐍 Environnement virtuel
└── README.md            # 📖 Documentation
```

## ⚙️ Configuration

### Prompts disponibles

#### 🎭 Prompts Système (personnalité de l'IA)
- **`neutre`** : Assistant utile et neutre
- **`creatif`** : Assistant créatif et imaginatif  
- **`strict`** : Assistant strict et factuel

#### 💬 Prompts Utilisateur (style de réponse)
- **`default`** : Réponses claires et concises
- **`detaille`** : Réponses détaillées et complètes
- **`amusant`** : Réponses amusantes et légères

### Personnalisation des prompts

Modifiez `prompts.toml` pour ajouter vos propres prompts :

```toml
[system_prompts]
expert = "Vous êtes un expert technique avec une connaissance approfondie."
philosophe = "Vous êtes un philosophe réfléchi qui explore les idées profondes."
assistant_code = "Vous êtes un assistant spécialisé en programmation."

[user_prompts]
educatif = "Expliquez comme si vous enseigniez à un étudiant débutant."
professionnel = "Répondez dans un style professionnel et formel."
technique = "Donnez des réponses techniques détaillées avec des exemples."
```

### Paramètres du modèle

- **Température** (0.0-2.0) : Contrôle la créativité
  - 0.0 = Très prévisible
  - 1.0 = Équilibré
  - 2.0 = Très créatif

- **Top P** (0.0-1.0) : Contrôle la diversité du vocabulaire
- **Max Tokens** (10-1000) : Limite la longueur des réponses

## 🧪 Surveillance et Génération de Dialogues

### 📁 Système de Surveillance de Dossier

L'application surveille automatiquement le dossier `dialogues_text/` et détecte :
- ✅ **Nouveaux fichiers** de dialogue ajoutés
- ✅ **Modifications** dans les dialogues existants  
- ✅ **Rechargement automatique** de l'interface
- ✅ **Analyse en temps réel** des personnages présents

### 🎭 Processus de Génération Assistée

#### 1. **Préparation des Dialogues**
Placez vos fichiers `.txt` dans `dialogues_text/` avec le format :
```
Enseignant: Bonjour classe, aujourd'hui on parle de Python.
Élève: J'ai une question sur les fonctions.
Enseignant: Bien sûr, vas-y.
Élève: Comment définir une fonction ?
```

#### 2. **Analyse Contextuelle Automatique**
L'application analyse automatiquement :
- 👥 **Personnages présents** dans le dialogue
- 🎯 **Contexte récent** (5 dernières interactions par défaut)
- 🎨 **Ton et style** de chaque personnage
- 📊 **Patterns conversationnels**

#### 3. **Génération Intelligente**
- **Sélection du personnage** : Choisissez qui doit répondre
- **Comportement adaptatif** : L'IA s'adapte au style du personnage
- **Options multiples** : Générez 1 à 5 variantes de réponse
- **Contrôle fin** : Ajustez prompts et paramètres en temps réel

#### 4. **Workflow d'Assistance**
```
📂 Dossier surveillé → 🔍 Analyse → 👤 Sélection personnage → 🎨 Configuration → ⚡ Génération → ✅ Validation
```

### 🎯 Types de Comportements Disponibles

#### Prompts Système (Personnalité de l'IA)
- **`neutre`** : Assistant équilibré pour dialogues naturels
- **`creatif`** : Réponses imaginatives et originales
- **`strict`** : Réponses factuelles et cohérentes
- **`empathique`** : Réponses bienveillantes et émotionnelles

#### Prompts Utilisateur (Style de Réponse)
- **`default`** : Réponses claires et naturelles
- **`detaille`** : Développement approfondi des idées
- **`amusant`** : Ton léger et humoristique
- **`dramatique`** : Tension émotionnelle accrue

### 🔄 Surveillance en Temps Réel

Le système utilise **Watchdog** pour :
- 📱 **Détection instantanée** des changements de fichiers
- 🔄 **Rechargement automatique** de l'interface
- ⚡ **Performance optimisée** (pas de polling)
- 🌐 **Cross-platform** (Windows, macOS, Linux)

### 📊 Métriques et Analyse

L'application fournit :
- 📈 **Statistiques** sur les personnages les plus actifs
- 🎯 **Analyse de cohérence** des réponses générées
- 📝 **Historique** des générations par session
- 🔍 **Debug visuel** des prompts envoyés au LLM

### Modèles recommandés

```bash
# Modèles généralistes
ollama pull llama2:latest          # 7B - Bon équilibre
ollama pull mistral:latest         # 7B - Rapide et efficace
ollama pull llama2-uncensored      # 7B - Sans filtres

# Modèles spécialisés
ollama pull codellama:latest       # Code et programmation
ollama pull vicuna:latest          # Conversations naturelles

# Modèles plus puissants (nécessitent plus de RAM)
ollama pull llama2:13b            # 13B - Plus performant
ollama pull wizard-coder:latest   # Spécialisé code
```

## 🛠️ Technologies utilisées

| Technologie | Usage | Version |
|-------------|-------|---------|
| **Streamlit** | Interface web interactive | Latest |
| **Ollama** | Modèles de langage locaux | Latest |
| **Python** | Langage principal | 3.8+ |
| **TOML** | Configuration des prompts | Latest |
| **Watchdog** | Surveillance des fichiers | Latest |

## 🚨 Dépannage

### Erreurs courantes

#### 1. "Impossible de contacter Ollama"
```bash
# Vérifier qu'Ollama tourne
ollama serve

# Vérifier les modèles installés
ollama list
```

#### 2. "Port 8501 déjà utilisé"
```bash
# Utiliser un autre port
streamlit run app.py --server.port=8502
```

#### 3. "Module non trouvé"
```bash
# Vérifier l'environnement virtuel
pip list
pip install -r requirements.txt
```

### Performance

- **RAM recommandée** : 8GB+ pour les modèles 7B
- **RAM nécessaire** : 16GB+ pour les modèles 13B+
- **CPU** : Plus de cœurs = réponses plus rapides

## 📝 Développement

### Structure du code

- `app.py` : Interface utilisateur Streamlit
- `ollama_utils.py` : Logique métier et communication Ollama
- `prompts.toml` : Configuration centralisée

### Ajouter une fonctionnalité

1. **Fork** le repository
2. **Créer une branche** : `git checkout -b feature/ma-fonctionnalite`
3. **Développer** et tester
4. **Commit** : `git commit -m "✨ Ajout de ma fonctionnalité"`
5. **Push** : `git push origin feature/ma-fonctionnalite`
6. **Pull Request** sur GitHub

### Tests

```bash
# Lancer l'application en mode développement
streamlit run app.py --server.runOnSave=true --server.fileWatcherType=watchdog
```

## � Licence

MIT License - Voir le fichier LICENSE pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! 

### Comment contribuer :

1. 🍴 **Fork** le projet
2. 🌿 **Créer une branche** pour votre fonctionnalité
3. ✅ **Tester** vos modifications
4. 📝 **Documenter** les changements
5. 🚀 **Soumettre** une Pull Request

### Idées de contributions :

- 🎨 Améliorer l'interface utilisateur
- 🔧 Ajouter de nouveaux types de prompts
- 📊 Ajouter des métriques et analytics
- 🌐 Support multilingue
- 💾 Sauvegarde de l'historique des conversations
- 🔌 Intégration avec d'autres LLMs

## 🆘 Support

- 📧 **Issues** : Ouvrir une issue sur GitHub
- 💬 **Discussions** : Section Discussions du repository
- 📖 **Documentation** : Ce README et les commentaires du code

---

⭐ **N'oubliez pas de mettre une étoile si ce projet vous est utile !** ⭐