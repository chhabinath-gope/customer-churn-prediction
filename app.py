from flask import Flask, request, render_template_string, session, redirect, url_for
import pandas as pd
import numpy as np
import os
import glob
import joblib
import pickle
import threading
import webbrowser
import time

app = Flask(__name__)

app.secret_key = "customer_churn_prediction_final_2026"
app.config["SESSION_PERMANENT"] = False


# ============================================================
# AUTOMATICALLY FIND YOUR EXISTING MODEL
# ============================================================

def find_model():

    possible_files = []

    possible_files.extend(
        glob.glob("*.pkl")
    )

    possible_files.extend(
        glob.glob("*.joblib")
    )

    if not possible_files:
        raise FileNotFoundError(
            "No .pkl or .joblib model file found in the project folder."
        )

    # Prefer churn/customer related model names
    preferred = [
        f for f in possible_files
        if any(word in f.lower()
               for word in ["churn", "customer", "model"])
    ]

    if preferred:
        return preferred[0]

    return possible_files[0]


MODEL_FILE = find_model()


# ============================================================
# LOAD MODEL
# ============================================================

try:
    model = joblib.load(MODEL_FILE)
except Exception:
    with open(MODEL_FILE, "rb") as f:
        model = pickle.load(f)


print("Model loaded:", MODEL_FILE)


# ============================================================
# COMMON HTML / CSS
# ============================================================

