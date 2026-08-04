#import tensorflow as tf
#import tensorflow_decision_forests as tfdf
import pandas as pd
import numpy as np
from scipy.stats import linregress

# Cargar un dataset (por ejemplo, desde un archivo .csv)
# dataset = pd.read_csv("tu_dataset.csv")

# Convertir tu Pandas DataFrame a un Dataset de TensorFlow
# tf_dataset = tfdf.keras.pd_dataframe_to_tf_dataset(dataset, label="nombre_columna_objetivo")

# Entrenar el modelo de Random Forest para clasificación
# model = tfdf.keras.RandomForestModel(task=tfdf.keras.Task.CLASSIFICATION)
# model.compile(metrics=["accuracy"])
# model.fit(tf_dataset)



ruta = "csv_BaseDatos/Base_estadistica_matricula_UEP_15_23.csv"

df = pd.read_csv(ruta, encoding="latin-1")
df = df[(df["NIVEL_FORMACION"] == "TERCER NIVEL DE GRADO") ]
df=df[df["CAMPO_AMPLIO"]!="NO_REGISTRA"]
print(df.shape)
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
    df.groupby(["UNIVERSIDAD", "CARRERA", "ANIO", "FINANCIAMIENTO","CAMPO"], as_index=False)
      .agg({
          "MATRICULA": "sum",
          "MODALIDAD": "first"
      })
      .sort_values(["UNIVERSIDAD", "CARRERA", "ANIO"])
)

analisis = resultado.groupby(["UNIVERSIDAD", "CARRERA", "ANIO"], as_index=False)["MATRICULA"].sum()


carreras_validas = analisis.groupby(["UNIVERSIDAD", "CARRERA"])["ANIO"].agg(anio_min="min", anio_max="max", n_anios="nunique").reset_index()
print(carreras_validas["n_anios"].value_counts().sort_index())

carreras_validas_entre_4=carreras_validas[(carreras_validas["n_anios"] >= 4)][["UNIVERSIDAD", "CARRERA"]]

N_ANIOS_ETIQUETA = 1   # cuántos de los últimos años se reservan como "futuro"

def calcular_features_y_etiqueta(grupo):
    grupo = grupo.sort_values("ANIO")
    m = grupo["MATRICULA"].values
    a = grupo["ANIO"].values
    n = len(a)
    if n < 4:
        return None
    m_feat, a_feat = m[:-N_ANIOS_ETIQUETA], a[:-N_ANIOS_ETIQUETA]
    m_label = m[-N_ANIOS_ETIQUETA:]
    variaciones_feat = (m_feat[1:] - m_feat[:-1]) / m_feat[:-1]
    r = np.mean(variaciones_feat)
    volatilidad = np.std(variaciones_feat, ddof=1)
    pendiente = linregress(a_feat, m_feat).slope

    m_ultimo_ventana = m_feat[-1]
    m_oculto = m_label[-1]
    delta_target = (m_oculto - m_ultimo_ventana) / m_ultimo_ventana
    diff_abs = abs(m_oculto - m_ultimo_ventana)
    

dataset=((
    resultado.groupby(["UNIVERSIDAD", "CARRERA"])
    .apply(calcular_features_y_etiqueta)
    .dropna()
    .reset_index()
))
