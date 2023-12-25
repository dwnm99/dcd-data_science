import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe
def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_purchase_date').agg({
        "order_id": "nunique",
        "payment_value": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "payment_value": "revenue"
    }, inplace=True)
    
    return daily_orders_df

def create_sum_order_status_df(df):
    sum_order_items_df = df.groupby("order_status").order_id.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def create_sum_delivery_status_df(df):
    sum_delivery_status_df = df.groupby("delivery_status").order_id.sum().sort_values(ascending=False).reset_index()
    return sum_delivery_status_df

def create_top10_order_city_df(df):
    top10_order_city_df = df.groupby(by="customer_city").order_id.nunique().sort_values(ascending=False).head(10).reset_index()
    top10_order_city_df = top10_order_city_df.sort_values(by='order_id', ascending=True).reset_index()
    top10_order_city_df.rename(columns={
        "order_id": "order_count"
    }, inplace=True)
    
    return top10_order_city_df

def create_top10_revenue_city_df(df):
    top10_revenue_city_df = df.groupby(by="customer_city").payment_value.sum().sort_values(ascending=False).head(10).reset_index()
    top10_revenue_city_df = top10_revenue_city_df.sort_values(by='payment_value', ascending=True).reset_index()
    top10_revenue_city_df.rename(columns={
        "payment_value": "revenue"
    }, inplace=True)
    
    return top10_revenue_city_df

# Load cleaned data
all_df = pd.read_csv("fact_order_data.csv")

datetime_columns = ["order_purchase_date", 
                    "order_purchase_month"
                    ]
all_df.sort_values(by="order_purchase_date", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Filter data
min_date = all_df["order_purchase_date"].min()
max_date = all_df["order_purchase_date"].max()

with st.sidebar:
    # Menambahkan logo 
    st.image("https://blog.disfold.com/wp-content/uploads/2019/05/ecommerce-brazil.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_purchase_date"] >= str(start_date)) & 
                (all_df["order_purchase_date"] <= str(end_date))]

# st.dataframe(main_df)

# # Menyiapkan berbagai dataframe
daily_orders_df = create_daily_orders_df(main_df)
sum_order_status_df = create_sum_order_status_df(main_df)
sum_delivery_status_df = create_sum_delivery_status_df(main_df)
top10_order_city_df = create_top10_order_city_df(main_df)
top10_revenue_city_df = create_top10_revenue_city_df(main_df)


# plot number of daily orders (2021)
st.header('Brazillian Ecommerce Dashboard :sparkles:')
st.subheader('Daily Orders')

col1, col2 = st.columns(2)

with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total orders", value=total_orders)

with col2:
    total_revenue = daily_orders_df.revenue.sum()
    st.metric("Total Revenue", value=round(total_revenue,2))

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_purchase_date"],
    daily_orders_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# plot top 10 cities with highest order_count and revenue
st.subheader("Top 10 cities with highest order_count and revenue")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

ax1.barh(top10_order_city_df['customer_city'], top10_order_city_df['order_count'], label='Total Orders')
ax1.set_xlabel('Total Orders')
ax1.set_ylabel('City')
ax1.set_title('Top 10 Cities by Total Orders')
ax1.grid(axis='x', linestyle='--', alpha=0.6)

ax2.barh(top10_revenue_city_df['customer_city'], top10_revenue_city_df['revenue'], label='Total Revenue')
ax2.set_xlabel('Total Revenue')
ax2.set_ylabel('City')
ax2.set_title('Top 10 Cities by Total Revenue')
ax2.grid(axis='x', linestyle='--', alpha=0.6)

st.pyplot(fig)

st.caption('Copyright (c) dimsum 2023')