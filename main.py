import pandas as pd
import numpy as np


ruta = "csv_BaseDatos/Base_estadistica_matricula_UEP_15_23.csv"
df = pd.read_csv(ruta, encoding="latin-1")
df = df[(df["NIVEL_FORMACION"] == "TERCER NIVEL DE GRADO") ]
df=df[df["CAMPO_AMPLIO"]!="NO_REGISTRA"]

df = df.rename(columns={
    df.columns[0]: "ANIO",
    "NOMBRE_IES": "UNIVERSIDAD",
    "NOMBRE_CARRERA": "CARRERA",
    "MODALIDAD": "MODALIDAD",
    "TIPO_FINANCIAMIENTO": "FINANCIAMIENTO",
    "CAMPO_AMPLIO": "CAMPO",
    "TOTAL": "MATRICULA"
})

resultado = (
    df.groupby(["UNIVERSIDAD", "CARRERA", "ANIO"], as_index=False)
      .agg({
          "MATRICULA": "sum",
          "MODALIDAD": "first"
      })
      .sort_values(["UNIVERSIDAD", "CARRERA", "ANIO"])
)

Espol = resultado[resultado["UNIVERSIDAD"] == "UNIVERSIDAD CASA GRANDE"]
analisis1 = Espol[Espol["CARRERA"] == "PERIODISMO CON MENCION EN CIENCIAS POLITICAS"]
analisis2= Espol[Espol["CARRERA"] == "CIENCIAS POLITICAS"]
analisis3= Espol[Espol["CARRERA"] == "LICENCIATURA EN CIENCIAS DE LA EDUCACION MENCION SICOLOGIA EDUCATIVA Y ORIENTACION VOCACIONAL."]
print(analisis1[["UNIVERSIDAD", "CARRERA", "ANIO", "MATRICULA"]].to_string(index=False))
print(analisis2[["UNIVERSIDAD", "CARRERA", "ANIO", "MATRICULA"]].to_string(index=False))
print(analisis3[["UNIVERSIDAD", "CARRERA", "ANIO", "MATRICULA"]].to_string(index=False))