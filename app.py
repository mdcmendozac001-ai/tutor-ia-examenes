import streamlit as st
import os
import json
import PyPDF2
from docx import Document
from openai import OpenAI

# Configuración de la página
st.set_page_config(
    page_title="Tutor IA - Plan de Estudios Completo", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ BASE DE CONOCIMIENTO PREESTABLECIDA ============
CONOCIMIENTO_BASE = """
[INTELIGENCIA ARTIFICIAL - IBERDROLA]
La IA es la combinación de algoritmos para crear máquinas con capacidades humanas. Procesa grandes conjuntos de datos para identificar patrones y tomar decisiones autónomas.

TIPOS SEGÚN RUSSELL Y NORVIG:
1. Sistemas que piensan como humanos (redes neuronales artificiales)
2. Sistemas que actúan como humanos (robots)
3. Sistemas que piensan racionalmente (sistemas expertos)
4. Sistemas que actúan racionalmente (agentes inteligentes)

POR CAPACIDADES:
- IA estrecha/débil (única existente hoy): Siri, Alexa, ChatGPT, asistentes virtuales
- IA general (teórica): resolvería problemas sin programación previa
- Súper IA (teórica): con emociones, creencias y deseos propios

POR FUNCIONALIDAD:
- IA reactiva: sin memoria, solo reacciona al estímulo actual
- IA de memoria limitada: almacena información temporalmente (chatbots actuales, coches autónomos)
- IA mental y emocional (teórica): entendería pensamientos y emociones
- IA autoconsciente (teórica): comprendería su condición y limitaciones

APLICACIONES PRÁCTICAS:
- Sanidad: análisis de imágenes médicas, detección de enfermedades, diagnóstico temprano de cáncer
- Agricultura: examen de composición del suelo, anticipación de plagas
- Logística: cálculo de rutas, predicción de averías
- Finanzas: identificación de fraude, automatización de decisiones
- Educación: adaptación de itinerarios formativos, detección de dificultades, identificación de plagios
- Smart Cities: eficiencia en transporte, trámites administrativos, seguridad
- Energía: análisis predictivo, trading algorítmico, optimización operativa, gestión de redes inteligentes
- Cambio climático: detección de fugas con drones submarinos, identificación de emisiones con satélites, predicción meteorológica

[CHATBOTS Y VOICEBOTS - IBERDROLA]
Software basado en IA que mantiene conversaciones en tiempo real mediante texto o voz. Utilizan PLN, modelos multimodales y Machine Learning.

TIPOS DE CHATBOTS:
1. Conversacional lineal: árbol de decisiones, poco inteligente, flujo lineal
2. Conversacional no lineal: interpreta intenciones y contexto con ML/PLN
3. Conversacional híbrido: combina ambos, deriva a humano si falla
4. Voicebot: comandos de voz (Alexa, Siri)
5. Chat de IA: simula conversación humana con PLN
6. Chat de IA generativa: crea contenido nuevo (ChatGPT, DALL·E, deepfakes)

IA AGÉNTICA:
Sistemas autónomos que comprenden, razonan, planifican y ejecutan acciones de extremo a extremo. Integran LLMs como motor de razonamiento, pueden tener objetivos propios, acceso a bases de datos y APIs, y delegar en otros agentes.

ECOSISTEMA IBERDROLA:
- España: atención al cliente, cobros, facturación, Bono Social, App Clientes
- Reino Unido (ScottishPower): Bruce Assistant, Koiné (soporte TI interno)
- Brasil (Neoenergia): bot transaccional en WhatsApp, agente digital de voz
- Portugal: chatbot de winback

IMPLEMENTACIÓN:
1. Atender experiencia de usuario (nombre, personalidad, lenguaje natural)
2. Analizar al cliente (tipo de negocio, perfil de usuario)
3. Definir tipo de chatbot (ventas, atención, generación de contenido)
4. Actualizar periódicamente (rendimiento, flujos de conversación)
5. Fijar objetivos (relación cliente, ventas, conexión generaciones)

VENTAJAS: disponibilidad 24/7, agilidad, aprendizaje constante, ahorro costes, personalización, gestión redes sociales
INCONVENIENTES: no captan sarcasmo/dobles sentidos, rechazo de algunos usuarios, posibles caídas del sistema

[MACHINE LEARNING - IBERDROLA]
Disciplina de la IA que dota a los ordenadores de capacidad de identificar patrones en datos masivos y elaborar predicciones sin programación explícita.

ALGORITMOS:
1. Aprendizaje supervisado: aprende de datos etiquetados (detector de spam, clasificación)
2. Aprendizaje no supervisado: encuentra patrones en datos sin etiquetar (segmentación marketing, clustering)
3. Aprendizaje por refuerzo: aprende por prueba y error con recompensas (reconocimiento facial, diagnósticos médicos, clasificación ADN)

BENEFICIOS EMPRESARIALES:
- Predice tendencias de compra y demanda
- Impulsa la innovación mediante análisis de datos masivos
- Mejora segmentación de público objetivo
- Reduce costes automatizando tareas
- Mejora segmentación de anuncios
- Mejora relación con cliente (chatbots 24/7)

APLICACIONES PRÁCTICAS:
- Recomendaciones: Spotify, YouTube, plataformas streaming (analizan historial y comparan con usuarios similares)
- Vehículos inteligentes: ajustan configuración interna, conducción autónoma
- Redes sociales: detección de spam (X), fake news y contenidos no permitidos (Facebook)
- PLN: traducción instantánea, reconocimiento de voz, análisis de sentimientos
- Búsquedas: optimización de resultados según eficacia (clics)
- Medicina: detección temprana cáncer de mama (MIT), neumonía, enfermedades de retina
- Ciberseguridad: escaneo, detección de malware, reconocimiento de anomalías
- Smart Grids: análisis LiDAR para mantenimiento de redes, modelos 3D de líneas de distribución

SECTOR ENERGÉTICO:
- Fortalece resiliencia de redes eléctricas frente a eventos extremos
- Analiza datos históricos y patrones de consumo
- Optimiza sistemas eléctricos y eficiencia energética
- Facilita integración de energías renovables
- Identifica áreas prioritarias para electrificación
- Diseña microrredes adaptadas a necesidades locales

[PROCESAMIENTO DE LENGUAJE NATURAL (PLN) - IBERDROLA]
Rama de la IA que dota a los ordenadores de capacidad de entender lenguaje hablado y escrito como humanos. Combina lingüística e informática.

EVOLUCIÓN HISTÓRICA:
- 1949: IBM patrocina Index Thomisticus (lingüística informática)
- 1950: Alan Turing propone Test de Turing
- 1954: Experimento Georgetown-IBM (traducción ruso-inglés)
- 1956: Se acuña término "inteligencia artificial"
- 1960s: Algoritmos de reconocimiento de patrones y "vecino más próximo"
- 1980s: Aprendizaje automático y generación de lenguaje natural
- 1990s: Reconocimiento avanzado del discurso y modelado de temas
- 2000s: Modelos estadísticos avanzados (LDA), surge "deep learning"
- 2010s: Traducción con máquinas neuronales, IA conversacional
- 2020s: Aplicación masiva en sectores de negocio

TIPOS DE ANÁLISIS:
1. Morfológico: distingue tipos de palabras (verbos, sustantivos, preposiciones) y variaciones (género, número, tiempo)
2. Sintáctico: separa frases, analiza partes (sujeto, verbo, predicado) para extraer sentido
3. Semántico: analiza significado de palabras, frases y discurso completo
4. Pragmático: extrae intención según contexto (ironía, ambigüedad, estado de ánimo)

APLICACIONES:
- Asistentes virtuales y chatbots inteligentes (Siri, Alexa, Google Assistant)
- Clasificación de documentos por temática o estilo
- Análisis de sentimiento y opinión en redes sociales
- Comparación de textos (detección de plagios, control de calidad)
- Anonimización de documentos (eliminación de datos personales)
- Traducción automática instantánea
- Recomendación de contenido (libros, películas, canciones)

HERRAMIENTAS:
- NLTK (Natural Language Toolkit): biblioteca Python modular
- MonkeyLearn: plataforma de análisis de textos y sentimientos
- IBM Watson: servicios de IA en nube
- Google Cloud Natural Language: API de análisis
- Amazon Comprehend: servicio de PLN en AWS
- SpaCy: biblioteca Python código abierto para grandes volúmenes
- GenSim: modelado de temas y similitud entre textos

[COMPONENTES DE IA - DIAGRAMA CIRCULAR]
La IA se compone de múltiples disciplinas interconectadas que trabajan de forma integrada:

COMPONENTES PRINCIPALES:
1. Machine Learning (Aprendizaje Automático): núcleo que permite aprender de datos
2. Deep Learning (Aprendizaje Profundo): redes neuronales profundas
3. Neural Networks (Redes Neuronales): inspiradas en el cerebro humano
4. NLP/PLN (Procesamiento de Lenguaje Natural): comprensión del lenguaje
5. Computer Vision (Visión Artificial): análisis de imágenes y vídeo
6. Robotics (Robótica): sistemas físicos autónomos
7. Expert Systems (Sistemas Expertos): basados en reglas y conocimiento
8. Speech Recognition (Reconocimiento de Voz): conversión voz-texto

RELACIONES:
- Machine Learning es el componente central que alimenta a otros
- Deep Learning es un subconjunto de Machine Learning
- Neural Networks son la base del Deep Learning
- NLP, Computer Vision y Speech Recognition aplican ML/DL
- Robotics integra todos los componentes para crear sistemas autónomos

APLICACIONES INTEGRADAS:
- Big Data: procesamiento de grandes volúmenes de datos
- IoT (Internet de las Cosas): dispositivos conectados que generan datos
- Cloud Computing: infraestructura escalable para IA
- Cybersecurity: protección de sistemas y datos
- Automation: automatización de procesos
- Simulations: modelado y simulación de escenarios
- Virtual Production: producción virtual y cadenas de suministro
- Autonomous Robots: robots que operan sin intervención humana
- Augmented Reality: realidad aumentada
- Additive Manufacturing: manufactura aditiva (impresión 3D)
- Systems Integration: integración de sistemas complejos

[EVOLUCIÓN Y TENDENCIAS]
- Especialización: de gran volumen a alta especialización en tareas
- Regulación: Ley de IA de la UE, gestión ética y responsable
- IA integrada: incorporación en buscadores, CRMs, aplicaciones móviles
- IA agéntica: agentes que planifican, deciden y ejecutan tareas complejas
- Modelos multimodales: comprensión de texto, imagen, voz simultáneamente

[REGLAMENTO EUROPEO DE IA]
Primera normativa mundial que establece marco legal común:
- Clasificación por riesgos: inaceptable, alto riesgo, riesgo limitado, mínimo riesgo
- Objetivos: ética, transparencia, seguridad
- Protección de derechos fundamentales
- Cumplimiento legal y gestión de datos
"""

# ============ FUNCIONES DE EXTRACCIÓN ============
def extraer_texto_pdf(archivo):
    try:
        reader = PyPDF2.PdfReader(archivo)
        return "\n".join([pagina.extract_text() or "" for pagina in reader.pages])
    except Exception as e:
        return f"Error leyendo PDF: {e}"

def extraer_texto_docx(archivo):
    try:
        doc = Document(archivo)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        return f"Error leyendo DOCX: {e}"

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

# ============ FUNCIONES DE IA ============
def obtener_cliente():
    api_key = os.environ.get("OPENAI_API_KEY") or st.session_state.get("api_key")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)

