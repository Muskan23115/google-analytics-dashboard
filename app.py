from flask import Flask, render_template, jsonify
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests

app = Flask(__name__)

KEY_PATH = "your_credentials.json"
PROPERTY_ID = "494127517"
SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]

credentials = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
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

@app.route("/api/active-users")
def active_users():
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        metrics=[Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date="7daysAgo", end_date="today")]
    )
    response = client.run_report(request)
    return jsonify({
        "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "data": [int(row.metric_values[0].value) for row in response.rows]
    })

@app.route("/api/devices")
def device_distribution():
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
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

@app.route("/api/countries")
def get_country_distribution():
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
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
    chart_labels, chart_data, table_data = [], [], []

    for row in response.rows:
        country = row.dimension_values[0].value
        users = int(row.metric_values[0].value)
        sessions = int(row.metric_values[1].value)
        bounce_rate = f"{float(row.metric_values[2].value):.1f}%"
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
        property=f"properties/{PROPERTY_ID}",
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
    avg_sec = int(float(values[3].value))
    return jsonify({
        "totalUsers": int(values[0].value),
        "bounceRate": f"{float(values[1].value):.1f}%",
        "newUsers": int(values[2].value),
        "avgTime": f"{avg_sec // 60}:{str(avg_sec % 60).zfill(2)}"
    })

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
    if not response.rows:
        return jsonify({"usersToday": 0, "newUsers": 0, "avgSession": "0:00"})

    values = response.rows[0].metric_values
    avg_sec = int(float(values[2].value))
    return jsonify({
        "usersToday": int(values[0].value),
        "newUsers": int(values[1].value),
        "avgSession": f"{avg_sec // 60}:{str(avg_sec % 60).zfill(2)}"
    })

@app.route("/api/realtime-users")
def get_realtime_users():
    try:
        # Refresh access token
        scoped_creds = credentials.with_scopes(["https://www.googleapis.com/auth/analytics.readonly"])
        scoped_creds.refresh(Request())

        headers = {
            "Authorization": f"Bearer {scoped_creds.token}"
        }

        payload = {
            "dimensions": [{"name": "minutesAgo"}],
            "metrics": [{"name": "activeUsers"}],
            "limit": 30
        }

        response = requests.post(
            f"https://analyticsdata.googleapis.com/v1beta/properties/{PROPERTY_ID}:runRealtimeReport",
            headers=headers,
            json=payload
        )

        data = response.json()
        active_users_last_30min = sum(int(row["metricValues"][0]["value"]) for row in data.get("rows", []))

        return jsonify({"activeUsersLast30Min": active_users_last_30min})

    except Exception as e:
        print("Realtime error:", e)
        return jsonify({"activeUsersLast30Min": 0})


if __name__ == '__main__':
    app.run(debug=True)
