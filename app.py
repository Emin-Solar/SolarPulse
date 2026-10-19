import streamlit as st
import pandas as pd

st.set_page_config(page_title="SolarPulse - Ağıllı Enerji İdarəetməsi", page_icon="☀️", layout="centered")

st.title("☀️ SolarPulse: Günəş Paneli İstehsal və İtki Kalkulyatoru")
st.write("Energetika mühəndisliyi və maliyyə qənaətinin təhlili.")

# Yan panel tənzimləmələri
st.sidebar.header("⚙️ Sistem Parametrləri")
panel_power = st.sidebar.slider("Panellərin Ümumi Gücü (kW)", 1.0, 50.0, 10.0, 0.5)
sun_hours = st.sidebar.slider("Gündəlik Günəşli Saat", 2.0, 10.0, 5.5, 0.5)
dust_loss = st.sidebar.slider("Tozlanma İtkisi (%)", 0.0, 40.0, 15.0, 1.0)
tariff = st.sidebar.number_input("Elektrik Tarifi (AZN / kWh)", value=0.07, step=0.01)

st.sidebar.header("💰 Maliyyə Parametrləri")
total_investment = st.sidebar.number_input("Stansiyanın Quraşdırma Dəyəri (AZN)", value=12000.0, step=500.0)

# Mühəndislik Hesablamaları
max_daily = panel_power * sun_hours
actual_daily = max_daily * (1 - dust_loss / 100)
lost_energy = max_daily - actual_daily

daily_rev = actual_daily * tariff
monthly_rev = daily_rev * 30
monthly_loss = (lost_energy * 30) * tariff

# Geri Ödəmə Müddəti (Amortizasiya) Hesablaması
if monthly_rev > 0:
    payback_months = total_investment / monthly_rev
    payback_years = payback_months / 12
else:
    payback_months = 0
    payback_years = 0

# Əsas Göstəricilər (Kartlar)
st.subheader("📊 Əsas Göstəricilər")

col1, col2, col3 = st.columns(3)
col1.metric("Gündəlik İstehsal", f"{round(actual_daily, 1)} kWh")
col2.metric("Aylıq Gəlir", f"{round(monthly_rev, 1)} AZN")
col3.metric("Tozlanma İtkisi", f"{round(monthly_loss, 1)} AZN", delta=f"-{dust_loss}%", delta_color="inverse")

st.metric("⏳ İnvestisiyanın Geri Ödəmə Müddəti", f"{round(payback_years, 1)} il ({round(payback_months)} ay)")

st.divider()

# Qrafik Əlavə Edirik
st.subheader("📈 Tozlanma İtkilərinin Müqayisəli Qrafiki")
st.write("Fərqli tozlanma faizlərinin aylıq gəlirə təsiri:")

chart_data = pd.DataFrame({
    'Tozlanma Faiz (%)': [0, 10, 20, 30, 40],
    'Aylıq Gəlir (AZN)': [
        (panel_power * sun_hours * 30 * tariff),
        (panel_power * sun_hours * (1 - 0.10) * 30 * tariff),
        (panel_power * sun_hours * (1 - 0.20) * 30 * tariff),
        (panel_power * sun_hours * (1 - 0.30) * 30 * tariff),
        (panel_power * sun_hours * (1 - 0.40) * 30 * tariff)
    ]
})

st.bar_chart(chart_data.set_index('Tozlanma Faiz (%)'))

# Mühəndislik məsləhəti
if dust_loss > 20:
    st.error("🚨 **Diqqət!** Tozlanma faizi çox yüksəkdir. Panellərin yuyulması tövsiyə olunur!")
elif dust_loss > 10:
    st.warning("⚠️ **Xəbərdarlıq:** Orta dərəcədə tozlanma var. Təmizlənməsi faydalı olar.")
else:
    st.success("✅ Sistem normal işləyir, itkilər minimumdadır.")
    