def generar_pregunta(contexto, modo, dificultad, tema_especifico=None):
    client = obtener_cliente()
    if not client:
        return None
    
    prompt_tema = f"\n\nENFOCAR ESPECÍFICAMENTE EN: {tema_especifico}" if tema_especifico else ""
    
    prompt = f"""Eres un tutor experto en exámenes sobre Inteligencia Artificial, Machine Learning, PLN y Chatbots. Basándote ÚNICAMENTE en el siguiente MATERIAL DE ESTUDIO, genera UNA pregunta de examen.

MATERIAL DE ESTUDIO:
{contexto[:5000]}

MODO: {modo}
DIFICULTAD: {dificultad}
{prompt_tema}

Responde SOLO en formato JSON válido, sin texto adicional ni markdown:
- Para "opcion_multiple": {{"pregunta": "...", "opciones": ["A) ...", "B) ...", "C) ...", "D) ..."], "respuesta_correcta": "A", "explicacion": "..."}}
- Para "verdadero_falso": {{"pregunta": "...", "respuesta_correcta": true, "explicacion": "..."}}
- Para "desarrollo": {{"pregunta": "...", "puntos_clave": ["...", "..."], "explicacion": "..."}}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Error al generar pregunta: {e}")
        return None

def evaluar_respuesta(pregunta, respuesta_usuario, modo):
    client = obtener_cliente()
    if not client:
        return None

    prompt = f"""Eres un tutor evaluador experto. Evalúa la respuesta del estudiante.