COMMON = r"""
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: Arial, Helvetica, sans-serif;
}

body {

    min-height: 100vh;

    background:
        radial-gradient(circle at 5% 5%, #6366f155, transparent 28%),
        radial-gradient(circle at 95% 90%, #a855f755, transparent 28%),
        linear-gradient(135deg, #0f172a, #172554);

    color: #172033;

    padding: 12px;
}

.page {
    animation: pageIn .5s ease;
}

@keyframes pageIn {

    from {
        opacity: 0;
        transform: translateY(12px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }

}

.wrapper {

    max-width: 1120px;

    margin: auto;
}

.header {

    text-align: center;

    color: white;

    margin-bottom: 9px;
}

.badge {

    display: inline-block;

    padding: 6px 15px;

    border-radius: 30px;

    background:
        linear-gradient(135deg, #6366f1, #a855f7);

    font-size: 10px;

    font-weight: bold;

    letter-spacing: .5px;

    box-shadow: 0 7px 22px #6366f155;

    margin-bottom: 5px;
}

.header h1 {

    font-size: 29px;

    margin-bottom: 3px;
}

.header p {

    color: #cbd5e1;

    font-size: 12px;
}


/* =========================
   PROGRESS
========================= */

.progress {

    display: flex;

    justify-content: center;

    align-items: center;

    margin: 7px 0 10px;
}

.circle {

    width: 30px;

    height: 30px;

    border-radius: 50%;

    display: flex;

    align-items: center;

    justify-content: center;

    background: #334155;

    color: #94a3b8;

    font-size: 11px;

    font-weight: bold;

    transition: .3s;
}

.circle.active {

    background:
        linear-gradient(135deg, #4f46e5, #a855f7);

    color: white;

    box-shadow: 0 0 17px #6366f180;

    transform: scale(1.08);
}

.line {

    width: 55px;

    height: 3px;

    background: #334155;
}

.line.active {

    background:
        linear-gradient(90deg, #6366f1, #a855f7);
}


/* =========================
   CARD
========================= */

.card {

    background: rgba(255,255,255,.98);

    border-radius: 21px;

    padding: 20px;

    box-shadow:
        0 20px 55px rgba(0,0,0,.30);
}

.step-title {

    display: flex;

    align-items: center;

    gap: 10px;

    margin-bottom: 15px;
}

.step-number {

    width: 35px;

    height: 35px;

    border-radius: 11px;

    background:
        linear-gradient(135deg,#4f46e5,#9333ea);

    color: white;

    display: flex;

    align-items: center;

    justify-content: center;

    font-weight: bold;
}

.step-title h2 {

    font-size: 19px;

    color: #1e293b;
}


/* =========================
   FORM
========================= */

.form-grid {

    display: grid;

    grid-template-columns: repeat(2, 1fr);

    gap: 12px 18px;
}

.field label {

    display: block;

    font-size: 10px;

    font-weight: bold;

    color: #475569;

    margin-bottom: 5px;
}

input,
select {

    width: 100%;

    padding: 9px 10px;

    border-radius: 10px;

    border: 2px solid #e2e8f0;

    background: #f8fafc;

    outline: none;

    font-size: 12px;

    transition: .25s;
}

select {

    cursor: pointer;
}

input:hover,
select:hover {

    border-color: #a5b4fc;
}

input:focus,
select:focus {

    border-color: #6366f1;

    background: white;

    box-shadow:
        0 0 0 4px #6366f118;
}


/* =========================
   BUTTONS
========================= */

.navigation {

    display: flex;

    justify-content: space-between;

    gap: 9px;

    margin-top: 17px;
}

.btn {

    display: inline-flex;

    align-items: center;

    justify-content: center;

    padding: 9px 17px;

    border: none;

    border-radius: 10px;

    font-size: 12px;

    font-weight: bold;

    text-decoration: none;

    cursor: pointer;

    transition: .25s;
}

.btn:hover {

    transform: translateY(-2px);
}

.next,
.predict {

    margin-left: auto;

    color: white;

    background:
        linear-gradient(135deg,#4f46e5,#9333ea);

    box-shadow: 0 7px 18px #6366f140;
}

.previous {

    color: #334155;

    background: #e2e8f0;
}

.new {

    color: white;

    background:
        linear-gradient(135deg,#0891b2,#2563eb);
}

.performance {

    color: white;

    background:
        linear-gradient(135deg,#7c3aed,#db2777);
}


/* =========================
   LOADING
========================= */

.loading {

    display: none;
}

.loading-active .normal-text {

    display: none;
}

.loading-active .loading {

    display: inline-flex;

    align-items: center;

    gap: 7px;
}

.spinner {

    width: 14px;

    height: 14px;

    border: 2px solid rgba(255,255,255,.4);

    border-top-color: white;

    border-radius: 50%;

    animation: spin .7s linear infinite;
}

@keyframes spin {

    to {
        transform: rotate(360deg);
    }
}


/* =========================
   RESULT
========================= */

.result-card {

    max-width: 950px;

    margin: auto;
}

.result-top {

    display: grid;

    grid-template-columns: .9fr 1.4fr;

    gap: 14px;
}

.result-left,
.result-right {

    background: #f8fafc;

    border-radius: 17px;

    padding: 16px;
}

.result-left {

    text-align: center;

    display: flex;

    flex-direction: column;

    justify-content: center;
}

.result-icon {

    width: 52px;

    height: 52px;

    border-radius: 50%;

    margin: 0 auto 7px;

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 24px;

    background:
        linear-gradient(135deg,#ede9fe,#ddd6fe);

    animation: pop .6s ease;
}

@keyframes pop {

    0% {
        transform: scale(.5);
        opacity: 0;
    }

    70% {
        transform: scale(1.1);
    }

    100% {
        transform: scale(1);
        opacity: 1;
    }
}

.result-left h2 {

    font-size: 16px;

    margin-bottom: 3px;
}

.prediction {

    font-size: 21px;

    font-weight: bold;

    color: #4f46e5;
}

.probability-label {

    color: #64748b;

    font-size: 10px;

    margin-top: 4px;
}

.probability {

    font-size: 38px;

    font-weight: bold;

    color: #4f46e5;
}

.bar {

    height: 10px;

    background: #e2e8f0;

    border-radius: 20px;

    overflow: hidden;

    margin: 7px 0 9px;
}

.fill {

    height: 100%;

    width: {{ probability }}%;

    border-radius: 20px;

    background:
        linear-gradient(90deg,#4f46e5,#a855f7);

    animation: barIn 1.2s ease;
}

@keyframes barIn {

    from {
        width: 0%;
    }

    to {
        width: {{ probability }}%;
    }
}

.risk {

    display: inline-block;

    padding: 6px 15px;

    border-radius: 30px;

    font-size: 11px;

    font-weight: bold;

    align-self: center;
}

.high {

    background: #fee2e2;

    color: #b91c1c;
}

.medium {

    background: #ffedd5;

    color: #c2410c;
}

.low {

    background: #dcfce7;

    color: #15803d;
}

.result-right h3 {

    font-size: 14px;

    margin-bottom: 6px;
}

.result-right p {

    color: #64748b;

    line-height: 1.45;

    font-size: 11px;
}

.summary {

    margin-top: 10px;

    display: grid;

    grid-template-columns: repeat(3,1fr);

    gap: 7px;
}

.summary-box {

    background: white;

    border-radius: 10px;

    padding: 8px;

    text-align: center;

    border: 1px solid #e2e8f0;
}

.summary-box small {

    display: block;

    color: #64748b;

    font-size: 9px;
}

.summary-box strong {

    font-size: 10px;
}

.model-info {

    margin-top: 10px;

    padding: 9px 11px;

    border-radius: 11px;

    background: #eef2ff;

    color: #3730a3;

    font-size: 10px;

    line-height: 1.5;
}


/* =========================
   PERFORMANCE
========================= */

.table-wrapper {

    overflow-x: auto;
}

table {

    width: 100%;

    border-collapse: collapse;
}

th {

    background: #4f46e5;

    color: white;

    padding: 9px;

    font-size: 10px;
}

td {

    padding: 9px;

    text-align: center;

    border-bottom: 1px solid #e2e8f0;

    font-size: 10px;
}

tr:nth-child(even) {

    background: #f8fafc;
}

.best {

    font-weight: bold;

    color: #4f46e5;
}

.info-box {

    margin-top: 13px;

    padding: 11px;

    background: #f8fafc;

    border-left: 4px solid #6366f1;

    border-radius: 10px;

    font-size: 11px;

    color: #475569;

    line-height: 1.5;
}


/* =========================
   FOOTER
========================= */

.footer {

    text-align: center;

    color: #94a3b8;

    margin-top: 7px;

    font-size: 9px;
}


/* =========================
   MOBILE
========================= */

@media(max-width:700px) {

    body {
        padding: 8px;
    }

    .header h1 {
        font-size: 24px;
    }

    .form-grid {
        grid-template-columns: 1fr;
    }

    .line {
        width: 22px;
    }

    .result-top {
        grid-template-columns: 1fr;
    }

    .summary {
        grid-template-columns: 1fr;
    }

    .navigation {
        flex-wrap: wrap;
    }

    .btn {
        flex: 1;
    }
}

</style>


<script>

/* =========================
   PREDICTION LOADING
========================= */

function startPrediction(button) {

    button.classList.add("loading-active");

    button.disabled = true;

    setTimeout(function() {

        button.form.submit();

    }, 450);
}


/* =========================
   ANIMATED PROBABILITY
========================= */

document.addEventListener("DOMContentLoaded", function() {

    const number =
        document.querySelector(".probability-number");

    if (!number) return;

    const target =
        parseFloat(number.dataset.value);

    let current = 0;

    const duration = 1100;

    const start = performance.now();

    function animate(now) {

        const progress =
            Math.min(
                (now - start) / duration,
                1
            );

        current = target * progress;

        number.textContent =
            current.toFixed(2) + "%";

        if (progress < 1) {

            requestAnimationFrame(animate);

        }

    }

    requestAnimationFrame(animate);

});


/* =========================
   SELECT HIGHLIGHT
========================= */

document.addEventListener("DOMContentLoaded", function() {

    document
        .querySelectorAll("select")
        .forEach(function(select) {

            function update() {

                select.style.borderColor =
                    "#6366f1";

                select.style.background =
                    "#eef2ff";
            }

            update();

            select.addEventListener(
                "change",
                update
            );

        });

});

</script>
"""


