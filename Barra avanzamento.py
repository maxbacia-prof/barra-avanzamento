import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configurazione Pagina
st.set_page_config(page_title="2EL Progress Tracker", layout="centered")

st.title("📊 Stato Avanzamento Progetti")
st.write("Monitoraggio in tempo reale delle competenze acquisite dalla classe 2EL.")

# 1. Connessione a Google Sheets
# Nota: Devi configurare le 'Secrets' su Streamlit Cloud con l'URL del tuo foglio
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Lettura dati (Specificare il nome del foglio se necessario)
    df = conn.read(ttl="1m")  # Aggiorna i dati ogni minuto

    # 2. Calcolo dei Progressi
    # Assumiamo 10 missioni totali per studente come da piano di lavoro
    missioni_per_studente = 10
    totale_possibile_classe = len(df) * missioni_per_studente
    totale_completate_classe = df['Totale'].sum()

    percentuale_globale = totale_completate_classe / totale_possibile_classe
    percentuale_display = int(percentuale_globale * 100)

    # 3. Visualizzazione Barra Gaming
    st.metric("Sfide Completate", f"{int(totale_completate_classe)}", f"{percentuale_display}% del modulo")

    # Colore dinamico della barra
    bar_color = "#ff4b4b"  # Rosso (Inizio)
    if percentuale_globale > 0.4: bar_color = "#ffa500"  # Arancio (Intermedio)
    if percentuale_globale > 0.8: bar_color = "#28a745"  # Verde (Esperti)

    st.markdown(f"""
        <div style="width: 100%; background-color: #ddd; border-radius: 20px;">
            <div style="width: {percentuale_display}%; background-color: {bar_color}; 
            padding: 10px; text-align: center; color: white; border-radius: 20px; font-weight: bold;">
                {percentuale_display}%
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 4. Messaggio Motivazionale basato sui CME
    st.write("---")
    if percentuale_globale < 0.5:
        st.info("🎯 **Fase attuale:** Fondamenti e Componenti Passivi (RCL)[cite: 104, 654].")
    else:
        st.success("⚡ **Fase attuale:** Semiconduttori e Circuiti Attivi (Diodi/BJT)[cite: 270, 829].")

except Exception as e:
    st.error("In attesa di collegamento con il Registro Digitale...")
    st.caption("Assicurati che il file Google Sheets sia accessibile.")