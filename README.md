# Customer Churn Prediction

An end-to-end Machine Learning web application that predicts whether a customer is likely to churn based on customer profile, services, contract, and billing information.

The project demonstrates a complete Machine Learning workflow — from data preprocessing and model evaluation to probability-based prediction, Flask application development, and cloud deployment.

---

## 🚀 Live Demo

**Live Application:**  
https://customer-churn-prediction-1ivq.onrender.com/profile

The application is deployed on Render and provides an interactive web interface for customer churn prediction.

---

## 📌 Project Overview

Customer churn refers to customers discontinuing their services.

The goal of this project is to build a Machine Learning classification system that can identify customers who are more likely to churn, allowing businesses to take preventive retention actions.

This project combines:

- Data preprocessing
- Exploratory Data Analysis
- Feature preparation
- Class imbalance handling
- Machine Learning classification
- Model performance comparison
- Probability-based prediction
- Risk classification
- Flask web application
- Cloud deployment

---

## 🎯 Problem Statement

Businesses often lose customers without being able to identify the warning signs early.

A customer churn prediction system can help identify customers who have a higher probability of leaving, allowing businesses to prioritize retention efforts and make data-driven decisions.

This project focuses on predicting whether a customer is likely to:

- **Churn**
- **Not Churn**

The application also provides a churn probability and risk classification to make the prediction easier to interpret.

---

## ✨ Features

- 👤 Customer profile input
- 🛠️ Customer services and support information
- 💳 Contract and billing information
- 🔮 Churn prediction
- 📈 Churn probability
- ⚠️ Risk classification
- 💡 Retention recommendation
- 📊 Model performance comparison
- 📱 Responsive web interface
- ☁️ Live cloud deployment

---

## 🖥️ Application Screenshots

### 👤 Customer Profile

![Customer Profile](https://raw.githubusercontent.com/chhabinath-gope/customer-churn-prediction/main/profile.png)

### 🛠️ Services & Support

![Services & Support](https://raw.githubusercontent.com/chhabinath-gope/customer-churn-prediction/main/services.png)

### 💳 Contract & Billing

![Contract & Billing](https://raw.githubusercontent.com/chhabinath-gope/customer-churn-prediction/main/billing.png)

### 🔮 Prediction Result

![Prediction Result](https://raw.githubusercontent.com/chhabinath-gope/customer-churn-prediction/main/prediction-result.png)

---

## 🤖 Machine Learning

Multiple classification models were evaluated to compare their performance.

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 80.7% | 66.0% | 56.1% | 60.7% | 84.2% |
| Decision Tree | 79.4% | 63.1% | 54.0% | 58.2% | 82.7% |
| Random Forest | 80.3% | 67.5% | 50.0% | 57.5% | 84.4% |
| Balanced Logistic Regression | 73.9% | 50.5% | 78.3% | 61.4% | 84.2% |

---

## 🎯 Selected Model

### Balanced Logistic Regression

The **Balanced Logistic Regression** model was selected because it provides substantially higher recall for churn customers.

For a churn prediction problem, recall is particularly important because missing a customer who is actually going to churn can result in a missed retention opportunity.

The selected model achieved:

- **Accuracy:** 73.9%
- **Precision:** 50.5%
- **Recall:** 78.3%
- **F1 Score:** 61.4%
- **ROC-AUC:** 84.2%

The higher recall allows the system to identify a larger proportion of potentially churning customers.

---

## 📊 Key Results

The final model achieved:

| Metric | Score |
|---|---:|
| Accuracy | 73.9% |
| Precision | 50.5% |
| Recall | 78.3% |
| F1 Score | 61.4% |
| ROC-AUC | 84.2% |

### Why Recall Matters

In customer retention, failing to identify a customer who is actually going to churn can mean losing an opportunity to intervene.

Therefore, the project prioritizes **churn recall** rather than selecting a model based only on overall accuracy.

---

## 🔄 Application Workflow

```text
Customer Information
        ↓
Data Preprocessing
        ↓
Feature Preparation
        ↓
Machine Learning Model
        ↓
Churn Prediction
        ↓
Churn Probability
        ↓
Risk Classification
        ↓
Recommended Action
