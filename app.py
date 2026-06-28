import streamlit as st
import random
import json

# Încărcăm datele din fișierul JSON
try:
    with open("loturi.json", "r", encoding="utf-8") as f:
        date_echipe = json.load(f)
except FileNotFoundError:
    st.error("Fișierul 'loturi.json' nu a fost găsit! Asigură-te că este în același folder cu app.py.")
    st.stop()

st.title("⚽ Predictor Mondial 2026")

col1, col2 = st.columns(2)
with col1:
    e1 = st.selectbox("Echipa 1", list(date_echipe.keys()), key="e1")
    t1 = st.multiselect("Selectează 11 titulari E1", date_echipe[e1], format_func=lambda x: x['nume'], key="t1", max_selections=11)
with col2:
    e2 = st.selectbox("Echipa 2", list(date_echipe.keys()), key="e2")
    t2 = st.multiselect("Selectează 11 titulari E2", date_echipe[e2], format_func=lambda x: x['nume'], key="t2", max_selections=11)

if st.button("Simulează Meciul"):
    if len(t1) < 11 or len(t2) < 11:
        st.warning("Te rog să selectezi exact 11 jucători pentru fiecare echipă!")
    else:
        v1 = sum([j['valoare'] for j in t1])
        v2 = sum([j['valoare'] for j in t2])
        # Algoritm simplificat de scor
        s1 = int(v1 / 50 + random.randint(0, 3))
        s2 = int(v2 / 50 + random.randint(0, 3))
        
        st.subheader(f"Rezultat Final: {e1} {s1} - {s2} {e2}")
        st.balloons()
