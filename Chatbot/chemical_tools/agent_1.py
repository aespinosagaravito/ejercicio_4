from google import genai
from dotenv import load_dotenv
from langchain.llms.base import LLM
from langchain.agents import initialize_agent, Tool, AgentOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.schema.agent import AgentFinish, AgentAction
import os, json
from tools import collect_product_info

# Cargar variables de entorno desde el archivo .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")


def get_llm_gemini(message: str) -> str:
    client = genai.Client(api_key=API_KEY)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=message,
    )
    return response.text.strip()


class GeminiLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "gemini"

    def _call(self, prompt: str, stop=None) -> str:
        return get_llm_gemini(prompt)


class CustomOutputParser(AgentOutputParser):
    def parse(self, text: str) -> AgentFinish:
        try:
            data = json.loads(text)
            return AgentFinish(return_values={"output": data["output"]}, log=text)
        except:
            return AgentFinish(return_values={"output": text}, log=text)

    @property
    def _type(self) -> str:
        return "custom"


def verificar_palindromo(palabra: str) -> str:
    # Limpiar la entrada: quitar espacios y convertir a minúsculas
    texto = palabra.strip().lower().replace(" ", "")
    # Comparar con su reverso
    if texto == texto[::-1]:
        return f"'{palabra}' es un palíndromo"
    return f"'{palabra}' no es palíndromo"


def llenar_diccionario(_input: str = "") -> str:
    """
    Esta herramienta solicita al usuario los datos necesarios para llenar el diccionario de contexto.

    Ejemplo de uso:
    Input: "llenar diccionario"
    Output: Se solicitarán datos como "Código", "Producto", "Peso dosificación", etc., y al final se mostrará el diccionario completado.
    """
    context = {}
    print("Iniciando proceso de llenado del diccionario de contexto.")
    print("Por favor, responde a las siguientes preguntas:")
    context["codigo"] = input("Código: ")
    context["producto"] = input("Producto: ")
    context["peso_dosificacion"] = input("Peso dosificación: ")
    context["nombre_generico"] = input("Nombre genérico: ")
    context["color"] = input("Color: ")
    context["lote_estandar"] = input("Lote estándar: ")
    context["forma_farmaceutica"] = input("Forma farmacéutica: ")
    context["unidad_medida_del_producto"] = input("Unidad de medida del producto: ")
    context["molde"] = input("Molde: ")

    materiales = []
    try:
        cantidad = int(input("Cantidad de materiales: "))
    except:
        cantidad = 0
    for i in range(cantidad):
        print(f"\nMaterial {i+1}:")
        material = {}
        material["codigo_sap"] = input("  Código SAP: ")
        material["descripcion"] = input("  Descripción: ")
        material["funcion"] = input("  Función: ")
        material["cantidad"] = input("  Cantidad: ")
        material["exceso"] = input("  Exceso: ")
        materiales.append(material)
    context["materiales"] = materiales

    diccionario_formateado = json.dumps(context, indent=4, ensure_ascii=False)
    print("\nDiccionario completado:")
    print(diccionario_formateado)
    return diccionario_formateado


# Herramienta para verificar palíndromos
product_tool = Tool(
    name="formula cuali_cuanti ",
    func=collect_product_info,
    description="""
    Usa esta herramienta para crear una formula cualicuantica.
    Ejemplos de uso:
    - input: "llenar diccionario" 
    - output: Se solicitara los datos necesarios para llenar el diccionario de product_dict, medinate preguntas interactivas al usuario.
    -codigo
    -producto
    -peso_dosificacion
    -color
    -lote_estandar
    -forma_farmaceutica
    -unidad_medida_del_producto
    -molde
   
    Y preguntar '¿cuantos materiales hay?' a cada material hay que solicitar la siguiente información:
    -codigo_sap
    -descripcion
    -funcion
    -cantidad
    -exceso
 
    y al finalizar mostrará el diccionario completado.
    Ejemplo:
    "codigo": "600551234",
        "producto": "citicolina",
        "peso_dosificacion": "500mg",
        "nombre_generico": "citicolina",
        "color": "rojo",
        "lote_estandar": "1234578",
        "forma_farmaceutica": "cápsula",
        "unidad_medida_del_producto": "mg/cap",
        "molde": "oval",
        "materiales": [
            {{
            "codigo_sap": "0001152432",
            "descripcion": "glicerina",
            "funcion": "vehiculo",
            "cantidad": "400mg",
            "exceso": "0",
        }},
         {{
             "codigo_sap": "0001233909",
            "descripcion": "aceite de soya",
            "funcion": "vehiculo",
            "cantidad": "300mg",
            "exceso": "0",
        }},
         {{
             "codigo_sap": "000133489",
            "descripcion": "lecitina",
            "funcion": "emulsificante",
            "cantidad": "4mg",
            "exceso": "0",
        }}
        ]
    """,
)

analytical_chemistry_tool = Tool(
    name="quimica analitica", ",
    func=collect_product_info,
    description="""
    Usa esta herramienta para crear una formula cualicuantica.
    Ejemplos de uso:
    - input: "llenar diccionario" 
    - output: Se solicitara los datos necesarios para llenar el diccionario de product_dict, medinate preguntas interactivas al usuario.
    -codigo
    -producto
    -peso_dosificacion
    -color
    -lote_estandar
    -forma_farmaceutica
    -unidad_medida_del_producto
    -molde
   
    Y preguntar '¿cuantos materiales hay?' a cada material hay que solicitar la siguiente información:
    -codigo_sap
    -descripcion
    -funcion
    -cantidad
    -exceso
 
    y al finalizar mostrará el diccionario completado.
    Ejemplo:
    "codigo": "600551234",
        "producto": "citicolina",
        "peso_dosificacion": "500mg",
        "nombre_generico": "citicolina",
        "color": "rojo",
        "lote_estandar": "1234578",
        "forma_farmaceutica": "cápsula",
        "unidad_medida_del_producto": "mg/cap",
        "molde": "oval",
        "materiales": [
            {{
            "codigo_sap": "0001152432",
            "descripcion": "glicerina",
            "funcion": "vehiculo",
            "cantidad": "400mg",
            "exceso": "0",
        }},
        {{
             "codigo_sap": "0001152432",
            "descripcion": "glicerina",
            "funcion": "vehiculo",
            "cantidad": "400mg",
            "exceso": "0",
        }},
         {{
             "codigo_sap": "0001152432",
            "descripcion": "glicerina",
            "funcion": "vehiculo",
            "cantidad": "400mg",
            "exceso": "0",
        }},
         {{
             "codigo_sap": "000133489",
            "descripcion": "lecitina",
            "funcion": "emulsificante",
            "cantidad": "4mg",
            "exceso": "0",
        }}
        ]
    """,
)
gemini_llm = GeminiLLM()
memory = ConversationBufferMemory(memory_key="chat_history")

agent = initialize_agent(
    tools=[product_tool],
    llm=gemini_llm,
    agent="conversational-react-description",
    verbose=False,
    memory=memory,
    agent_kwargs={"output_parser": CustomOutputParser()},
)

print("Hola, soy un chatbot 🤖. ¿En qué puedo ayudarte hoy?")
while True:
    user_input = input("Tú: ")
    if user_input.lower() in ["salir", "exit", "quit"]:
        print("¡Hasta luego!")
        break
    response = agent.invoke({"input": user_input})
    bot_response = response.get("output", "").split("AI: ")[-1]
    print("Bot:", bot_response)