# ============================================================
# PROGRESS
# ============================================================

def progress(step):

    result = '<div class="progress">'

    for i in range(1, 5):

        active = "active" if i <= step else ""

        result += f"""
        <div>
            <div class="circle {active}">
                {i}
            </div>
        </div>
        """

        if i < 4:

            line = "active" if i < step else ""

            result += f"""
            <div class="line {line}"></div>
            """

    result += "</div>"

    return result


# ============================================================
# STEP 1
# ============================================================

@app.route("/")
def start():

    session.clear()

    return redirect(url_for("profile"))


@app.route("/profile", methods=["GET", "POST"])
def profile():

    if request.method == "POST":

        fields = [
            "gender",
            "SeniorCitizen",
            "Partner",
            "Dependents",
            "tenure",
            "PhoneService"
        ]

        for key in fields:

            session[key] = request.form[key]

        return redirect(url_for("services"))


    data = {

        "gender":
            session.get("gender", "Female"),

        "SeniorCitizen":
            session.get("SeniorCitizen", "0"),

        "Partner":
            session.get("Partner", "No"),

        "Dependents":
            session.get("Dependents", "No"),

        "tenure":
            session.get("tenure", ""),

        "PhoneService":
            session.get("PhoneService", "Yes")
    }


    return render_template_string(
        COMMON + r"""

<div class="page">

<div class="wrapper">

<div class="header">

<div class="badge">
CUSTOMER ANALYTICS • ML MODEL
</div>

<h1>
Customer Churn Prediction
</h1>

<p>
Predict customer churn probability using machine learning
</p>

</div>

{{ progress|safe }}

<div class="card">

<div class="step-title">

<div class="step-number">
1
</div>

<h2>
Customer Profile
</h2>

</div>


<form method="POST">

<div class="form-grid">


<div class="field">

<label>
Gender
</label>

<select name="gender">

<option value="Female"
{% if data.gender == "Female" %}selected{% endif %}>
👩 Female
</option>

<option value="Male"
{% if data.gender == "Male" %}selected{% endif %}>
👨 Male
</option>

</select>

</div>


<div class="field">

<label>
Senior Citizen
</label>

<select name="SeniorCitizen">

<option value="0"
{% if data.SeniorCitizen == "0" %}selected{% endif %}>
🟢 No
</option>

<option value="1"
{% if data.SeniorCitizen == "1" %}selected{% endif %}>
🔴 Yes
</option>

</select>

</div>


<div class="field">

<label>
Partner
</label>

<select name="Partner">

<option value="No"
{% if data.Partner == "No" %}selected{% endif %}>
🔵 No
</option>

<option value="Yes"
{% if data.Partner == "Yes" %}selected{% endif %}>
🟣 Yes
</option>

</select>

</div>


<div class="field">

<label>
Dependents
</label>

<select name="Dependents">

<option value="No"
{% if data.Dependents == "No" %}selected{% endif %}>
🔵 No
</option>

<option value="Yes"
{% if data.Dependents == "Yes" %}selected{% endif %}>
🟣 Yes
</option>

</select>

</div>


<div class="field">

<label>
Tenure (Months)
</label>

<input
type="number"
name="tenure"
min="0"
value="{{ data.tenure }}"
placeholder="Enter tenure"
required
>

</div>


<div class="field">

<label>
Phone Service
</label>

<select name="PhoneService">

<option value="No"
{% if data.PhoneService == "No" %}selected{% endif %}>
🔵 No
</option>

<option value="Yes"
{% if data.PhoneService == "Yes" %}selected{% endif %}>
🟣 Yes
</option>

</select>

</div>


</div>


<div class="navigation">

<button
class="btn next"
type="submit"
>
Continue →
</button>

</div>

</form>

</div>

<div class="footer">
Customer Churn Prediction • Machine Learning Portfolio Project
</div>

</div>

</div>

""",
        progress=progress(1),
        data=data
    )


