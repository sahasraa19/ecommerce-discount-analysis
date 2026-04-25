import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="E-Commerce Discount Analysis", page_icon="🛒", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_data.csv")
    return df

df = load_data()

st.title("🛒 E-Commerce Discount Analysis")
st.markdown("**Studying discount patterns on Flipkart and Shopsy**")
st.divider()

st.sidebar.title("🔍 Filters")
selected_platforms = st.sidebar.multiselect("Platform", options=df["platform"].unique(), default=df["platform"].unique())
selected_categories = st.sidebar.multiselect("Category", options=df["category"].unique(), default=df["category"].unique())
min_discount, max_discount = st.sidebar.slider("Discount Range (%)", 0, 100, (0, 100))

filtered_df = df[
    (df["platform"].isin(selected_platforms)) &
    (df["category"].isin(selected_categories)) &
    (df["discount_calculated"] >= min_discount) &
    (df["discount_calculated"] <= max_discount)
]

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Products", len(filtered_df))
col2.metric("Avg Discount", f"{filtered_df['discount_calculated'].mean():.1f}%")
col3.metric("Max Discount", f"{filtered_df['discount_calculated'].max():.1f}%")
col4.metric("Avg Savings", f"₹{filtered_df['savings_inr'].mean():.0f}")
col5.metric("Avg Rating", f"{filtered_df['star_rating'].mean():.1f} ⭐")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("📦 Avg Discount by Category")
    avg_cat = filtered_df.groupby("category")["discount_calculated"].mean().reset_index()
    fig = px.bar(avg_cat, x="category", y="discount_calculated", color="category", color_discrete_sequence=["#E53E3E","#0D9488","#0F2044"], text="discount_calculated", labels={"discount_calculated":"Avg Discount (%)","category":"Category"})
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(showlegend=False, plot_bgcolor="white", height=380)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🏪 Flipkart vs Shopsy")
    avg_platform = filtered_df.groupby(["category","platform"])["discount_calculated"].mean().reset_index()
    fig = px.bar(avg_platform, x="category", y="discount_calculated", color="platform", barmode="group", color_discrete_map={"Flipkart":"#F7931E","Shopsy":"#7B2FBE"}, text="discount_calculated", labels={"discount_calculated":"Avg Discount (%)","category":"Category"})
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(plot_bgcolor="white", height=380)
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("💰 Price vs Discount")
    fig = px.scatter(filtered_df, x="selling_price_inr", y="discount_calculated", color="category", hover_name="product_name", hover_data=["platform","mrp_inr","savings_inr"], opacity=0.7, labels={"selling_price_inr":"Selling Price (₹)","discount_calculated":"Discount (%)"})
    fig.update_layout(plot_bgcolor="white", height=380)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🏷️ Discount Band Distribution")
    discount_counts = filtered_df["discount_band"].value_counts().reset_index()
    discount_counts.columns = ["discount_band","count"]
    fig = px.pie(discount_counts, values="count", names="discount_band", color_discrete_sequence=["#38A169","#0D9488","#E53E3E"], hole=0.4)
    fig.update_layout(height=380)
    st.plotly_chart(fig, use_container_width=True)

st.subheader("🏆 Top 15 Most Discounted Products")
top15 = filtered_df.nlargest(15, "discount_calculated").copy()
top15["short_name"] = top15["product_name"].str[:45] + "..."
fig = px.bar(top15, x="discount_calculated", y="short_name", color="platform", orientation="h", color_discrete_map={"Flipkart":"#F7931E","Shopsy":"#7B2FBE"}, text="discount_calculated", labels={"discount_calculated":"Discount (%)","short_name":"Product"})
fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
fig.update_layout(plot_bgcolor="white", height=480, yaxis=dict(autorange="reversed"))
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("💵 Savings by Category")
    fig = px.box(filtered_df, x="category", y="savings_inr", color="platform", color_discrete_map={"Flipkart":"#F7931E","Shopsy":"#7B2FBE"}, points="outliers", labels={"savings_inr":"Savings (₹)","category":"Category"})
    fig.update_layout(plot_bgcolor="white", height=380)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📊 Avg Discount by Price Band")
    price_band_avg = filtered_df.groupby("price_band")["discount_calculated"].mean().reset_index()
    order = ["Budget","Mid Range","Premium"]
    price_band_avg["price_band"] = pd.Categorical(price_band_avg["price_band"], categories=order, ordered=True)
    price_band_avg = price_band_avg.sort_values("price_band")
    fig = px.bar(price_band_avg, x="price_band", y="discount_calculated", color="price_band", color_discrete_sequence=["#38A169","#0D9488","#0F2044"], text="discount_calculated", labels={"discount_calculated":"Avg Discount (%)","price_band":"Price Band"})
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(showlegend=False, plot_bgcolor="white", height=380)
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("📋 Browse the Data")
st.markdown(f"Showing **{len(filtered_df)}** products")
show_cols = ["product_name","category","platform","selling_price_inr","mrp_inr","discount_calculated","star_rating","price_band","savings_inr"]
st.dataframe(filtered_df[show_cols].sort_values("discount_calculated", ascending=False).reset_index(drop=True), use_container_width=True, height=400)

st.divider()
st.markdown("**E-Commerce Discount Analysis** · Sri Sahasra Badagoni · IIT Bhilai · April 2026")
