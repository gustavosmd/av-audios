import markdown2
from weasyprint import HTML
from pydub import AudioSegment
import os
from google import genai
import datetime
import pytz

def markdown_to_pdf(markdown_text, pdf_file):
    """Converts a Markdown file to PDF using markdown2 and WeasyPrint."""
    try:
        html_content = markdown2.markdown(markdown_text,
                                          extras=['fenced-code-blocks'])

        HTML(string=html_content).write_pdf(pdf_file)

        print("Successfully converted pdf!")

    except Exception as e:
        print(f"Error: {e}")

def get_summary(m4a_file):
    # Convertir el archivo a un formato compatible si es necesario
    audio_path = m4a_file
    converted_audio_path = "converted_audio.wav"

    # Convertir M4A a WAV

    audio = AudioSegment.from_ogg(audio_path)

    audio.export(converted_audio_path, format="wav")
    print(f"Conversion successful: {audio_path} -> {converted_audio_path}")

    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"), )

    audio_file = client.files.upload(file='converted_audio.wav')

    print("Inicio de proceso de transcript...")

    response = client.models.generate_content(
        model = "gemini-2.0-flash-lite",
        contents = [
            audio_file,
            "Dame el transcript de este audio. Por favor sólo el transcript, sin introducciones, saludos o cualquier otra cordialidad."
        ])

    print("...proceso de transcript terminado.")

    print("Inicio de proceso de GenAI...")

    response2 = client.models.generate_content(
        model = "gemini-2.0-flash-lite",
        contents = [
            response.text,
            "Dame un resumen de este dia de campo. Por favor, generar este resumen con las siguientes secciones: datos generales (nombre de la persona que hizo la visita, zona de trabajo, fecha), datos del cliente (nombre, segmento, zona específica, area), objetivos, logros y siguientes pasos. En caso, hayan aprendizajes que no pertenezcan a alguna de estas secciones, agregar una sección de otros aprendizajes. Puede que haya sido mal escrito el nombre de nuestro producto principal: BioC NPK. En cuanto a la fecha de la visita, si solo se menciona un dia del mes, o de la semana sin especificar la fecha exacta, considerar la última occurrencia de esto, siendo la fecha de hoy " + str(datetime.datetime.now(pytz.timezone('America/Lima'))) + ". Por favor corregirlo por el nombre correcto. Por favor sólo el resumen, sin introducciones, saludos o cualquier otra cordialidad."
        ])

    # response2 = client.models.generate_content(
    #     model="gemini-2.0-flash",
    #     contents=[
    #         response.text,
    #         "Dame un resumen de este audio que hice con las notas de esta llamada telefónica. Por favor, generar este resumen con las siguientes secciones: datos generales (con quién fue la llamada, cuando fue y la fecha de la llamada), objetivo de la llamada, conclusiones de la llamada y siguientes pasos. En cuanto a la fecha de la llamada, si solo se menciona un dia del mes, o de la semana sin especificar la fecha exacta, considerar la última occurrencia de esto, siendo la fecha de hoy " + str(datetime.datetime.now(pytz.timezone('America/Lima'))) + ". Por favor corregirlo por el nombre correcto. Por favor sólo el resumen, sin introducciones, saludos o cualquier otra cordialidad."
    #     ])

    print("...fin de proceso de GenAI!!!")

    print(response2.text)

    new_file_path = "pdfs/" + str(audio_path.name)[:-4] + ".pdf"

    markdown_to_pdf(response2.text, new_file_path)

    return new_file_path
