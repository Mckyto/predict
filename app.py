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

st.title("⚽ Predictor Mondial")

col1, col2 = st.columns(2)
with col1:
    e1 = st.selectbox("Echipa 1", list(date_echipe.keys()), key="e1")
    t1 = st.multiselect("Titulari E1", date_echipe[e1], format_func=lambda x: x['nume'], key="t1", max_selections=11)
with col2:
    e2 = st.selectbox("Echipa 2", list(date_echipe.keys()), key="e2")
    t2 = st.multiselect("Titulari E2", date_echipe[e2], format_func=lambda x: x['nume'], key="t2", max_selections=11)

if st.button("Simulează Meciul"):
    if len(t1) < 11 or len(t2) < 11:
        st.warning("Te rog să selectezi 11 jucători pentru fiecare echipă!")
    else:
        # Calcul valori
        v1 = sum([j['valoare'] for j in t1])
        v2 = sum([j['valoare'] for j in t2])
        
        # Logica pentru scor
        forta1 = math.log1p(v1) * 0.8 + random.gauss(0, 0.5)
        forta2 = math.log1p(v2) * 0.8 + random.gauss(0, 0.5)
        
        s1 = min(max(0, int(forta1 + random.randint(-1, 1))), 4)
        s2 = min(max(0, int(forta2 + random.randint(-1, 1))), 4)
        
        # Afișare rezultat și valori loturi
        st.subheader(f"Rezultat Final: {e1} {s1} - {s2} {e2}")
        st.info(f"Valoare totală loturi: {e1} ({v1} mil. €) vs {e2} ({v2} mil. €)")
        
        # Marcatori cu minutul golului
        if s1 > 0 or s2 > 0:
            st.write("---")
            st.subheader("⚽ Marcatori:")
            
            # Generăm minute aleatorii pentru goluri
            minute_goluri = sorted([random.randint(1, 90) for _ in range(s1 + s2)])
            
            for _ in range(s1):
                minut = random.randint(1, 90)
                st.write(f"min. {minut}' - {e1}: **{random.choice(t1)['nume']}**")
            for _ in range(s2):
                minut = random.randint(1, 90)
                st.write(f"min. {minut}' - {e2}: **{random.choice(t2)['nume']}**")
