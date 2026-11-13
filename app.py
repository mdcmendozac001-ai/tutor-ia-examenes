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
═══════════════════════════════════════════════════════════════
MATERIAL 1: INTELIGENCIA ARTIFICIAL (Iberdrola)
═══════════════════════════════════════════════════════════════

DEFINICIÓN: La IA es la combinación de algoritmos planteados con el propósito de crear máquinas que presenten las mismas capacidades que el ser humano. Opera mediante el procesamiento de grandes conjuntos de datos, a partir de los cuales identifica patrones subyacentes que le permiten tomar decisiones autónomas o producir resultados específicos. A diferencia de los sistemas tradicionales que ejecutan instrucciones predeterminadas, la IA optimiza su rendimiento de forma continua conforme asimila mayor volumen de información y ejemplos, en un proceso análogo al aprendizaje humano basado en la práctica y la experiencia acumulada.

DEFINICIÓN UE (Ley de la IA): «Un sistema basado en una máquina que está diseñado para funcionar con distintos niveles de autonomía y que puede mostrar capacidad de adaptación tras el despliegue, y que, para objetivos explícitos o implícitos, infiere de la información de entrada que recibe la manera de generar resultados de salida, como predicciones, contenidos, recomendaciones o decisiones, que pueden influir en entornos físicos o virtuales».

CLASIFICACIÓN DE RUSSELL Y NORVIG (4 tipos):
1. Sistemas que PIENSAN COMO HUMANOS: Automatizan actividades como la toma de decisiones, la resolución de problemas y el aprendizaje. Ejemplo: redes neuronales artificiales.
2. Sistemas que ACTÚAN COMO HUMANOS: Computadoras que realizan tareas de forma similar a como lo hacen las personas. Ejemplo: los robots.
3. Sistemas que PIENSAN RACIONALMENTE: Intentan emular el pensamiento lógico racional de los humanos (percibir, razonar y actuar). Ejemplo: sistemas expertos.
4. Sistemas que ACTÚAN RACIONALMENTE: Imitan de manera racional el comportamiento humano. Ejemplo: agentes inteligentes.

TIPOS POR CAPACIDADES:
- IA ESTRECHA O DÉBIL: La única que existe en la actualidad. Tecnología entrenada para realizar una tarea única o limitada de manera más rápida que una mente humana. Ejemplos: Siri, Alexa, ChatGPT, Sora, DALL·E, chatbots.
- IA GENERAL: Teórica. Sería capaz de resolver problemas sin programación previa específica y aprender con nuevos contextos en tiempo real.
- SÚPER IA: Teórica. Capaz de pensar, razonar, emitir juicios y sentir emociones, tener deseos, creencias y necesidades propias.

TIPOS POR FUNCIONALIDAD:
- IA REACTIVA: No guarda memoria, solo reacciona ante el estímulo actual. No se puede entrenar.
- IA DE MEMORIA LIMITADA: Almacena información durante un periodo corto. Es la más habitual actualmente (IA generativas, asistentes virtuales, coches autónomos).
- IA MENTAL Y EMOCIONAL: Teórica (Teoría de la mente). Entendería pensamientos y emociones humanos.
- IA AUTOCONSCIENTE: Teórica. Comprendería su condición y limitaciones, desarrollaría emociones similares a las humanas.

APLICACIONES PRÁCTICAS:
- SANIDAD: Analizan imágenes médicas, cruzan historiales clínicos, detectan enfermedades con precisión de especialista.
- AGRICULTURA: Examinan composición del suelo y anticipan plagas.
- LOGÍSTICA: Calculan rutas y prevén averías en tiempo real.
- FINANZAS: Identifican fraude y automatizan decisiones.
- EDUCACIÓN: Adaptan itinerarios formativos, detectan dificultades antes del fracaso escolar, identifican plagios.
- SMART CITIES: Eficiencia en transporte, trámites administrativos, mayor seguridad.
- ENERGÍA: Análisis predictivo, trading algorítmico de energía, optimización de la operativa diaria.
- CAMBIO CLIMÁTICO: Vehículos submarinos no tripulados detectan fugas en oleoductos; satélites identifican emisiones; predicción meteorológica de eventos extremos; drones plantan árboles a escala industrial.

