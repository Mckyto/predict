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
        
        # Scor realist (folosim sqrt pentru a echilibra diferențele mari de valoare)
        # Plafonăm scorul la maxim 5 goluri
        s1 = min(5, int(math.sqrt(v1) / 2 + random.randint(0, 2)))
        s2 = min(5, int(math.sqrt(v2) / 2 + random.randint(0, 2)))
        
        # O mică șansă de a evita 0-0 dacă ambele sunt slabe
        if s1 == 0 and s2 == 0 and random.random() > 0.6:
            s1 = 1
        
        st.subheader(f"Rezultat Final: {e1} {s1} - {s2} {e2}")
        st.write(f"📊 Valori loturi: {e1} ({v1} mil. €) vs {e2} ({v2} mil. €)")
        
        # Marcatori
        st.write("---")
        st.subheader("⚽ Marcatori:")
        
        for _ in range(s1):
            marcator = random.choice(t1)
            st.write(f"{e1}: **{marcator['nume']}** ({marcator['club']})")
            
        for _ in range(s2):
            marcator = random.choice(t2)
            st.write(f"{e2}: **{marcator['nume']}** ({marcator['club']})")

        if s1 == s2:
            st.info("Rezultat egal! Se merge la lovituri de departajare...")
        
        st.balloons()
