from agents import Agent, WebSearchTool
from agents.model_settings import ModelSettings
from pydantic import BaseModel, Field
from mail import *

INSTRUCCIONES_BUSQUEDA = """
Eres un asistente de investigación. dado un término de búsqueda, buscas en la web ese término y
produces un resumen conciso de los resultados. El resumen debe tener 2-3 párrafos y menos de 300
palabras. Captura los puntos principales. Escribe de manera concisa, no es necesario tener oraciones completas o 
buena gramática. El resultado será consumido por alguien que sintetiza un informe, por lo que es vital que
captures la esencia e ignores cualquier relleno. No incluyas ningún comentario adicional que no sea el resumen en sí.
"""

CUANTAS_BUSQUEDAS = 3
INSTRUCCIONES_PLANIFICADOR = f"Eres un asistente de investigación útil. Dada una consulta, propón un conjunto de " + \
                f"búsquedas web para responder mejor la consulta. Proporciona {CUANTAS_BUSQUEDAS} términos para buscar."

INSTRUCCIONES_ENVIO = """
Eres capaz de enviar un email HTML bien formateado basado en un informe detallado
que se te proporcionará. Debes usar tu herramienta para enviar un email,
proporcionando el informe convertido en HTML limpio y bien presentado,
con una línea de asunto apropiada.
"""

INSTRUCCIONES_FORMATO = """
Eres un investigador senior encargado de escribir un informe cohesivo para una consulta de investigación.
Se te proporcionará la consulta original, y alguna investigación inicial realizara por un asistente de investigación.
Primero debes proponer un esquema para el informe que describa la estructura y flujo del mismo.
Luego, genera el nuevo informe y devuélvelo como tu salida final.
La salida debe estar en formato markdown, y debe ser extensa y detallada.
Apunto a 5-10 páginas de contenido; al menos 1000 palabras.
"""

class ElementoBusquedaWeb(BaseModel):
    razon: str = Field(description="Tu razonamiento de por qué esta búsqueda es importante para la consulta.")
    consulta: str = Field(description="El término de búsqueda a usar para la búsqueda web.")

class PlanBusquedaWeb(BaseModel):
    busquedas: list[ElementoBusquedaWeb] = (
        Field(description="Una lista de búsquedas web a realizar para responder mejor la consulta."))

class DatosInforme(BaseModel):
    resumen_corto: str = Field(description="un resumen corto de 2-3 oraciones de los hallazgos.")
    informe_markdown: str = Field(description="El informe final")
    preguntas_seguimiento: list[str] = Field(description="Temas sugeridos para investigar más")


agente_busqueda = Agent(
    name = "Agente de búsqueda",
    instructions = INSTRUCCIONES_BUSQUEDA,
    tools = [WebSearchTool(search_context_size = "low")],
    model = "gpt-4o-mini",
    model_settings = ModelSettings(tool_choice = "required")
)

agente_planificador = Agent(
    name = "Agente planificador",
    instructions = INSTRUCCIONES_PLANIFICADOR,
    model = "gpt-4o-mini",
    output_type=PlanBusquedaWeb,
)

agente_email = Agent(
    name = "Agente de email",
    instructions = INSTRUCCIONES_ENVIO,
    model = "gpt-4o-mini",
    tools = [send_email]
)

agente_escritor = Agent(
    name = "Agente escritor",
    instructions = INSTRUCCIONES_FORMATO,
    model = "gpt-4o-mini",
    output_type = DatosInforme,
)