TENDENCIAS:
- Especialización: de gran volumen a alta especialización.
- Regulación y exigencias de seguridad.
- IA integrada: en buscadores, CRMs, apps ofimáticas.

IBERDROLA EN IA:
- Asistente Smart Avanzado (desarrollado en Innovation Middle East Center, sobre AWS).
- MeteoFlow (Iberdrola Renovables): predice producción de instalaciones renovables.
- Redes inteligentes con contadores inteligentes y mantenimiento preventivo.

LEYES SOBRE IA:
- UE: Ley de la IA aprobada en 2024, normas basadas en riesgo. Pacto sobre la IA (iniciativa voluntaria).
- EE.UU.: normas federales, estatales y de agencias.
- China: regulaciones centradas en algoritmos y IA generativa, protección de datos, marcaje de deepfakes.

═══════════════════════════════════════════════════════════════
MATERIAL 2: QUÉ ES UN CHATBOT (Iberdrola)
═══════════════════════════════════════════════════════════════

DEFINICIÓN: Un chatbot es un software basado en Inteligencia Artificial que mantiene conversaciones en tiempo real mediante texto o voz. Utiliza herramientas avanzadas de Procesamiento del Lenguaje Natural (PLN), modelos de base multimodales y capacidades de Machine Learning para comprender la intención del usuario, interpretar el contexto y proporcionar respuestas útiles o ejecutar acciones.

DOS FAMILIAS:
- Chatbots (texto): presentes en web, app, redes sociales, WhatsApp.
- Voicebots (voz): asistentes por teléfono, IVR conversacional, altavoces inteligentes.
Ambos comparten tecnologías NLU, orquestación de flujos y modelos predictivos.

TIPOS DE CHATBOTS (6):
1. CHAT CONVERSACIONAL LINEAL: arquitectura tipo árbol de decisiones, poco inteligente, flujo lineal, respuestas automáticas no fluidas.
2. CHAT CONVERSACIONAL NO LINEAL: gracias a ML y PLN interpretan intenciones y contexto, devuelven opciones ajustadas.
3. CHAT CONVERSACIONAL HÍBRIDO: combinación de ambos, si no sabe responder avisa a agente humano e integra su respuesta.
4. CHAT POR VOZ O VOICEBOT: comandos de voz (Alexa, Siri), puede traducir en tiempo real.
5. CHAT DE IA: simulan conversaciones humanas gracias a PLN, modelos de base y aprendizaje automático.
6. CHAT DE IA GENERATIVA: van un paso más allá, crean contenido (imágenes, videos, historias, canciones). Ejemplos: deepfakes, ChatGPT.

IA AGÉNTICA: Sistemas autónomos capaces de comprender su entorno, razonar, planificar y ejecutar acciones, trabajando de forma iterativa hasta alcanzar un objetivo. Integran LLMs como motor de razonamiento. Cada agente tiene objetivo propio, herramientas y fuentes de información asignadas (bases de datos, APIs corporativas), y delegan en otros agentes.

HISTORIA: Eliza (años 60, MIT) fue el primer chatbot, rudimentario, con comparación de patrones. Hoy el 62% de consumidores prefiere interactuar con un chatbot de IA que con un humano. Mercado esperado: 27.300 millones de dólares para 2030.

PASOS PARA IMPLEMENTAR UN CHATBOT:
1. Atender a la experiencia de usuario (nombre, personalidad, lenguaje natural).
2. Analizar al cliente (tipo de negocio, perfil de usuario).
3. Definir el tipo de chatbot (venta, atención, generación de contenido).
4. Actualizar periódicamente (rendimiento, flujos de conversación).
5. Fijar objetivos (relación cliente, nuevas plataformas, nuevas generaciones).

