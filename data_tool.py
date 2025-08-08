import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Local Data Analysis Tool", layout="wide")
st.title("📊 Local Data Analysis Tool")

uploaded_file = st.file_uploader("Upload your Excel or CSV file", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("File loaded successfully!")
    st.write("### Preview of Data")
    st.dataframe(df)

    numeric_cols = df.select_dtypes(include='number').columns.tolist()

    st.sidebar.header("📌 Analysis Options")
    filter_col = st.sidebar.selectbox("Filter by column", options=df.columns)
    filter_vals = st.sidebar.multiselect("Choose values to include", df[filter_col].unique())
    if filter_vals:
        df = df[df[filter_col].isin(filter_vals)]

    chart_type = st.sidebar.selectbox("Select chart type", ["Bar", "Line", "Pie"])
    x_col = st.sidebar.selectbox("X-axis", options=df.columns)
    y_col = st.sidebar.selectbox("Y-axis (numeric)", options=numeric_cols)

    st.write("### 📈 Chart")
    if chart_type == "Bar":
        fig = px.bar(df, x=x_col, y=y_col)
    elif chart_type == "Line":
        fig = px.line(df, x=x_col, y=y_col)
    elif chart_type == "Pie":
        fig = px.pie(df, names=x_col, values=y_col)

    st.plotly_chart(fig, use_container_width=True)
    st.download_button("Download filtered data as CSV", df.to_csv(index=False), "filtered_data.csv", "text/csv")
else:
    st.info("Upload a file to begin.")