PREGUNTA: {pregunta['pregunta']}
{f"OPCIONES: {pregunta['opciones']}" if modo == "opcion_multiple" else ""}
{f"RESPUESTA CORRECTA ESPERADA: {pregunta['respuesta_correcta']}" if modo != "desarrollo" else f"PUNTOS CLAVE: {pregunta['puntos_clave']}"}

RESPUESTA DEL ESTUDIANTE: {respuesta_usuario}

Responde SOLO en formato JSON válido:
{{"correcta": true/false, "puntuacion": 0-10, "feedback": "explicación detallada y constructiva", "consejo": "sugerencia específica de qué repasar"}}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Error al evaluar: {e}")
        return None

# ============ INTERFAZ DE USUARIO ============
def main():
    st.title("🎓 Tutor de Exámenes: IA, ML, PLN y Chatbots")
    st.markdown("""
    **Prepárate para tu examen** con preguntas generadas por IA basadas en:
    - 📚 Material preestablecido de Iberdrola sobre IA, Chatbots, Machine Learning y PLN
    - 📄 Tus propios archivos (PDF, DOCX, TXT)
    """)

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        api_key = st.text_input("🔑 API Key de OpenAI", type="password", 
                               value=os.environ.get("OPENAI_API_KEY", ""),
                               help="Introduce tu clave de OpenAI para comenzar")
        if api_key:
            st.session_state.api_key = api_key
            os.environ["OPENAI_API_KEY"] = api_key
        
        st.divider()
        
        modo = st.selectbox("📝 Tipo de Pregunta", 
                           ["opcion_multiple", "verdadero_falso", "desarrollo"],
                           format_func=lambda x: {
                               "opcion_multiple": "🔘 Opción Múltiple",
                               "verdadero_falso": "✅❌ Verdadero/Falso",
                               "desarrollo": "📝 Respuesta Abierta"
                           }[x])
        
        dificultad = st.selectbox("📊 Nivel de Dificultad", 
                                 ["fácil", "medio", "difícil"],
                                 format_func=lambda x: {
                                     "fácil": "⭐ Fácil",
                                     "medio": "⭐⭐ Medio",
                                     "difícil": "⭐⭐⭐ Difícil"
                                 }[x])
        
        temas = ["Todos los temas", "Inteligencia Artificial", "Chatbots", 
                "Machine Learning", "Procesamiento de Lenguaje Natural"]
        tema_seleccionado = st.selectbox("🎯 Tema Específico", temas)
        
        usar_base_conocimiento = st.checkbox("📚 Incluir material preestablecido", 
                                           value=True,
                                           help="Incluye la información de Iberdrola sobre IA, chatbots, ML y PLN")
        
        st.divider()
        st.subheader("📈 Tu Progreso")
        if "aciertos" not in st.session_state:
            st.session_state.aciertos = 0
            st.session_state.total = 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total", st.session_state.total)
        with col2:
            st.metric("Aciertos", st.session_state.aciertos)
        
        if st.session_state.total > 0:
            pct = (st.session_state.aciertos / st.session_state.total) * 100
            st.progress(pct / 100)
            st.caption(f"{pct:.1f}% éxito")
        
        if st.button("🔄 Reiniciar Progreso"):
            st.session_state.aciertos = 0
            st.session_state.total = 0
            st.rerun()
        
        st.divider()
        st.info("💡 **Consejo:** Combina el material preestablecido con tus propios apuntes para un estudio completo.")

    # Área principal - Subida de archivos
    st.subheader("📂 Material de Estudio")
    
    st.markdown("**📤 Subir documentos** (PDF, DOCX, TXT)")
    archivos_doc = st.file_uploader(
        "Arrastra archivos aquí o haz clic para seleccionar",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        key="docs",
        label_visibility="collapsed"
    )

    # Procesar archivos
    contexto_total = CONOCIMIENTO_BASE if usar_base_conocimiento else ""
    archivos_procesados = []
    
    if archivos_doc:
        with st.spinner("🔄 Procesando archivos..."):
            for archivo in archivos_doc:
                texto = procesar_archivo(archivo)
                if texto and not texto.startswith("Error"):
                    contexto_total += f"\n\n--- ARCHIVO: {archivo.name} ---\n{texto[:2000]}"
                    archivos_procesados.append(archivo.name)
                elif texto.startswith("Error"):
                    st.warning(f"⚠️ Error en {archivo.name}: {texto}")
        
        if archivos_procesados:
            st.success(f"✅ {len(archivos_procesados)} archivo(s) procesado(s) correctamente")

    # Verificar configuración
    if not obtener_cliente():
        st.warning("🔑 **Introduce tu API Key de OpenAI** en la barra lateral para comenzar.")
        st.info("💡 Puedes obtener tu clave en: https://platform.openai.com/api-keys")
        st.stop()
    
    if not (usar_base_conocimiento or archivos_procesados):
        st.warning("⚠️ Activa 'Incluir material preestablecido' o sube al menos un archivo.")
        st.stop()

    # Botón de generación
    st.divider()
    
    if st.button("🚀 Generar Nueva Pregunta", type="primary", use_container_width=True):
        with st.spinner("🧠 La IA está creando una pregunta personalizada..."):
            pregunta = generar_pregunta(contexto_total, modo, dificultad, 
                                       None if tema_seleccionado == "Todos los temas" else tema_seleccionado)
            if pregunta:
                st.session_state.pregunta_actual = pregunta
                st.session_state.respondida = False
                st.session_state.modo_actual = modo
                st.rerun()
            else:
                st.error("No se pudo generar la pregunta. Verifica tu API Key.")

    # Mostrar pregunta
    if "pregunta_actual" in st.session_state and not st.session_state.get("respondida", False):
        p = st.session_state.pregunta_actual
        modo_actual = st.session_state.modo_actual
        
        st.divider()
        st.subheader("❓ Pregunta de Examen")
        
        badge_dificultad = {"fácil": "🟢", "medio": "🟡", "difícil": "🔴"}
        st.caption(f"Dificultad: {badge_dificultad.get(dificultad, '')} {dificultad.capitalize()}")
        
        st.info(p["pregunta"], icon="💡")
        
        respuesta = None
        
        if modo_actual == "opcion_multiple":
            respuesta = st.radio(
                "Selecciona la respuesta correcta:",
                p["opciones"],
                index=None,
                key="radio_respuesta"
            )
        elif modo_actual == "verdadero_falso":
            respuesta = st.radio(
                "¿Verdadero o Falso?",
                ["Verdadero", "Falso"],
                key="radio_vf"
            )
        elif modo_actual == "desarrollo":
            respuesta = st.text_area(
                "Escribe tu respuesta:",
                height=200,
                placeholder="Desarrolla tu respuesta de forma clara y estructurada...",
                key="texto_desarrollo"
            )
        
        if st.button("✅ Enviar Respuesta", type="primary"):
            if respuesta:
                with st.spinner("📝 Evaluando tu respuesta..."):
                    evaluacion = evaluar_respuesta(p, respuesta, modo_actual)
                    if evaluacion:
                        st.session_state.respondida = True
                        st.session_state.evaluacion = evaluacion
                        st.session_state.respuesta_usuario = respuesta
                        
                        st.session_state.total += 1
                        if evaluacion["correcta"]:
                            st.session_state.aciertos += 1
                        st.rerun()
            else:
                st.warning("Por favor, selecciona o escribe una respuesta.")

    # Mostrar evaluación
    if st.session_state.get("respondida", False):
        ev = st.session_state.evaluacion
        p = st.session_state.pregunta_actual
        modo_actual = st.session_state.modo_actual
        
        st.divider()
        st.subheader("📊 Resultado")
        
        if ev["correcta"]:
            st.balloons()
            st.success(f"🎉 **¡Correcto!** Puntuación: **{ev['puntuacion']}/10**")
        else:
            st.error(f"❌ **No es correcto.** Puntuación: **{ev['puntuacion']}/10**")
        
        with st.expander("🔍 Ver Evaluación Detallada", expanded=True):
            st.markdown("### Tu Respuesta")
            st.info(st.session_state.respuesta_usuario)
            
            st.markdown("### Respuesta Correcta")
            if modo_actual == "opcion_multiple":
                idx = ord(p['respuesta_correcta']) - 65
                st.success(p['opciones'][idx])
            elif modo_actual == "verdadero_falso":
                st.success("✅ Verdadero" if p['respuesta_correcta'] else "❌ Falso")
            elif modo_actual == "desarrollo":
                st.markdown("**Puntos clave que debías mencionar:**")
                for punto in p['puntos_clave']:
                    st.markdown(f"- {punto}")
            
            st.markdown("### 📖 Explicación del Tema")
            st.write(p['explicacion'])
            
            st.markdown("### 💬 Feedback del Tutor")
            st.write(ev['feedback'])
            
            st.markdown("### 🎯 Consejo de Estudio")
            st.warning(ev['consejo'])
        
        if st.button("🔄 Otra Pregunta", use_container_width=True):
            st.session_state.respondida = False
            st.rerun()

    # Footer
    st.divider()
    st.caption("""
    **Tutor de Exámenes con IA** | Basado en material de Iberdrola sobre Inteligencia Artificial, 
    Machine Learning, Procesamiento de Lenguaje Natural y Chatbots.
    """)

if __name__ == "__main__":
    main()