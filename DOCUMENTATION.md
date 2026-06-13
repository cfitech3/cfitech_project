# 📘 Documentation Technique CFI-TECH
## Centre de Formation et d'Innovation Technologique — Bamako, Mali

---

## 🏗️ ARCHITECTURE DU PROJET

```
cfitech_project/
├── cfitech/                    # Configuration Django principale
│   ├── settings.py             # Paramètres (dev + prod)
│   ├── urls.py                 # URLs centrales
│   └── wsgi.py
├── core/                       # App principale
│   ├── models.py               # SiteConfig, Partner, Blog, FAQ, Newsletter...
│   ├── views.py                # Accueil, À propos, Contact, Blog, FAQ...
│   ├── admin.py                # Dashboard admin complet
│   ├── urls.py                 # Routes core
│   ├── context_processors.py   # Config globale dans tous les templates
│   └── sitemaps.py             # SEO Sitemap
├── formations/                 # App formations
│   ├── models.py               # Domain, Trainer, Formation, Inscription
│   ├── views.py                # Liste, Détail, Inscription
│   ├── admin.py                # Admin formations + export CSV
│   └── urls.py
├── services/                   # App services
│   ├── models.py               # Service
│   ├── views.py
│   └── urls.py
├── templates/                  # Templates HTML
│   ├── base.html               # Layout principal
│   ├── home.html               # Page d'accueil
│   ├── about.html              # À propos
│   ├── contact.html            # Contact
│   ├── faq.html                # FAQ
│   ├── galerie.html            # Galerie
│   ├── temoignages.html        # Témoignages
│   ├── includes/
│   │   ├── navbar.html         # Navigation
│   │   └── footer.html         # Pied de page + newsletter
│   ├── formations/
│   │   ├── list.html           # Liste des formations
│   │   ├── detail.html         # Détail formation
│   │   ├── inscription.html    # Formulaire inscription
│   │   └── inscription_success.html
│   ├── services/
│   │   ├── list.html
│   │   └── noor_energy.html
│   ├── partenaires/
│   │   └── list.html
│   └── blog/
│       ├── list.html
│       └── detail.html
├── static/
│   ├── css/
│   │   ├── main.css            # Styles principaux
│   │   └── components.css      # Composants détails
│   ├── js/
│   │   └── main.js             # JavaScript principal
│   └── images/
│       └── placeholder/
├── google_apps_script/
│   └── inscriptions.gs         # Script Google Sheets
├── requirements.txt
├── .env.example
├── manage.py
└── DOCUMENTATION.md
```

---

## ⚡ INSTALLATION RAPIDE

### 1. Prérequis
```bash
Python 3.10+   # Requis
pip             # Gestionnaire packages
git             # Contrôle de version
```

### 2. Cloner et configurer
```bash
git clone https://github.com/cfitech/site.git
cd cfitech_project

# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate          # Linux/Mac
# venv\Scripts\activate           # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Variables d'environnement
Créer le fichier `.env` à la racine :
```env
SECRET_KEY=votre-cle-secrete-tres-longue-ici-CHANGEZ-MOI
DEBUG=True
ALLOWED_HOSTS=localhost 127.0.0.1

# Email Gmail
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=cfitech3@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-app-gmail

# Google Sheets (optionnel)
GOOGLE_SCRIPT_URL=https://script.google.com/macros/s/VOTRE_ID/exec

# Production (PostgreSQL)
# DATABASE_URL=postgresql://user:password@host:5432/cfitech_db
```

### 4. Initialiser la base de données
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
# → Créer un compte admin : admin / votre-mot-de-passe

# Charger les données initiales (optionnel)
python manage.py loaddata initial_data.json

# Collecter les fichiers statiques
python manage.py collectstatic

# Lancer le serveur de développement
python manage.py runserver
```

### 5. Accéder au site
- **Site public :** http://localhost:8000
- **Admin Django :** http://localhost:8000/cfitech-admin/

---

## 🔧 CONFIGURATION INITIALE (Admin Django)

### Étape 1 : Configuration du site
1. Aller dans Admin → **Configuration du site**
2. Remplir : logo, banderole, slogan, téléphone, WhatsApp, email, adresse
3. Renseigner les statistiques (étudiants, taux réussite...)
4. Ajouter les liens réseaux sociaux
5. Sauvegarder

