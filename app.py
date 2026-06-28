import streamlit as st
import json

# Încărcare loturi
with open("loturi.json", "r", encoding="utf-8") as f:
    data = json.load(f)

st.title("⚽ Predictor Mondial 2026")

def calculeaza_sinergie(jucatori_selectati):
    cluburi = [j['club'] for j in jucatori_selectati]
    bonus = 0
    # Bonus de 5% pentru fiecare pereche de jucători de la același club
    for club in set(cluburi):
        if cluburi.count(club) >= 2:
            bonus += 0.05
    return bonus

# Interfață
col1, col2 = st.columns(2)
with col1:
    echipa1 = st.selectbox("Echipa 1", list(data.keys()))
    selectie1 = st.multiselect("Selectează 11 jucători (Echipa 1)", data[echipa1], format_func=lambda x: x['nume'])

with col2:
    echipa2 = st.selectbox("Echipa 2", list(data.keys()))
    selectie2 = st.multiselect("Selectează 11 jucători (Echipa 2)", data[echipa2], format_func=lambda x: x['nume'])

if st.button("Simulează Meciul"):
    if len(selectie1) != 11 or len(selectie2) != 11:
        st.error("Atenție: Trebuie să alegi exact 11 jucători pentru fiecare echipă pentru a putea calcula scorul corect.")
    else:
        # Calcul valori
        val1 = sum([j['valoare'] for j in selectie1])
        val2 = sum([j['valoare'] for j in selectie2])
        
        # Calcul bonus
        bonus1 = val1 * calculeaza_sinergie(selectie1)
        bonus2 = val2 * calculeaza_sinergie(selectie2)
        
        # Afișare
        total1 = val1 + bonus1
        total2 = val2 + bonus2
        
        st.subheader("Verdict:")
        if total1 > total2:
            st.success(f"Câștigă {echipa1} cu un scor ajustat de {total1:.1f} mil. €")
        elif total2 > total1:
            st.success(f"Câștigă {echipa2} cu un scor ajustat de {total2:.1f} mil. €")
        else:
            st.info("Egalitate perfectă pe hârtie!")
            
        with st.expander("Vezi detaliile calculului"):
            st.write(f"Sinergie {echipa1}: +{bonus1:.1f} mil. €")
            st.write(f"Sinergie {echipa2}: +{bonus2:.1f} mil. €")