# ============================================================
# STEP 2
# ============================================================

@app.route("/services", methods=["GET", "POST"])
def services():

    if request.method == "POST":

        fields = [

            "MultipleLines",
            "InternetService",
            "OnlineSecurity",
            "OnlineBackup",
            "DeviceProtection",
            "TechSupport",
            "StreamingTV",
            "StreamingMovies"

        ]

        for key in fields:

            session[key] = request.form[key]

        return redirect(url_for("billing"))


    defaults = {

        "MultipleLines": "No",
        "InternetService": "DSL",
        "OnlineSecurity": "No",
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "No",
        "StreamingMovies": "No"

    }

    data = {

        key: session.get(key, value)

        for key, value in defaults.items()

    }


    return render_template_string(
        COMMON + r"""

<div class="page">

<div class="wrapper">

<div class="header">

<div class="badge">
CUSTOMER SERVICES
</div>

<h1>
Customer Churn Prediction
</h1>

<p>
Services and support information
</p>

</div>

{{ progress|safe }}

<div class="card">

<div class="step-title">

<div class="step-number">
2
</div>

<h2>
Services & Support
</h2>

</div>


<form method="POST">

<div class="form-grid">


<div class="field">

<label>
Multiple Lines
</label>

<select name="MultipleLines">

<option value="No"
{% if data.MultipleLines == "No" %}selected{% endif %}>
🔵 No
</option>

<option value="Yes"
{% if data.MultipleLines == "Yes" %}selected{% endif %}>
🟣 Yes
</option>

<option value="No phone service"
{% if data.MultipleLines == "No phone service" %}selected{% endif %}>
⚪ No phone service
</option>

</select>

</div>


<div class="field">

<label>
Internet Service
</label>

<select name="InternetService">

<option value="DSL"
{% if data.InternetService == "DSL" %}selected{% endif %}>
🔵 DSL
</option>

<option value="Fiber optic"
{% if data.InternetService == "Fiber optic" %}selected{% endif %}>
🟣 Fiber optic
</option>

<option value="No"
{% if data.InternetService == "No" %}selected{% endif %}>
⚪ No internet service
</option>

</select>

</div>


{% for name, label in [

("OnlineSecurity","Online Security"),
("OnlineBackup","Online Backup"),
("DeviceProtection","Device Protection"),
("TechSupport","Tech Support"),
("StreamingTV","Streaming TV"),
("StreamingMovies","Streaming Movies")

] %}

<div class="field">

<label>
{{ label }}
</label>

<select name="{{ name }}">

<option value="No"
{% if data[name] == "No" %}selected{% endif %}>
🔵 No
</option>

<option value="Yes"
{% if data[name] == "Yes" %}selected{% endif %}>
🟣 Yes
</option>

<option value="No internet service"
{% if data[name] == "No internet service" %}selected{% endif %}>
⚪ No internet service
</option>

</select>

</div>

{% endfor %}


</div>


<div class="navigation">

<a
href="/profile"
class="btn previous"
>
← Previous
</a>

<button
class="btn next"
type="submit"
>
Continue →
</button>

</div>

</form>

</div>

<div class="footer">
Customer Churn Prediction • Machine Learning Portfolio Project
</div>

</div>

</div>

""",
        progress=progress(2),
        data=data
    )