### Étape 2 : Créer les domaines de formation
Admin → **Domaines de formation** → Ajouter :
```
Exemples :
- Maintenance informatique (icône: monitor, couleur: #1565C0)
- Programmation (icône: code, couleur: #6200EA)
- Développement web (icône: globe, couleur: #0097A7)
- Cybersécurité (icône: shield, couleur: #C62828)
- Intelligence artificielle (icône: cpu, couleur: #1B5E20)
- Énergie solaire (icône: sun, couleur: #FF6F00)
```

### Étape 3 : Ajouter des formateurs
Admin → **Formateurs** → Ajouter les formateurs avec photo, titre, biographie

### Étape 4 : Créer les formations
Admin → **Formations** → Nouvelle formation :
- Choisir le domaine
- Télécharger l'affiche (1024x1024 optimal)
- Définir le statut : `open` pour ouvrir les inscriptions
- Définir le nombre de places, la date de début, le prix

### Étape 5 : Partenaires
Admin → **Partenaires** → Ajouter Noor Energy en cochant "Noor Energy"

---

## 📊 GOOGLE SHEETS — CONFIGURATION

### 1. Créer le Google Sheet
1. Ouvrir Google Drive → Nouveau → Feuille de calcul
2. Nommer : "Inscriptions CFI-TECH"
3. Copier l'ID depuis l'URL :
   `https://docs.google.com/spreadsheets/d/`**`1ABC...XYZ`**`/edit`

### 2. Déployer le script
1. Dans Google Sheets → Extensions → Apps Script
2. Coller le contenu de `google_apps_script/inscriptions.gs`
3. Remplacer `VOTRE_SPREADSHEET_ID_ICI` par l'ID copié
4. Cliquer **Déployer** → Nouvelle déploiement
   - Type : Application Web
   - Exécuter en tant que : **Moi**
   - Accès : **Tout le monde**
5. Autoriser les permissions
6. Copier l'URL de déploiement

### 3. Configurer Django
Dans `.env` :
```
GOOGLE_SCRIPT_URL=https://script.google.com/macros/s/VOTRE_ID_DEPLOIEMENT/exec
```

Chaque inscription sera automatiquement :
- ✅ Enregistrée dans la feuille Google Sheets
- ✅ Notifiée par email à cfitech3@gmail.com
- ✅ Marquée comme synchronisée dans l'admin Django

---

## 🚀 DÉPLOIEMENT EN PRODUCTION

### Option A : VPS Linux (Ubuntu 22.04) — RECOMMANDÉ

```bash
# 1. Mettre à jour le serveur
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib -y

# 2. Créer la base de données PostgreSQL
sudo -u postgres psql
CREATE DATABASE cfitech_db;
CREATE USER cfitech_user WITH PASSWORD 'mot-de-passe-fort';
GRANT ALL PRIVILEGES ON DATABASE cfitech_db TO cfitech_user;
\q

# 3. Configurer Django pour la production
# Dans .env :
DEBUG=False
ALLOWED_HOSTS=votre-domaine.ml www.votre-domaine.ml
DATABASE_URL=postgresql://cfitech_user:mdp@localhost:5432/cfitech_db
SECRET_KEY=cle-secrete-production-tres-longue

# 4. Gunicorn (serveur WSGI)
pip install gunicorn
gunicorn cfitech.wsgi:application --bind 0.0.0.0:8000 --workers 3

# 5. Service systemd
sudo nano /etc/systemd/system/cfitech.service
```

Contenu du service systemd :
```ini
[Unit]
Description=CFI-TECH Django Application
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/cfitech_project
Environment="PATH=/home/ubuntu/cfitech_project/venv/bin"
ExecStart=/home/ubuntu/cfitech_project/venv/bin/gunicorn cfitech.wsgi:application --bind unix:/run/cfitech.sock --workers 3

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable cfitech
sudo systemctl start cfitech
```

Configuration Nginx :
```nginx
server {
    listen 80;
    server_name cfitech.ml www.cfitech.ml;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root /home/ubuntu/cfitech_project;
    }

    location /media/ {
        root /home/ubuntu/cfitech_project;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/cfitech.sock;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/cfitech /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
# HTTPS avec Let's Encrypt
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d cfitech.ml -d www.cfitech.ml
```

### Option B : Railway (Cloud gratuit pour commencer)

```bash
# Installer Railway CLI
npm install -g @railway/cli
railway login
railway init
railway add postgresql
railway up
```

Ajouter les variables d'environnement dans le dashboard Railway.

