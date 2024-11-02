#!/bin/bash

# Script de Bash para programar la ejecución del script de Python cada lunes

# Ruta del script de Python
PYTHON_SCRIPT="/ruta/completa/al/script/send_greetings.py"

# Comando para invocar el script de Python
function enviar_saludos {
    /usr/bin/python3 "$PYTHON_SCRIPT"
}

enviar_saludos

# Configurar el cronjob para que se ejecute cada lunes
# PARA SO LINUX
# Para añadir esta tarea al cron, ejecuta "crontab -e" y agrega la siguiente línea:
# 0 9 * * 1 /ruta/completa/al/script/send_greetings.sh > /ruta/completa/al/script/send_greetings.log 2>&1
# La tarea anterior se ejecutará cada lunes a las 9:00 AM y guardará un log de la ejecución.
