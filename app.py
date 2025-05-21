import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime

st.title("📋 Evidencija rada na opremi")

equipment_list = pd.read_csv("equipment_list.csv")

# Stanje za kontrolu prikaza kamere
if "scan_mode" not in st.session_state:
    st.session_state.scan_mode = False

def start_scan():
    st.session_state.scan_mode = True

def stop_scan():
    st.session_state.scan_mode = False

with st.form("servis_forma"):
    oprema = st.selectbox("Odaberi opremu", equipment_list["Naziv"])
    opis = st.text_area("Opis intervencije")
    barkod = st.text_input("Barkod - upiši ili skeniraj", key="barkod_input")

    col1, col2 = st.columns(2)
    with col1:
        scan_button = st.form_submit_button("Pokreni kameru za skeniranje", on_click=start_scan)
    with col2:
        save_button = st.form_submit_button("Spremi podatke")

    datum = st.date_input("Datum", datetime.today())
    korisnik = st.text_input("Ime osobe koja unosi podatke")

    if save_button:
        data = {
            "Datum": datum.strftime("%Y-%m-%d"),
            "Oprema": oprema,
            "Opis": opis,
            "Barkod": st.session_state.barkod_input,
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

if st.session_state.scan_mode:
    st.write("🎥 Kamera je uključena. Skeniraj barkod i zatvori kameru kad završiš.")
    barcode_html = """
    <div>
      <video id="video" width="300" height="200" style="border: 1px solid gray"></video>
      <p id="result">Skeniraj barkod...</p>
      <button onclick="stopScan()">Zatvori kameru</button>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/quagga/0.12.1/quagga.min.js"></script>
    <script>
      const resultEl = document.getElementById('result');

      function stopScan() {
          Quagga.stop();
          window.parent.postMessage({action: "stop_scan"}, "*");
      }

      Quagga.init({
          inputStream: {
              type : "LiveStream",
              target: document.querySelector('#video'),
              constraints: {
                  facingMode: "environment"
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
          alert("Barkod skeniran: " + code + "\\nMolimo kopirajte ga i zalijepite u polje 'Barkod'.");
          Quagga.stop();
      });
    </script>
    """
    components.html(barcode_html, height=350)

# Primamo poruke iz JS da možemo zaustaviti skeniranje (radi na custom komponentama, ovdje je placeholder)
# Streamlit standardno ne može primiti JS poruke, ovo možeš ignorirati ili proširiti s React komponentom

