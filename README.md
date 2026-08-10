Customer Churn Prediction

An end-to-end Machine Learning web application that predicts whether a customer is likely to churn based on customer profile, services, contract, and billing information.

🚀 Live Demo

Live Application:
https://customer-churn-prediction-1ivq.onrender.com/profile

The application is deployed on Render and provides an interactive web interface for customer churn prediction.

---

📌 Project Overview

Customer churn refers to customers discontinuing their services.

The goal of this project is to build a Machine Learning model that can identify customers who are more likely to churn, allowing businesses to take preventive retention actions.

This project combines:

- Data preprocessing
- Exploratory Data Analysis
- Machine Learning
- Class imbalance handling
- Probability-based prediction
- Flask web application
- Cloud deployment

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

### 👤 Customer Profile

![Customer Profile](https://raw.githubusercontent.com/chhabinath-gope/customer-churn-prediction/main/profile.png)

### 🛠️ Services & Support

![Services & Support](https://raw.githubusercontent.com/chhabinath-gope/customer-churn-prediction/main/services.png)

### 💳 Contract & Billing

![Contract & Billing](https://raw.githubusercontent.com/chhabinath-gope/customer-churn-prediction/main/billing.png)

### 🔮 Prediction Result

![Prediction Result](https://raw.githubusercontent.com/chhabinath-gope/customer-churn-prediction/main/prediction-result.png)

---

🤖 Machine Learning

Multiple classification models were evaluated:

Model| Accuracy| Precision| Recall| F1 Score| ROC-AUC
Logistic Regression| 80.7%| 66.0%| 56.1%| 60.7%| 84.2%
Decision Tree| 79.4%| 63.1%| 54.0%| 58.2%| 82.7%
Random Forest| 80.3%| 67.5%| 50.0%| 57.5%| 84.4%
Balanced Logistic Regression| 73.9%| 50.5%| 78.3%| 61.4%| 84.2%

🎯 Selected Model

Balanced Logistic Regression

The balanced model was selected because it provides significantly higher recall for churn customers.

A higher recall is useful for customer retention because the business can identify more potentially churning customers and take preventive action.

---

📊 Key Results

The Balanced Logistic Regression model achieved:

- Accuracy: 73.9%
- Precision: 50.5%
- Recall: 78.3%
- F1 Score: 61.4%
- ROC-AUC: 84.2%

The higher recall makes the model useful for identifying potential churn customers.

---

🔄 Application Workflow

Customer Information
        ↓
Data Preprocessing
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

🛠️ Technologies Used

Programming & Data Science

- Python
- Pandas
- NumPy
- Scikit-learn
- Joblib

Web Development

- Flask
- HTML
- CSS
- JavaScript

Deployment

- GitHub
- Render
- Gunicorn

---

📁 Project Structure

Customer-Churn-Prediction/
│
├── app.py
├── customer_churn_model.pkl
├── requirements.txt
├── runtime.txt
├── README.md
│
├── profile.png
├── services.png
├── billing.png
└── prediction-result.png

File Description

app.py
Contains the Flask web application and prediction logic.

customer_churn_model.pkl
Contains the trained Machine Learning model.

requirements.txt
Contains the Python dependencies required to run the application.

runtime.txt
Specifies the Python runtime used for deployment.

README.md
Contains project documentation and application screenshots.

PNG files
Contain screenshots of the deployed web application.

---

💼 Business Use Case

Customer churn prediction can help businesses:

- Identify customers at risk of leaving
- Prioritize retention campaigns
- Offer personalized incentives
- Improve customer satisfaction
- Reduce customer acquisition costs
- Make data-driven retention decisions

---

☁️ Deployment

The application is deployed using Render.

The deployment process includes:

1. Source code hosted on GitHub
2. Dependencies installed using "requirements.txt"
3. Flask application served using Gunicorn
4. Machine Learning model loaded by the application
5. Application deployed to a public Render URL

Live Demo:
https://customer-churn-prediction-1ivq.onrender.com/profile

---

💻 Run Locally

1. Clone the repository

git clone https://github.com/YOUR-USERNAME/Customer-Churn-Prediction.git

2. Open the project folder

cd Customer-Churn-Prediction

3. Install dependencies

pip install -r requirements.txt

4. Run the application

python app.py

5. Open in browser

http://127.0.0.1:5006/profile

---

🎯 Why This Project Matters

Customer churn is an important business problem because retaining existing customers is often more cost-effective than acquiring new ones.

This project demonstrates how Machine Learning can be used to:

- Analyze customer behavior
- Identify potential churners
- Estimate churn probability
- Classify customer risk
- Support data-driven retention strategies

---

🔮 Future Improvements

Possible future improvements include:

- SHAP-based model explainability
- Interactive analytics dashboard
- Customer segmentation
- Automated retention recommendations
- Model monitoring
- Database integration
- Authentication and user management
- Automated model retraining

---

👨‍💻 Project

Customer Churn Prediction — Machine Learning Portfolio Project

Built using Python, Machine Learning, Flask and Cloud Deployment.

Live Demo:
https://customer-churn-prediction-1ivq.onrender.com/profile
