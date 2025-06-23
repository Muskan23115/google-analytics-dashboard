# 📊 Google Analytics Dashboard

This project is a **website analytics dashboard** built using **Flask** and the **Google Analytics 4 (GA4) API**. It visually displays key metrics like total users, device distribution, and country-wise visits using dynamic charts powered by **Chart.js**.

---

## 🚀 Features

- 🔐 **Google Analytics API Integration** (via service account)
- 📈 **Line Chart** for total users over the past 7 days
- 🖥️ **Pie Chart** for user device categories (desktop, mobile, tablet)
- 🌍 **Bar Chart** for country-wise user distribution
- 🧭 Smooth one-page layout with scroll-based navigation
- 🌗 Responsive UI with current time, greeting, and quick stats

---

## 📦 Tech Stack

| Tool/Tech           | Role                            |
|---------------------|----------------------------------|
| **Flask**           | Backend framework (Python)       |
| **GA4 API**         | Data source                      |
| **Chart.js**        | Interactive chart rendering      |
| **HTML/CSS/JS**     | Frontend & interactivity         |

---

## 🔧 Setup Instructions

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/google-analytics-dashboard.git
   cd google-analytics-dashboard


2. **Create a virtual environment & install dependencies** 
   python -m venv venv
   venv\Scripts\activate   # On Windows
   pip install -r requirements.txt


3. **Google Analytics Setup**
   1. Create a Google Cloud project and enable Google Analytics Data API

   2. Create a Service Account and download your_credentials.json

   3. Place your_credentials.json in the root of your project (but DO NOT commit it)


4. **Run the App**
   python app.py

**⚠️ Notes**
   1. Ensure your GA4 property is collecting real website data or simulate data with tools like Tag Assistant

   2. Never push your_credentials.json — it contains sensitive keys

   3. Works best with a live or test site receiving traffic

