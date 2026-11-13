import streamlit as st
import os
import PyPDF2
from docx import Document
import google.generativeai as genai

st.set_page_config(
    page_title="Tutor IA - Iberdrola", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ BASE DE CONOCIMIENTO COMPLETA ============
CONOCIMIENTO_BASE = """
[INTELIGENCIA ARTIFICIAL - IBERDROLA]
La IA es la combinación de algoritmos para crear máquinas con capacidades humanas. Identifica patrones y toma decisiones autónomas.
- Russell y Norvig: 1) Piensan como humanos (redes neuronales), 2) Actúan como humanos (robots), 3) Piensan racionalmente (sistemas expertos), 4) Actúan racionalmente (agentes inteligentes).
- Por capacidades: IA estrecha/débil (Siri, ChatGPT, única existente), IA general (teórica), Súper IA (teórica).
- Por funcionalidad: Reactiva (sin memoria), Memoria limitada (chatbots actuales), Mental/emocional (teórica), Autoconsciente (teórica).
- Aplicaciones: Sanidad, Agricultura, Logística, Finanzas, Educación, Smart Cities, Energía (MeteoFlow, trading algorítmico), Cambio climático.

[CHATBOTS Y VOICEBOTS - IBERDROLA]
Software de IA para conversaciones en tiempo real (texto o voz) usando PLN y ML.
- Tipos: 1) Lineal (árbol de decisiones), 2) No lineal (interpreta contexto), 3) Híbrido, 4) Voicebot (Alexa, Siri), 5) Chat de IA, 6) IA generativa (crea contenido nuevo).
- IA Agéntica: Sistemas autónomos que comprenden, razonan, planifican y ejecutan acciones de extremo a extremo.
- Ecosistema Iberdrola: España (atención cliente, Bono Social), UK (Bruce Assistant, Koiné), Brasil (Neoenergia WhatsApp), Portugal (winback).
- Ventajas: 24/7, agilidad, ahorro costes. Inconvenientes: no captan sarcasmo, posibles caídas.

[MACHINE LEARNING - IBERDROLA]
Disciplina de la IA que identifica patrones en datos masivos y elabora predicciones sin programación explícita.
- Algoritmos: 1) Supervisado (datos etiquetados, ej: spam), 2) No supervisado (sin etiquetar, ej: segmentación), 3) Por refuerzo (prueba y error con recompensas).
- Beneficios: Predice tendencias, impulsa innovación, reduce costes.
- Aplicaciones: Recomendaciones (Spotify, YouTube), vehículos inteligentes, redes sociales, medicina (detección cáncer), ciberseguridad, Smart Grids (LiDAR).

[PROCESAMIENTO DE LENGUAJE NATURAL (PLN) - IBERDROLA]
Rama de la IA para entender lenguaje hablado y escrito.
- Análisis: 1) Morfológico (tipos de palabras), 2) Sintáctico (estructura frases), 3) Semántico (significado), 4) Pragmático (intención, ironía).
- Aplicaciones: Asistentes virtuales, clasificación de documentos, análisis de sentimiento, traducción automática.
- Herramientas: NLTK, MonkeyLearn, IBM Watson, Google Cloud NLP, Amazon Comprehend, SpaCy, GenSim.

[DIAGRAMA CIRCULAR - COMPONENTES DE IA]
- Núcleo: Machine Learning.
- Segundo anillo: Deep Learning, Neural Networks.
- Tercer anillo: NLP/PLN, Computer Vision, Speech Recognition, Expert Systems.
- Cuarto anillo: Robotics (integra todo).
- Entorno: Big Data, IoT, Cloud Computing, Cybersecurity, Automation, Simulations, Virtual Production, Autonomous Robots, Augmented Reality, Additive Manufacturing, Systems Integration.
"""

# ============ EXTRACCIÓN DE ARCHIVOS ============
def procesar_archivo(archivo):
    try:
        nombre = archivo.name.lower()
        if nombre.endswith(".pdf"):
            reader = PyPDF2.PdfReader(archivo)
            return "\n".join([p.extract_text() or "" for p in reader.pages])
        elif nombre.endswith(".docx"):
            doc = Document(archivo)
            return "\n".join([p.text for p in doc.paragraphs])
        elif nombre.endswith(".txt"):
            return archivo.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return f"Error al leer: {e}"
    return ""

# ============ INTERFAZ PRINCIPAL ============
def main():
    st.title("🎓 Tutor IA Conversacional - Material Iberdrola")
    
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        # 1. API KEY
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            st.error("🔑 Falta la GEMINI_API_KEY en los Secrets de Streamlit")
            st.stop()
        
        # 2. MENÚ DESPLEGABLE DE MODELOS (A PRUEBA DE ERRORES 404)
        st.markdown("**Modelo de IA:**")
        modelo_nombre = st.selectbox(
            "Selecciona uno:",
            options=[
                "gemini-pro",               # 🏆 EL MÁS ESTABLE Y RECOMENDADO
                "gemini-1.5-flash-latest",  # Versión más reciente y rápida
                "gemini-1.5-pro-latest",    # Versión más reciente y potente
                "gemini-1.0-pro"            # Versión clásica, muy compatible
            ],
            index=0 # Empieza con gemini-pro por defecto
        )
        
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(modelo_nombre)
            st.success(f"✅ Modelo `{modelo_nombre}` cargado correctamente")
        except Exception as e:
            st.error(f"❌ Error al cargar: {str(e)}")
            st.stop()
            
        st.divider()
        
        # 3. SUBIDA DE ARCHIVOS
        st.subheader("📂 Material adicional")
        st.info("⚠️ Descarga el PDF del Drive y súbelo aquí manualmente.")
        archivos = st.file_uploader(
            "Subir PDF, DOCX o TXT", 
            type=["pdf", "docx", "txt"], 
            accept_multiple_files=True, 
            key="archivos_chat"
        )
        
        contexto_total = CONOCIMIENTO_BASE
        if archivos:
            with st.spinner("Leyendo archivos..."):
                for archivo in archivos:
                    texto = procesar_archivo(archivo)
                    if texto and not texto.startswith("Error"):
                        contexto_total += f"\n\n--- ARCHIVO: {archivo.name} ---\n{texto[:3000]}"
            st.success(f"✅ {len(archivos)} archivo(s) procesados")
        
        st.divider()
        
        # 4. CONTROLES
        if st.button("🗑️ Reiniciar Chat", use_container_width=True):
            st.session_state.mensajes = [{"role": "assistant", "content": "💬 Chat reiniciado. ¿En qué te ayudo?"}]
            st.rerun()

    # ============ INICIALIZAR CHAT ============
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [
            {"role": "assistant", "content": "¡Hola! 👋 Soy tu tutor de IA basado en el material de Iberdrola.\n\n💬 Hazme preguntas sobre IA, ML, PLN o Chatbots\n📝 Escribe **/pregunta** para una pregunta de examen\n📂 **IMPORTANTE:** Sube el PDF del Google Drive en la barra lateral.\n\n¿Empezamos? 🎓"}
        ]

    # ============ MOSTRAR HISTORIAL ============
    st.divider()
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

    # ============ PROCESAR ENTRADA DEL USUARIO ============
    if prompt := st.chat_input("Escribe tu pregunta o /pregunta..."):
        st.session_state.mensajes.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        system_prompt = f"""Eres un tutor experto. Responde SOLO basándote en este material:
{contexto_total[:4000]}

Si el usuario escribe '/pregunta', genera UNA pregunta de examen con opciones múltiples y espera su respuesta.
Si el usuario responde a una pregunta, evalúa dando: 📊 Puntuación (0-10), ✅ Respuesta correcta, 💬 Feedback."""

        chat_history = []
        for msg in st.session_state.mensajes[-4:]:
            if msg["role"] != "system":
                role = "user" if msg["role"] == "user" else "model"
                chat_history.append({"role": role, "parts": [msg["content"]]})
        
        with st.spinner(f"🤔 Pensando con {modelo_nombre}..."):
            try:
                chat = model.start_chat(history=chat_history)
                if len(st.session_state.mensajes) <= 2:
                    final_prompt = f"{system_prompt}\n\nUsuario: {prompt}"
                else:
                    final_prompt = prompt
                
                response = chat.send_message(final_prompt)
                respuesta = response.text
                
                st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
                with st.chat_message("assistant"):
                    st.markdown(respuesta)
                    
            except Exception as e:
                error_msg = f"❌ **Error de la API:** {str(e)}\n\n💡 *Solución:* Cambia el modelo en el menú desplegable de la barra lateral a otra opción (ej. 'gemini-1.0-pro')."
                st.session_state.mensajes.append({"role": "assistant", "content": error_msg})
                with st.chat_message("assistant"):
                    st.error(error_msg)

if __name__ == "__main__":
    main()
