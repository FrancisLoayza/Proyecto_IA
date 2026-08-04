import pandas as pd

ruta = "csv_BaseDatos/Base_estadistica_matricula_UEP_15_23.csv"
df = pd.read_csv(ruta, encoding="latin-1")

# Cambiar el nombre de la carrera
df.loc[
    (df["NOMBRE_IES"] == "ESCUELA POLITECNICA NACIONAL") &
    (df["NOMBRE_CARRERA"] == "INGENIERIA GEOLOGICA"),
    "NOMBRE_CARRERA"
] = "INGENIERIA GEOLOGICA"



# Guardar el CSV actualizado
df.to_csv(ruta, index=False, encoding="latin-1")