VENTAJAS: disponibilidad 24/7, agilidad, eficiencia, aprendizaje constante, ahorro de costes, personalización, gestión de redes sociales.
INCONVENIENTES: no captan dobles sentidos, sarcasmo o estados de ánimo; rechazo de personas mayores; posibles caídas del sistema.

DIFERENCIA CHATBOT vs ASISTENTE VIRTUAL:
- Chatbot de IA: procesa lenguaje y genera respuestas que imitan el habla humana.
- Asistente virtual: combina PLN + RPA (procesos robóticos automatizados), su objetivo es ACTUAR sobre la petición minimizando intervención humana (envía mapas, vuelos, opciones).

ECOSISTEMA IBERDROLA:
- ESPAÑA: soporte masivo a atención al cliente, cobros, App Clientes, facturación, ventas, Bono Social, chatbot de winback en Portugal, voicebot de Bono Social, verificación de ventas.
- REINO UNIDO (ScottishPower): Bruce Assistant (llamadas y email), bots de autorespuesta, recobro, llamadas salientes. Koiné (ITNow): chatbot interno 24×7 de soporte TI (desbloqueos SAP, reinicios contraseña).
- BRASIL (Neoenergia): bot transaccional en WhatsApp, agente digital de voz para negociación de débitos.

═══════════════════════════════════════════════════════════════
MATERIAL 3: MACHINE LEARNING (Iberdrola)
═══════════════════════════════════════════════════════════════

DEFINICIÓN: El Machine Learning es una disciplina del campo de la Inteligencia Artificial que, a través de algoritmos, dota a los ordenadores de la capacidad de identificar patrones en datos masivos y elaborar predicciones (análisis predictivo). Permite realizar tareas específicas de forma autónoma, sin necesidad de ser programados.

ORIGEN: Término utilizado por primera vez en 1959. Relevancia actual por aumento de capacidad de computación y boom de los datos. Parte fundamental del Big Data.

MARCO DE JEFF HAWKINS (2004, "Sobre la inteligencia"): define inteligencia como la capacidad de predecir el futuro en base a patrones almacenados en la memoria (marco memoria-predicción).

IA RESPONSABLE: gestión adoptada por empresas tecnológicas enfocada en transparencia y rendición de cuentas.

REGULACIÓN EUROPEA (3 categorías de riesgo):
- Riesgo inaceptable
- Alto riesgo (ej: herramienta de escaneo de CV)
- Riesgo limitado/no prohibido (regulación más flexible)

ALGORITMOS (3 categorías):
1. APRENDIZAJE SUPERVISADO: aprendizaje previo basado en sistema de etiquetas asociadas a datos. Ejemplo: detector de spam que etiqueta emails como spam/no spam según patrones aprendidos (remitente, relación texto/imágenes, palabras clave).
2. APRENDIZAJE NO SUPERVISADO: sin conocimiento previo, enfrentan el caos de datos para encontrar patrones. Ejemplo: marketing, extraer patrones de redes sociales para campañas segmentadas.
3. APRENDIZAJE POR REFUERZO: aprende a partir de la propia experiencia, prueba y error con recompensas. Ejemplo: reconocimiento facial, diagnósticos médicos, clasificación de ADN.

BENEFICIOS EMPRESARIALES (6):
1. Predice tendencias (qué productos tendrán demanda, cuándo subir/bajar precios).
2. Impulsa la innovación (búsqueda de nuevas soluciones).
3. Mejora la segmentación del público objetivo.
4. Reduce costes (automatiza tareas, optimiza tiendas online).
5. Mejora la segmentación de los anuncios.
6. Mejora la relación con el cliente (chatbots 24/7 que recogen datos).

