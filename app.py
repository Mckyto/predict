import streamlit as st
import random
import json
import math

# 1. Încărcarea datelor
try:
    with open("loturi.json", "r", encoding="utf-8") as f:
        date_echipe = json.load(f)
except FileNotFoundError:
    st.error("Fișierul 'loturi.json' nu a fost găsit!")
    st.stop()

st.title("⚽ Predictor Mondial 2026")

# 2. Layout selecție
col1, col2 = st.columns(2)
with col1:
    e1 = st.selectbox("Echipa 1", list(date_echipe.keys()), key="e1")
    t1 = st.multiselect("Selectează 11 titulari E1", date_echipe[e1], format_func=lambda x: x['nume'], key="t1", max_selections=11)
with col2:
    e2 = st.selectbox("Echipa 2", list(date_echipe.keys()), key="e2")
    t2 = st.multiselect("Selectează 11 titulari E2", date_echipe[e2], format_func=lambda x: x['nume'], key="t2", max_selections=11)

# 3. Logica de simulare
if st.button("Simulează Meciul"):
    if len(t1) < 11 or len(t2) < 11:
        st.warning("Te rog să selectezi exact 11 jucători pentru fiecare echipă!")
    else:
        # Calcul valori
        v1 = sum([j['valoare'] for j in t1])
        v2 = sum([j['valoare'] for j in t2])
        
        # Scor realist cu divizor mai mare (4.0) pentru a evita scorurile maxime
        # Folosim max(0, ...) ca să nu avem goluri negative
        # Variația este dată de random.randint(-1, 3)
        s1 = min(5, max(0, int(math.sqrt(v1) / 4.0 + random.randint(-1, 3))))
        s2 = min(5, max(0, int(math.sqrt(v2) / 4.0 + random.randint(-1, 3))))
        
        # O mică șansă de a forța un gol dacă scorul este 0-0
        if s1 == 0 and s2 == 0 and random.random() > 0.5:
            if random.random() > 0.5: s1 = 1
            else: s2 = 1
        
        st.subheader(f"Rezultat Final: {e1} {s1} - {s2} {e2}")
        st.write(f"📊 Valori loturi: {e1} ({v1} mil. €) vs {e2} ({v2} mil. €)")
        
        # Marcatori
        st.write("---")
        st.subheader("⚽ Marcatori:")
        
        # Colectăm marcatorii pentru a-i afișa corect
        marcatori_e1 = [random.choice(t1)['nume'] for _ in range(s1)]
        marcatori_e2 = [random.choice(t2)['nume'] for _ in range(s2)]
        
        for nume in marcatori_e1:
            st.write(f"{e1}: **{nume}**")
        for nume in marcatori_e2:
            st.write(f"{e2}: **{nume}**")

        if s1 == s2:
            st.info("Rezultat egal! Se merge la lovituri de departajare...")
        
        st.balloons()
