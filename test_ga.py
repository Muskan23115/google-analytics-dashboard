from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric
from google.oauth2 import service_account

print("✅ Script started...")

try:
    # Load credentials
    credentials = service_account.Credentials.from_service_account_file("your_credentials.json")
    print("🔐 Credentials loaded successfully.")
    
    # Set property ID
    property_id = "494127517"
    
    # Initialize the client
    client = BetaAnalyticsDataClient(credentials=credentials)
    print("📡 Client initialized.")

    # Build the report request with a wider date range
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="date")],
        metrics=[Metric(name="totalUsers")],
        date_ranges=[DateRange(start_date="2024-06-01", end_date="today")]  # <-- key change here
    )

    print("📊 Sending GA report request...")
    response = client.run_report(request)
    print("✅ Got response from GA API.")

    if not response.rows:
        print("⚠️ No user data found.")
    else:
        print("📈 User data:")
        for row in response.rows:
            date = row.dimension_values[0].value
            users = row.metric_values[0].value
            print(f"📅 {date}: 👤 {users} users")

except Exception as e:
    print("❌ Error:", e)
