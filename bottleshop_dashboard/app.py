
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Bottleshop Dashboard", layout="wide")

# Use logo from GitHub raw URL
LOGO_URL = "https://raw.githubusercontent.com/Emmanuelzux/data-analysis-tool/main/bottleshop_dashboard/assets/logo.png"

# Sidebar navigation
with st.sidebar:
    st.image("assets/logo.png", width=150)
    st.title("Bottleshop Dashboard")
    page = st.radio("Navigation", ["📁 Upload", "📊 Analyze", "📤 Export"])


@st.cache_data
def load_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

# Fallback sample dataset: generic and unbranded
sample_data = pd.DataFrame({
    "Department": ["HR", "Finance", "IT", "Marketing", "Sales"],
    "Employees": [25, 18, 40, 22, 35],
    "Budget": [100000, 150000, 120000, 90000, 110000]
})

uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    df = load_data(uploaded_file)
else:
    st.info("No file uploaded — using generic sample dataset for preview.")
    df = sample_data.copy()

# Page: Upload Preview
if page == "📁 Upload":
    st.header("📁 Data Preview")
    st.dataframe(df)
    st.caption(f"Data contains {df.shape[0]} rows and {df.shape[1]} columns.")

# Page: Analysis
elif page == "📊 Analyze":
    st.header("📊 Explore Your Data")

    categorical_cols = df.select_dtypes(include="object").columns.tolist()
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    # Filters
    st.sidebar.subheader("🔍 Column Filters")
    filtered_df = df.copy()
    for col in categorical_cols:
        choices = st.sidebar.multiselect(f"Filter `{col}`", df[col].unique(), default=list(df[col].unique()))
        filtered_df = filtered_df[filtered_df[col].isin(choices)]

    # Summary Metrics
    if numeric_cols:
        st.subheader("📌 Summary Metrics")
        col1, col2, col3 = st.columns(3)
        for i, col in enumerate(numeric_cols[:3]):
            col_val = filtered_df[col].sum()
            [col1, col2, col3][i].metric(f"Total {col}", f"{col_val:,.2f}")

    # Charts
    if categorical_cols and numeric_cols:
        st.subheader("📈 Chart Visualization")
        chart_type = st.selectbox("Chart Type", ["Bar", "Line", "Pie"])
        group_col = st.selectbox("Group by (categorical)", options=categorical_cols)
        value_col = st.selectbox("Aggregate (numeric)", options=numeric_cols)

        grouped = filtered_df.groupby(group_col)[value_col].sum().reset_index()

        if chart_type == "Bar":
            fig = px.bar(grouped, x=group_col, y=value_col)
        elif chart_type == "Line":
            fig = px.line(grouped, x=group_col, y=value_col)
        elif chart_type == "Pie":
            fig = px.pie(grouped, names=group_col, values=value_col)

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Chart requires both numeric and categorical columns.")

# Page: Export
elif page == "📤 Export":
    st.header("📤 Export Filtered Data")
    st.download_button("Download CSV", df.to_csv(index=False), "filtered_data.csv", "text/csv")
