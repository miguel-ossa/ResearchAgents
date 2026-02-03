import asyncio
from actions import *

# for key, value in os.environ.items():
#     print(f"{key}={value}")

"""
Para ver la traza:
https://platform.openai.com/logs?api=traces
"""


def main():
    resultado = asyncio.run(ejecutar_busqueda())
    print(resultado.final_output)
    # resultado = asyncio.run(ejecutar_planificador())
    # print(resultado.final_output)

    #print(send_email)

    #asyncio.run(ejecutar_investigacion())

if __name__ == "__main__":
    main()