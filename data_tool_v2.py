
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📊 Data Analysis Dashboard", layout="wide")

st.title("📊 Bottleshop Data Analysis Dashboard")

uploaded_file = st.file_uploader("Upload an Excel or CSV file", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ File loaded successfully!")

    with st.expander("🔍 Data Preview & Shape"):
        st.dataframe(df)
        st.write(f"Rows: {df.shape[0]} | Columns: {df.shape[1]}")

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(include='object').columns.tolist()

    # MULTI-FILTERING SECTION
    st.sidebar.header("🔎 Filters")
    filtered_df = df.copy()

    for col in categorical_cols:
        unique_vals = df[col].dropna().unique()
        selected_vals = st.sidebar.multiselect(f"Filter by `{col}`", options=unique_vals, default=unique_vals)
        if selected_vals:
            filtered_df = filtered_df[filtered_df[col].isin(selected_vals)]

    # SUMMARY STATS
    st.subheader("📈 Summary Statistics")
    if not filtered_df.empty:
        st.dataframe(filtered_df.describe())
    else:
        st.warning("⚠️ No data to show. Try adjusting your filters.")

    # CHART OPTIONS
    st.sidebar.header("📊 Chart Options")
    chart_type = st.sidebar.selectbox("Select chart type", ["Bar", "Line", "Pie"])
    x_col = st.sidebar.selectbox("X-axis", options=filtered_df.columns)
    y_col = st.sidebar.selectbox("Y-axis (numeric only)", options=numeric_cols)

    st.subheader("📊 Chart")
    if not filtered_df.empty:
        if chart_type == "Bar":
            fig = px.bar(filtered_df, x=x_col, y=y_col)
        elif chart_type == "Line":
            fig = px.line(filtered_df, x=x_col, y=y_col)
        elif chart_type == "Pie":
            fig = px.pie(filtered_df, names=x_col, values=y_col)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Upload a file and select valid filters to generate chart.")

    # EXPORT
    st.subheader("📤 Export Data")
    st.download_button("Download Filtered Data as CSV", filtered_df.to_csv(index=False), "filtered_data.csv", "text/csv")

else:
    st.info("📁 Upload a file to begin.")
