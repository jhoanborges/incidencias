# Dynamic KPI Dashboard for "Acceso a SAP"

This application is a Streamlit-based dynamic KPI dashboard that provides insights and visualizations for tickets related to "Acceso a SAP". The dashboard includes KPIs, bar charts, line charts, and pie charts, along with detailed tables for better understanding and tracking.

---

## Features

1. **High-Level KPIs**: Display total tickets, resolved tickets, pending tickets, average response time, and ticket period.
2. **Category Analysis**: Visualize ticket counts by category and drill down for detailed analysis.
3. **Tickets Over Time**: Trend analysis of ticket registration dates.
4. **Sucursal Analysis**: Top 10 sucursales by ticket count in a pie chart.
5. **Details and Links**: Includes tables with detailed ticket data and external links for quick navigation.

---

## Prerequisites

Ensure the following are installed:

- Python 3.8 or above
- Required Python libraries:
  - `pandas`
  - `streamlit`
  - `plotly`
  - `openpyxl`

---

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-repo/accesos-dashboard.git
   cd accesos-dashboard
   
2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt

3. Place the Excel file Incidencias.xlsx in the files/ directory.
4. Run the Streamlit app:
   ```bash
   streamlit run accesos.py

---
## Usage Instructions
Launch the app using the command:

 ```bash
streamlit run accesos.py
```
- Interact with the dashboard:
- View high-level KPIs.
- Explore ticket details by category.
- Visualize trends over time and analyze sucursales with the most tickets.
- Click on external links in the tables to access specific records.
