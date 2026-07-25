import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from pathlib import Path

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
from pathlib import Path

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    BASE_DIR = Path(__file__).parent

    orders = pd.read_csv(BASE_DIR / "olist_orders_dataset.csv")
    order_items = pd.read_csv(BASE_DIR / "olist_order_items_dataset.csv")
    order_payments = pd.read_csv(BASE_DIR / "olist_order_payments_dataset.csv")
    order_reviews = pd.read_csv(BASE_DIR / "olist_order_reviews_dataset.csv")
    customers = pd.read_csv(BASE_DIR / "olist_customers_dataset.csv")
    product = pd.read_csv(BASE_DIR / "olist_products_dataset.csv")
    seller = pd.read_csv(BASE_DIR / "olist_sellers_dataset.csv")
    translation = pd.read_csv(BASE_DIR / "product_category_name_translation.csv")

    df = (
        orders.merge(customers, on="customer_id", how="left")
        .merge(order_items, on="order_id", how="left")
        .merge(order_payments, on="order_id", how="left")
        .merge(order_reviews, on="order_id", how="left")
        .merge(product, on="product_id", how="left")
        .merge(seller, on="seller_id", how="left")
    )

    df = df.drop_duplicates()

    df["order_approved_at"] = pd.to_datetime(
        df["order_approved_at"], errors="coerce"
    )

    df["order_date"] = df["order_approved_at"].dt.date
    df["order_month"] = df["order_approved_at"].dt.to_period("M").astype(str)

    df = df.merge(
        translation,
        on="product_category_name",
        how="left"
    )

    return df

full_df = load_data()

# -----------------------------
# Additional Data (from your provided stats)
# -----------------------------
# Top sellers
top_sellers_data = {
    "seller_state": ["SP", "PR", "MG", "SC", "RJ", "RS", "DF", "BA", "GO", "PE", "ES", "MA", "MT", "PB"],
    "no_of_sellers": [278, 47, 44, 24, 21, 18, 6, 4, 3, 2, 1, 1, 1, 1]
}
top_sellers_df = pd.DataFrame(top_sellers_data)
customer_data={
    "Toatal no. of customers":[99441],
    "Total no. of returning customers":[2875],
    "Percentage of retuening customers":[2.99]
}
customers_data_df=pd.DataFrame(customer_data)

# Payment methods summary
payment_summary = {
    "Payment Method": ["credit_card", "boleto", "voucher", "debit_card"],
    "Orders": [87719, 23159, 6379, 1706]
}
payment_df = pd.DataFrame(payment_summary)

# -----------------------------
# App Title & Layout
# -----------------------------
st.set_page_config(page_title="Olist E-Commerce Dashboard", layout="wide")
st.title("📊 Olist E-Commerce Dashboard")

# -----------------------------
# Key Metrics
# -----------------------------
total_revenue = full_df["payment_value"].sum()
total_orders = full_df["order_id"].nunique()
total_customers = full_df["customer_id"].nunique()
avg_order_value = total_revenue / total_orders

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
col2.metric("🛒 Total Orders", f"1,18,966")
col3.metric("👥 Total Customers", f"{total_customers:,}")
col4.metric("📈 Avg Order Value", f"${avg_order_value:,.2f}")

st.markdown("---")

# -----------------------------
# Revenue & Sellers (Side by Side)
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by State")
    state_revenue = full_df.groupby("customer_state")["payment_value"].sum().reset_index()
    state_revenue["revenue_pct"] = (state_revenue["payment_value"] / total_revenue) * 100
    fig = px.choropleth(
        state_revenue,
        geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
        locations="customer_state",
        featureidkey="properties.sigla",
        color="revenue_pct",
        color_continuous_scale="reds",
        scope="south america",
        title="Revenue Percentage by State",
        hover_data=["payment_value", "revenue_pct"]
    )
    fig.update_layout(width=700, height=900,
                      geo=dict(center={"lat": -14.2, "lon": -51.9}, projection_scale=3))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Revenue Trend by State")
    state_choice = st.selectbox("Select a state:", full_df["customer_state"].dropna().unique())
    monthly_state_revenue = full_df[full_df["customer_state"] == state_choice]\
        .groupby("order_month")["payment_value"].sum().reset_index()
    fig_line = px.line(monthly_state_revenue, x="order_month", y="payment_value",
                       title=f"Monthly Revenue Trend in {state_choice}", markers=True)
    fig_line.update_layout(xaxis_title="Month", yaxis_title="Revenue")
    st.plotly_chart(fig_line)

