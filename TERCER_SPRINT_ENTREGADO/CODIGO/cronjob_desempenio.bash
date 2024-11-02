#!/bin/bash

# Script: automate_birthday_emails.bash
# Descripcion: Automatiza la ejecucion diaria del script Python para enviar correos de rendimiento.

# Ruta del archivo Python
PYTHON_SCRIPT="/c/Users/DyTy18/Downloads/Soluciones_innovadoras_en_el_lenguaje_de_programacion_local/emails_pdf_desempeno.py"

# Automatizar la ejecucion del script Python todos los dias a las 9 AM
(crontab -l ; echo "0 9 * * * /usr/bin/python3 $PYTHON_SCRIPT") | crontab -

# Mensaje de confirmacion
echo "Tarea programada para ejecutar el script Python todos los dias a las 9 AM."
