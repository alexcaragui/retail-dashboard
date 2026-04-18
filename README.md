# 📊 Business Analytics Dashboard

A full-stack business intelligence dashboard for retail operations, built with Python, FastAPI, and PostgreSQL.

## Features

- **Sales Dashboard** — monthly trends, top products, daily revenue charts
- **Customer Analysis** — new vs returning customers, top spenders, city distribution
- **Inventory Management** — low stock alerts, reorder levels, stock rotation
- **Sales Prediction** — linear regression model estimating next 30 days of revenue

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend API | FastAPI + Uvicorn |
| Frontend | Streamlit + Plotly |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Data Processing | Pandas + NumPy |
| ML / Predictions | scikit-learn |

## Architecture

PostgreSQL → SQLAlchemy → FastAPI (REST API) → HTTP/JSON → Streamlit

The backend exposes REST endpoints (e.g. `/api/sales/monthly`) which the
Streamlit frontend consumes to render interactive charts and tables.

## 📁 Project Structure

retail-dashboard/
├── backend/
│   ├── main.py              # FastAPI app + router registration
│   └── routers/
│       ├── sales.py         # Sales endpoints
│       ├── customers.py     # Customer endpoints
│       └── inventory.py     # Inventory endpoints
├── analytics/
│   └── predictions.py       # Linear regression model
├── db/
│   ├── connection.py        # SQLAlchemy engine
│   └── schema.sql           # PostgreSQL schema
├── data/
│   └── generate_data.py     # Fake data generator
└── app.py                   # Streamlit frontend

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/username/retail-dashboard.git
cd retail-dashboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup PostgreSQL
- Create a database named `retail_dashboard`
- Run `db/schema.sql` in pgAdmin or psql
- Update credentials in `db/connection.py`

### 4. Generate fake data
```bash
python data/generate_data.py
```

### 5. Start the backend
```bash
uvicorn backend.main:app --reload
```

### 6. Start the frontend
```bash
streamlit run app.py
```

Open `http://localhost:8501` for the dashboard and `http://localhost:8000/docs` for the API docs.

## 📸 Screenshots

*Coming soon*

## 📄 License
MIT