with col2:
    st.subheader("Seller Distribution & Top Sellers")
    st.dataframe(top_sellers_df)
    seller_revenue = full_df.groupby("seller_state")["payment_value"].sum().reset_index()
    seller_revenue["revenue_pct"] = (seller_revenue["payment_value"] / seller_revenue["payment_value"].sum()) * 100
    fig2 = px.choropleth(
        seller_revenue,
        geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
        locations="seller_state",
        featureidkey="properties.sigla",
        color="revenue_pct",
        color_continuous_scale="Greens",
        scope="south america",
        title="Seller Revenue by State",
        hover_data=["payment_value", "revenue_pct"]
    )
    fig2.update_layout(width=700, height=900,
                       geo=dict(center={"lat": -14.2, "lon": -51.9}, projection_scale=3))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# -----------------------------
# Payment Methods
# -----------------------------
st.subheader("Customer analysis")
st.dataframe(customer_data)

st.markdown("---")

# -----------------------------
# Customers Analysis
# -----------------------------
st.subheader("Customer Analysis")
customer_df = full_df.groupby("customer_unique_id").agg(
    total_spent=("payment_value", "sum"),
    first_order=("order_approved_at", "min"),
    last_order=("order_approved_at", "max")
).reset_index()

churned_customers = customer_df[customer_df["first_order"] != customer_df["last_order"]]
churn_pct = 2.99

col1, col2 = st.columns(2)
with col1:
    st.subheader("Payment Methods Overview")
    st.dataframe(payment_df)
with col2:
    st.write("Top 5 Customers by Revenue")
    st.dataframe(customer_df.sort_values(by="total_spent", ascending=False).head(5))

st.markdown("---")

# -----------------------------
# Products
# -----------------------------
st.subheader("Products Analysis")
product_category_df = full_df.groupby("product_category_name_english")["payment_value"].sum().reset_index()
product_category_df = product_category_df.dropna()

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(px.treemap(product_category_df, path=["product_category_name_english"],
                               values="payment_value", title="Revenue by Category"), use_container_width=True)

with col2:
    st.subheader("Top 6 Categories (Monthly Revenue)")
    top6 = product_category_df.sort_values(by="payment_value", ascending=False).head(6)
    filtered = full_df[full_df["product_category_name_english"].isin(top6["product_category_name_english"])]
    monthly_df = filtered.groupby(["product_category_name_english", "order_month"])["payment_value"].sum().reset_index()
    st.plotly_chart(px.line(monthly_df, x="order_month", y="payment_value", color="product_category_name_english",
                            title="Monthly Revenue Trend (Top 6 Categories)"), use_container_width=True)

st.markdown("---")

# -----------------------------
# Reviews
# -----------------------------
st.subheader("Customer Reviews Analysis")
review_df = full_df[["review_answer_timestamp", "customer_state", "review_score"]].dropna()
review_df["review_answer_timestamp"] = pd.to_datetime(review_df["review_answer_timestamp"], errors="coerce")
review_df["review_month"] = review_df["review_answer_timestamp"].dt.to_period('M').astype(str)

state = st.selectbox("Select a state to analyze reviews:", full_df["customer_state"].dropna().unique())
state_reviews = review_df[review_df["customer_state"] == state]
monthly_reviews = state_reviews.groupby("review_month")["review_score"].mean().reset_index()

fig = px.line(
    monthly_reviews,
    x="review_month",
    y="review_score",
    markers=True,
    title=f"Average Review Score Trend in {state}"
)

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Average Score",
    xaxis_tickangle=45,
    template="plotly_white"
)

st.plotly_chart(fig)
st.title("📌 Business Insights Summary")

st.subheader("1. Geographical Presence")
st.write("""
    - The business is currently concentrated in the **South-East region** of the country.  
    - **Most buyers and sellers** are from this region.  
    - 👉 **Recommendation**: Expand seller & buyer acquisition in other regions to balance growth.
    """)

st.subheader("2. Customer Behavior")
st.write("""
    - Around **97% of customers are new**, while only **3% return**.  
    - Revenue is heavily dependent on **new customer acquisition** (driven by advertising).  
    - 👉 **Recommendation**: Improve retention strategies (loyalty programs, discounts, better CX) to increase repeat purchases.
    """)

st.subheader("3. Revenue Dependency")
st.write("""
    - Heavy reliance on marketing spend for new customer growth.  
    - 👉 **Recommendation**: Focus on building brand trust & repeat purchase incentives to reduce dependency on ads.
    """)
st.subheader("4. Product Category Trends")
st.write("""
    - When one product category shows a **spike in sales**, other categories also tend to grow.  
    - Indicates **complementary demand** or shared **seasonal effects**.  
    - 👉 **Recommendation**: Bundle products, cross-sell during spikes, and run multi-category promotions to maximize revenue.
    """)


st.subheader("Next Steps")
st.markdown("""
    ✅ Explore expansion in **North & West regions**  
    ✅ Launch **loyalty programs** to improve repeat rate  
    ✅ Invest in **seller onboarding** outside South-East  
    """)
