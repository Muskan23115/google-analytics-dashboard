from flask import Flask, jsonify, render_template
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest
from google.oauth2 import service_account

app = Flask(__name__)

# Load credentials and initialize client
PROPERTY_ID = "494127517"
credentials = service_account.Credentials.from_service_account_file("your_credentials.json")
client = BetaAnalyticsDataClient(credentials=credentials)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')



# ========== API Routes ==========

@app.route('/analytics/users')
def get_users_data():
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        dimensions=[Dimension(name="date")],
        metrics=[Metric(name="activeUsers")],  # <-- changed here
        date_ranges=[DateRange(start_date="7daysAgo", end_date="today")]
    )
    response = client.run_report(request)

    labels = [row.dimension_values[0].value for row in response.rows]
    data = [int(row.metric_values[0].value) for row in response.rows]

    return jsonify({"labels": labels, "data": data})


@app.route('/analytics/devices')
def get_devices_data():
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        dimensions=[Dimension(name="deviceCategory")],
        metrics=[Metric(name="totalUsers")],
        date_ranges=[DateRange(start_date="7daysAgo", end_date="today")]
    )
    response = client.run_report(request)

    labels = [row.dimension_values[0].value.capitalize() for row in response.rows]
    data = [int(row.metric_values[0].value) for row in response.rows]

    return jsonify({"labels": labels, "data": data})

@app.route('/analytics/countries')
def get_country_data():
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        dimensions=[Dimension(name="country")],
        metrics=[Metric(name="totalUsers")],
        date_ranges=[DateRange(start_date="7daysAgo", end_date="today")]
    )
    response = client.run_report(request)

    labels = [row.dimension_values[0].value for row in response.rows]
    data = [int(row.metric_values[0].value) for row in response.rows]

    return jsonify({"labels": labels, "data": data})


if __name__ == '__main__':
    app.run(debug=True)
