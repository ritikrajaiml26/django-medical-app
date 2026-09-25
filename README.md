# 💊 MediCare - Smart Medicine Reminder & Health Tracker

An intelligent, fully animated medical reminder web application built with Python & Django. Helps users schedule prescriptions, track daily compliance streaks, and receive smart audio alarms so they never miss a dose.

---

## 📁 Project Architecture & Folder Structure

The repository is organized into clean, modular **Frontend** and **Backend** directories:

```text
Medicine Reminder App/
│
├── 📂 backend/                      # Django Full-Stack & REST API Server
│   ├── manage.py                    # Django CLI management script
│   ├── db.sqlite3                   # SQLite Database
│   ├── Procfile                     # Deployment process config
│   │
│   ├── 📂 myapp/                    # Core Medical Reminder Application
│   │   ├── admin.py                 # Django Admin configurations
│   │   ├── apps.py                  # App configuration
│   │   ├── models.py                # Database models (User, Reminder, Profile)
│   │   ├── views.py                 # Business logic, Auth, CRUD & REST APIs
│   │   ├── urls.py                  # App routes
│   │   │
│   │   ├── 📂 templates/            # Modern Animated UI Templates
│   │   │   ├── home.html            # Animated 3D Landing Page
│   │   │   ├── login.html           # Glassmorphism Login
│   │   │   ├── register.html        # Secure Account Registration
│   │   │   ├── dashboard.html       # Live Dashboard with Active Alarm Modal
│   │   │   ├── add_reminder.html    # Add / Edit Medicine Form
│   │   │   └── profile.html         # User Profile & Medical Notes
│   │   │
│   │   └── 📂 static/               # Static Assets
│   │       ├── 📂 css/
│   │       │   ├── app_modern.css   # Unified responsive theme (Dark & Light)
│   │       │   ├── home.css         # Hero 3D & Particle animations
│   │       │   └── profile.css      # Profile specific styles
│   │       └── 📂 sound/
│   │           └── m_tone.mp3       # Reminder alarm audio ringtone
│   │
│   ├── 📂 myproject/                # Project Settings & Root Routing
│   │   ├── settings.py              # App settings, static & media configurations
│   │   ├── urls.py                  # Root URL declarations
│   │   └── wsgi.py                  # WSGI entrypoint for production
│   │
│   └── 📂 media/                    # User profile photos and uploads
│
├── 📂 frontend/                     # Standalone Client Web App (HTML/CSS/JS)
│   ├── index.html                   # Login interface
│   ├── signup.html                  # Sign up interface
│   ├── dashboard.html               # Frontend dashboard
│   ├── auth.js                      # Client authentication logic
│   ├── reminder.js                  # Client medicine reminder logic
│   ├── style.css                    # Styling
│   └── iphone_16_messege_tone.mp3   # Notification audio
│
├── .gitignore                       # Git ignore rules (clean repository)
├── requirements.txt                 # Python dependencies
└── README.md                        # Documentation & setup guide
```

---

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.10+
* Git

### 2. Setup & Installation
```bash
# Clone the repository
git clone https://github.com/ritikrajaiml26/django-medical-app.git
cd django-medical-app

# Install dependencies
pip install -r requirements.txt
```

### 3. Running the Django Application (Backend & Full-Stack UI)
```bash
# Navigate to backend directory
cd backend

# Run database migrations (optional if db already present)
python manage.py migrate

# Start the development server
python manage.py runserver
```

Open your browser and visit:
* **Home Page:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **Dashboard:** [http://127.0.0.1:8000/dashboard/](http://127.0.0.1:8000/dashboard/)
* **Login:** [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)
* **Register:** [http://127.0.0.1:8000/register/](http://127.0.0.1:8000/register/)

---

## ✨ Key Features
- **Modern Animated UI:** Glassmorphism cards, ambient particle glow, and ECG heartbeat lines.
- **Dark & Light Mode:** Toggleable theme with local state persistence.
- **Smart Audio Alarm:** Automatic ringtone and pulsing modal alert when prescription time hits.
- **Snooze & Take Actions:** Snooze reminders for 5 minutes or mark them as taken with celebratory feedback.
- **Complete CRUD Operations:** Create, Read, Update, and Delete prescriptions with user data isolation.
- **Emergency Medical Notes:** Profile section for storing blood group, physician info, and allergy notes.

---

## 👨‍💻 Author
Made with ❤️ by **Ritik Raj**