# ============================================================
# STEP 3
# ============================================================

@app.route("/billing", methods=["GET", "POST"])
def billing():

    if request.method == "POST":

        fields = [

            "Contract",
            "PaperlessBilling",
            "PaymentMethod",
            "MonthlyCharges",
            "TotalCharges"

        ]

        for key in fields:

            session[key] = request.form[key]

        return redirect(url_for("predict"))


    data = {

        "Contract":
            session.get(
                "Contract",
                "Month-to-month"
            ),

        "PaperlessBilling":
            session.get(
                "PaperlessBilling",
                "Yes"
            ),

        "PaymentMethod":
            session.get(
                "PaymentMethod",
                "Electronic check"
            ),

        "MonthlyCharges":
            session.get(
                "MonthlyCharges",
                ""
            ),

        "TotalCharges":
            session.get(
                "TotalCharges",
                ""
            )
    }


    return render_template_string(
        COMMON + r"""

<div class="page">

<div class="wrapper">

<div class="header">

<div class="badge">
BILLING ANALYTICS
</div>

<h1>
Customer Churn Prediction
</h1>

<p>
Contract and billing information
</p>

</div>

{{ progress|safe }}

<div class="card">

<div class="step-title">

<div class="step-number">
3
</div>

<h2>
Contract & Billing
</h2>

</div>


<form method="POST">

<div class="form-grid">


<div class="field">

<label>
Contract
</label>

<select name="Contract">

<option value="Month-to-month"
{% if data.Contract == "Month-to-month" %}selected{% endif %}>
🟠 Month-to-month
</option>

<option value="One year"
{% if data.Contract == "One year" %}selected{% endif %}>
🔵 One year
</option>

<option value="Two year"
{% if data.Contract == "Two year" %}selected{% endif %}>
🟢 Two year
</option>

</select>

</div>


<div class="field">

<label>
Paperless Billing
</label>

<select name="PaperlessBilling">

<option value="No"
{% if data.PaperlessBilling == "No" %}selected{% endif %}>
🔵 No
</option>

<option value="Yes"
{% if data.PaperlessBilling == "Yes" %}selected{% endif %}>
🟣 Yes
</option>

</select>

</div>


<div class="field">

<label>
Payment Method
</label>

<select name="PaymentMethod">

<option value="Electronic check"
{% if data.PaymentMethod == "Electronic check" %}selected{% endif %}>
🟣 Electronic check
</option>

<option value="Mailed check"
{% if data.PaymentMethod == "Mailed check" %}selected{% endif %}>
🔵 Mailed check
</option>

<option value="Bank transfer (automatic)"
{% if data.PaymentMethod == "Bank transfer (automatic)" %}selected{% endif %}>
🟢 Bank transfer
</option>

<option value="Credit card (automatic)"
{% if data.PaymentMethod == "Credit card (automatic)" %}selected{% endif %}>
🟠 Credit card
</option>

</select>

</div>


<div class="field">

<label>
Monthly Charges
</label>

<input
type="number"
step="0.01"
name="MonthlyCharges"
value="{{ data.MonthlyCharges }}"
placeholder="Enter monthly charges"
required
>

</div>


<div class="field">

<label>
Total Charges
</label>

<input
type="number"
step="0.01"
name="TotalCharges"
value="{{ data.TotalCharges }}"
placeholder="Enter total charges"
required
>

</div>


</div>


<div class="navigation">

<a
href="/services"
class="btn previous"
>
← Previous
</a>


<button
class="btn predict"
type="submit"
onclick="startPrediction(this)"
>

<span class="normal-text">
🔮 Predict Churn
</span>

<span class="loading">
<span class="spinner"></span>
Analyzing...
</span>

</button>

</div>

</form>

</div>

<div class="footer">
Customer Churn Prediction • Machine Learning Portfolio Project
</div>

</div>

</div>

""",
        progress=progress(3),
        data=data
    )


