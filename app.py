from flask import Flask, render_template, jsonify
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest
from google.oauth2 import service_account

app = Flask(__name__)

# 🔐 Replace with your actual credentials filename
KEY_PATH = "your_credentials.json"
PROPERTY_ID = "494127517"

credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
client = BetaAnalyticsDataClient(credentials=credentials)

@app.route('/')
@app.route('/welcome')
def welcome():
    return render_template("welcome.html")

@app.route('/users')
def users():
    return render_template("users.html")

@app.route('/devices')
def devices():
    return render_template("devices.html")

@app.route('/countries')
def countries():
    return render_template("countries.html")

#  API: Active Users for Users Chart
@app.route("/api/active-users")
def active_users():
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        metrics=[Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date="7daysAgo", end_date="today")]
    )
    response = client.run_report(request)

    return jsonify({
        "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],  # Placeholder
        "data": [int(row.metric_values[0].value) for row in response.rows]
    })

@app.route("/api/devices")
def device_distribution():
    request = RunReportRequest(
        property=f"properties/494127517",
        dimensions=[Dimension(name="deviceCategory")],
        metrics=[Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date="7daysAgo", end_date="today")]
    )
    response = client.run_report(request)

    counts = {"Mobile": 0, "Desktop": 0, "Tablet": 0}
    for row in response.rows:
        device = row.dimension_values[0].value.title()
        value = int(row.metric_values[0].value)
        counts[device] = value

    return jsonify({
        "labels": list(counts.keys()),
        "data": list(counts.values())
    })

from google.analytics.data_v1beta.types import Dimension, Metric, RunReportRequest, DateRange

@app.route("/api/countries")
def get_country_distribution():
    request = RunReportRequest(
        property=f"properties/494127517",
        dimensions=[Dimension(name="country")],
        metrics=[
            Metric(name="activeUsers"),
            Metric(name="sessions"),
            Metric(name="bounceRate"),
            Metric(name="averageSessionDuration")
        ],
        date_ranges=[DateRange(start_date="7daysAgo", end_date="today")]
    )
    response = client.run_report(request)

    chart_labels = []
    chart_data = []
    table_data = []

    for row in response.rows:
        country = row.dimension_values[0].value
        users = int(row.metric_values[0].value)
        sessions = int(row.metric_values[1].value)
        bounce_rate = f"{float(row.metric_values[2].value):.1f}%"
        
        # Convert seconds to MM:SS format
        total_sec = int(float(row.metric_values[3].value))
        avg_session = f"{total_sec // 60}:{str(total_sec % 60).zfill(2)}"

        chart_labels.append(country)
        chart_data.append(users)

        table_data.append({
            "country": country,
            "users": users,
            "sessions": sessions,
            "bounceRate": bounce_rate,
            "avgSession": avg_session
        })

    return jsonify({
        "labels": chart_labels,
        "data": chart_data,
        "table": table_data
    })

@app.route("/api/user-metrics")
def get_user_metrics():
    request = RunReportRequest(
        property=f"properties/494127517",
        metrics=[
            Metric(name="totalUsers"),
            Metric(name="bounceRate"),
            Metric(name="newUsers"),
            Metric(name="averageSessionDuration")
        ],
        date_ranges=[DateRange(start_date="7daysAgo", end_date="today")]
    )

    response = client.run_report(request)
    values = response.rows[0].metric_values

    total_users = int(values[0].value)
    bounce_rate = f"{float(values[1].value):.1f}%"
    new_users = int(values[2].value)
    avg_sec = int(float(values[3].value))
    avg_time = f"{avg_sec // 60}:{str(avg_sec % 60).zfill(2)}"

    return jsonify({
        "totalUsers": total_users,
        "bounceRate": bounce_rate,
        "newUsers": new_users,
        "avgTime": avg_time
    })

@app.route("/api/device-metrics")
def get_device_metrics():
    request = RunReportRequest(
        property=f"properties/494127517",
        dimensions=[Dimension(name="deviceCategory")],
        metrics=[Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date="7daysAgo", end_date="today")]
    )

    response = client.run_report(request)

    metrics = {}
    total = 0

    for row in response.rows:
        device = row.dimension_values[0].value.lower()  # 'mobile', 'desktop', etc.
        count = int(row.metric_values[0].value)
        metrics[device] = count
        total += count

    # Convert to percentages
    for key in metrics:
        metrics[key] = round((metrics[key] / total) * 100)

    return jsonify(metrics)

@app.route("/api/welcome-metrics")
def get_welcome_metrics():
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        metrics=[
            Metric(name="activeUsers"),
            Metric(name="newUsers"),
            Metric(name="averageSessionDuration")
        ],
        date_ranges=[DateRange(start_date="today", end_date="today")]
    )

    response = client.run_report(request)

    # Check for empty response
    if not response.rows:
        return jsonify({
            "usersToday": 0,
            "newUsers": 0,
            "avgSession": "0:00"
        })

    values = response.rows[0].metric_values

    users_today = int(values[0].value)
    new_users = int(values[1].value)
    avg_seconds = int(float(values[2].value))
    avg_session = f"{avg_seconds // 60}:{str(avg_seconds % 60).zfill(2)}"

    return jsonify({
        "usersToday": users_today,
        "newUsers": new_users,
        "avgSession": avg_session
    })


if __name__ == '__main__':
    app.run(debug=True)
