import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="US Population Dashboard", layout="wide")

st.title("📊 US Population Dashboard")

# التحقق من وجود الملف
data_path = os.path.join("datasets", "us-population-2010-2019.csv")
if not os.path.exists(data_path):
    st.error(f"❌ الملف غير موجود: {data_path}")
    st.stop()

# قراءة البيانات
df = pd.read_csv(data_path)

# اختيار السنة
selected_year = st.slider("Select Year", min_value=2010, max_value=2019, value=2019)

df_selected_year = df[df["year"] == selected_year]

# عرض البيانات كجدول
st.subheader(f"Data for {selected_year}")
st.dataframe(df_selected_year)

# رسم خريطة Choropleth
choropleth = px.choropleth(
    df_selected_year,
    locations="states_code",
    color="population",
    locationmode="USA-states",
    color_continuous_scale="blues",
    range_color=(0, max(df_selected_year.population)),
    scope="usa",
    labels={"population": "Population"}
)

choropleth.update_layout(
    template="plotly_dark",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=0, r=0, t=0, b=0),
    height=600
)

st.plotly_chart(choropleth)
