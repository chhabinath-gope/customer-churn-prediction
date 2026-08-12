from flask import Flask, request, render_template_string, session, redirect, url_for
import pandas as pd
import os
import glob
import joblib
import pickle
import threading
import webbrowser
import time


# ============================================================
# APP CONFIGURATION
# ============================================================

app = Flask(__name__)

# Render / production mein environment variable use hoga.
# Local machine par fallback value use hogi.
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "customer_churn_prediction_final_2026"
)

app.config["SESSION_PERMANENT"] = False


# ============================================================
# FIND MODEL
# ============================================================

def find_model():

    # Your actual model is preferred first.
    preferred_files = [
        "customer_churn_model.pkl",
        "customer_churn_model.joblib"
    ]

    for filename in preferred_files:
        if os.path.isfile(filename):
            return filename

    # Fallback: search for any pkl/joblib file.
    possible_files = []

    possible_files.extend(glob.glob("*.pkl"))
    possible_files.extend(glob.glob("*.joblib"))

    if not possible_files:
        raise FileNotFoundError(
            "No .pkl or .joblib model file found in the project folder."
        )

    # Prefer churn/customer/model related files.
    preferred = [
        f for f in possible_files
        if any(
            word in f.lower()
            for word in ["churn", "customer", "model"]
        )
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

    try:

        with open(MODEL_FILE, "rb") as f:
            model = pickle.load(f)

    except Exception as e:

        raise RuntimeError(
            f"Unable to load model file: {MODEL_FILE}\n{e}"
        )


print("Model loaded:", MODEL_FILE)


# ============================================================
# COMMON HTML / CSS / JAVASCRIPT
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
    color: #4f
