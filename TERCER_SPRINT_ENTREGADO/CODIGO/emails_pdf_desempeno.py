import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from dotenv import load_dotenv
from datetime import datetime
from fpdf import FPDF
import random

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración del servidor SMTP
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
USERNAME = os.getenv('EMAIL_USERNAME')
PASSWORD = os.getenv('EMAIL_PASSWORD')  # Usar variable de entorno para la contraseña


def crear_pdf(nombre_empleado, rendimiento):
    """
    Crea un PDF personalizado con un informe de rendimiento aleatorio.

    :param nombre_empleado: Nombre del empleado para personalizar el PDF.
    :param rendimiento: Descripción del rendimiento del empleado.
    :return: Ruta del archivo PDF creado.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="Informe de Rendimiento de: {}".format(nombre_empleado), ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="Este informe contiene un resumen del desempeño del empleado durante el último período. El rendimiento ha sido evaluado como: {}".format(rendimiento))
    nombre_pdf = "informe_rendimiento_{}.pdf".format(nombre_empleado.replace(" ", "_"))
    pdf.output(nombre_pdf)
    return nombre_pdf


def enviar_saludo(destinatario, nombre_empleado, rendimiento):
    """
    Envía un saludo al destinatario especificado, adjuntando un PDF personalizado.

    :param destinatario: Correo electrónico del destinatario.
    :param nombre_empleado: Nombre del empleado para personalizar el mensaje.
    :param rendimiento: Descripción del rendimiento del empleado para personalizar el PDF.
    """
    # Configurar el correo electrónico
    mensaje = MIMEMultipart()
    mensaje['From'] = USERNAME
    mensaje['To'] = destinatario
    mensaje['Subject'] = 'Saludos desde Soluciones innovadoras en el lenguaje de programación local'

    # Leer el cuerpo del correo desde el archivo HTML
    with open('felicitaciones.html', 'r', encoding='utf-8') as file:
        cuerpo = file.read().replace("{nombre_empleado}", nombre_empleado)

    mensaje.attach(MIMEText(cuerpo, 'html'))

    # Crear el PDF personalizado y adjuntarlo al correo
    pdf_path = crear_pdf(nombre_empleado, rendimiento)
    with open(pdf_path, "rb") as pdf_file:
        mensaje.attach(MIMEApplication(pdf_file.read(), _subtype="pdf", Name=pdf_path))

    # Enviar el correo
    try:
        servidor = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        servidor.starttls()
        servidor.login(USERNAME, PASSWORD)
        servidor.sendmail(USERNAME, destinatario, mensaje.as_string())
        servidor.quit()
        print(f'Correo enviado a {destinatario}')
    except smtplib.SMTPAuthenticationError:
        print(f'Error de autenticación al enviar correo a {destinatario}: Verifique las credenciales.')
    except Exception as e:
        print(f'Error al enviar correo a {destinatario}: {e}')


def leer_lista_desempeno(archivo_csv):
    """
    Lee la lista de empleados desde un archivo CSV y envía informes de desempeño aleatorios.

    :param archivo_csv: Ruta del archivo CSV con la lista de empleados.
    """
    evaluaciones = ["Excelente", "Muy bueno", "Bueno", "Regular", "Necesita mejorar"]
    with open(archivo_csv, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Saltar la cabecera
        for row in reader:
            if row:
                nombre_empleado = row[0]
                destinatario = row[2]  # Utilizar el email especificado en la tercera columna
                rendimiento = random.choice(evaluaciones)
                enviar_saludo(destinatario, nombre_empleado, rendimiento)


# Ruta del archivo CSV con la lista de empleados
archivo_csv = 'empleados_desempeno.csv'

# Ejecutar la función para leer la lista y enviar los saludos
leer_lista_desempeno(archivo_csv)
