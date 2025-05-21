import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime

# Barkod skener komponenta
def barcode_scanner():
    # HTML + JS za QuaggaJS barkod skener
    barcode_html = """
    <div>
      <video id="video" width="300" height="200" style="border: 1px solid gray"></video>
      <p id="result">Skeniraj barkod...</p>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/quagga/0.12.1/quagga.min.js"></script>
    <script>
      const resultEl = document.getElementById('result');
      Quagga.init({
          inputStream: {
              type : "LiveStream",
              target: document.querySelector('#video'),
              constraints: {
                  facingMode: "environment" // stražnja kamera na mobitelu
              }
          },
          decoder: {
              readers: ["code_128_reader","ean_reader","ean_8_reader","code_39_reader","code_39_vin_reader","codabar_reader","upc_reader","upc_e_reader"]
          }
      }, function(err) {
          if (err) {
              console.log(err);
              return;
          }
          Quagga.start();
      });

      Quagga.onDetected(function(data) {
          var code = data.codeResult.code;
          resultEl.innerText = "Barkod: " + code;
          // Pošalji barkod u Streamlit pomoću custom event
          window.parent.postMessage({barcode: code}, "*");
          Quagga.stop();
      });
    </script>
    """
    components.html(barcode_html, height=250)

st.title("📋 Evidencija rada na opremi")

# Oprema lista
equipment_list = pd.read_csv("equipment_list.csv")

# Pojednostavljena forma
with st.form("servis_forma"):
    oprema = st.selectbox("Odaberi opremu", equipment_list["Naziv"])
    opis = st.text_area("Opis intervencije")
    
    # Barkod input i skeniranje
    barkod = st.text_input("Barkod")
    if st.button("Skeniraj barkod"):
        barcode_scanner()

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
        try:
            df_existing = pd.read_csv("submitted_data.csv")
            df_existing = df_existing.append(data, ignore_index=True)
        except FileNotFoundError:
            df_existing = pd.DataFrame([data])
        df_existing.to_csv("submitted_data.csv", index=False)
        st.success("✅ Podaci su spremljeni!")

