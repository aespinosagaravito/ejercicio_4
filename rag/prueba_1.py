import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import InMemoryVectorStore


def test_asistente_quimico():
    """Función que crea y prueba un asistente de química analítica"""

    class AsistenteQuimico:
        def __init__(self):
            """Inicializa el asistente con configuraciones necesarias"""
            self.pdf_path = Path("input/quimica_analitica.pdf")
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            self.almacen_vectorial = InMemoryVectorStore(embedding=self.embeddings)
            self.inicializado = False

            try:
                load_dotenv()
                api_key = os.getenv("GEMINI_API_KEY")
                if not api_key:
                    raise ValueError("API Key no encontrada en .env")

                genai.configure(api_key=api_key)
                self.modelo_gemini = genai.GenerativeModel("gemini-1.5-flash")
                self._inicializar_sistema()

            except Exception as e:
                print(f"⚠️ Error de configuración: {str(e)}")
                sys.exit(1)

        def _inicializar_sistema(self):
            """Inicializa el sistema con validaciones mejoradas"""
            try:
                if not self.pdf_path.exists():
                    error_msg = [
                        "❌ ¡Archivo PDF no encontrado!",
                        f"🔎 Ruta esperada: {self.pdf_path.absolute()}",
                        "📌 Solución:",
                        "  1. Crea la carpeta 'input'",
                        "  2. Coloca 'quimica_analitica.pdf' dentro",
                        "  3. Verifica permisos de lectura",
                    ]
                    raise FileNotFoundError("\n".join(error_msg))

                loader = PyPDFLoader(str(self.pdf_path))
                documentos = loader.load()

                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000, chunk_overlap=200, add_start_index=True
                )
                splits = text_splitter.split_documents(documentos)

                self.almacen_vectorial.add_documents(splits)
                self.inicializado = True
                print("✅ Sistema inicializado correctamente")
                print(f"📄 PDF procesado: {self.pdf_path.name}")
                print(f"🔢 Fragmentos generados: {len(splits)}")

            except Exception as e:
                print(f"❌ Error al procesar PDF: {str(e)}")
                sys.exit(1)

        def consultar(self, pregunta: str) -> str:
            """Genera respuestas con manejo de errores integrado"""
            if not self.inicializado:
                return "⚠️ Sistema no inicializado"

            try:
                documentos = self.almacen_vectorial.similarity_search(pregunta, k=5)
                contexto = "\n\n".join(
                    f"📖 Página {d.metadata['page']+1}:\n{d.page_content}"
                    for d in documentos
                )

                respuesta = self.modelo_gemini.generate_content(
                    f"Contexto:\n{contexto}\n\nPregunta: {pregunta}\nRespuesta técnica en español:"
                )
                return respuesta.text.strip()

            except Exception as e:
                return f"❌ Error generando respuesta: {str(e)}"

    # 🔹 Crear instancia del asistente
    asistente = AsistenteQuimico()

    # 🔹 Probar consulta
    pregunta = "¿Cuáles son los métodos más utilizados en química analítica?"
    respuesta = asistente.consultar(pregunta)

    print("\n💬 Pregunta:", pregunta)
    print("🤖 Respuesta:", respuesta)


# 🔍 Ejecutar la función de prueba
test_asistente_quimico()
