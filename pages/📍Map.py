import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(layout="wide")
st.title("📍 Pollution Map")

data_file = "datasets/AirQualityUCI.csv"
df = None

if os.path.exists(data_file):
    try:
        # Try common separators and decimal formats
        df = pd.read_csv(data_file, sep=';', decimal=',')
    except Exception:
        try:
            df = pd.read_csv(data_file)
        except Exception as e:
            st.warning(f"تعذّر قراءة {data_file}: {e}")

# Heuristics to find lat/lon/pollution columns
def find_coord_columns(df):
    lat_cols = [c for c in df.columns if c.lower() in ("latitude","lat","y")]
    lon_cols = [c for c in df.columns if c.lower() in ("longitude","lon","x")]
    return lat_cols, lon_cols

data = None
if df is not None:
    lat_cols, lon_cols = find_coord_columns(df)
    if lat_cols and lon_cols:
        lat_col = lat_cols[0]
        lon_col = lon_cols[0]
        st.write(f"تمّ إيجاد إحداثيات في الداتا: `{lat_col}`, `{lon_col}`")
        data = df[[lat_col, lon_col]].dropna().rename(columns={lat_col:'lat', lon_col:'lon'})
        # Try to find a pollution-related column
        pol_candidates = [c for c in df.columns if any(k in c.lower() for k in ('co','pm','no2','nox','c6h6','poll'))]
        if pol_candidates:
            data['pollution'] = df[pol_candidates[0]].fillna(0)
        else:
            data['pollution'] = np.random.randint(100,1500,size=len(data))
    else:
        st.info("لا توجد أعمدة إحداثيات واضحة في dataset. يمكنك رفع CSV يحتوي على `lat, lon, pollution`.")

uploaded = st.file_uploader("أو ارفع CSV يحتوي على الأعمدة lat, lon, pollution", type=['csv'])
if uploaded is not None:
    try:
        uploaded_df = pd.read_csv(uploaded)
        data = uploaded_df.rename(columns={uploaded_df.columns[0]:'lat'}) if len(uploaded_df.columns)>=3 else uploaded_df
        st.success("تم رفع الملف.")
    except Exception as e:
        st.error(f"خطأ عند قراءة الملف: {e}")

if data is None:
    st.info("استخدام بيانات تجريبية مع نقاط داخل الأردن لعرض الخريطة.")
    data = pd.DataFrame({
        "lat":[31.963158,32.0,31.8,32.1,31.95,31.85],
        "lon":[35.930359,35.95,35.85,35.97,35.9,35.88],
        "pollution":[750,1200,450,900,300,1100]
    })

# Map visualization using pydeck if available; fallback to st.map
def pollution_to_color(val, vmin=0, vmax=1500):
    ratio = float(val - vmin) / float(max(1, vmax - vmin))
    ratio = max(0.0, min(1.0, ratio))
    r = int(255 * ratio)
    g = 0
    b = int(255 * (1 - ratio))
    return [r, g, b]

data['color'] = data['pollution'].apply(lambda x: pollution_to_color(x))
data['radius'] = data['pollution'].apply(lambda x: 200 + (float(x)/1500.0)*2000.0)

try:
    import pydeck as pdk
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=data,
        get_position='[lon, lat]',
        get_fill_color='color',
        get_radius='radius',
        pickable=True,
        auto_highlight=True
    )
    view_state = pdk.ViewState(latitude=float(data['lat'].mean()), longitude=float(data['lon'].mean()), zoom=10, pitch=0)
    deck = pdk.Deck(layers=[layer], initial_view_state=view_state)
    st.pydeck_chart(deck)
except Exception as e:
    st.warning(f"pydeck غير متواجد أو فشل عرضه: {e}\nعرض خريطة بسيطة باستخدام st.map.")
    st.map(data[['lat','lon']])

st.markdown("**مفتاح الألوان**: الأزرق = نظيف، الأحمر = ملوث. حجم الدائرة يعكس مستوى التلوث.")
