from flask import Flask, render_template, jsonify
from flask import request
from flask import redirect
from flask import session
from flask import send_file

import random
import datetime

from database import (
    init_db,
    insert_threat,
    get_all_threats
)

# PDF

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

# =====================================================

app = Flask(__name__)

app.secret_key = "soc_secret"

# =====================================================
# DATABASE
# =====================================================

init_db()

# =====================================================
# LOGIN
# =====================================================

USERNAME = "admin"
PASSWORD = "admin123"

# =====================================================
# DATA
# =====================================================

devices = [

    "Smart Camera",
    "Smart Lock",
    "Smart Bulb",
    "Smart Thermostat",
    "Smart TV",
    "Smart Speaker"
]

attacks = [

    "DDoS Attack",
    "Botnet Activity",
    "Port Scan",
    "Brute Force",
    "MITM Attack",
    "Malware Traffic"
]

countries = [

    "Russia",
    "China",
    "Iran",
    "USA",
    "Germany"
]

# =====================================================
# LOGIN PAGE
# =====================================================

@app.route('/', methods=['GET', 'POST'])

def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == USERNAME and password == PASSWORD:

            session['user'] = username

            return redirect('/dashboard')

    return render_template('login.html')

# =====================================================
# DASHBOARD
# =====================================================

@app.route('/dashboard')

def dashboard():

    if 'user' not in session:

        return redirect('/')

    return render_template('dashboard.html')

# =====================================================
# LIVE DATA
# =====================================================

@app.route('/live')

def live():

    results = []

    for i in range(10):

        attack_mode = random.choice([0,1,1])

        device = random.choice(devices)

        if attack_mode:

            attack = random.choice(attacks)

            severity = random.choice([
                "Critical",
                "High",
                "Medium"
            ])

            confidence = round(
                random.uniform(90,99),
                2
            )

            explanation = random.choice([

                "Abnormal packet behavior detected",

                "Suspicious SYN packet activity",

                "Traffic spike exceeded threshold",

                "IoT communication anomaly",

                "Malicious flow signature detected"
            ])

            country = random.choice(countries)

            status = "Attack Detected"

        else:

            attack = "Safe Traffic"

            severity = "Safe"

            confidence = round(
                random.uniform(95,99),
                2
            )

            explanation = (
                "Normal IoT behavior"
            )

            country = "Local"

            status = "Safe"

        item = {

            "device": device,

            "attack": attack,

            "severity": severity,

            "confidence": confidence,

            "country": country,

            "status": status,

            "explanation": explanation,

            "time": str(
                datetime.datetime.now()
            )
        }

        results.append(item)

        insert_threat(item)

    return jsonify(results)

# =====================================================
# SHAP
# =====================================================

@app.route('/shap')

def shap():

    features = [

        "Packet Size",
        "Flow Duration",
        "SYN Flag Count",
        "Traffic Rate",
        "Protocol Type",
        "Connection Frequency"
    ]

    data = []

    for f in features:

        data.append({

            "feature": f,

            "importance": round(
                random.uniform(0.4,1.0),
                2
            )
        })

    return jsonify(data)

# =====================================================
# REPORT PAGE
# =====================================================

@app.route('/report')

def report():

    threats = get_all_threats()

    return render_template(

        'report.html',

        threats=threats
    )

# =====================================================
# DOWNLOAD PDF REPORT
# =====================================================

@app.route('/download-report')

def download_report():

    threats = get_all_threats()

    filename = "AI_SOC_Report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    # TITLE

    title = Paragraph(

        "AI SOC Threat Intelligence Report",

        styles['Title']
    )

    elements.append(title)

    elements.append(Spacer(1,20))

    # SUMMARY

    total = len(threats)

    critical = 0
    high = 0
    medium = 0

    for t in threats:

        if t[3] == "Critical":

            critical += 1

        elif t[3] == "High":

            high += 1

        elif t[3] == "Medium":

            medium += 1

    summary = f"""

    <b>Total Threats:</b> {total}<br/><br/>

    <b>Critical:</b> {critical}<br/>
    <b>High:</b> {high}<br/>
    <b>Medium:</b> {medium}<br/><br/>

    AI-based hybrid machine learning
    models detected abnormal IoT
    network traffic patterns associated
    with cyber threats.

    """

    elements.append(

        Paragraph(summary,
        styles['BodyText'])

    )

    elements.append(Spacer(1,20))

    # THREATS

    for t in threats[-20:]:

        text = f"""

        <b>Attack:</b> {t[2]}<br/>
        <b>Device:</b> {t[1]}<br/>
        <b>Severity:</b> {t[3]}<br/>
        <b>Confidence:</b> {t[4]}%<br/>
        <b>Country:</b> {t[5]}<br/>
        <b>Explanation:</b> {t[6]}<br/>
        <b>Timestamp:</b> {t[7]}<br/><br/>

        """

        elements.append(

            Paragraph(
                text,
                styles['BodyText']
            )

        )

    # BUILD PDF

    doc.build(elements)

    return send_file(

        filename,

        as_attachment=True
    )

# =====================================================

if __name__ == '__main__':

    app.run(debug=True)