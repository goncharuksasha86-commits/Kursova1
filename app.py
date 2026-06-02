import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

st.set_page_config(page_title="Log Analyzer", layout="wide")

st.title("📊 Log Analyzer (Streamlit)")

def plot_port_distribution_by_scan_type(df):
    if 'port' not in df.columns or 'scan_type' not in df.columns:
        st.info("ℹ️ Для побудови 'Рисунку 3.2' необхідні стовпці 'port' та 'scan_type'.")
        return

    grouped = df.groupby(['scan_type', 'port']).size().unstack(fill_value=0)

    fig, ax = plt.subplots()
    grouped.T.plot(kind='bar', ax=ax)
    ax.set_title("Розподіл сканованих портів за типом атаки (Рисунок 3.2)")
    ax.set_xlabel("Port")
    ax.set_ylabel("Count")

    st.pyplot(fig)

uploaded = st.file_uploader("Upload log file (CSV)", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
    st.write("### Data Preview")
    st.dataframe(df)

    if st.checkbox("Show basic stats"):
        st.write(df.describe())

    if st.checkbox("Show columns"):
        st.write(df.columns.tolist())

    # --- ОНОВЛЕНИЙ БЛОК ДЛЯ ГРАФІКА ЧАСУ ЧЕРЕЗ ALTAIR ---
    time_col = None
    # Автоматично шукаємо стовпець часу
    for c in df.columns:
        c_low = str(c).lower().strip()
        if 'timestamp' in c_low or 'time' in c_low or 'познач' in c_low or 'час' in c_low or 'дата' in c_low:
            time_col = c
            break

    if time_col is None and len(df.columns) > 0:
        time_col = df.columns[0]

    if time_col:
        st.write("## Часова діаграма активності підозрілих IP-адрес")
        
        # Групуємо дані за часом та рахуємо кількість подій
        chart_data = df.groupby(time_col).size().reset_index(name="Граф 1")
        # Примусово робимо час текстовим форматом для красивих підписів
        chart_data[time_col] = chart_data[time_col].astype(str)
        
        # Будуємо графік за допомогою Altair для точного відображення підписів дат
        chart = alt.Chart(chart_data).mark_bar(color="#0066cc").encode(
            x=alt.X(f"{time_col}:N", title="", axis=alt.Axis(labelAngle=-90, labelFontSize=10)),
            y=alt.Y("Граф 1:Q", title=""),
            tooltip=[alt.Tooltip(f"{time_col}:N", title="Часова мітка"), alt.Tooltip("Граф 1:Q", title="Граф 1")]
        ).properties(
            width='container',
            height=400
        )
        
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("⚠️ Не вдалося знайти стовпець часу у файлі.")
    # ----------------------------------------------------------------------

    # Селектбокс для аналізу інших колонок
    col = st.selectbox("Select column to analyze", df.columns)
    if col:
        st.write(f"### Розподіл для значення: {col}")
        st.bar_chart(df[col].value_counts())

    st.write("## 📌 Рисунок 3.2 — Розподіл портів за типом атаки")
    plot_port_distribution_by_scan_type(df)

else:
    st.info("Upload a CSV file to start")
