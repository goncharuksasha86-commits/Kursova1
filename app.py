import streamlit as st
import pandas as pd

st.set_page_config(page_title="Log Analyzer", layout="wide")

st.title("📊 Log Analyzer (Streamlit)")

def plot_port_distribution_by_scan_type(df):
    if 'port' not in df.columns or 'scan_type' not in df.columns:
        st.warning("⚠️ Columns 'port' and 'scan_type' not found in dataset")
        return

    # Імпортуємо pyplot локально, щоб не навантажувати додаток без потреби
    import matplotlib.pyplot as plt
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
        
        # --- БЛОК ІДЕНТИЧНОЇ ЧАСОВОЇ ДІАГРАМИ (ЯК НА СКРИНШОТІ) ---
        time_col = None
        # Автоматичний пошук колонки часу (враховуючи можливі переклади браузера)
        for c in df.columns:
            c_low = str(c).lower().strip()
            if 'timestamp' in c_low or 'time' in c_low or 'познач' in c_low or 'час' in c_low or 'дата' in c_low:
                time_col = c
                break
        
        # Якщо за назвою не знайшли, беремо першу колонку
        if time_col is None and len(df.columns) > 0:
            time_col = df.columns[0]

        if time_col:
            st.write("## Значення вартості")
            
            # Створюємо зведену таблицю, де індексом є час, а значенням — кількість подій (Граф 1)
            # Переіменовуємо колонку в 'Граф 1', щоб підказка при наведенні була як на скриншоті
            chart_data = df.groupby(time_col).size().to_frame(name="Граф 1")
            
            # Будуємо оригінальний інтерактивний графік Streamlit
            st.bar_chart(chart_data, color="#0066cc")
        # -------------------------------------------------------------------------

    st.write("## 📌 Рисунок 3.2 — Розподіл портів за типом атаки")
    plot_port_distribution_by_scan_type(df)

else:
    st.info("Upload a CSV file to start")
