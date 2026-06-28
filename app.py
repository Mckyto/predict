import streamlit as st
import random
import json
import math

# Încărcare date
try:
    with open("loturi.json", "r", encoding="utf-8") as f:
        date_echipe = json.load(f)
except FileNotFoundError:
    st.error("Fișierul 'loturi.json' lipsește!")
    st.stop()

st.title("⚽ Predictor Mondial - Mod Realist")

col1, col2 = st.columns(2)
with col1:
    e1 = st.selectbox("Echipa 1", list(date_echipe.keys()), key="e1")
    t1 = st.multiselect("Titulari E1", date_echipe[e1], format_func=lambda x: x['nume'], key="t1", max_selections=11)
with col2:
    e2 = st.selectbox("Echipa 2", list(date_echipe.keys()), key="e2")
    t2 = st.multiselect("Titulari E2", date_echipe[e2], format_func=lambda x: x['nume'], key="t2", max_selections=11)

if st.button("Simulează Meciul"):
    if len(t1) < 11 or len(t2) < 11:
        st.warning("Selectează 11 jucători!")
    else:
        # Calculăm forța: folosim logaritm pentru a nu avea scoruri astronomice
        # Valoarea echipei contează, dar forma de moment (random) poate schimba meciul
        v1 = sum([j['valoare'] for j in t1])
        v2 = sum([j['valoare'] for j in t2])
        
        # Algoritm mai echilibrat:
        # 1. Diferența de valoare dă un mic avantaj (nu totul)
        # 2. 'random.gauss' simulează distribuția normală (scoruri probabile: 0, 1, 2)
        forta1 = math.log1p(v1) * 0.8 + random.gauss(0, 0.5)
        forta2 = math.log1p(v2) * 0.8 + random.gauss(0, 0.5)
        
        # Calculăm golurile
        s1 = max(0, int(forta1 + random.randint(-1, 1)))
        s2 = max(0, int(forta2 + random.randint(-1, 1)))
        
        # Limităm scorul pentru a evita scorurile de hochei
        s1 = min(s1, 4)
        s2 = min(s2, 4)
        
        st.subheader(f"Rezultat Final: {e1} {s1} - {s2} {e2}")
        
        # Marcatori (opțional)
        if s1 > 0 or s2 > 0:
            st.write("---")
            st.subheader("⚽ Marcatori:")
            for _ in range(s1): st.write(f"{e1}: {random.choice(t1)['nume']}")
            for _ in range(s2): st.write(f"{e2}: {random.choice(t2)['nume']}")
