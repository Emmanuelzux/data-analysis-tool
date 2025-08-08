
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Bottleshop Dashboard", layout="wide")

# Logo and Title
with st.sidebar:
    st.image("assets/logo.png", width=150)
    st.title("Bottleshop Dashboard")
    page = st.radio("Go to", ["📁 Upload", "📊 Analysis", "📤 Export"])

@st.cache_data
def load_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

sample_data = pd.DataFrame({
    "Store": ["Kitwe", "Ndola", "Solwezi", "Kitwe", "Ndola"],
    "Product": ["Beer", "Whisky", "Vodka", "Gin", "Beer"],
    "Sales": [1200, 1800, 800, 1500, 1000],
    "Qty": [30, 45, 20, 40, 25]
})

uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

if uploaded_file:
    df = load_data(uploaded_file)
else:
    st.info("No file uploaded. Using sample data.")
    df = sample_data.copy()

if page == "📁 Upload":
    st.header("📁 Data Preview")
    st.dataframe(df)
    st.write(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")

elif page == "📊 Analysis":
    st.header("📊 Data Analysis")

    categorical_cols = df.select_dtypes(include="object").columns.tolist()
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    # Filters
    st.sidebar.subheader("🔍 Filters")
    filtered_df = df.copy()
    for col in categorical_cols:
        values = st.sidebar.multiselect(f"{col}", options=df[col].unique(), default=df[col].unique())
        filtered_df = filtered_df[filtered_df[col].isin(values)]

    st.subheader("📌 Summary Metrics")
    cols = st.columns(3)
    if "Sales" in filtered_df.columns:
        cols[0].metric("Total Sales", f"${filtered_df['Sales'].sum():,.2f}")
        cols[1].metric("Average Sale", f"${filtered_df['Sales'].mean():,.2f}")
    if "Qty" in filtered_df.columns:
        cols[2].metric("Total Quantity", int(filtered_df["Qty"].sum()))

    st.subheader("📈 Chart")
    chart_type = st.selectbox("Chart type", ["Bar", "Line", "Pie"])
    group_col = st.selectbox("Group by (X-axis)", options=categorical_cols)
    y_col = st.selectbox("Y-axis (numeric)", options=numeric_cols)

    grouped = filtered_df.groupby(group_col)[y_col].sum().reset_index()

    if chart_type == "Bar":
        fig = px.bar(grouped, x=group_col, y=y_col)
    elif chart_type == "Line":
        fig = px.line(grouped, x=group_col, y=y_col)
    elif chart_type == "Pie":
        fig = px.pie(grouped, names=group_col, values=y_col)

    st.plotly_chart(fig, use_container_width=True)

elif page == "📤 Export":
    st.header("📤 Export Filtered Data")
    st.download_button("Download CSV", df.to_csv(index=False), "filtered_data.csv", "text/csv")
