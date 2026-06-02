import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Log Analyzer", layout="wide")

st.title("📊 Log Analyzer (Streamlit)")

def plot_port_distribution_by_scan_type(df):
    if 'port' not in df.columns or 'scan_type' not in df.columns:
        st.warning("⚠️ Columns 'port' and 'scan_type' not found in dataset")
        return

    grouped = df.groupby(['scan_type', 'port']).size().unstack(fill_value=0)

    fig, ax = plt.subplots()
    grouped.T.plot(kind='bar', ax=ax)
    ax.set_title("Розподіл сканованих portent за типом атаки (Рисунок 3.2)")
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
        
        # --- ОСТАТОЧНИЙ БЛОК ДЛЯ ТОЧНОГО ВІДТВОРЕННЯ ГРАФІКА ---
        time_col = None
        for c in df.columns:
            c_low = str(c).lower().strip()
            if 'timestamp' in c_low or 'time' in c_low or 'познач' in c_low or 'час' in c_low or 'дата' in c_low:
                time_col = c
                break
        
        if time_col is None and len(df.columns) > 0:
            time_col = df.columns[0]

        if time_col:
            # Створюємо чистий заголовок, як на скриншоті
            st.markdown("<h3 style='margin-bottom: -20px;'>Значення вартості</h3>", unsafe_html=True)
            
            # Рахуємо кількість записів для кожної часової мітки
            time_counts = df.groupby(time_col).size()
            
            # Створюємо графік matplotlib з точними пропорціями (широкий та низький)
            fig, ax = plt.subplots(figsize=(16, 3.5))
            
            # Малюємо насичені сині стовпчики з тонкими білими межами (width=0.8 регулює товщину)
            time_counts.plot(kind='bar', color='#0066cc', edgecolor='white', linewidth=0.6, ax=ax, width=0.85)
            
            # Налаштування підписів осей (прибираємо назву знизу, залишаємо лише мітки часу)
            ax.set_xlabel("")
            ax.set_ylabel("")
            
            # Робимо мітки часу вертикальними під кутом 90 градусів (розмір шрифту 8)
            ax.set_xticklabels(time_counts.index, rotation=90, fontsize=8, color='#444444')
            
            # Встановлюємо межі по осі Y від 0 до 1.0 (як на скриншоті)
            ax.set_ylim(0, 1.05)
            ax.set_yticklabels(['0.0', '0.5', '1.0'], fontsize=9, color='#555555')
            ax.set_yticks([0.0, 0.5, 1.0])
            
            # Прибираємо верхню та праву рамки графіка для мінімалістичного вигляду
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#cccccc')
            ax.spines['bottom'].set_color('#cccccc')
            
            # Додаємо легку горизонтальну сітку
            ax.grid(axis='y', linestyle='-', alpha=0.2, color='#888888')
            
            # Вирівнюємо елементи графіку
            plt.tight_layout()
            
            # Виводимо графік у Streamlit
            st.pyplot(fig)
        # ----------------------------------------------------------------------

    st.write("## 📌 Рисунок 3.2 — Розподіл портів за типом атаки")
    plot_port_distribution_by_scan_type(df)

else:
    st.info("Upload a CSV file to start")
