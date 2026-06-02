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
        
        # --- НОВИЙ БЛОК: Побудова точної часової діаграми ---
        # Перевіряємо, чи є в датасеті стовпець з часом (наприклад, 'timestamp' або 'time')
        time_col = next((c for c in df.columns if 'time' in c.lower() or 'date' in c.lower()), None)
        
        if time_col:
            st.write(f"### Часова діаграма для значення вартості ({col})")
            
            # Групуємо дані за часом та рахуємо кількість записів обраного стовпця (наприклад, scan_type)
            time_counts = df.groupby(time_col)[col].count()
            
            # Налаштування стилю графіка, як на зображенні
            fig, ax = plt.subplots(figsize=(14, 4))
            
            # Малюємо сині стовпчики з тонкими білими межами
            time_counts.plot(kind='bar', color='#0066cc', edgecolor='white', linewidth=0.5, ax=ax, width=0.8)
            
            # Налаштування осей та назви
            ax.set_title("Значення вартості", fontsize=16, loc='left', pad=15)
            ax.set_xlabel("") # Прибираємо назву осі X, бо там і так дати
            ax.set_ylabel("")
            
            # Повертаємо підписи дат вертикально на 90 градусів і робимо їх сірими
            ax.set_xticklabels(time_counts.index, rotation=90, fontsize=8, color='#555555')
            
            # Налаштування сітки та меж (мінімалістичний стиль)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#cccccc')
            ax.spines['bottom'].set_color('#cccccc')
            ax.grid(axis='y', linestyle='-', alpha=0.3)
            
            # Відображаємо графік у Streamlit
            st.pyplot(fig)
        else:
            st.info("ℹ️ Для побудови часової діаграми у таблиці має бути стовпець із часовою міткою (наприклад, timestamp або time).")
        # ----------------------------------------------------