APLICACIONES PRÁCTICAS:
- RECOMENDACIONES: Spotify, YouTube, streaming (analizan historial y comparan con usuarios similares).
- VEHÍCULOS INTELIGENTES: ajustan configuración interna (temperatura, música, respaldo), mueven el volante solos.
- REDES SOCIALES: X reduce spam; Facebook detecta fake news y contenidos no permitidos en directos.
- PLN: asistentes traducen instantáneamente, reconocen voz, analizan sentimientos; traducen jerga legal.
- BÚSQUEDAS: optimizan resultados según eficacia medida por clics.
- MEDICINA: MIT detecta cáncer de mama con antelación; neumonía y enfermedades de retina.
- CIBERSEGURIDAD: antivirus y motores de detección de malware potencian escaneado y reconocen anomalías.
- IA AGÉNTICA: asistentes de IA para programación (ej: Claude).
- SMART GRIDS: fortalecen resiliencia frente a tormentas, olas de calor, inundaciones. Tecnología LiDAR construye modelos 3D de líneas de distribución.

SECTOR ENERGÉTICO:
- Redes más eficientes, seguras y sostenibles.
- Anticipar problemas, optimizar recursos.
- Lucha contra cambio climático: adaptación, optimización eléctrica, integración de renovables.
- Objetivo Iberdrola: reducir emisiones de carbono, suministrar electricidad sin nuevas infraestructuras.
- Imágenes satelitales + sensores: identificar áreas prioritarias de electrificación, diseñar microrredes locales.

═══════════════════════════════════════════════════════════════
MATERIAL 4: PROCESAMIENTO DE LENGUAJE NATURAL (Iberdrola)
═══════════════════════════════════════════════════════════════

DEFINICIÓN (IBM): Rama de la informática —más concretamente, de la inteligencia artificial— que se ocupa de dotar a los ordenadores de la capacidad de entender lenguaje hablado y escrito del mismo modo que los seres humanos. Aúna lingüística e inteligencia artificial. Consiste en transformar el lenguaje natural en un lenguaje formal que los ordenadores puedan procesar.

EJEMPLO COTIDIANO: Alexa/Siri entienden "¿qué hora es?" y "¿me puedes decir la hora?". Google Translate detecta matices según contexto.

EVOLUCIÓN HISTÓRICA:
- 1949: IBM patrocina Index Thomisticus (Roberto Busa, inventor de lingüística informática).
- 1950: Alan Turing publica "Máquinas computacionales e inteligencia" (Test de Turing).
- 1954: Experimento Georgetown-IBM: traducción automática de más de 60 frases ruso→inglés.
- 1956: John McCarthy, Marvin Minsky y Claude Shannon acuñan "inteligencia artificial" (Conferencia de Dartmouth).
- Década 1960: algoritmos de reconocimiento de patrones y "vecino más próximo".
- Década 1980: algoritmos de aprendizaje automático, generación de lenguaje natural.
- Década 1990: reconocimiento avanzado del discurso, modelado de temas.
- Década 2000: modelos estadísticos (LDA), surge "deep learning".
- Década 2010: traducción con máquinas neuronales (sin intervención humana), salto IA conversacional.
- Década 2020: aplicación en sectores de negocio + visión artificial (Industria 4.0).

CÓMO FUNCIONA:
- Primeros modelos: SIMBÓLICOS (reglas codificadas manualmente).
- Años 80-90: revolución ESTADÍSTICA (inferencia estadística, patrones).
- Ventajas modelos estadísticos: más fiables con nuevas palabras, detectan errores ortográficos.
- Sistemas actuales: combinación de modelos simbólicos y estadísticos.

TIPOS DE ANÁLISIS (4):
1. MORFOLÓGICO: distingue tipos de palabras (verbos, sustantivos, preposiciones) y variaciones (género, número, tiempo).
2. SINTÁCTICO: separa frases y analiza partes (sujeto, verbo, predicado) para extraer sentido.
3. SEMÁNTICO: analiza significado de palabras, frases y discurso en su conjunto.
4. PRAGMÁTICO: extrae intención según contexto (ironía, ambigüedad, estado de ánimo).

APLICACIONES (7):
1. Asistentes virtuales y chatbots inteligentes (Siri, Alexa, Google Assistant).
2. Clasificación de documentos por temática o estilo.
3. Análisis de sentimiento y opinión (comentarios en redes sociales).
4. Comparación de textos (detección de plagios, control de calidad).
5. Anonimización de documentos (eliminar datos personales).
6. Traducción automática instantánea.
7. Recomendación de contenido (libros, películas, canciones).

