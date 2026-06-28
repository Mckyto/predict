import streamlit as st
import json
import random

# --- CONFIGURARE ---
st.set_page_config(page_title="Predictor Mondial 2026", page_icon="⚽")

# --- FUNCȚII ---
@st.cache_data
def incarca_date():
    with open("loturi.json", "r", encoding="utf-8") as f:
        return json.load(f)

def calculeaza_sinergie(jucatori_selectati):
    cluburi = [j['club'] for j in jucatori_selectati]
    bonus = 0
    for club in set(cluburi):
        if cluburi.count(club) >= 2:
            bonus += 0.05
    return bonus

def genereaza_scor(val1, val2):
    diferenta = (val1 - val2) / 100 
    scor1 = int(max(0, 1 + diferenta + random.uniform(-0.5, 1.5)))
    scor2 = int(max(0, 1 - diferenta + random.uniform(-0.5, 1.0)))
    return scor1, scor2

def alege_marcator(selectie):
    nume = [j['nume'] for j in selectie]
    valori = [j['valoare'] for j in selectie]
    return random.choices(nume, weights=valori, k=1)[0]

def genereaza_minut():
    return random.choices([random.randint(1, 45), random.randint(46, 90)], weights=[40, 60], k=1)[0]

# --- INTERFAȚĂ ---
data = incarca_date()
st.title("⚽ Predictor Fotbal - Mondial 2026")

col1, col2 = st.columns(2)

with col1:
    echipa1 = st.selectbox("Echipa 1", list(data.keys()), key="select_echipa1")
    selectie1 = st.multiselect(
        f"Selectează 11 titulari pentru {echipa1}", 
        data[echipa1], 
        format_func=lambda x: x['nume'],
        key="selectie1_jucatori"
    )

with col2:
    echipa2 = st.selectbox("Echipa 2", list(data.keys()), key="select_echipa2")
    selectie2 = st.multiselect(
        f"Selectează 11 titulari pentru {echipa2}", 
        data[echipa2], 
        format_func=lambda x: x['nume'],
        key="selectie2_jucatori"
    )

if st.button("Simulează Meciul"):
    if len(selectie1) != 11 or len(selectie2) != 11:
        st.error("Te rog să selectezi exact 11 jucători pentru fiecare echipă!")
    else:
        # Calcul Valori
        val1 = sum([j['valoare'] for j in selectie1])
        val2 = sum([j['valoare'] for j in selectie2])
        
        # Calcul Sinergie
        bonus1 = val1 * calculeaza_sinergie(selectie1)
        bonus2 = val2 * calculeaza_sinergie(selectie2)
        total1, total2 = val1 + bonus1, val2 + bonus2
        
        # Scor și Marcatori
        scor1, scor2 = genereaza_scor(total1, total2)
        st.subheader(f"Rezultat Final: {echipa1} {scor1} - {scor2} {echipa2}")
        
        goluri = []
        for _ in range(scor1):
            goluri.append({"echipa": echipa1, "marcator": alege_marcator(selectie1), "minut": genereaza_minut()})
        for _ in range(scor2):
            goluri.append({"echipa": echipa2, "marcator": alege_marcator(selectie2), "minut": genereaza_minut()})
        
        st.write("⚽ **Cronologia evenimentelor:**")
        for gol in sorted(goluri, key=lambda x: x['minut']):
            st.write(f"⏱️ Minutul {gol['minut']}: **{gol['marcator']}** ({gol['echipa']})")

        with st.expander("Vezi detaliile tehnice"):
            st.write(f"Valoare ajustată {echipa1}: {total1:.1f} mil. €")
            st.write(f"Valoare ajustată {echipa2}: {total2:.1f} mil. €")
