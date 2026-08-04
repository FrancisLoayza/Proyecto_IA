import pandas as pd
import shutil
import os

ruta = "csv_BaseDatos/Base_estadistica_matricula_UEP_15_23.csv"
backup = "csv_BaseDatos/backups/Base_estadistica_matricula_UEP_15_23.csv"

# Crear la carpeta de backups si no existe
os.makedirs("csv_BaseDatos/backups", exist_ok=True)

# Actualizar el respaldo antes de modificar el archivo
shutil.copy2(ruta, backup)

df = pd.read_csv(ruta, encoding="latin-1")