HERRAMIENTAS (lenguaje principal: Python):
- NLTK (Natural Language Toolkit): biblioteca Python modular, etiquetado y clasificación.
- MonkeyLearn: plataforma de análisis de textos/sentimientos, clasificación, extracción de palabras clave.
- IBM Watson: servicios de IA en nube, identificación y extracción de categorías, sentimientos, entidades.
- Google Cloud Natural Language: API para análisis de sentimientos, clasificación, extracción de entidades.
- Amazon Comprehend: servicio de PLN en AWS, análisis de sentimientos, modelado de temas, reconocimiento de entidades.
- SpaCy: biblioteca de código abierto, diseñada para grandes volúmenes de datos.
- GenSim: modelado de temas, reconocimiento de similitudes entre textos, navegación entre documentos.

═══════════════════════════════════════════════════════════════
MATERIAL 5: DIAGRAMA CIRCULAR - COMPONENTES DE IA
═══════════════════════════════════════════════════════════════

El diagrama circular muestra la IA como un ecosistema de disciplinas interconectadas organizadas en an concéntrico:

NÚCLEO CENTRAL: MACHINE LEARNING (aprendizaje automático) - el motor que permite aprender de datos.

SEGUNDO ANILLO (disciplinas fundamentales):
- DEEP LEARNING (aprendizaje profundo): redes neuronales con múltiples capas.
- NEURAL NETWORKS (redes neuronales): inspiradas en el cerebro humano.

TERCER ANILLO (aplicaciones del ML/DL):
- NLP/PLN (Procesamiento de Lenguaje Natural): comprensión del lenguaje.
- COMPUTER VISION (visión artificial): análisis de imágenes y vídeo.
- SPEECH RECOGNITION (reconocimiento de voz): conversión voz-texto.
- EXPERT SYSTEMS (sistemas expertos): basados en reglas y conocimiento.

CUARTO ANILLO (integración física):
- ROBOTICS (robótica): sistemas físicos autónomos que integran todos los componentes.

APLICACIONES TRANSVERSALES (entorno del diagrama):
- BIG DATA: procesamiento de grandes volúmenes de datos.
- IOT (Internet de las Cosas): dispositivos conectados que generan datos.
- CLOUD COMPUTING: infraestructura escalable para IA.
- CYBERSECURITY: protección de sistemas y datos.
- AUTOMATION: automatización de procesos.
- SIMULATIONS: modelado y simulación de escenarios.
- VIRTUAL PRODUCTION: producción virtual y cadenas de suministro.
- AUTONOMOUS ROBOTS: robots que operan sin intervención humana.
- AUGMENTED REALITY: realidad aumentada.
- ADDITIVE MANUFACTURING: manufactura aditiva (impresión 3D).
- SYSTEMS INTEGRATION: integración de sistemas complejos.

REGLAS DE RELACIÓN:
- Machine Learning es el núcleo central que alimenta a los demás.
- Deep Learning es un subconjunto de Machine Learning.
- Neural Networks son la base del Deep Learning.
- NLP, Computer Vision y Speech Recognition aplican ML/DL.
- Robotics integra todos los componentes para crear sistemas autónomos.

═══════════════════════════════════════════════════════════════
NOTA: El PDF del Google Drive no pudo ser extraído automáticamente.
El estudiante debe subirlo manualmente como archivo PDF al chatbot.
═══════════════════════════════════════════════════════════════
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

# ============ CONFIGURAR GEMINI ============
def configurar_gemini():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    # ⚠️ IMPORTANTE: "gemini-3.8-flash" NO es un nombre válido oficial.
    # Prueba en este orden hasta que funcione:
    modelos_a_probar = [
        'gemini-2.0-flash',        # El más rápido actualmente
        'gemini-1.5-flash',        # Rápido y estable
        'gemini-1.5-flash-8b',     # Versión ligera
        'gemini-pro',              # Estable pero más lento
    ]
    for modelo in modelos_a_probar:
        try:
            return genai.GenerativeModel(modelo)
        except Exception:
            continue
    return None

