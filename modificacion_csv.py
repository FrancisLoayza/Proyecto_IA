import pandas as pd
import os

ruta = "csv_BaseDatos/Base_estadistica_matricula_UEP_15_23.csv"
ruta_temp = "csv_BaseDatos/Base_estadistica_matricula_UEP_15_23_temp.csv"

df = pd.read_csv(ruta, encoding="latin-1")

df.loc[
    (df["NOMBRE_IES"] == "UNIVERSIDAD POLITECNICA SALESIANA") &
    (df["NOMBRE_CARRERA"] == "INGENIERIA EN SISTEMAS"),
    "NOMBRE_CARRERA"
] = "COMPUTACION"

# Escribir primero al archivo temporal
df.to_csv(ruta_temp, index=False, encoding="latin-1")

# Solo si terminó correctamente, reemplazar el original
os.replace(ruta_temp, ruta)