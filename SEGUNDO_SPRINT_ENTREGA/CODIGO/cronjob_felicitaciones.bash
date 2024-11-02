#!/bin/bash

# Ruta del archivo CSV con la lista de cumpleaños
CSV_FILE="cumpleanos_fechas.csv"

# Obtener la fecha de hoy en formato dd/mm/yyyy
HOY=$(date +"%d/%m/%Y")

# Iterar sobre cada línea del archivo CSV (exceptuando la cabecera)
while IFS=',' read -r nombre fecha email
  do
    # Saltar la cabecera
    if [[ "$nombre" == "Nombre" ]]; then
      continue
    fi
    
    # Comprobar si la fecha coincide con la fecha actual
    if [[ "$fecha" == "$HOY" ]]; then
        echo "Enviando correo a $nombre ($email)..."
        # Ejecutar el script de Python para enviar el correo
        python3 emails_felicitaciones.py "$nombre" "$email"
    fi
done < <(tail -n +2 "$CSV_FILE")