# ============================================================
# CREATE RAW CUSTOMER DATA
# ============================================================

def get_customer_dataframe():

    data = {

        "gender":
            session["gender"],

        "SeniorCitizen":
            int(session["SeniorCitizen"]),

        "Partner":
            session["Partner"],

        "Dependents":
            session["Dependents"],

        "tenure":
            int(session["tenure"]),

        "PhoneService":
            session["PhoneService"],

        "MultipleLines":
            session["MultipleLines"],

        "InternetService":
            session["InternetService"],

        "OnlineSecurity":
            session["OnlineSecurity"],

        "OnlineBackup":
            session["OnlineBackup"],

        "DeviceProtection":
            session["DeviceProtection"],

        "TechSupport":
            session["TechSupport"],

        "StreamingTV":
            session["StreamingTV"],

        "StreamingMovies":
            session["StreamingMovies"],

        "Contract":
            session["Contract"],

        "PaperlessBilling":
            session["PaperlessBilling"],

        "PaymentMethod":
            session["PaymentMethod"],

        "MonthlyCharges":
            float(session["MonthlyCharges"]),

        "TotalCharges":
            float(session["TotalCharges"])

    }

    return pd.DataFrame([data])


# ============================================================
# MODEL INPUT COMPATIBILITY
# ============================================================

