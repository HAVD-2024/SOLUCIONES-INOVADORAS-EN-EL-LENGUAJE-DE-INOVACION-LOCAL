import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from datetime import datetime

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración del servidor SMTP
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
USERNAME = os.getenv('EMAIL_USERNAME')
PASSWORD = os.getenv('EMAIL_PASSWORD')  # Usar variable de entorno para la contraseña


def enviar_saludo(destinatario, nombre_empleado):
    """
    Envía un saludo de cumpleaños al destinatario especificado.

    :param destinatario: Correo electrónico del destinatario.
    :param nombre_empleado: Nombre del empleado para personalizar el mensaje.
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


def leer_lista_cumpleanos(archivo_csv):
    """
    Lee la lista de cumpleaños desde un archivo CSV y envía saludos si la fecha coincide con hoy.

    :param archivo_csv: Ruta del archivo CSV con la lista de cumpleaños.
    """
    hoy = datetime.now().strftime('%d/%m/%Y')
    with open(archivo_csv, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Saltar la cabecera
        for row in reader:
            if row and row[1] == hoy:
                nombre_empleado = row[0]
                destinatario = row[2]  # Utilizar el email especificado en la tercera columna
                enviar_saludo(destinatario, nombre_empleado)


# Ruta del archivo CSV con la lista de cumpleaños
archivo_csv = 'cumpleanos_fechas.csv'

# Ejecutar la función para leer la lista y enviar los saludos
leer_lista_cumpleanos(archivo_csv)
