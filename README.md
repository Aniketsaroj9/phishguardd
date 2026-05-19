# 🛡️ PhishGuard

PhishGuard is a web-based cybersecurity application that detects phishing URLs and scam messages (SMS/email) using a hybrid approach combining rule-based threat analysis and machine learning classification. 

Users can paste a suspicious URL or text content and instantly receive a risk assessment, threat classification, and explainable human-readable reasoning—no cybersecurity expertise required.

![PhishGuard Banner](https://img.shields.io/badge/Status-MVP%20Complete-success)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-API-lightgrey)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-ML-orange)

## ✨ Features

- **URL Analysis Engine**: Evaluates URLs against 12 heuristic rules (e.g., suspicious keywords, IP-based URLs, double slash redirects, TLD checks) and generates a risk score.
- **Message Analysis Engine**: Uses a trained Machine Learning pipeline (TF-IDF + Logistic Regression) to classify SMS/email text as Safe or Scam with 96%+ accuracy.
- **Explainable AI**: Returns human-readable explanations for *why* a link or message was flagged.
- **Dashboard & History**: A modern Single Page Application (SPA) frontend that tracks your scan metrics and provides a paginated history of past scans.
- **Auto-Initializing Database**: Automatically connects to your local MySQL server and provisions the required tables on the first run.

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3 (Bootstrap 5), Vanilla JavaScript
- **Backend**: Python 3, Flask, flask-cors
- **Machine Learning**: scikit-learn, pandas, NLTK
- **Database**: MySQL (via XAMPP)

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

1. **Python 3.10+**: Make sure Python is installed and added to your system PATH.
2. **XAMPP**: Required for the local MySQL database.

### 1. Database Setup

1. Open the **XAMPP Control Panel**.
2. Click **Start** next to the **MySQL** module. (Ensure it turns green and runs on port `3306`).
3. *Note: You do not need to manually create the database. The Flask app will automatically create `phishguard_db` and the required tables upon starting.*

### 2. Backend Setup

1. Open your terminal and navigate to the project directory:
   ```cmd
   cd phisingguard/backend
   ```
2. Create a virtual environment:
   ```cmd
   python -m venv venv
   ```
3. Activate the virtual environment:
   - **Windows:** `venv\Scripts\activate`
   - **Mac/Linux:** `source venv/bin/activate`
4. Install the required dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

### 3. Running the Application

1. Ensure your virtual environment is activated and XAMPP MySQL is running.
2. Start the Flask backend server:
   ```cmd
   python app.py
   ```
3. The server will start on `http://localhost:5000` and automatically initialize your database.
4. Open the frontend interface by double-clicking the `index.html` file located at:
   `phisingguard/frontend/index.html`
   *(Alternatively, if Apache is running in XAMPP, navigate to `http://localhost/phisingguard/frontend/index.html` in your browser).*

---

## 🧠 Machine Learning Model

The project comes with a pre-trained model located in `backend/ml/`. If you want to retrain the model yourself from scratch:

1. Ensure your virtual environment is activated.
2. Navigate to the backend directory:
   ```cmd
   cd backend
   ```
3. Run the training script (it will automatically download the SMS Spam Collection dataset, process it, evaluate it, and save the new `.pkl` files):
   ```cmd
   python ml/train_model.py
   ```

## 📝 License

This project is created as a reference and learning implementation for cybersecurity and AI threat detection.
