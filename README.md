Customer Churn Prediction

An end-to-end Machine Learning web application that predicts whether a customer is likely to churn based on customer profile, services, contract, and billing information.

The project demonstrates a complete Machine Learning workflow — from data preprocessing and model evaluation to probability-based prediction, risk classification, Flask application development, and cloud deployment.

---

🚀 Live Demo

Live Application:
https://customer-churn-prediction-1ivq.onrender.com/profile

The application is deployed on Render and provides an interactive web interface for customer churn prediction.

---

📌 Project Overview

Customer churn refers to customers discontinuing their services.

The goal of this project is to build a Machine Learning classification system that can identify customers who are more likely to churn, allowing businesses to take preventive retention actions and make data-driven decisions.

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

🎯 Problem Statement

Businesses often lose customers without being able to identify the warning signs early.

A customer churn prediction system can help identify customers who have a higher probability of leaving, allowing businesses to prioritize retention efforts and make data-driven decisions.

This project focuses on predicting whether a customer is likely to:

- Churn
- Not Churn

The application also provides a churn probability and risk classification to make the prediction easier to interpret.

---

🛠️ Tech Stack

Programming & Data Science

- Python
- Pandas
- NumPy
- Scikit-learn

Machine Learning

- Logistic Regression
- Decision Tree
- Random Forest
- Balanced Logistic Regression
- Classification
- Probability-based Prediction

Web Development

- Flask
- HTML
- CSS

Deployment

- Render

Development Tools

- Jupyter Notebook
- Git
- GitHub

---

✨ Features

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

🖥️ Application Screenshots

👤 Customer Profile

"Customer Profile" (https://raw.githubusercontent.com/chhabinath-gope/customer-churn-prediction/main/profile.png)

🛠️ Services & Support

"Services & Support" (https://raw.githubusercontent.com/chhabinath-gope/customer-churn-prediction/main/services.png)

💳 Contract & Billing

"Contract & Billing" (https://raw.githubusercontent.com/chhabinath-gope/customer-churn-prediction/main/billing.png)

🔮 Prediction Result

"Prediction Result" (https://raw.githubusercontent.com/chhabinath-gope/customer-churn-prediction/main/prediction-result.png)

---

🤖 Machine Learning Approach

Multiple classification models were evaluated to compare their performance.

Model| Accuracy| Precision| Recall| F1 Score| ROC-AUC
Logistic Regression| 80.7%| 66.0%| 56.1%| 60.7%| 84.2%
Decision Tree| 79.4%| 63.1%| 54.0%| 58.2%| 82.7%
Random Forest| 80.3%| 67.5%| 50.0%| 57.5%| 84.4%
Balanced Logistic Regression| 73.9%| 50.5%| 78.3%| 61.4%| 84.2%

---

🎯 Selected Model

Balanced Logistic Regression

The Balanced Logistic Regression model was selected because it provides substantially higher recall for churn customers.

For a churn prediction problem, recall is particularly important because missing a customer who is actually going to churn can result in a missed retention opportunity.

The selected model achieved:

- Accuracy: 73.9%
- Precision: 50.5%
- Recall: 78.3%
- F1 Score: 61.4%
- ROC-AUC: 84.2%

The higher recall allows the system to identify a larger proportion of potentially churning customers.

---

📊 Key Results

Metric| Score
Accuracy| 73.9%
Precision| 50.5%
Recall| 78.3%
F1 Score| 61.4%
ROC-AUC| 84.2%

Why Recall Matters

In customer retention, failing to identify a customer who is actually going to churn can mean losing an opportunity to intervene.

Therefore, the project prioritizes churn recall rather than selecting a model based only on overall accuracy.

---

🔄 Application Workflow

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

---

📂 Project Structure

customer-churn-prediction/
│
├── app.py
├── customer_chum_model.pkl
├── requirements.txt
├── runtime.txt
├── profile.png
├── services.png
├── billing.png
├── prediction-result.png
└── README.md

---

💻 Run Locally

1. Clone the repository

git clone https://github.com/chhabinath-gope/customer-churn-prediction.git

2. Open the project directory

cd customer-churn-prediction

3. Install dependencies

pip install -r requirements.txt

4. Run the Flask application

python app.py

5. Open the application

Visit:

http://127.0.0.1:5000/

---

🌐 Deployment

The application is deployed using Render and is publicly accessible through the live demo.

🔗 "Open Live Application" (https://customer-churn-prediction-1ivq.onrender.com/profile)

---

🔮 Future Improvements

Potential future improvements include:

- Hyperparameter tuning
- Advanced model experimentation
- Improved probability calibration
- Additional feature engineering
- Model explainability
- Performance monitoring
- More advanced retention recommendations

---

📚 Learning Outcomes

Through this project, I gained practical experience in:

- Data preprocessing
- Exploratory Data Analysis
- Handling class imbalance
- Machine Learning classification
- Model evaluation
- Recall-focused model selection
- Probability-based predictions
- Flask application development
- Git & GitHub
- Cloud deployment

---

👨‍💻 Author

Chhabinath Gope

BCA Student | Aspiring Data Scientist

- 💼 "LinkedIn" (https://www.linkedin.com/in/chhabinathgope/)
- 🌐 "Portfolio" (https://chhabinath-gope.github.io/my-portfolio/)
- 💻 "GitHub" (https://github.com/chhabinath-gope)

---

⭐ Project Links

Live Demo:
https://customer-churn-prediction-1ivq.onrender.com/profile

Source Code:
https://github.com/chhabinath-gope/customer-churn-prediction

---

«Built as a practical Machine Learning project to explore customer churn prediction and data-driven decision making.»
