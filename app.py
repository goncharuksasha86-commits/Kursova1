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
    
    # 🔥 КРОК 1: Очищаємо назви ВСІХ стовпців від прихованих пробілів та символів переносу
    df.columns = df.columns.str.strip().str.replace(r'\s+', ' ', regex=True)
    
    st.write("### Data Preview")
    st.dataframe(df)

    if st.checkbox("Show basic stats"):
        st.write(df.describe())

    if st.checkbox("Show columns"):
        st.write(df.columns.tolist())

    # --- СУПЕР-НАДІЙНИЙ БЛОК ШУКАЧА ЧАСУ ---
    time_col = None
    
    # Спочатку шукаємо за ключовими словами
    for c in df.columns:
        c_low = str(c).lower().strip()
        if 'познач' in c_low or 'час' in c_low or 'timestamp' in c_low or 'time' in c_low or 'дата' in c_low:
            time_col = c
            break

    # 🔥 РЕЗЕРВНИЙ ВАРІАНТ: Якщо за текстом не знайшли, беремо НАЙПЕРШУ колонку таблиці
    if time_col is None and len(df.columns) > 0:
        time_col = df.columns[0]

    if time_col:
        st.write("## Часова діаграма активності підозрілих IP-адрес")
        
        # Очищаємо текстові значення дат від слова "рік", щоб повернути стандартний формат
        df[time_col] = df[time_col].astype(str).str.replace('рік', '', case=False).str.strip()
        
        # Групуємо дані строго за цією часовою колонкою
        chart_data = df.groupby(time_col).size().to_frame(name="Граф 1")
        
        # Перетворюємо індекс на текст для коректного відображення осей
        chart_data.index = chart_data.index.astype(str)
        
        # Малюємо синій інтерактивний графік
        st.bar_chart(chart_data, color="#0066cc")
    else:
        st.warning("⚠️ Не вдалося знайти жодного стовпця в таблиці.")
    # ----------------------------------------------------------------------

    # Селектбокс нижче