# ============ CHAT CON TIMEOUT ============
def chat_con_ia_con_timeout(mensajes, contexto, modo_examen=False, timeout=20):
    model = configurar_gemini()
    if not model:
        return "❌ Error: No hay API Key configurada o modelo no disponible."
    
    if modo_examen:
        system_prompt = f"""Eres un tutor experto que prepara exámenes sobre el siguiente material de Iberdrola sobre IA, Chatbots, ML y PLN.

MATERIAL COMPLETO:
{contexto}

INSTRUCCIONES:
- Genera UNA pregunta de examen basada en el material (NO inventes fuera de él)
- Espera la respuesta del estudiante
- Evalúa con: 📊 Puntuación (0-10), ✅ Respuesta correcta, 💬 Feedback, 🎯 Consejo
- Después pregunta si quiere otra o tiene dudas."""
    else:
        system_prompt = f"""Eres un tutor experto en IA, ML, PLN y Chatbots según el material de Iberdrola.

MATERIAL COMPLETO:
{contexto}

INSTRUCCIONES:
- Responde SOLO basándote en el material proporcionado
- Sé claro, didáctico y usa ejemplos del texto
- Responde en español
- Si no está en el material, dilo"""
    
    # Solo últimos 3 mensajes (clave para velocidad)
    chat_history = []
    for msg in mensajes[-3:]:
        if msg["role"] != "system":
            role = "user" if msg["role"] == "user" else "model"
            chat_history.append({"role": role, "parts": [msg["content"]]})
    
    try:
        chat = model.start_chat(history=chat_history)
        ultimo = mensajes[-1]['content']
        full_prompt = f"{system_prompt}\n\nPregunta: {ultimo}" if len(mensajes) <= 2 else ultimo
        
        # TIMEOUT para evitar cuelgues
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(chat.send_message, full_prompt)
            try:
                response = future.result(timeout=timeout)
                return response.text
            except concurrent.futures.TimeoutError:
                return "⏱️ La IA tardó demasiado. Intenta con una pregunta más corta o espera unos segundos."
    except Exception as e:
        return f"Error: {str(e)}"

# ============ INICIALIZAR ============
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {"role": "assistant", "content": "¡Hola! 👋 Soy tu tutor de IA basado en el material de Iberdrola sobre IA, Chatbots, Machine Learning y PLN.\n\n💬 Hazme preguntas sobre cualquier tema\n📝 Escribe **/pregunta** para una pregunta de examen\n🎯 Escribe **/examen** para modo examen continuo\n📂 Sube el PDF del Drive en la barra lateral si quieres que lo incluya\n\n¿Empezamos? 🎓"}
    ]

if "modo_examen" not in st.session_state:
    st.session_state.modo_examen = False

# ============ INTERFAZ ============
def main():
    st.title("🎓 Tutor IA Conversacional - Material Iberdrola")
    
    with st.sidebar:
        st.header("⚙️ Configuración")
        model = configurar_gemini()
        if not model:
            st.error("🔑 No hay API Key de Gemini configurada")
            st.stop()
        st.success(f"✅ Conectado con {model.model_name}")
        st.divider()
        
        st.subheader("📂 Material adicional")
        st.info("⚠️ Sube aquí el PDF del Google Drive que no pude leer automáticamente")
        archivos = st.file_uploader(
            "PDF, DOCX o TXT", 
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
                        contexto_total += f"\n\n═══════════════════════════════════════\nARCHIVO: {archivo.name}\n═══════════════════════════════════════\n{texto}"
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
        st.caption(f"Modo: {'🎯 Examen' if st.session_state.modo_examen else '💬 Chat'}")

    st.divider()
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

    if prompt := st.chat_input("Escribe tu pregunta o /pregunta..."):
        st.session_state.mensajes.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.spinner("🤔 Consultando el material..."):
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
