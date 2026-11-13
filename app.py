import streamlit as st
import os
import PyPDF2
from docx import Document
import google.generativeai as genai
import concurrent.futures

st.set_page_config(
    page_title="Tutor IA - Iberdrola", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ BASE DE CONOCIMIENTO COMPLETA (Iberdrola + Diagrama) ============
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
        return f"Error: {e}"
    return ""

# ============ CONFIGURAR GEMINI (CORREGIDO SEGÚN TU ERROR) ============
def configurar_gemini():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    
    # La API nos pide explícitamente este modelo. Lo usamos de primero.
    # Si falla, tiene respaldos probados.
    modelos_a_probar = [
        'gemini-3.8-flash',  # EL QUE PIDE EL ERROR DE GOOGLE
        'gemini-2.0-flash',  # Alternativa rápida
        'gemini-1.5-flash',  # El más estable y probado
        'gemini-pro'         # Último recurso
    ]
    
    for modelo in modelos_a_probar:
        try:
            model = genai.GenerativeModel(modelo)
            return model, modelo # Retornamos el modelo y su nombre para mostrarlo
        except Exception:
            continue
            
    return None, None

# ============ CHAT CON TIMEOUT (EVITA QUE SE CUELGUE) ============
def chat_con_ia_con_timeout(mensajes, contexto, modo_examen=False, timeout=20):
    model, modelo_nombre = configurar_gemini()
    if not model:
        return "❌ Error: No hay API Key configurada o ningún modelo está disponible."
    
    if modo_examen:
        system_prompt = f"""Eres un tutor experto que prepara exámenes sobre este material de Iberdrola.
MATERIAL: {contexto}
INSTRUCCIONES: Genera UNA pregunta de examen basada SOLO en el material. Al evaluar da: 📊 Puntuación (0-10), ✅ Respuesta correcta, 💬 Feedback, 🎯 Consejo."""
    else:
        system_prompt = f"""Eres un tutor experto en IA, ML, PLN y Chatbots según el material de Iberdrola.
MATERIAL: {contexto}
INSTRUCCIONES: Responde SOLO basándote en el material. Sé claro, didáctico y responde en español."""
    
    # Solo últimos 3 mensajes para máxima velocidad
    chat_history = []
    for msg in mensajes[-3:]:
        if msg["role"] != "system":
            role = "user" if msg["role"] == "user" else "model"
            chat_history.append({"role": role, "parts": [msg["content"]]})
    
    try:
        chat = model.start_chat(history=chat_history)
        ultimo = mensajes[-1]['content']
        full_prompt = f"{system_prompt}\n\nPregunta: {ultimo}" if len(mensajes) <= 2 else ultimo
        
        # TIMEOUT: Si tarda más de 20 segundos, corta y avisa (evita el "pegado" infinito)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(chat.send_message, full_prompt)
            try:
                response = future.result(timeout=timeout)
                return response.text
            except concurrent.futures.TimeoutError:
                return "⏱️ La IA tardó demasiado en responder. Intenta con una pregunta más corta o espera unos segundos."
            except Exception as e:
                return f"Error de conexión: {str(e)}"
    except Exception as e:
        return f"Error al configurar el chat: {str(e)}"

# ============ INICIALIZAR ============
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {"role": "assistant", "content": "¡Hola! 👋 Soy tu tutor de IA basado en el material de Iberdrola.\n\n💬 Hazme preguntas sobre IA, ML, PLN o Chatbots\n📝 Escribe **/pregunta** para una pregunta de examen\n🎯 Escribe **/examen** para modo examen continuo\n📂 **IMPORTANTE:** Sube el PDF del Google Drive en la barra lateral para que tenga toda la info.\n\n¿Empezamos? 🎓"}
    ]

if "modo_examen" not in st.session_state:
    st.session_state.modo_examen = False

# ============ INTERFAZ ============
def main():
    st.title("🎓 Tutor IA Conversacional - Material Iberdrola")
    
    with st.sidebar:
        st.header("⚙️ Configuración")
        model, modelo_nombre = configurar_gemini()
        if not model:
            st.error("🔑 No hay API Key de Gemini configurada")
            st.stop()
        st.success(f"✅ Conectado con: `{modelo_nombre}`")
        st.divider()
        
        st.subheader("📂 Material adicional")
        st.warning("⚠️ Sube aquí el PDF del Google Drive (el enlace no se pudo leer automáticamente)")
        archivos = st.file_uploader(
            "PDF, DOCX o TXT", 
            type=["pdf", "docx", "txt"], 
            accept_multiple_files=True, 
            key="archivos_chat"
        )
        
        contexto_total = CONOCIMIENTO_BASE
        if archivos:
            with st.spinner("Procesando archivos..."):
                for archivo in archivos:
                    texto = procesar_archivo(archivo)
                    if texto and not texto.startswith("Error"):
                        contexto_total += f"\n\n--- ARCHIVO: {archivo.name} ---\n{texto}"
            st.success(f"✅ {len(archivos)} archivo(s) añadidos al contexto")
        
        st.divider()
        st.subheader("🎮 Controles")
        if st.button("💬 Modo Chat", use_container_width=True):
            st.session_state.modo_examen = False
            st.session_state.mensajes.append({"role": "assistant", "content": "✅ Modo chat normal."})
            st.rerun()
        if st.button("🎯 Modo Examen", use_container_width=True):
            st.session_state.modo_examen = True
            st.session_state.mensajes.append({"role": "assistant", "content": "🎯 Modo examen activado. Escribe 'salir' para volver."})
            st.rerun()
        if st.button("🗑️ Limpiar", use_container_width=True):
            st.session_state.mensajes = [{"role": "assistant", "content": "💬 Conversación reiniciada."}]
            st.session_state.modo_examen = False
            st.rerun()

    st.divider()
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

    if prompt := st.chat_input("Escribe tu pregunta o /pregunta..."):
        st.session_state.mensajes.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.spinner(f"🤔 Consultando el material (modelo: {modelo_nombre})..."):
            if prompt.lower() == "/pregunta":
                respuesta = chat_con_ia_con_timeout(st.session_state.mensajes, contexto_total, modo_examen=True, timeout=20)
            elif prompt.lower() == "/examen":
                st.session_state.modo_examen = True
                respuesta = "🎯 **Modo examen activado.** Escribe 'salir' para volver.\n\n"
                respuesta += chat_con_ia_con_timeout(st.session_state.mensajes, contexto_total, modo_examen=True, timeout=20)
            elif prompt.lower() == "salir" and st.session_state.modo_examen:
                st.session_state.modo_examen = False
                respuesta = "✅ Volviendo al modo chat."
            else:
                respuesta = chat_con_ia_con_timeout(st.session_state.mensajes, contexto_total, modo_examen=st.session_state.modo_examen, timeout=20)
        
        st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
        with st.chat_message("assistant"):
            st.markdown(respuesta)

if __name__ == "__main__":
    main()
