import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

    col = st.selectbox("Select column to analyze", df.columns)

    if col:
        st.write("### Value counts")
        st.bar_chart(df[col].value_counts())
        
        # --- ПРАВИЛЬНИЙ ІНТЕРАКТИВНИЙ БЛОК ГРАФІКА ЧАСУ ---
        time_col = None
        
        # Шукаємо стовпець часу (враховуючи переклади та регістр)
        for c in df.columns:
            c_low = str(c).lower().strip()
            if 'timestamp' in c_low or 'time' in c_low or 'познач' in c_low or 'час' in c_low or 'дата' in c_low:
                time_col = c
                break
        
        # Якщо за назвою не знайшли, беремо найпершу колонку таблиці
        if time_col is None and len(df.columns) > 0:
            time_col = df.columns[0]
        
        if time_col:
            st.write("## Часова діаграма активності підозрілих IP-адрес")
            
            # Рахуємо кількість подій строго для КОЖНОЇ мітки часу (на осі X буде час!)
            chart_data = df.groupby(time_col).size().to_frame(name="Граф 1")
            
            # Малюємо рідну інтерактивну діаграму Streamlit
            st.bar_chart(chart_data, color="#0066cc")
        else:
            st.warning("⚠️ Не вдалося визначити стовпець часу в таблиці.")
        # ----------------------------------------------------

    st.write("## 📌 Рисунок 3.2 — Розподіл портів за типом атаки")
    plot_port_distribution_by_scan_type(df)

else:
    st.info("Upload a CSV file to start")
