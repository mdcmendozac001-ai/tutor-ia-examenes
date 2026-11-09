import streamlit as st
import os
import json
import PyPDF2
from docx import Document
import google.generativeai as genai

st.set_page_config(
    page_title="Tutor IA Conversacional", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ BASE DE CONOCIMIENTO ============
CONOCIMIENTO_BASE = """
[INTELIGENCIA ARTIFICIAL - IBERDROLA]
La IA es la combinación de algoritmos para crear máquinas con capacidades humanas. Procesa grandes conjuntos de datos para identificar patrones y tomar decisiones autónomas.

TIPOS SEGÚN RUSSELL Y NORVIG:
1. Sistemas que piensan como humanos (redes neuronales artificiales)
2. Sistemas que actúan como humanos (robots)
3. Sistemas que piensan racionalmente (sistemas expertos)
4. Sistemas que actúan racionalmente (agentes inteligentes)

POR CAPACIDADES:
- IA estrecha/débil (única existente hoy): Siri, Alexa, ChatGPT
- IA general (teórica): resolvería problemas sin programación previa
- Súper IA (teórica): con emociones, creencias y deseos propios

POR FUNCIONALIDAD:
- IA reactiva: sin memoria, solo reacciona al estímulo actual
- IA de memoria limitada: almacena información temporalmente
- IA mental y emocional (teórica): entendería pensamientos y emociones
- IA autoconsciente (teórica): comprendería su condición y limitaciones

APLICACIONES: Sanidad, Agricultura, Logística, Finanzas, Educación, Smart Cities, Energía, Cambio climático

[CHATBOTS Y VOICEBOTS - IBERDROLA]
Software basado en IA que mantiene conversaciones en tiempo real mediante texto o voz.

TIPOS:
1. Conversacional lineal: árbol de decisiones, poco inteligente
2. Conversacional no lineal: interpreta intenciones y contexto
3. Conversacional híbrido: combina ambos, deriva a humano si falla
4. Voicebot: comandos de voz (Alexa, Siri)
5. Chat de IA: simula conversación humana
6. Chat de IA generativa: crea contenido nuevo (ChatGPT, DALL·E)

IA AGÉNTICA: Sistemas autónomos que comprenden, razonan, planifican y ejecutan acciones.

ECOSISTEMA IBERDROLA: España (atención cliente, cobros), UK (Bruce Assistant, Koiné), Brasil (Neoenergia WhatsApp), Portugal (winback)

VENTAJAS: 24/7, agilidad, aprendizaje constante, ahorro costes
INCONVENIENTES: no captan sarcasmo, rechazo de usuarios, posibles caídas

[MACHINE LEARNING - IBERDROLA]
Disciplina de la IA que identifica patrones en datos masivos y elabora predicciones sin programación explícita.

ALGORITMOS:
1. Supervisado: aprende de datos etiquetados (detector de spam)
2. No supervisado: encuentra patrones sin etiquetar (segmentación marketing)
3. Por refuerzo: aprende por prueba y error con recompensas

BENEFICIOS: Predice tendencias, impulsa innovación, mejora segmentación, reduce costes

APLICACIONES: Recomendaciones (Spotify, YouTube), vehículos inteligentes, redes sociales, medicina, ciberseguridad, Smart Grids

[PROCESAMIENTO DE LENGUAJE NATURAL (PLN) - IBERDROLA]
Rama de la IA que dota a los ordenadores de capacidad de entender lenguaje hablado y escrito.

TIPOS DE ANÁLISIS:
1. Morfológico: tipos de palabras y variaciones
2. Sintáctico: estructura de frases
3. Semántico: significado de palabras y frases
4. Pragmático: intención según contexto (ironía, ambigüedad)

APLICACIONES: Asistentes virtuales, clasificación de documentos, análisis de sentimiento, traducción automática

HERRAMIENTAS: NLTK, MonkeyLearn, IBM Watson, Google Cloud Natural Language, Amazon Comprehend, SpaCy, GenSim

[COMPONENTES DE IA]
1. Machine Learning: núcleo que permite aprender de datos
2. Deep Learning: redes neuronales profundas
3. Neural Networks: inspiradas en el cerebro humano
4. NLP/PLN: comprensión del lenguaje
5. Computer Vision: análisis de imágenes
6. Robotics: sistemas físicos autónomos
7. Expert Systems: basados en reglas
8. Speech Recognition: conversión voz-texto

[REGLAMENTO EUROPEO DE IA]
- Clasificación por riesgos: inaceptable, alto riesgo, riesgo limitado, mínimo riesgo
- Objetivos: ética, transparencia, seguridad
"""

# ============ FUNCIONES DE EXTRACCIÓN ============
def extraer_texto_pdf(archivo):
    try:
        reader = PyPDF2.PdfReader(archivo)
        return "\n".join([pagina.extract_text() or "" for pagina in reader.pages])
    except Exception as e:
        return f"Error: {e}"

def extraer_texto_docx(archivo):
    try:
        doc = Document(archivo)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        return f"Error: {e}"

def extraer_texto_txt(archivo):
    return archivo.read().decode("utf-8", errors="ignore")

def procesar_archivo(archivo):
    nombre = archivo.name.lower()
    if nombre.endswith(".pdf"):
        return extraer_texto_pdf(archivo)
    elif nombre.endswith(".docx"):
        return extraer_texto_docx(archivo)
    elif nombre.endswith(".txt"):
        return extraer_texto_txt(archivo)
    return ""

# ============ CONFIGURAR GEMINI ============
def configurar_gemini():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-3.8-flash')

# ============ SISTEMA DE CHAT ============
def chat_con_ia(mensajes, contexto, modo_examen=False):
    model = configurar_gemini()
    if not model:
        return "Error: No hay API Key de Gemini configurada."
    
    # Sistema de instrucciones
    if modo_examen:
        system_prompt = f"""Eres un tutor experto que genera preguntas de examen y evalúa respuestas.

MATERIAL DE ESTUDIO:
{contexto[:4000]}

INSTRUCCIONES:
- Genera UNA pregunta de examen basada en el material
- Espera la respuesta del estudiante
- Evalúa la respuesta dando: puntuación (0-10), feedback constructivo, y consejo de estudio
- Formato de respuesta:
  📊 Puntuación: X/10
  ✅ Respuesta correcta: [si aplica]
  💬 Feedback: [explicación]
  🎯 Consejo: [sugerencia]
  
Después de evaluar, pregunta si quiere otra pregunta o tiene dudas sobre el tema."""
    else:
        system_prompt = f"""Eres un tutor experto en Inteligencia Artificial, Machine Learning, PLN y Chatbots.

MATERIAL DE ESTUDIO:
{contexto[:4000]}

INSTRUCCIONES:
- Responde preguntas sobre el material de forma clara y didáctica
- Usa ejemplos prácticos cuando sea posible
- Si te piden generar preguntas de examen, hazlo
- Mantén un tono cercano y motivador
- Responde en español"""
    
    # Construir historial de conversación
    chat_history = []
    for msg in mensajes[-10:]:  # Últimos 10 mensajes
        role = "user" if msg["role"] == "user" else "model"
        chat_history.append({"role": role, "parts": [msg["content"]]})
    
    try:
        # Iniciar chat con historial
        chat = model.start_chat(history=chat_history)
        
        # Enviar mensaje con system prompt
        full_prompt = f"{system_prompt}\n\n---\n\n{mensajes[-1]['content']}" if chat_history else system_prompt
        
        response = chat.send_message(full_prompt)
        return response.text
    except Exception as e:
        return f"Error al generar respuesta: {e}"

# ============ INICIALIZAR SESIÓN ============
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {"role": "assistant", "content": "¡Hola! 👋 Soy tu tutor de IA. Puedo ayudarte de dos formas:\n\n1️⃣ **Hazme preguntas** sobre IA, Machine Learning, PLN o Chatbots\n2️⃣ Escribe **/pregunta** para que te genere una pregunta de examen\n3️⃣ Escribe **/examen** para modo examen continuo\n\n¿Por dónde empezamos? 🎓"}
    ]

