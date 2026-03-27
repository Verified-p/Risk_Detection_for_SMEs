🔐 TrustLens AI

AI‑Powered Cybersecurity Risk Detection Platform for SMEs

📌 Overview

TrustLens AI is an intelligent security monitoring solution designed for Small and Medium Enterprises (SMEs). The platform captures, analyzes, and responds to suspicious user activities in real time by combining Machine Learning (Isolation Forest) with Heuristic Rule-Based Analysis.

By assigning dynamic risk scores (0–100%), TrustLens AI identifies compromised accounts, insider threats, and abnormal access patterns before they escalate into data breaches.

🏗️ Project Structure

To ensure the system runs correctly, organize your files as follows:


trustlens-ai/

├── main.py              # FastAPI Backend API

├── dashboard.py         # Streamlit Frontend UI

├── model_engine.py      # Logic for Isolation Forest & Risk Scoring

├── requirements.txt     # List of Python libraries

├── data/
│   └── security_logs.db # SQLite Database for event persistence

├── models/
│   └── iso_forest.joblib # Saved ML Model state

└── assets/
    └── logo.png         # Project branding
    
🛠️ Installation & Setup

1. Prerequisites

Ensure you have Python 3.9 or higher installed on your system.

2. Install Required Libraries

Run the following command to install all necessary dependencies:

Bash

pip install fastapi uvicorn streamlit pandas numpy scikit-learn joblib plotly requests
Libraries Included:

fastapi & uvicorn: For the high-speed backend API.

streamlit: For the interactive web dashboard.

scikit-learn: For the Isolation Forest ML model.

pandas & numpy: For data processing and numerical analysis.

plotly: For real-time risk charts and maps.

🚀 How to Run the Platform

To get the full system running, you need to start the Backend and the Frontend in two separate terminal windows.

Step 1: Start the AI Backend (FastAPI)
Bash

uvicorn main:app --reload

The API will be live at: http://127.0.0.1:8000

View API Documentation at: http://127.0.0.1:8000/docs


Step 2: Start the Admin Dashboard (Streamlit)

Bash

streamlit run dashboard.py

The Dashboard will open automatically in your browser at: http://localhost:8501

🧠 Core Methodology

1. AI Anomaly Detection

The system utilizes the Isolation Forest algorithm. It functions by isolating observations in a forest of decision trees. Anomalies are isolated significantly faster (shorter path length) than normal data points.

2. Hybrid Risk Scoring
TrustLens AI uses a weighted formula to combine AI results with hard security rules:

AI Score: Measures statistical deviation from the norm.

Rule Score: Flags specific violations (e.g., Logins at 3:00 AM, Unknown Devices, Foreign IPs).

Final Score: A normalized percentage categorizing threats as Low, Medium, or High.

🖥️ Platform Features
Live Attack Map: Visualizes the geographic origin of security threats.

Real-time Risk Ticker: A live feed of incoming login attempts and their AI-assigned risk.

Explainable AI (XAI): Provides a "Reasoning" field for every block action (e.g., "Flagged due to unusual geographic shift").

Historical Auditing: All events are saved to an SQLite database for forensic review.

👥 Research Team (Kisii University)

Andrew Otieno - IN13/00079/23 | Lazarus Gommit - IN13/00058/23

Osano David - IN13/00080/23 | George Omollo - IN13/00081/23

Basil Alphonse - IN13/00125/23 | Cyprian Joash - IN13/00167/23

Domain: Cybersecurity / Artificial Intelligence