import streamlit as st
import google.generativeai as genai

# Sayfa tasarımı
st.set_page_config(page_title="ArduUsta", page_icon="🤖")
st.title("🤖 ArduUsta: Arduino Eğitmeni")

# API Anahtarını Streamlit Secrets üzerinden alıyoruz (Güvenlik için)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# Ajanın Kuralları (Burayı görev kağıdındaki kendi kurallarınızla değiştirebilirsiniz)
sistem_komutu = """Senin adın ArduUsta. Ortaokul öğrencilerine Arduino öğreten bir asistansın.
Öğrenci proje sorduğunda ASLA hazır tam kod verme. Sadece kullanılması gereken komutları 
günlük hayattan örneklerle anlat, kodu öğrencinin birleştirmesini iste."""

model = genai.GenerativeModel(
    model_name="models/gemini-3.5-flash-lite",
    system_instruction=sistem_komutu
)

# Sohbet hafızasını başlatma
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_session = model.start_chat(history=[])

# Sayfa yenilendiğinde eski mesajları ekranda gösterme
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan yeni mesaj alma çubuğu
if prompt := st.chat_input("ArduUsta'ya bir görev ver veya soru sor..."):
    # Kullanıcının mesajını ekrana ekle
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Gemini'den yanıt alma
    with st.chat_message("assistant"):
        response = st.session_state.chat_session.send_message(prompt)
        st.markdown(response.text)
    
    # Yanıtı hafızaya kaydetme
    st.session_state.messages.append({"role": "assistant", "content": response.text})
