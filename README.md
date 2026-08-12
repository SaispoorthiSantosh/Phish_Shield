# 🛡️ PhishShield

## AI-Powered Phishing Email Detector

PhishShield is a web-based cybersecurity application that uses Machine Learning to analyze emails and detect potential phishing threats.

The application analyzes the email content and provides a **Risk Score, AI Confidence, Threat Level, Detection Reasons, and Security Recommendation**.

---

## 🚀 Features

- 🔍 Phishing email detection
- 🤖 Machine Learning based classification
- 📊 Risk Score calculation
- 🎯 AI Confidence percentage
- ⚠️ Threat Level detection
  - Low
  - Medium
  - High
- 🔗 URL/Link detection
- 🚨 Urgency detection
- 💰 Prize/Money-related content detection
- 📝 Detection reasons
- 🛡️ Security recommendations
- 🎨 User-friendly cybersecurity dashboard
- ⚡ Real-time email analysis

---

## 🧠 Machine Learning

PhishShield uses a **Multinomial Naive Bayes** machine learning algorithm.

The email text is converted into numerical features using **TF-IDF (Term Frequency-Inverse Document Frequency)**.

### Machine Learning Pipeline

Email Text  
↓  
Text Preprocessing  
↓  
TF-IDF Vectorization  
↓  
Naive Bayes Model  
↓  
Phishing Probability  
↓  
Risk Score & Threat Level

---

## 📊 Model Performance

The trained model achieved the following results on the test dataset:

| Metric | Score |
|---|---:|
| Accuracy | 91.49% |
| Precision | 99.83% |
| Recall | 79.25% |
| F1 Score | 88.36% |

These values were obtained during model evaluation using a test dataset.

---

## 🛠️ Technologies Used

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask

### Machine Learning
- Scikit-learn
- TF-IDF Vectorizer
- Multinomial Naive Bayes

### Libraries
- Pandas
- Joblib

---

## 📁 Project Structure

```text
PhishShield/
│
├── dataset/
│   └── Phishing_Email.csv
│
├── model/
│   ├── model.pkl
│   └── vectorizer.pkl
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   └── index.html
│
├── app.py
├── train_model.py
├── requirements.txt
└── README.md
