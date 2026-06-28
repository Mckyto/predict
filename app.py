import streamlit as st
import random
import json

with open("loturi.json", "r", encoding="utf-8") as f:
    date_echipe = json.load(f)

st.title("⚽ Predictor Mondial 2026")

col1, col2 = st.columns(2)
with col1:
    e1 = st.selectbox("Echipa 1", list(date_echipe.keys()), key="e1")
    t1 = st.multiselect("Titulari E1", date_echipe[e1], format_func=lambda x: x['nume'], key="t1", max_selections=11)
with col2:
    e2 = st.selectbox("Echipa 2", list(date_echipe.keys()), key="e2")
    t2 = st.multiselect("Titulari E2", date_echipe[e2], format_func=lambda x: x['nume'], key="t2", max_selections=11)

if st.button("Simulează Meciul"):
    if len(t1) < 11 or len(t2) < 11:
        st.warning("Selectează 11 titulari pentru ambele echipe!")
    else:
        v1 = sum([j['valoare'] for j in t1])
        v2 = sum([j['valoare'] for j in t2])
        
        # Logica de scor (divizorul 15 este mai realist pentru valori mici)
        s1 = max(0, int((v1 / 15) + random.randint(-1, 2)))
        s2 = max(0, int((v2 / 15) + random.randint(-1, 2)))
        
        # Afișare rezultat
        st.subheader(f"Rezultat: {e1} {s1} - {s2} {e2}")
        st.write(f"📊 Valori loturi: {e1} ({v1} mil. €) vs {e2} ({v2} mil. €)")
        
        # Generare marcatori
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
