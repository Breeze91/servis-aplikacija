import streamlit as st
import pandas as pd
from datetime import datetime

# Učitavanje postojeće liste opreme
@st.cache_data
def load_equipment():
    return pd.read_csv("equipment_list.csv")

def save_entry(data):
    df = pd.DataFrame([data])
    try:
        df_existing = pd.read_csv("submitted_data.csv")
        df = pd.concat([df_existing, df], ignore_index=True)
    except FileNotFoundError:
        pass
    df.to_csv("submitted_data.csv", index=False)

st.set_page_config(page_title="Evidencija Servisa", layout="centered")

st.title("📋 Evidencija rada na opremi")

equipment_list = load_equipment()

with st.form("servis_forma"):
    st.subheader("Unos podataka")
    
    oprema = st.selectbox("Odaberi opremu", equipment_list["Naziv"])
    opis = st.text_area("Opis intervencije")
    barkod = st.text_input("Unesi ili skeniraj barkod")
    datum = st.date_input("Datum", datetime.today())
    korisnik = st.text_input("Ime osobe koja unosi podatke")

    submitted = st.form_submit_button("Spremi")

    if submitted:
        data = {
            "Datum": datum,
            "Oprema": oprema,
            "Opis": opis,
            "Barkod": barkod,
            "Korisnik": korisnik,
            "Vrijeme": datetime.now().strftime("%H:%M:%S")
        }
        save_entry(data)
        st.success("✅ Podaci su uspješno spremljeni!")
