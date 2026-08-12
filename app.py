from flask import Flask, render_template, request, jsonify
import joblib
import re

app = Flask(__name__)

# Load trained model and vectorizer
model = joblib.load("model/model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")


# -----------------------------
# Suspicious words
# -----------------------------

high_words = [
    "click",
    "verify",
    "verification",
    "password",
    "login",
    "account",
    "suspended",
    "blocked",
    "urgent",
    "immediately",
    "confirm",
    "security alert",
    "reset",
    "otp",
    "winner",
    "prize",
    "reward",
    "free",
    "bitcoin",
    "cryptocurrency",
    "bank",
    "payment",
    "refund",
    "claim",
    "limited time",
    "act now"
]


# -----------------------------
# Home page
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Prediction
# -----------------------------

@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    if not data or "email" not in data:
        return jsonify({
            "error": "No email provided"
        }), 400

    email = data["email"].strip().lower()

    # Check empty email
    if not email:
        return jsonify({
            "error": "Please enter an email before analyzing."
        }), 400


    # -----------------------------
    # AI Prediction
    # -----------------------------

    email_vector = vectorizer.transform([email])

    prediction = model.predict(email_vector)[0]

    probability = model.predict_proba(email_vector)[0]

    # Probability of phishing
    phishing_probability = probability[1]

    risk = round(phishing_probability * 100)

    # AI confidence
    confidence = round(max(probability) * 100, 2)


    # -----------------------------
    # Detect suspicious words
    # -----------------------------

    reasons = []

    for word in high_words:

        if word in email:

            reasons.append(
                f"Contains suspicious word: {word}"
            )


    # Remove duplicate reasons
    reasons = list(dict.fromkeys(reasons))


    # -----------------------------
    # Detect URLs
    # -----------------------------

    urls = re.findall(
        r'https?://[^\s]+|www\.[^\s]+',
        email
    )

    link_count = len(urls)


    if link_count > 0:

        reasons.append(
            f"Contains {link_count} suspicious link(s)"
        )


    # -----------------------------
    # Detect urgency
    # -----------------------------

    urgency_words = [
        "urgent",
        "immediately",
        "act now",
        "within 24 hours",
        "as soon as possible",
        "limited time"
    ]

    urgency_detected = []

    for word in urgency_words:

        if word in email:

            urgency_detected.append(word)


    if len(urgency_detected) > 0:

        reasons.append(
            "Uses urgent or threatening language"
        )


    # -----------------------------
    # Detect money / prize
    # -----------------------------

    money_words = [
        "money",
        "cash",
        "prize",
        "winner",
        "reward",
        "bitcoin",
        "payment",
        "refund",
        "lottery",
        "million",
        "dollar"
    ]

    money_detected = []

    for word in money_words:

        if word in email:

            money_detected.append(word)


    if len(money_detected) > 0:

        reasons.append(
            "Contains money, prize or reward related content"
        )


    # -----------------------------
    # Risk classification
    # -----------------------------

    if risk >= 70:

        status = "Phishing Detected"
        threat = "High"

        recommendation = (
            "Do not click links, download attachments, "
            "or provide personal information."
        )

    elif risk >= 40:

        status = "Suspicious Email"
        threat = "Medium"

        recommendation = (
            "Verify the sender and links before taking any action."
        )

    else:

        status = "Safe Email"
        threat = "Low"

        recommendation = (
            "No major phishing indicators detected. "
            "Still remain cautious with unknown senders."
        )


    # -----------------------------
    # If AI says safe but obvious
    # indicators exist, show reasons
    # -----------------------------

    if len(reasons) == 0:

        reasons.append(
            "No major suspicious indicators detected."
        )


    # -----------------------------
    # Final response
    # -----------------------------

    return jsonify({

        "risk": risk,

        "status": status,

        "threat": threat,

        "confidence": confidence,

        "reasons": reasons,

        "link_count": link_count,

        "urgency": len(urgency_detected) > 0,

        "money_related": len(money_detected) > 0,

        "recommendation": recommendation

    })


# -----------------------------
# Run Flask
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)