if "modo_examen" not in st.session_state:
    st.session_state.modo_examen = False

# ============ INTERFAZ PRINCIPAL ============
def main():
    st.title("🎓 Tutor IA Conversacional")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        model = configurar_gemini()
        if not model:
            st.error("🔑 No hay API Key de Gemini configurada")
            st.stop()
        
        st.success("✅ Conectado con Google Gemini")
        
        st.divider()
        
        # Subida de archivos
        st.subheader("📂 Material adicional")
        st.markdown("Sube PDF, DOCX o TXT para ampliar el conocimiento del tutor")
        archivos = st.file_uploader(
            "Archivos",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True,
            key="archivos_chat"
        )
        
        contexto_total = CONOCIMIENTO_BASE
        if archivos:
            with st.spinner("Procesando..."):
                for archivo in archivos:
                    texto = procesar_archivo(archivo)
                    if texto and not texto.startswith("Error"):
                        contexto_total += f"\n\n--- {archivo.name} ---\n{texto[:2000]}"
            st.success(f"✅ {len(archivos)} archivo(s) cargado(s)")
        
        st.divider()
        
        # Controles de chat
        st.subheader("🎮 Controles")
        
        if st.button("💬 Modo Chat Normal", use_container_width=True):
            st.session_state.modo_examen = False
            st.session_state.mensajes.append({
                "role": "assistant",
                "content": "✅ Cambiado a modo chat normal. Hazme cualquier pregunta sobre el material."
            })
            st.rerun()
        
        if st.button("🎯 Modo Examen Continuo", use_container_width=True):
            st.session_state.modo_examen = True
            st.session_state.mensajes.append({
                "role": "assistant",
                "content": "🎯 Activado modo examen continuo. Te haré preguntas una tras otra. Escribe 'salir' para volver al modo chat."
            })
            st.rerun()
        
        if st.button("🗑️ Limpiar conversación", use_container_width=True):
            st.session_state.mensajes = [
                {"role": "assistant", "content": "💬 Conversación reiniciada. ¿En qué puedo ayudarte?"}
            ]
            st.session_state.modo_examen = False
            st.rerun()
        
        st.divider()
        st.caption(f"Modo actual: {'🎯 Examen' if st.session_state.modo_examen else '💬 Chat'}")

    # Mostrar historial de chat
    st.divider()
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

    # Input del usuario
    if prompt := st.chat_input("Escribe tu pregunta o /pregunta para un examen..."):
        # Mostrar mensaje del usuario
        st.session_state.mensajes.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Procesar comandos especiales
        if prompt.lower() == "/pregunta":
            # Generar una pregunta de examen
            with st.spinner("🧠 Generando pregunta..."):
                respuesta = chat_con_ia(
                    st.session_state.mensajes, 
                    contexto_total, 
                    modo_examen=True
                )
            st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
            with st.chat_message("assistant"):
                st.markdown(respuesta)
        
        elif prompt.lower() == "/examen":
            st.session_state.modo_examen = True
            with st.spinner("Activando modo examen..."):
                respuesta = "🎯 **Modo examen activado.** Te haré preguntas continuamente. Responde y te evaluaré. Escribe 'salir' para volver al chat normal.\n\n"
                respuesta += chat_con_ia(st.session_state.mensajes, contexto_total, modo_examen=True)
            st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
            with st.chat_message("assistant"):
                st.markdown(respuesta)
        
        elif prompt.lower() == "salir" and st.session_state.modo_examen:
            st.session_state.modo_examen = False
            respuesta = "✅ Volviendo al modo chat normal. ¿Tienes alguna duda sobre lo que hemos visto?"
            st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
            with st.chat_message("assistant"):
                st.markdown(respuesta)
        
        else:
            # Respuesta normal del chat
            with st.spinner("🤔 Pensando..."):
                respuesta = chat_con_ia(
                    st.session_state.mensajes, 
                    contexto_total, 
                    modo_examen=st.session_state.modo_examen
                )
            st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
            with st.chat_message("assistant"):
                st.markdown(respuesta)

if __name__ == "__main__":
    main()
