import pandas as pd
import streamlit as st
import plotly.express as px

# Load the Excel file
file_path = "files/Incidencias_SAP_Commissions_20250127.xlsx"
sheet_name = "BD"

# Read the data from the BD sheet
data = pd.read_excel(file_path, sheet_name=sheet_name)

# Filter for "Acceso a SAP" in the "8. Tipo de Incidencia" column
filtered_data = data[data["8. Tipo de Incidencia"] == "Acceso a SAP"]

if not filtered_data.empty:
    # Parse dates
    filtered_data["3. Fecha de registro"] = pd.to_datetime(filtered_data["3. Fecha de registro"], errors="coerce")
    filtered_data["Fecha estimada resolución"] = pd.to_datetime(filtered_data["Fecha estimada resolución"], errors="coerce")

    # Calculate Tiempo de respuesta del ticket
    filtered_data["Tiempo de respuesta del ticket"] = filtered_data.apply(
        lambda row: (
            (row["Fecha estimada resolución"] - row["3. Fecha de registro"])
            if pd.notnull(row["Fecha estimada resolución"]) and pd.notnull(row["3. Fecha de registro"])
            else pd.NaT
        ),
        axis=1,
    )

    # Calculate the period of dates
    min_date = filtered_data["3. Fecha de registro"].min()
    max_date = filtered_data["3. Fecha de registro"].max()

    # Format dates for display
    min_date_str = min_date.strftime("%Y-%m-%d") if pd.notnull(min_date) else "N/A"
    max_date_str = max_date.strftime("%Y-%m-%d") if pd.notnull(max_date) else "N/A"

    # High-Level KPIs
    total_tickets = len(filtered_data)
    resolved_tickets = len(filtered_data[filtered_data["Estado"] == "Resuelto"])
    pending_tickets = total_tickets - resolved_tickets
    avg_response_time = filtered_data["Tiempo de respuesta del ticket"].mean()

    # Format average response time for display
    avg_response_time_days = avg_response_time.days if pd.notnull(avg_response_time) else "N/A"
    avg_response_time_hours = avg_response_time.seconds // 3600 if pd.notnull(avg_response_time) else "N/A"

    # Display KPIs
    st.title("Dynamic KPI Dashboard for 'Acceso a SAP'")
    st.subheader("High-Level KPIs")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Tickets", total_tickets)
    col2.metric("Resolved Tickets", resolved_tickets)
    col3.metric("Pending Tickets", pending_tickets)
    col4.metric("Avg Response Time", f"{avg_response_time_days} days {avg_response_time_hours} hours")
    col5.metric("Period", f"{min_date_str} to {max_date_str}")

    # Summary of Tickets by Category (4. Categoría)
    st.subheader("Tickets by Category")
    category_summary = filtered_data["4. Categoría"].value_counts().reset_index()
    category_summary.columns = ["Categoría", "Count"]

    # Display as a bar chart
    fig_category = px.bar(
        category_summary,
        x="Count",
        y="Categoría",
        title="Tickets by Category",
        text="Count",
        orientation="h",
    )
    fig_category.update_traces(textposition="outside")
    st.plotly_chart(fig_category)

    # Dynamic Selection: Choose a category to drill down
    selected_category = st.selectbox("Select a Category to View Details", category_summary["Categoría"])

    if selected_category:
        # Filter data for the selected category
        category_data = filtered_data[filtered_data["4. Categoría"] == selected_category]

        # Tickets left to respond
        pending_in_category = len(category_data[category_data["Estado"] != "Resuelto"])

        st.subheader(f"Details for Category: {selected_category}")
        st.write(f"Total Tickets in Category: {len(category_data)}")
        st.write(f"Pending Tickets in Category: {pending_in_category}")

        # Additional Table: 1. Código and Dates
        st.subheader("Ticket Response Time Details")
        response_time_data = category_data[
            ["1. Código", "3. Fecha de registro", "Fecha estimada resolución", "Tiempo de respuesta del ticket"]
        ]
        st.dataframe(response_time_data)

    # Line Chart for 3. Fecha de registro
    st.subheader("Trend: Tickets Over Time")
    if "3. Fecha de registro" in filtered_data.columns:
        trend_data = filtered_data.groupby(filtered_data["3. Fecha de registro"].dt.date).size().reset_index(name="Count")
        trend_data.columns = ["Fecha", "Count"]

        fig_trend = px.line(trend_data, x="Fecha", y="Count", title="Tickets Over Time")
        st.plotly_chart(fig_trend)

    # Tickets by Sucursal (Top 10 by Count)
    st.subheader("Top 10 Sucursales by Number of Tickets")

    # Count the number of tickets per Sucursal
    sucursal_counts = filtered_data["2. Sucursal"].value_counts().reset_index()
    sucursal_counts.columns = ["Sucursal", "Ticket Count"]

    # Select the top 10 Sucursales
    top_10_sucursales = sucursal_counts.head(10)

    # Create a pie chart for the top 10
    fig_sucursal = px.pie(
        top_10_sucursales,
        names="Sucursal",
        values="Ticket Count",
        title="Top 10 Sucursales by Number of Tickets",
    )
    st.plotly_chart(fig_sucursal)



else:
    st.title("Dynamic KPI Dashboard for 'Acceso a SAP'")
    st.write("No data available for 'Acceso a SAP'.")
