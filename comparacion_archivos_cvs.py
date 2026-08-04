import pandas as pd

ruta = "csv_BaseDatos/Base_estadistica_matricula_UEP_15_23.csv"
ruta2="archivo.csv"


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
    df.groupby(["UNIVERSIDAD", "CARRERA"], as_index=False)
      .agg({
          "MATRICULA": "sum",
          "MODALIDAD": "first"
      })
      .sort_values(["UNIVERSIDAD", "CARRERA"])
)

df_copia = pd.read_csv(ruta2, encoding="latin-1")
df_copia = df_copia[(df_copia["NIVEL_FORMACION"] == "TERCER NIVEL DE GRADO") ]
df_copia=df_copia[df_copia["CAMPO_AMPLIO"]!="NO_REGISTRA"]

df_copia = df_copia.rename(columns={
    df_copia.columns[0]: "ANIO",
    "NOMBRE_IES": "UNIVERSIDAD",
    "NOMBRE_CARRERA": "CARRERA",
    "MODALIDAD": "MODALIDAD",
    "TIPO_FINANCIAMIENTO": "FINANCIAMIENTO",
    "CAMPO_AMPLIO": "CAMPO",
    "TOTAL": "MATRICULA"
})

resultado_copia = (
    df_copia.groupby(["UNIVERSIDAD", "CARRERA"], as_index=False)
      .agg({
          "MATRICULA": "sum",
          "MODALIDAD": "first"
      })
      .sort_values(["UNIVERSIDAD", "CARRERA"])
)
with open("comparacion_carreras.txt", "w", encoding="utf-8") as f:

    universidades = sorted(
        set(resultado["UNIVERSIDAD"]).union(resultado_copia["UNIVERSIDAD"])
    )

    for universidad in universidades:

        f.write("=" * 120 + "\n")
        f.write(f"UNIVERSIDAD: {universidad}\n")
        f.write("=" * 120 + "\n\n")

        f.write(f"{'ORIGINAL':<70}COPIA\n")
        f.write("-" * 120 + "\n")

        carreras_original = sorted(
            resultado.loc[
                resultado["UNIVERSIDAD"] == universidad, "CARRERA"
            ].tolist()
        )

        carreras_copia = sorted(
            resultado_copia.loc[
                resultado_copia["UNIVERSIDAD"] == universidad, "CARRERA"
            ].tolist()
        )

        max_filas = max(len(carreras_original), len(carreras_copia))

        for i in range(max_filas):
            original = carreras_original[i] if i < len(carreras_original) else ""
            copia = carreras_copia[i] if i < len(carreras_copia) else ""

            f.write(f"{original:<70}{copia}\n")

        f.write("\n\n")

print("Archivo 'comparacion_carreras.txt' creado.")