def prepare_model_input(raw_df):

    # If the saved model is a Pipeline,
    # normally it expects the original raw columns.

    if hasattr(model, "named_steps"):

        return raw_df


    # If the model remembers feature names,
    # try to reproduce the encoded feature structure.

    if hasattr(model, "feature_names_in_"):

        expected = list(model.feature_names_in_)

        encoded = pd.get_dummies(
            raw_df,
            drop_first=False
        )

        final = pd.DataFrame(
            0,
            index=raw_df.index,
            columns=expected
        )

        for column in expected:

            if column in encoded.columns:

                final[column] = encoded[column]

        return final


    return raw_df


# ============================================================
# PREDICTION
# ============================================================

@app.route("/predict")
def predict():

    required = [

        "gender",
        "SeniorCitizen",
        "Partner",
        "Dependents",
        "tenure",
        "PhoneService",
        "MultipleLines",
        "InternetService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
        "Contract",
        "PaperlessBilling",
        "PaymentMethod",
        "MonthlyCharges",
        "TotalCharges"

    ]

    if not all(
        key in session
        for key in required
    ):

        return redirect(
            url_for("profile")
        )


    raw_df = get_customer_dataframe()

    model_input = prepare_model_input(raw_df)


    try:

        prediction = model.predict(
            model_input
        )[0]

        if hasattr(
            model,
            "predict_proba"
        ):

            probability_value = float(
                model.predict_proba(
                    model_input
                )[0][1]
            )

        else:

            probability_value = (
                float(prediction)
            )


    except Exception as e:

        return f"""
        <h2>Model Input Error</h2>

        <p>
        The model loaded successfully, but its
        expected input format is different from
        the current form.
        </p>

        <pre>{e}</pre>

        <p>
        Model file:
        {MODEL_FILE}
        </p>
        """


    probability = round(
        probability_value * 100,
        2
    )


    # -----------------------------
    # Prediction label
    # -----------------------------

    if int(prediction) == 1:

        result = "Churn: Yes"

        icon = "⚠️"

    else:

        result = "Churn: No"

        icon = "✓"


    # -----------------------------
    # Risk
    # -----------------------------

    if probability_value >= 0.60:

        risk = "High Risk"

        risk_class = "high"

        recommendation = (

            "This customer has a high estimated "
            "churn risk. Consider a personalized "
            "retention offer, service support or "
            "a long-term contract incentive."

        )

    elif probability_value >= 0.30:

        risk = "Medium Risk"

        risk_class = "medium"

        recommendation = (

            "This customer has a moderate churn "
            "risk. Monitor engagement and consider "
            "targeted customer retention strategies."

        )

    else:

        risk = "Low Risk"

        risk_class = "low"

        recommendation = (

            "This customer has a relatively low "
            "churn risk. Continue regular engagement "
            "and maintain service quality."

        )


    return render_template_string(

        COMMON + r"""

<div class="page">

<div class="wrapper">

<div class="header">

<div class="badge">
PREDICTION COMPLETE
</div>

<h1>
Customer Churn Prediction
</h1>

<p>
Machine learning analysis result
</p>

</div>


{{ progress|safe }}


<div class="card result-card">


<div class="result-top">


<div class="result-left">

<div class="result-icon">
{{ icon }}
</div>

<h2>
Prediction
</h2>

<div class="prediction">
{{ result }}
</div>

<div class="probability-label">
Churn Probability
</div>

<div
class="probability probability-number"
data-value="{{ probability }}"
>
0.00%
</div>


<div class="bar">

<div class="fill"></div>

</div>


<div class="risk {{ risk_class }}">
{{ risk }}
</div>

</div>


<div class="result-right">

<h3>
💡 Recommended Action
</h3>

<p>
{{ recommendation }}
</p>


<div class="summary">


<div class="summary-box">

<small>
Contract
</small>

<strong>
{{ contract }}
</strong>

</div>


<div class="summary-box">

<small>
Tenure
</small>

<strong>
{{ tenure }} months
</strong>

</div>


<div class="summary-box">

<small>
Monthly Charges
</small>

<strong>
₹{{ monthly }}
</strong>

</div>


</div>


<div class="model-info">

<b>Model:</b>
Customer Churn Machine Learning Classifier

<br>

<b>Model file:</b>
{{ model_file }}

<br>

<b>Output:</b>
Probability-based customer risk assessment.

</div>


</div>


</div>


<div class="navigation">


<a
href="/billing"
class="btn previous"
>
← Previous
</a>


<a
href="/performance"
class="btn performance"
>
📊 Model Performance
</a>


<a
href="/new"
class="btn new"
>
+ New Prediction
</a>


</div>


</div>


<div class="footer">

Customer Churn Prediction •
Machine Learning Portfolio Project

</div>

</div>

</div>

""",

        progress=progress(4),

        result=result,

        probability=probability,

        risk=risk,

        risk_class=risk_class,

        recommendation=recommendation,

        icon=icon,

        contract=session["Contract"],

        tenure=session["tenure"],

        monthly=session["MonthlyCharges"],

        model_file=MODEL_FILE

    )


