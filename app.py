import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Log Analyzer", layout="wide")

st.title("📊 Log Analyzer (Streamlit)")

# --- ФУНКЦІЯ 1: Розподіл портів ---
def plot_port_distribution_by_scan_type(df):
    if 'port' not in df.columns or 'scan_type' not in df.columns:
        st.warning("⚠️ Columns 'port' and 'scan_type' not found in dataset")
        return

    grouped = df.groupby(['scan_type', 'port']).size().unstack(fill_value=0)

    fig, ax = plt.subplots(figsize=(10, 5))
    grouped.T.plot(kind='bar', ax=ax)
    ax.set_title("Розподіл сканованих портів за типом атаки (Рисунок 3.2)")
    ax.set_xlabel("Port")
    ax.set_ylabel("Count")
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

# --- ФУНКЦІЯ 2: Часова діаграма активності IP (НОВА) ---
def plot_ip_activity_over_time(df):
    time_col = 'timestamp'  
    ip_col = 'source_ip'    
    
    if time_col not in df.columns or ip_col not in df.columns:
        st.warning(f"⚠️ Для часової діаграми потрібні колонки '{time_col}' та '{ip_col}'")
        return

    df_time = df.copy()
    
    df_time[time_col] = pd.to_datetime(df_time[time_col])
    df_time['time_bucket'] = df_time[time_col].dt.round('H') 
    
    timeline = df_time.groupby(['time_bucket', ip_col]).size().unstack(fill_value=0)
    
    fig, ax = plt.subplots(figsize=(12, 5))
    timeline.plot(kind='line', ax=ax, marker='o')
    
    ax.set_title("Часова діаграма активності підозрілих IP-адрес (Рисунок 3.3)")
    ax.set_xlabel("Час фіксації")
    ax.set_ylabel("Кількість запитів (пакетів)")
    ax.grid(True, linestyle='--')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    st.pyplot(fig)
    plt.close(fig)

# --- ОСНОВНА ЛОГІКА ДОДАТКА ---
uploaded = st.file_uploader("