### Option C : Render.com

1. Connecter GitHub
2. Créer un Web Service → Python
3. Build Command : `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate`
4. Start Command : `gunicorn cfitech.wsgi:application`
5. Ajouter PostgreSQL depuis le dashboard

---

## 🔍 SEO — OPTIMISATIONS APPLIQUÉES

| Élément | Implémenté | Détails |
|---------|-----------|---------|
| Meta title | ✅ | Par page, incluant "CFI-TECH Mali" |
| Meta description | ✅ | 160 chars max, unique par page |
| Open Graph | ✅ | Facebook, LinkedIn sharing |
| Twitter Card | ✅ | summary_large_image |
| Structured Data | ✅ | EducationalOrganization JSON-LD |
| Sitemap XML | ✅ | Auto-généré via django.contrib.sitemaps |
| Robots.txt | ✅ | Route dédiée |
| URLs canoniques | ✅ | Chaque page |
| Slugs SEO-friendly | ✅ | Formations, blog articles |
| Images alt | ✅ | Toutes les images |
| Lazy loading | ✅ | Images non critiques |
| HTTPS redirect | ✅ | Production |

**Mots-clés cibles :**
- "formation informatique Bamako"
- "CFI-TECH Mali"
- "centre formation technologique Mali"
- "programmation Bamako"
- "cybersécurité Afrique de l'Ouest"
- "énergie solaire Mali formation"

---

## 🛡️ SÉCURITÉ — MESURES APPLIQUÉES

| Mesure | Status |
|--------|--------|
| CSRF Protection | ✅ Django intégré |
| XSS Protection | ✅ Auto-escaping Django + headers |
| SQL Injection | ✅ ORM Django (zero raw SQL) |
| Anti-spam formulaire | ✅ Honeypot field + validation |
| Validation frontend | ✅ HTML5 + JavaScript |
| Validation backend | ✅ Django views |
| HTTPS (prod) | ✅ Let's Encrypt |
| Secret key env | ✅ Variables d'environnement |
| Debug=False prod | ✅ Contrôlé via .env |
| HSTS | ✅ Production |
| Clickjacking | ✅ X-Frame-Options DENY |

---

## 📱 FONCTIONNALITÉS

### ✅ Implémentées
- Page d'accueil avec hero, statistiques, formations, témoignages, partenaires, blog
- Gestion des formations (16 domaines, niveaux, modes, places, dates)
- Formulaire d'inscription avec validation + synchronisation Google Sheets
- Dashboard admin complet (Django Admin personnalisé)
- Export CSV des inscriptions
- Blog/Actualités avec pagination
- FAQ avec accordéon par catégorie
- Galerie avec lightbox
- Témoignages avec slider Swiper
- Section Noor Energy
- Gestion des partenaires (évolutive)
- Newsletter AJAX
- WhatsApp flottant
- Bouton partage réseaux sociaux (WhatsApp, Facebook, LinkedIn)
- SEO complet (méta, sitemap, robots.txt, JSON-LD)
- Compte à rebours inscriptions
- Barre de progression places disponibles
- Bouton retour en haut
- Barre de progression lecture

### 🔮 Évolutions futures recommandées

#### Court terme (1-3 mois)
- [ ] **Paiement en ligne** : Orange Money, Moov Money via Cinetpay
- [ ] **Téléchargement attestations** PDF auto-générés
- [ ] **Système de messagerie** interne (admin → étudiant)
- [ ] **Galerie vidéo** YouTube intégrée

#### Moyen terme (3-6 mois)
- [ ] **Espace étudiant** : Connexion, suivi des formations
- [ ] **E-learning** : Cours vidéo, quiz, exercices en ligne
- [ ] **Application mobile** : API REST Django + Flutter
- [ ] **Multilingue** : Anglais + Bambara (django-modeltranslation)

#### Long terme (6-12 mois)
- [ ] **Certification numérique** : QR code + vérification en ligne
- [ ] **Plateforme partenaires** : Espace dédié B2B
- [ ] **Système de recommandation** formations
- [ ] **Live streaming** cours en direct

---

## 📞 SUPPORT TECHNIQUE

Pour toute question technique :
- **Email** : cfitech3@gmail.com
- **WhatsApp** : +223 78 78 73 39
- **Adresse** : Moussabougou, Bamako, Mali

---

*Documentation générée le 2025 — CFI-TECH © Tous droits réservés*