# ============================================================
# PERFORMANCE PAGE
# ============================================================

@app.route("/performance")
def performance():

    return render_template_string(

        COMMON + r"""

<div class="page">

<div class="wrapper">

<div class="header">

<div class="badge">
MODEL EVALUATION
</div>

<h1>
Model Performance
</h1>

<p>
Comparison of machine learning models
</p>

</div>


<div class="card">


<div class="step-title">

<div class="step-number">
📊
</div>

<h2>
Model Comparison
</h2>

</div>


<div class="table-wrapper">

<table>

<tr>

<th>
Model
</th>

<th>
Accuracy
</th>

<th>
Precision
</th>

<th>
Recall
</th>

<th>
F1 Score
</th>

<th>
ROC-AUC
</th>

</tr>


<tr>

<td>
Logistic Regression
</td>

<td>
80.7%
</td>

<td>
66.0%
</td>

<td>
56.1%
</td>

<td>
60.7%
</td>

<td>
84.2%
</td>

</tr>


<tr>

<td>
Decision Tree
</td>

<td>
79.4%
</td>

<td>
63.1%
</td>

<td>
54.0%
</td>

<td>
58.2%
</td>

<td>
82.7%
</td>

</tr>


<tr>

<td>
Random Forest
</td>

<td>
80.3%
</td>

<td>
67.5%
</td>

<td>
50.0%
</td>

<td>
57.5%
</td>

<td class="best">
84.4%
</td>

</tr>


<tr>

<td class="best">
Balanced Logistic Regression
</td>

<td>
73.9%
</td>

<td>
50.5%
</td>

<td class="best">
78.3%
</td>

<td>
61.4%
</td>

<td>
84.2%
</td>

</tr>

</table>

</div>


<div class="info-box">

<b>
Why Balanced Logistic Regression?
</b>

<br>

The balanced model improves
<b>Recall for churn customers</b>.
This is useful for customer retention because
identifying more potential churners allows the
business to take preventive action.

</div>


<div class="navigation">

<a
href="/predict"
class="btn previous"
>
← Back to Result
</a>

<a
href="/new"
class="btn new"
>
+ New Prediction
</a>

</div>


</div>


<div class="footer">

Customer Churn Prediction •
Machine Learning Portfolio Project

</div>

</div>

</div>

"""

    )


# ============================================================
# NEW PREDICTION
# ============================================================

@app.route("/new")
def new_prediction():

    session.clear()

    return redirect(
        url_for("profile")
    )


# ============================================================
# NO CACHE
# ============================================================

@app.after_request
def no_cache(response):

    response.headers[
        "Cache-Control"
    ] = "no-store, no-cache, must-revalidate, max-age=0"

    response.headers[
        "Pragma"
    ] = "no-cache"

    response.headers[
        "Expires"
    ] = "0"

    return response


# ============================================================
# AUTO OPEN BROWSER
# ============================================================

def open_browser():

    time.sleep(1.5)

    webbrowser.open(
        "http://127.0.0.1:5006"
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 55)
    print(" CUSTOMER CHURN PREDICTION")
    print("=" * 55)
    print()
    print("Model:", MODEL_FILE)
    print()
    print("Starting application...")
    print("URL: http://127.0.0.1:5006")
    print()

    threading.Thread(
        target=open_browser,
        daemon=True
    ).start()

    app.run(
        host="127.0.0.1",
        port=5006,
        debug=False,
        use_reloader=False
    )