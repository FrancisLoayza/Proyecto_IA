import pandas as pd
import numpy as np

# =========================
# Leer la base
# =========================

ruta = "csv_BaseDatos/Base_estadistica_matricula_UEP_15_23.csv"

df = pd.read_csv(ruta, encoding="latin-1")

df = df[df["NIVEL_FORMACION"] == "TERCER NIVEL DE GRADO"]
df = df[df["CAMPO_AMPLIO"] != "NO_REGISTRA"]

df = df.rename(columns={
    df.columns[0]: "ANIO",
    "NOMBRE_IES": "UNIVERSIDAD",
    "NOMBRE_CARRERA": "CARRERA",
    "MODALIDAD": "MODALIDAD",
    "TIPO_FINANCIAMIENTO": "FINANCIAMIENTO",
    "CAMPO_AMPLIO": "CAMPO",
    "TOTAL": "MATRICULA"
})

# =========================
# Agrupar
# =========================

resultado = (
    df.groupby(["UNIVERSIDAD", "CARRERA", "ANIO"], as_index=False)
      .agg({
          "MATRICULA": "sum",
          "MODALIDAD": "first"
      })
      .sort_values(["UNIVERSIDAD", "CARRERA", "ANIO"])
)

# =========================
# Crear archivo TXT
# =========================

with open("universidades_carreras_nuevo.txt", "w", encoding="utf-8") as f:

    for universidad in sorted(resultado["UNIVERSIDAD"].unique()):

        f.write(universidad + "\n")
        f.write("-" * len(universidad) + "\n")

        carreras = (
            resultado[resultado["UNIVERSIDAD"] == universidad]
            .groupby("CARRERA")["ANIO"]
            .agg(["min", "max"])
            .reset_index()
            .sort_values("CARRERA")
        )

        for _, fila in carreras.iterrows():

            carrera = fila["CARRERA"]
            anio_inicio = int(fila["min"])
            anio_fin = int(fila["max"])

            f.write(f"  - {carrera} ({anio_inicio} - {anio_fin})\n")

        f.write("\n\n")

print("Archivo 'universidades_carreras.txt' generado correctamente.")