timestamp,ip,level,method,endpoint,status_code,response_time_sec
2026-01-01 00:00:00,192.168.1.206,WARNING,GET,/api/data,200,1.45
2026-01-01 00:05:00,192.168.1.52,INFO,PUT,/api/data,200,0.928
2026-01-01 00:10:00,192.168.1.50,INFO,POST,/api/report,200,0.848
2026-01-01 00:15:00,192.168.1.135,INFO,PUT,/api/login,404,0.769
2026-01-01 00:20:00,192.168.1.219,INFO,PUT,/api/data,500,1.184
2026-01-01 00:25:00,192.168.1.83,INFO,DELETE,/api/report,200,1.241
2026-01-01 00:30:00,192.168.1.53,INFO,DELETE,/api/login,200,0.977
2026-01-01 00:35:00,192.168.1.204,WARNING,PUT,/api/login,404,0.382
2026-01-01 00:40:00,192.168.1.175,INFO,DELETE,/api/report,201,0.805
2026-01-01 00:45:00,192.168.1.62,ERROR,POST,/api/login,200,1.062
2026-01-01 00:50:00,192.168.1.198,INFO,PUT,/api/user,200,0.867
2026-01-01 00:55:00,192.168.1.152,INFO,PUT,/api/login,200,1.46
2026-01-01 01:00:00,192.168.1.46,INFO,POST,/api/report,200,1.344
2026-01-01 01:05:00,192.168.1.198,WARNING,POST,/api/user,403,1.061
2026-01-01 01:10:00,192.168.1.90,INFO,DELETE,/api/data,400,0.695
2026-01-01 01:15:00,192.168.1.197,INFO,POST,/api/user,201,0.461
2026-01-01 01:20:00,192.168.1.206,ERROR,GET,/api/user,404,0.688
2026-01-01 01:25:00,192.168.1.4,INFO,PUT,/api/data,500,0.994
2026-01-01 01:30:00,192.168.1.124,INFO,PUT,/api/report,201,1.127
2026-01-01 01:35:00,192.168.1.173,WARNING,PUT,/api/login,200,1.07
2026-01-01 01:40:00,192.168.1.102,INFO,GET,/api/login,404,1.456
2026-01-01 01:45:00,192.168.1.106,WARNING,PUT,/api/report,200,1.372
2026-01-01 01:50:00,192.168.1.127,WARNING,GET,/api/report,200,0.707
2026-01-01 01:55:00,192.168.1.98,INFO,GET,/api/logout,401,1.033
2026-01-01 02:00:00,192.168.1.157,INFO,GET,/api/login,200,0.469
2026-01-01 02:05:00,192.168.1.245,INFO,GET,/api/data,200,0.894
2026-01-01 02:10:00,192.168.1.70,WARNING,GET,/api/user,200,0.394
2026-01-01 02:15:00,192.168.1.143,INFO,GET,/api/logout,400,0.328
2026-01-01 02:20:00,192.168.1.198,ERROR,DELETE,/api/report,200,0.602
2026-01-01 02:25:00,192.168.1.79,INFO,POST,/api/login,200,0.298
2026-01-01 02:30:00,192.168.1.71,INFO,PUT,/api/data,200,0.337
2026-01-01 02:35:00,192.168.1.25,ERROR,PUT,/api/user,200,0.612
2026-01-01 02:40:00,192.168.1.56,INFO,POST,/api/user,403,1.012
2026-01-01 02:45:00,192.168.1.145,ERROR,DELETE,/api/login,401,1.122
2026-01-01 02:50:00,192.168.1.249,INFO,PUT,/api/login,200,0.103
2026-01-01 02:55:00,192.168.1.221,INFO,GET,/api/user,404,1.366
2026-01-01 03:00:00,192.168.1.12,ERROR,DELETE,/api/login,200,1.199
2026-01-01 03:05:00,192.168.1.151,INFO,DELETE,/api/login,200,0.71
2026-01-01 03:10:00,192.168.1.99,INFO,POST,/api/login,500,0.399
2026-01-01 03:15:00,192.168.1.22,INFO,DELETE,/api/user,200,1.29
2026-01-01 03:20:00,192.168.1.72,INFO,DELETE,/api/logout,400,0.427
2026-01-01 03:25:00,192.168.1.205,INFO,GET,/api/data,200,1.092
2026-01-01 03:30:00,192.168.1.26,INFO,GET,/api/logout,200,1.288
2026-01-01 03:35:00,192.168.1.67,INFO,PUT,/api/logout,401,0.917
2026-01-01 03:40:00,192.168.1.21,INFO,POST,/api/report,403,0.224
2026-01-01 03:45:00,192.168.1.219,WARNING,PUT,/api/login,400,0.806
2026-01-01 03:50:00,192.168.1.103,INFO,POST,/api/login,404,0.588
2026-01-01 03:55:00,192.168.1.198,INFO,GET,/api/logout,201,0.5
2026-01-01 04:00:00,192.168.1.250,ERROR,PUT,/api/user,200,1.378
2026-01-01 04:05:00,192.168.1.30,INFO,DELETE,/api/user,404,0.317
2026-01-01 04:10:00,192.168.1.184,INFO,POST,/api/logout,200,0.261
2026-01-01 04:15:00,192.168.1.11,INFO,POST,/api/user,201,0.468
2026-01-01 04:20:00,192.168.1.182,INFO,POST,/api/logout,403,1.341
2026-01-01 04:25:00,192.168.1.194,WARNING,PUT,/api/login,200,0.11
2026-01-01 04:30:00,192.168.1.177,ERROR,PUT,/api/logout,200,1.426
2026-01-01 04:35:00,192.168.1.28,INFO,GET,/api/report,200,0.438
2026-01-01 04:40:00,192.168.1.11,INFO,POST,/api/user,200,0.496
2026-01-01 04:45:00,192.168.1.94,INFO,GET,/api/user,200,1.459
2026-01-01 04:50:00,192.168.1.33,INFO,DELETE,/api/data,200,1.42
2026-01-01 04:55:00,192.168.1.62,INFO,GET,/api/login,500,0.609
2026-01-01 05:00:00,192.168.1.25,ERROR,POST,/api/user,200,0.639
2026-01-01 05:05:00,192.168.1.182,WARNING,DELETE,/api/data,400,1.28
2026-01-01 05:10:00,192.168.1.17,INFO,GET,/api/logout,200,0.394
2026-01-01 05:15:00,192.168.1.184,WARNING,PUT,/api/user,200,1.023
2026-01-01 05:20:00,192.168.1.180,WARNING,POST,/api/logout,200,0.43
2026-01-01 05:25:00,192.168.1.103,INFO,POST,/api/logout,200,0.937
2026-01-01 05:30:00,192.168.1.214,ERROR,PUT,/api/logout,201,1.375
2026-01-01 05:35:00,192.168.1.83,INFO,DELETE,/api/logout,400,0.796
2026-01-01 05:40:00,192.168.1.252,INFO,PUT,/api/data,500,1.199
2026-01-01 05:45:00,192.168.1.128,INFO,POST,/api/login,200,0.609
2026-01-01 05:50:00,192.168.1.64,INFO,POST,/api/report,403,1.403
2026-01-01 05:55:00,192.168.1.207,WARNING,PUT,/api/report,200,1.04
2026-01-01 06:00:00,192.168.1.237,INFO,GET,/api/data,403,0.332
2026-01-01 06:05:00,192.168.1.44,WARNING,DELETE,/api/report,200,1.077
2026-01-01 06:10:00,192.168.1.15,INFO,GET,/api/user,400,0.128
2026-01-01 06:15:00,192.168.1.63,INFO,POST,/api/report,401,0.515
2026-01-01 06:20:00,192.168.1.158,INFO,DELETE,/api/user,404,0.667
2026-01-01 06:25:00,192.168.1.158,INFO,POST,/api/logout,400,0.477
2026-01-01 06:30:00,192.168.1.214,INFO,GET,/api/data,201,1.179
2026-01-01 06:35:00,192.168.1.110,INFO,PUT,/api/user,200,0.95
2026-01-01 06:40:00,192.168.1.71,INFO,PUT,/api/report,200,1.021
2026-01-01 06:45:00,192.168.1.211,WARNING,DELETE,/api/data,200,1.149
2026-01-01 06:50:00,192.168.1.224,WARNING,GET,/api/report,400,0.349
2026-01-01 06:55:00,192.168.1.86,INFO,DELETE,/api/login,500,0.431
2026-01-01 07:00:00,192.168.1.204,WARNING,DELETE,/api/login,500,0.899
2026-01-01 07:05:00,192.168.1.82,INFO,DELETE,/api/login,400,0.507
2026-01-01 07:10:00,192.168.1.219,ERROR,PUT,/api/logout,500,0.85
2026-01-01 07:15:00,192.168.1.90,INFO,GET,/api/logout,200,1.391
2026-01-01 07:20:00,192.168.1.218,INFO,DELETE,/api/login,201,0.826
2026-01-01 07:25:00,192.168.1.139,INFO,GET,/api/logout,201,0.602
2026-01-01 07:30:00,192.168.1.57,WARNING,POST,/api/data,200,1.014
2026-01-01 07:35:00,192.168.1.115,INFO,DELETE,/api/report,400,0.831
2026-01-01 07:40:00,192.168.1.40,INFO,GET,/api/login,200,0.203
2026-01-01 07:45:00,192.168.1.31,WARNING,GET,/api/user,200,0.292
2026-01-01 07:50:00,192.168.1.95,INFO,POST,/api/user,200,0.882
2026-01-01 07:55:00,192.168.1.196,INFO,PUT,/api/report,500,0.49
2026-01-01 08:00:00,192.168.1.113,INFO,GET,/api/data,403,0.338
2026-01-01 08:05:00,192.168.1.212,INFO,PUT,/api/logout,500,0.506
2026-01-01 08:10:00,192.168.1.242,INFO,DELETE,/api/user,201,1.189
2026-01-01 08:15:00,192.168.1.245,INFO,POST,/api/report,200,1.402
    st.write("## 📌 Рисунок 3.2 — Розподіл портів за типом атаки")
    plot_port_distribution_by_scan_type(df)

else:
    st.info("Upload a CSV file to start")
