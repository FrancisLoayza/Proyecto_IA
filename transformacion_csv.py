import pandas as pd

# Leer el archivo Excel
df = pd.read_excel("/home/francis-loayza/Descargas/Base_estadistica_matricula.xlsx")

# Guardarlo como CSV
df.to_csv("Base_estadistica_matricula_UEP_15_23_temp.csv", index=False, encoding="utf-8-sig")