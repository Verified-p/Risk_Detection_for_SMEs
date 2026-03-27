# 🔐 TrustLens AI

## AI‑Powered Cybersecurity Risk Detection Platform for SMEs

---

## 📌 Overview

**TrustLens AI** is an AI‑powered cybersecurity risk detection platform designed to help **Small and Medium Enterprises (SMEs)** monitor, analyze, and respond to suspicious user activities in real time. The system combines **machine learning**, **rule‑based analysis**, and **behavioral patterns** to assign dynamic risk scores to security events such as logins, access attempts, and privilege usage.

The platform provides decision‑makers with **actionable insights**, enabling early detection of threats such as compromised accounts, insider misuse, and abnormal access behavior.

---

## 🎯 Problem Statement

Many SMEs lack the financial and technical capacity to deploy full‑scale Security Operations Centers (SOCs). As a result:

* Suspicious login behavior goes unnoticed
* Insider threats are detected too late
* Security logs are rarely analyzed in real time
* Incident response is mostly reactive

TrustLens AI addresses this gap by offering an **intelligent, lightweight, and explainable security monitoring system** tailored for SMEs.

---

## 🚀 Objectives

* Detect abnormal user behavior using AI
* Assign clear and interpretable risk scores
* Explain *why* an event is risky (explainable AI)
* Support early decision‑making and incident response
* Provide real‑time visibility into security posture

---

## 🧠 How TrustLens AI Works

### 1. Event Ingestion

The system processes security events containing attributes such as:

* Login time
* Device recognition status
* Location recognition status
* Access frequency
* User role or privilege level

These events represent interactions by authenticated users within an organization’s systems.

---

### 2. AI‑Based Anomaly Detection

TrustLens AI uses an **Isolation Forest** machine learning model to detect unusual behavior patterns by:

* Learning what *normal* activity looks like
* Identifying deviations from established behavior
* Assigning anomaly scores to events

This enables the system to flag activities that statistically differ from typical usage.

---

### 3. Rule‑Based Risk Evaluation

In addition to AI detection, the system applies security rules such as:

* Login outside normal working hours
* Access from unknown devices
* Access from unfamiliar locations
* Excessive access attempts
* High‑privilege role used in risky contexts

Each triggered rule contributes to the overall risk score.

---

### 4. Risk Scoring Engine

The AI score and rule‑based score are combined into a **single normalized risk percentage (0–100%)**, which is classified into:

* **Low Risk**: Normal activity
* **Medium Risk**: Suspicious behavior requiring monitoring
* **High Risk**: Critical threat requiring immediate action

---

### 5. Explainable Decisions

For every analyzed event, TrustLens AI provides:

* The computed risk level
* Clear reasons explaining the risk
* Recommended response actions

This ensures transparency and trust in AI‑driven decisions.

---

## 🖥️ Platform Features

* 📊 Real‑time risk dashboard
* 🔎 Detailed high‑risk event analysis
* 📈 Risk trend visualization
* 🧠 AI + rule‑based hybrid detection
* 📄 Log file analysis support (CSV / JSON)
* ⚡ Live monitoring simulation

---

## 🏗️ System Architecture

* **Frontend**: Streamlit dashboard
* **Backend**: Python application logic
* **Machine Learning**: Scikit‑learn (Isolation Forest)
* **Data Handling**: Pandas, NumPy
* **Model Persistence**: Joblib

---

## 🔐 Security Scope

TrustLens AI is designed to monitor **authorized users within an organization**, such as:

* Employees
* Managers
* Administrators

The system focuses on detecting **misuse, compromise, or abnormal behavior** within considered access boundaries.

---

## 📚 Use Cases

* Detect compromised employee accounts
* Identify suspicious admin activity
* Monitor abnormal login behavior
* Strengthen internal security controls
* Support compliance and audit readiness

---

## 🧪 Extensibility

The platform can be extended to include:

* Integration with real authentication logs
* IP reputation analysis
* User behavior profiling over time
* Alert notifications (email, SIEM tools)
* Role‑based access visualization

---

## 🎓 Academic Value

TrustLens AI demonstrates practical application of:

* Artificial Intelligence in cybersecurity
* Anomaly detection algorithms
* Explainable AI principles
* Secure system design
* Real‑time data analysis

It serves as a strong foundation for academic research, demonstrations, and further innovation.

---

## 🏁 Conclusion

TrustLens AI provides a modern, intelligent, and scalable approach to cybersecurity monitoring for SMEs. By combining AI‑driven anomaly detection with clear rule‑based logic, the system delivers **transparent, actionable, and real‑time security insights**, helping organizations move from reactive to proactive defense strategies.

---

**Project Name:** TrustLens AI
**Domain:** Cybersecurity / Artificial Intelligence
**Focus:** Risk Detection & Behavioral Analysis
