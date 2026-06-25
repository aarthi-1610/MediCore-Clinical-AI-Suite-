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

📸 Screenshots

<img width="1372" height="725" alt="Screenshot 2026-02-27 190835" src="https://github.com/user-attachments/assets/6fe67f0c-4785-40ac-8285-feaecd5be2be" />
<img width="1377" height="726" alt="Screenshot 2026-02-27 190915" src="https://github.com/user-attachments/assets/c3af281b-5b79-432c-9455-dd1fcaad7b15" />
<img width="1379" height="728" alt="Screenshot 2026-02-27 190947" src="https://github.com/user-attachments/assets/938590bb-589b-45ce-b803-794521d1cb51" />
<img width="1920" height="1020" alt="Screenshot 2026-03-04 132252" src="https://github.com/user-attachments/assets/c81c58ac-1168-462e-b66a-a0eb8d4125f1" />
<img width="1920" height="1020" alt="Screenshot 2026-03-04 135224" src="https://github.com/user-attachments/assets/ca1bfd29-380e-4ae3-a57c-82cf3318ad69" />
<img width="1920" height="1020" alt="Screenshot 2026-03-04 135503" src="https://github.com/user-attachments/assets/944f9999-ec46-4dd0-9de4-1af4af919bd0" />
<img width="1920" height="1020" alt="Screenshot 2026-03-11 153513" src="https://github.com/user-attachments/assets/206b99f6-a63a-4e01-bc8a-27d10dc34b84" />
<img width="1000" height="793" alt="Screenshot 2026-03-11 153605" src="https://github.com/user-attachments/assets/fdaf8028-e1ad-4c8f-83aa-f288554de7c8" />
<img width="1920" height="1020" alt="Screenshot 2026-03-11 153938" src="https://github.com/user-attachments/assets/a5b1e26a-ff02-4f39-bc27-193bce4dcfdc" />
<img width="874" height="915" alt="Screenshot 2026-03-11 154155" src="https://github.com/user-attachments/assets/f3bba129-1f9f-44a0-b091-7eebe77ae7cc" />
<img width="1920" height="1020" alt="Screenshot 2026-03-11 154654" src="https://github.com/user-attachments/assets/e99b6dba-4185-4f49-8ac7-814287ff633c" />
<img width="1920" height="1020" alt="Screenshot 2026-03-11 155144" src="https://github.com/user-attachments/assets/8784332a-c3b0-4d14-94c9-779743ab5382" />
<img width="1920" height="1020" alt="Screenshot 2026-03-11 155225" src="https://github.com/user-attachments/assets/7481afac-eb3a-42cd-a2bc-565b6f87394b" />
<img width="1904" height="861" alt="Screenshot 2026-03-11 155548" src="https://github.com/user-attachments/assets/312d2b6c-a4c7-46e0-8a18-5fe90c5e5058" />
<img width="1920" height="1020" alt="Screenshot 2026-03-11 155736" src="https://github.com/user-attachments/assets/e3731573-744b-445b-983b-f87fc2dda40f" />
<img width="1920" height="1020" alt="Screenshot 2026-03-11 160145" src="https://github.com/user-attachments/assets/5748167d-d306-4201-8b1c-a34c68541d5b" />
<img width="1920" height="1020" alt="Screenshot 2026-03-11 160433" src="https://github.com/user-attachments/assets/d556cb67-bb36-4545-9a3f-756df6525a74" />

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
