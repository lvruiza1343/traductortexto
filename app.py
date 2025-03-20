import streamlit as st
import os
import time
import glob
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
from googletrans import Translator
from langdetect import detect

def remove_old_files(n):
    """Elimina archivos de audio viejos."""
    mp3_files = glob.glob("temp/*mp3")
    now = time.time()
    n_days = n * 86400
    for f in mp3_files:
        if os.stat(f).st_mtime < now - n_days:
            os.remove(f)

# Crear carpeta temporal para audios
os.makedirs("temp", exist_ok=True)
remove_old_files(7)

# Configuración de la página
st.set_page_config(page_title="OCR y TTS", page_icon="📝", layout="wide")
st.title("📜 OCR con Traducción y Conversión a Voz 🗣️")
st.write("Extrae texto de imágenes, tradúcelo y escúchalo en voz alta.")

# Cargar imagen
guardar_img = None
img_file_buffer = st.file_uploader("📂 Cargar una imagen", type=["png", "jpg", "jpeg"])
if img_file_buffer:
    img = Image.open(img_file_buffer)
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    st.image(img, caption="📸 Imagen Cargada", use_container_width=True)

    # Extraer texto con OCR
    text = pytesseract.image_to_string(img_cv)
    st.subheader("📄 Texto Extraído:")
    st.text_area("", text, height=150)
    
    # Detección automática de idioma
    try:
        detected_lang = detect(text)
    except:
        detected_lang = "No detectado"
    st.write(f"🌍 **Idioma Detectado:** {detected_lang}")
    
    # Selección de idioma de salida
    translator = Translator()
    idiomas = {"Inglés": "en", "Español": "es", "Francés": "fr", "Alemán": "de", "Japonés": "ja", "Chino": "zh-cn"}
    output_language = st.selectbox("🌐 Traducir a:", list(idiomas.keys()))
    
    # Control de velocidad de voz
    velocidad = st.slider("🎚️ Velocidad de la voz", 0.5, 1.5, 1.0)
    
    # Botón de conversión
    if st.button("🎤 Convertir a Voz"):
        if text.strip():
            translated_text = translator.translate(text, dest=idiomas[output_language]).text
            tts = gTTS(translated_text, lang=idiomas[output_language], slow=False)
            audio_path = f"temp/audio_{time.time()}.mp3"
            tts.save(audio_path)
            
            st.success("✅ ¡Audio generado!")
            st.audio(audio_path, format="audio/mp3")
            
            # Descargar audio
            with open(audio_path, "rb") as f:
                st.download_button("📥 Descargar Audio", f, file_name="voz.mp3", mime="audio/mp3")
        else:
            st.warning("⚠️ No se encontró texto en la imagen. Intenta con otra.")


 
    

