import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración del servidor SMTP
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
USERNAME = os.getenv('EMAIL_USERNAME')
PASSWORD = os.getenv('EMAIL_PASSWORD')  # Usar variable de entorno para la contraseña

# Crear una función para enviar el saludo
def enviar_saludo(destinatario):
    # Configurar el correo electrónico
    mensaje = MIMEMultipart()
    mensaje['From'] = USERNAME
    mensaje['To'] = destinatario
    mensaje['Subject'] = (
        'Saludos desde Soluciones innovadoras en el lenguaje de programación local'
    )

    # Cuerpo del correo
    cuerpo = """
    Hola,

    Espero que estés teniendo un excelente día.

    Saludos cordiales,
    """
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    # Enviar el correo
    try:
        servidor = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        servidor.starttls()
        servidor.login(USERNAME, PASSWORD)
        servidor.sendmail(USERNAME, destinatario, mensaje.as_string())
        servidor.quit()
        print(f'Correo enviado a {destinatario}')
    except smtplib.SMTPAuthenticationError:
        print(
            f'Error de autenticación al enviar correo a {destinatario}: Verifique las credenciales.'
        )
    except Exception as e:
        print(f'Error al enviar correo a {destinatario}: {e}')

# Leer la lista de correos del archivo CSV
def leer_lista_correos(archivo_csv):
    with open(archivo_csv, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Saltar la cabecera
        for row in reader:
            if row:
                enviar_saludo(row[0])

# Ruta del archivo CSV con la lista de correos
archivo_csv = 'emails.csv'

# Ejecutar la función para leer la lista y enviar los saludos
leer_lista_correos(archivo_csv)
