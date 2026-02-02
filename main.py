from agents import trace, Runner
import asyncio
from agentes import *

# for key, value in os.environ.items():
#     print(f"{key}={value}")

"""
Para ver la traza:
https://platform.openai.com/logs?api=traces
"""

mensaje = "Últimos frameworks de Agentes de IA en 2025-2026"

async def ejecutar_busqueda():
    with trace("Búsqueda"):
        resultado = await Runner.run(agente_busqueda, mensaje)
    return resultado

async def ejecutar_planificador():
    with trace("Planificador"):
        resultado = await Runner.run(agente_planificador, mensaje)
    return resultado

async def planificar_busquedas(consulta: str):
    """Usa el agente planificador para planificar qué búsquedas ejecutar para la consulta"""
    print("Planificando búsquedas...")
    #with trace("Planificar"):
    resultado = await Runner.run(agente_planificador, f"Consulta: {consulta}")
    print(f"Se realizaron {len(resultado.final_output.busquedas)} búsquedas")
    return resultado

async def buscar(elemento: ElementoBusquedaWeb):
    """Usa el agente de búsqueda para ejecutar una búsqueda web para cada elemento en el plan de búsqueda"""
    entrada = f"Término de búsqueda: {elemento.consulta}\nRazón para buscar: {elemento.razon}"
    resultado = await Runner.run(agente_busqueda, entrada)
    return resultado

async def realizar_busquedas(plan_busqueda: PlanBusquedaWeb):
    """Llama a buscar() para cada elemento en el plan de búsqueda"""
    print("Buscando...")
    plan = plan_busqueda.final_output
    tareas = [asyncio.create_task(buscar(elemento)) for elemento in plan.busquedas]
    resultados = await asyncio.gather(*tareas)
    print("Búsqueda terminada")
    return resultados

async def escribir_informe(consulta: str, resultados_busqueda: list[str]):
    """Usa el agente escritor para escribir un informe basado en los resultados de búsqueda"""
    print("Construyendo el informe...")
    entrada = f"Consulta original: {consulta}\nResultados de búsqueda resumidos: {resultados_busqueda}"
    resultado = await Runner.run(agente_escritor, entrada)
    print("Informe terminado")
    return resultado

async def enviar_email_informe(informe: DatosInforme):
    """Usa el agente de email para enviar un email con el informe"""
    print("Enviando email...")
    #informe_output = informe.final_output
    entrada = f"""
    Redacta un email con:
    - Asunto claro y profesional
    - HTML bien formateado

    INFORME:
    {informe.final_output.informe_markdown}
    """
    resultado = await Runner.run(agente_email, entrada)
    print("Email enviado")
    return informe.final_output

async def ejecutar_investigacion():
    consulta = "Últimos marcos de Agentes de IA en 2025-2026"

    with trace("Rastreo de investigación"):
        print("Iniciando investigación...")
        plan_busqueda = await planificar_busquedas(consulta)
        resultados_busqueda = await realizar_busquedas(plan_busqueda)
        informe = await escribir_informe(consulta, resultados_busqueda)
        await enviar_email_informe(informe)
        print("Done!")


def main():
    # resultado = asyncio.run(ejecutar_busqueda())
    # print(resultado.final_output)
    # resultado = asyncio.run(ejecutar_planificador())
    # print(resultado.final_output)

    #print(send_email)

    asyncio.run(ejecutar_investigacion())


    #send_email(subject: str, html: str, to: str = "miguel.ossa.abellan@gmail.com")

if __name__ == "__main__":
    main()