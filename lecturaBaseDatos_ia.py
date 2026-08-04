import pandas as pd
import numpy as np
from scipy.stats import linregress

ruta = "csv_BaseDatos/Base_estadistica_matricula_UEP_15_23.csv"

df = pd.read_csv(ruta)
df = df[(df["NIVEL_FORMACION"] == "TERCER NIVEL DE GRADO")]
df = df[df["CAMPO_AMPLIO"]!="NO_REGISTRA"]
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
    df.groupby(["UNIVERSIDAD", "CARRERA", "ANIO", "FINANCIAMIENTO", "CAMPO"], as_index=False)
      .agg({"MATRICULA": "sum", "MODALIDAD": "first"})
      .sort_values(["UNIVERSIDAD", "CARRERA", "ANIO"])
)
print(resultado.shape)
# --- PASO 1: diagnóstico de cobertura por carrera-universidad (tu exploración, pero automática) ---
cobertura = (
    resultado.groupby(["UNIVERSIDAD", "CARRERA"])["ANIO"]
    .agg(anio_min="min", anio_max="max", n_anios="nunique")
    .reset_index()
)
cobertura["rango_completo"] = (cobertura["anio_max"] - cobertura["anio_min"] + 1) == cobertura["n_anios"]

print(cobertura["n_anios"].value_counts().sort_index())
print(f"Con huecos (años faltantes en medio del rango): {(~cobertura['rango_completo']).sum()}")

# --- PASO 2: umbral mínimo de historial ---
MIN_ANIOS = 5          # mínimo total para tener features + etiqueta confiables
N_ANIOS_ETIQUETA = 2   # cuántos de los últimos años se reservan como "futuro"

carreras_validas = cobertura[cobertura["n_anios"] >= MIN_ANIOS][["UNIVERSIDAD", "CARRERA"]]
print(f"Carreras con historial suficiente: {len(carreras_validas)} de {len(cobertura)}")

# --- PASO 3: ventana relativa por grupo (no año fijo global) ---
def calcular_features_y_etiqueta(grupo):
    grupo = grupo.sort_values("ANIO")
    m = grupo["MATRICULA"].values
    a = grupo["ANIO"].values
    n = len(m)
    if n < MIN_ANIOS:
        return None

    m_feat, a_feat = m[:-N_ANIOS_ETIQUETA], a[:-N_ANIOS_ETIQUETA]
    m_label = m[-N_ANIOS_ETIQUETA:]

    variaciones_feat = (m_feat[1:] - m_feat[:-1]) / m_feat[:-1]
    r = np.mean(variaciones_feat)
    volatilidad = np.std(variaciones_feat)
    pendiente = linregress(a_feat, m_feat).slope
    delta_abs = np.mean(m_feat[1:] - m_feat[:-1])

    # etiqueta: promedio de variaciones dentro de TODA la ventana de etiqueta
    serie_label = np.append(m_feat[-1], m_label)
    variaciones_label = (serie_label[1:] - serie_label[:-1]) / serie_label[:-1]
    r_futuro = np.mean(variaciones_label)
    delta_futuro = np.mean(serie_label[1:] - serie_label[:-1])

    DELTA = 5
    if r_futuro > 0.05 and delta_futuro >= DELTA:
        clase = "Crecimiento"
    elif r_futuro < -0.05 and delta_futuro <= -DELTA:
        clase = "Disminución"
    else:
        clase = "Estabilidad"

    return pd.Series({
        "r": r, "volatilidad": volatilidad, "pendiente": pendiente,
        "delta_abs": delta_abs, "claseTendencia": clase,
        "campo": grupo["CAMPO"].mode().iloc[0],   # moda, no groupby key
        "n_anios": n
    })

# Agrupar SOLO por universidad + carrera (no por campo)
dataset = (
    resultado.groupby(["UNIVERSIDAD", "CARRERA"])
    .apply(calcular_features_y_etiqueta)
    .dropna()
    .reset_index()
)

promedio_campo = dataset.groupby("campo")["r"].transform("mean")
dataset["posicion_relativa"] = dataset["r"] - promedio_campo
print(dataset)