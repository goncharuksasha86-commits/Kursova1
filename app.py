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

    # --- АВТОНОМНИЙ БЛОК ДЛЯ ІНТЕРАКТИВНОЇ ДІАГРАМИ ЧАСУ ---
    time_col = None
    
    # 1. Автоматичний пошук колонки часу (ігноруючи переклад браузера чи регістр)
    for c in df.columns:
        c_low = str(c).lower().strip()
        if 'timestamp' in c_low or 'time' in c_low or 'познач' in c_low or 'час' in c_low or 'дата' in c_low:
            time_col = c
            break
            
    # 2. Якщо за ключовими словами не знайшли, беремо найпершу колонку таблиці
    if time_col is None and len(df.columns) > 0:
        time_col = df.columns[0]

    if time_col:
        st.write("## Часова діаграма активності підозрілих IP-адрес")
        
        # Створюємо таблицю: індексом (віссю X) стає час, значенням — кількість подій (Граф 1)
        # Перетворюємо індекс на тип string, щоб Streamlit малював послідовні мітки часу
        chart_data = df.groupby(time_col).size().to_frame(name="Граф 1")
        chart_data.index = chart_data.index.astype(str)
        
        # Будуємо синій інтерактивний графік
        st.bar_chart(chart_data, color="#0066cc")
    else:
        st.warning("⚠️ Не вдалося знайти стовпець із часовою міткою у файлі.")
    # ----------------------------------------------------------------------

    # Селектбокс залишається нижче для аналізу інших характеристик за вибором
    col = st.selectbox("Select column to analyze", df.columns)

    if col:
        st.write(f"### Розподіл для значення: {col}")
        st.bar_chart(df[col].value_counts())

    st.write("## 📌 Рисунок 3.2 — Розподіл портів за типом атаки")
    plot_port_distribution_by_scan_type(df)

else:
    st.info("Upload a CSV file to start")
