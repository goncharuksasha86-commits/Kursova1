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
        
        # --- БЛОК ПОБУДОВИ ЧАСОВОЇ ДІАГРАМИ ---
        if 'timestamp' in df.columns:
            st.write(f"### Часова діаграма для значення вартості ({col})")
            
            time_counts = df.groupby('timestamp')[col].count()
            
            fig, ax = plt.subplots(figsize=(15, 4))
            time_counts.plot(kind='bar', color='#0066cc', edgecolor='white', linewidth=0.5, ax=ax, width=0.8)
            
            ax.set_title("Значення вартості", fontsize=16, loc='left', pad=15)
            ax.set_xlabel("") 
            ax.set_ylabel("")
            ax.set_xticklabels(time_counts.index, rotation=90, fontsize=8, color='#555555')
            
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#cccccc')
            ax.spines['bottom'].set_color('#cccccc')
            ax.grid(axis='y', linestyle='-', alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("⚠️ Стовпець 'timestamp' не знайдено в завантаженому файлі.")
        # ----------------------------------------------------

    st.write("## 📌 Рисунок 3.2 — Розподіл портів за типом атаки")
    plot_port_distribution_by_scan_type(df)

else:
    st.info("Upload a CSV file to start")
