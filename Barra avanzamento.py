import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configurazione Pagina
st.set_page_config(page_title="2EL Progress Tracker", layout="centered")

st.title("📊 Stato Avanzamento Progetti")
st.write("Monitoraggio in tempo reale delle competenze acquisite dalla classe 2EL.")

# 1. Connessione a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

if st.button('🔄 Aggiorna Progressi'):
    st.cache_data.clear()
    st.rerun()

try:
    # Lettura dati
    df = conn.read(ttl="1m")

    # 2. Calcolo dei Progressi basato sul tuo foglio
    # Usiamo le colonne 'Sfide Totali' e 'Sfide Fatte' che vedo nello screenshot
    totale_possibile_classe = df['Sfide Totali'].sum()
    totale_completate_classe = df['Sfide Fatte'].sum()

    if totale_possibile_classe > 0:
        percentuale_globale = totale_completate_classe / totale_possibile_classe
        percentuale_display = int(percentuale_globale * 100)

        # 3. Visualizzazione Metriche
        col1, col2 = st.columns(2)
        col1.metric("Sfide Completate", int(totale_completate_classe))
        col2.metric("Progresso Classe", f"{percentuale_display}%")

        # Colore dinamico della barra
        bar_color = "#ff4b4b"  # Rosso
        if percentuale_globale > 0.4: bar_color = "#ffa500"  # Arancio
        if percentuale_globale > 0.8: bar_color = "#28a745"  # Verde

        # Barra di avanzamento personalizzata
        st.markdown(f"""
            <div style="width: 100%; background-color: #ddd; border-radius: 20px; margin: 10px 0;">
                <div style="width: {percentuale_display}%; background-family: Arial; background-color: {bar_color}; 
                padding: 10px; text-align: center; color: white; border-radius: 20px; font-weight: bold;">
                    {percentuale_display}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 4. Nota didattica basata sul piano di lavoro [cite: 22, 101]
        st.write("---")
        if percentuale_globale < 0.5:
            st.info("🎯 **Fase attuale:** Fondamenti e Componenti Passivi (RCL)[cite: 101, 104].")
        else:
            st.success("⚡ **Fase attuale:** Semiconduttori e Circuiti Attivi (Diodi/BJT)[cite: 289, 291].")
    else:
        st.warning("Aggiungi i dati degli studenti nel foglio per vedere il progresso.")

except Exception as e:
    st.error("Errore: Assicurati che i nomi delle colonne nel foglio siano 'Sfide Totali' e 'Sfide Fatte'.")
    st.caption(f"Dettaglio tecnico: {e}")