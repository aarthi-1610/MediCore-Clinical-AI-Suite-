<div align="center">

# 🏥 MediCore — Clinical AI Suite

[![Streamlit](https://img.shields.io/badge/Live%20Demo-Streamlit%20Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://medicore-app.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Deployed-brightgreen?style=for-the-badge)]()

> **A production-ready, 3-role Clinical AI Suite** powered by Random Forest ML, LLaMA 3.3 70B chatbot, bilingual NLP (English & Tamil), automated PDF reports, and Power BI dashboards — deployed live on Streamlit Cloud.

</div>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Live Demo](#-live-demo)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [System Architecture](#-system-architecture)
- [Role-Based Modules](#-role-based-modules)
- [ML Model — Health Risk Prediction](#-ml-model--health-risk-prediction)
- [MediBot — Bilingual AI Chatbot](#-medibot--bilingual-ai-chatbot)
- [Screenshots](#-screenshots)
- [Project Structure](#-project-structure)
- [Setup & Run Locally](#-setup--run-locally)
- [Developer](#-developer)

---

## 🔍 Overview

**MediCore** is a full-featured Clinical AI Suite built with Python and Streamlit, designed to streamline patient management, health risk prediction, and medical consultations in one unified platform.

It supports **3 distinct user roles** — Admin, Doctor, and Patient — each with tailored dashboards and capabilities. The system integrates a **Random Forest ML model** for health risk prediction (88% accuracy), a **bilingual AI chatbot (MediBot)** powered by LLaMA 3.3 70B via Groq API, automated **PDF medical reports** via ReportLab, and **Power BI dashboards** for analytics.

---

## 🌐 Live Demo

| 🔗 Link | Description |
|---|---|
| [medicore-app.streamlit.app](https://medicore-app.streamlit.app) | Live deployed application on Streamlit Cloud |
| [GitHub Repository](https://github.com/aarthi-1610/MediCore-Clinical-AI-Suite-) | Source code |

---

## ✨ Key Features

- 🔐 **Role-Based Access Control** — Separate secure login for Admin, Doctor, and Patient
- 🤖 **MediBot AI Chatbot** — LLaMA 3.3 70B (Groq API) with bilingual English & Tamil support
- 🎙️ **Voice Input** — Bilingual voice recognition for Tamil and English queries
- 🌿 **Health Risk Prediction** — Random Forest ML model with **88% accuracy**
- 📅 **Appointment Booking** — Patient self-scheduling with doctor availability management
- 💳 **Automated Billing** — Auto-generated invoices with payment status tracking
- 📄 **PDF Report Generation** — Medical summaries auto-generated via ReportLab
- 📊 **Power BI Dashboards** — Real-time analytics on patient data and health trends
- 🗄️ **SQLite Backend** — Lightweight, fully structured relational database
- ☁️ **Deployed on Streamlit Cloud** — Publicly accessible with zero-setup demo

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend / UI** | Streamlit, HTML, CSS |
| **Backend** | Python 3.10+ |
| **Machine Learning** | Scikit-learn, Random Forest, Logistic Regression |
| **AI / LLM** | LLaMA 3.3 70B via Groq REST API |
| **NLP** | Bilingual NLP — English & Tamil |
| **Voice Input** | SpeechRecognition |
| **Database** | SQLite |
| **PDF Generation** | ReportLab |
| **Data Visualization** | Power BI, Matplotlib |
| **Deployment** | Streamlit Cloud |
| **Version Control** | Git, GitHub |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        MediCore Frontend                        │
│                    (Streamlit UI — Python)                      │
└────────────────────┬───────────────────────┬────────────────────┘
                     │                       │
          ┌──────────▼──────────┐   ┌────────▼────────┐
          │   Auth & Role Gate  │   │   MediBot Chat  │
          │  (Admin/Dr/Patient) │   │  (Groq LLaMA)   │
          └──────────┬──────────┘   └────────┬────────┘
                     │                       │
     ┌───────────────┼───────────────────────┤
     │               │                       │
┌────▼─────┐  ┌──────▼──────┐  ┌────────────▼────────────┐
│  ML Risk │  │ Appointment │  │ Billing & PDF Generator │
│Prediction│  │  Scheduler  │  │     (ReportLab)         │
│(Random   │  │             │  │                         │
│ Forest)  │  │             │  │                         │
└────┬─────┘  └──────┬──────┘  └────────────┬────────────┘
     │               │                       │
     └───────────────▼───────────────────────┘
                      │
              ┌───────▼────────┐
              │  SQLite DB     │
              │  (users,       │
              │  patients,     │
              │  appointments, │
              │  billing)      │
              └────────────────┘
```

---

## 👥 Role-Based Modules

### 🔴 Admin Panel
| Feature | Description |
|---|---|
| Dashboard | System-wide stats — total patients, doctors, appointments |
| Doctor Management | Add, update, remove doctor profiles |
| Patient Records | Full CRUD on patient data |
| Billing Overview | Monitor all invoices and payment statuses |
| Power BI Analytics | Embedded dashboards for health trend analysis |

### 🟢 Doctor Dashboard
| Feature | Description |
|---|---|
| Appointment View | See scheduled patients for the day |
| Patient Records | Access medical history and reports |
| Health Risk Report | View ML-generated risk scores per patient |
| PDF Reports | Generate and download patient medical summaries |

### 🔵 Patient Portal
| Feature | Description |
|---|---|
| Book Appointment | Self-schedule with available doctors |
| MediBot | 24/7 bilingual AI health assistant |
| Health Risk Check | Input vitals → get instant ML risk prediction |
| View Bills | Access invoices and payment records |
| Download Reports | PDF medical summaries |

---

## 🤖 ML Model — Health Risk Prediction

| Attribute | Detail |
|---|---|
| **Algorithm** | Random Forest Classifier |
| **Accuracy** | **88%** on test data |
| **Library** | Scikit-learn |
| **Input Features** | Age, BMI, Blood Pressure, Glucose, Cholesterol, etc. |
| **Output** | Risk Level (Low / Medium / High) + Probability Score |
| **Preprocessing** | Feature scaling, missing value handling, train-test split |

```python
# Model pipeline (simplified)
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', RandomForestClassifier(n_estimators=100, random_state=42))
])
pipeline.fit(X_train, y_train)
# Accuracy: 88%
```

---

## 💬 MediBot — Bilingual AI Chatbot

MediBot is the AI health assistant embedded inside MediCore, powered by **LLaMA 3.3 70B** accessed via the **Groq REST API**.

| Feature | Detail |
|---|---|
| **LLM** | LLaMA 3.3 70B |
| **API** | Groq REST API |
| **Languages** | English + Tamil (Bilingual) |
| **Voice Input** | Yes — speech-to-text in both languages |
| **Domain** | Medical Q&A, symptom guidance, appointment help |
| **Context-Aware** | Maintains conversation history within session |

```python
# MediBot API call (simplified)
import requests

response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
    json={
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are MediBot, a bilingual (English & Tamil) medical AI assistant."},
            {"role": "user", "content": user_query}
        ]
    }
)
```

---
## 📁 Project Structure

```
MediCore-Clinical-AI-Suite/
│
├── app.py                     # Main Streamlit entry point
├── requirements.txt           # Python dependencies
├──healthcare_dataset.csv
├── risk_model.pkl
```
<img width="670" height="617" alt="Screenshot 2026-03-11 195301" src="https://github.com/user-attachments/assets/1dec17df-3011-48d4-9852-96cf3da98897" />

---

## ⚙️ Setup & Run Locally

### Prerequisites
- Python 3.10+
- Groq API Key → [console.groq.com](https://console.groq.com)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/aarthi-1610/MediCore-Clinical-AI-Suite-.git
cd MediCore-Clinical-AI-Suite-

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your Groq API key
# Create a .env file or set in Streamlit secrets
echo "GROQ_API_KEY=your_api_key_here" > .env

# 4. Initialize the database
python database/db_setup.py

# 5. Run the app
streamlit run app.py
```

### Requirements
```
streamlit
scikit-learn
pandas
numpy
requests
reportlab
speechrecognition
matplotlib
python-dotenv
```

---
