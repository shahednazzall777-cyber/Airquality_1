import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ---- إعداد الصفحة ----
st.set_page_config(
    page_title="🌿 Air Quality Dashboard",
    page_icon="🌍",
    layout="wide"
)

# ---- HEADER ----
st.markdown("""
    <div style="background-color:#0B3954;padding:20px;border-radius:10px">
        <h1 style="color:white;text-align:center;">🌍 لوحة بيانات جودة الهواء</h1>
        <p style="color:white;text-align:center;font-size:18px;">
        متابعة جودة الهواء في الولايات المختلفة مع إحصاءات ورسوم بيانية تفاعلية.
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---- SIDEBAR ----
st.sidebar.header("🔍 خيارات المستخدم")
st.sidebar.markdown("اختر السنة لعرض البيانات.")

# ---- تعديل مسار الملف ----
data_path = os.path.join("datasets", "us-population-2010-2019-reshaped.csv")
if not os.path.exists(data_path):
    st.error(f"❌ الملف غير موجود: {data_path}")
    st.stop()

# قراءة البيانات
df = pd.read_csv(data_path)

# اختيار السنة
selected_year = st.sidebar.slider(
    "اختر السنة",
    int(df["year"].min()),
    int(df["year"].max()),
    int(df["year"].max())
)

df_selected_year = df[df["year"] == selected_year]

# ---- MAIN CONTENT ----
st.subheader(f"📊 بيانات السكان لعام {selected_year}")

# عرض الجدول
st.dataframe(df_selected_year)

# رسم خريطة Choropleth
choropleth = px.choropleth(
    df_selected_year,
    locations="states_code",
    color="population",
    locationmode="USA-states",
    color_continuous_scale="blues",
    range_color=(0, df_selected_year["population"].max()),
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

st.plotly_chart(choropleth, use_container_width=True)

# ---- FOOTER ----
st.markdown("""
<div style="background-color:#0B3954;padding:10px;border-radius:10px;margin-top:20px;">
<p style="color:white;text-align:center;">© 2025 Air Quality Dashboard | تم التطوير بواسطة شهد</p>
</div>
""", unsafe_allow_html=True)
