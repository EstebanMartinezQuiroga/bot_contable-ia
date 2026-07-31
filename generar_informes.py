import os
from dotenv import load_dotenv
from google import genai
from docx import Document

# Cargar la API Key desde .env
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def guardar_word(texto, nombre="informe_generado.docx"):
    documento = Document()
    documento.add_heading("Informe Ejecutivo", level=1)
    documento.add_paragraph(texto)
    documento.save(nombre)


def procesar_audio(ruta_audio):
    print("Subiendo audio...")

    # Subir el archivo de audio
    audio = client.files.upload(file=ruta_audio)

    print("Generando informe...")

    # Enviar el audio a Gemini
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=[
            "Eres un contador público experto. Escucha el siguiente audio y genera un informe ejecutivo profesional con:\n"
            "1. Título\n"
            "2. Resumen ejecutivo\n"
            "3. Puntos clave\n"
            "4. Cifras importantes\n"
            "5. Tareas pendientes\n"
            "6. Conclusión",
            audio,
        ],
    )

    # Eliminar el archivo de la API
    client.files.delete(name=audio.name)

    return response.text


if __name__ == "__main__":

    archivo = "audio_prueba.mp3"

    if not os.path.exists(archivo):
        print(f"No existe el archivo '{archivo}'.")
        exit()

    try:
        informe = procesar_audio(archivo)

        print("\n==============================")
        print("INFORME GENERADO")
        print("==============================\n")
        print(informe)

        guardar_word(informe)

        print("\n✅ Informe guardado como 'informe_generado.docx'")

    except Exception as e:
        print("\n❌ Ocurrió un error:")
        print(e)