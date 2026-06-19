import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
import geopandas as gpd
from shapely.geometry import Point
import os
import seaborn as sns
import branca.colormap as cm
from folium import plugins
from PIL import Image
from streamlit_folium import st_folium


# ─────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Comparendos Electrónicos – Barranquilla",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
# ESTILOS GLOBALES
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --bg:       #0d1117;
    --surface:  #161b22;
    --surface2: #1c2330;
    --border:   #2d3748;
    --accent:   #3b82f6;
    --accent2:  #06b6d4;
    --success:  #10b981;
    --warn:     #f59e0b;
    --danger:   #ef4444;
    --text:     #e2e8f0;
    --muted:    #94a3b8;
    --heading:  #f8fafc;
}

html, body, .stApp {
    background-color: var(--bg) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .stRadio label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.92rem;
    font-weight: 500;
    color: var(--muted) !important;
    padding: 6px 10px;
    border-radius: 8px;
    transition: all 0.15s;
    white-space: normal;
    line-height: 1.4;
}
[data-testid="stSidebar"] .stRadio label:hover {
    color: var(--text) !important;
    background: var(--surface2);
}

h1 {
    font-family: 'DM Serif Display', serif !important;
    font-size: 2.5rem !important;
    color: var(--heading) !important;
    letter-spacing: -0.5px;
    line-height: 1.15;
    margin-bottom: 0.25rem !important;
}
h2 {
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.75rem !important;
    color: var(--heading) !important;
    border-left: 3px solid var(--accent);
    padding-left: 14px;
    margin-top: 2rem !important;
    margin-bottom: 1rem !important;
}
h3 {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    color: var(--accent2) !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 1.5rem !important;
    margin-bottom: 0.5rem !important;
}
h4 {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: var(--text) !important;
    margin-top: 1.2rem !important;
}

.pill {
    display: inline-block;
    background: rgba(59,130,246,0.12);
    color: var(--accent);
    font-family: 'DM Sans', sans-serif;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 999px;
    border: 1px solid rgba(59,130,246,0.3);
    margin-right: 6px;
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.div-line {
    border: none;
    border-top: 1px solid var(--border);
    margin: 26px 0;
}

.results-block {
    background: var(--surface2);
    border-left: 3px solid var(--accent2);
    border-radius: 0 10px 10px 0;
    padding: 16px 20px;
    margin: 4px 0 16px 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.81rem;
    color: var(--text);
    line-height: 1.75;
    white-space: pre-wrap;
}
.results-block .ok   { color: #6ee7b7; font-weight: 600; }
.results-block .fail { color: #fca5a5; font-weight: 600; }
.results-block .warn { color: #fcd34d; font-weight: 600; }
.results-block .hdr  { color: #7dd3fc; font-weight: 600; }

.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.70rem;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 6px;
}

.tag {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 4px;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.tag-chart  { background: rgba(59,130,246,0.15); color: #93c5fd; border: 1px solid rgba(59,130,246,0.3); }
.tag-result { background: rgba(16,185,129,0.15); color: #6ee7b7; border: 1px solid rgba(16,185,129,0.3); }
.tag-table  { background: rgba(245,158,11,0.15); color: #fcd34d; border: 1px solid rgba(245,158,11,0.3); }

.chart-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--muted);
    margin-bottom: 6px;
    text-align: center;
}

.best-badge {
    background: linear-gradient(135deg, rgba(16,185,129,0.15), rgba(6,182,212,0.15));
    border: 1px solid rgba(16,185,129,0.4);
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 0.85rem;
    color: #6ee7b7;
    margin-bottom: 16px;
    font-family: 'DM Sans', sans-serif;
}

.streamlit-expanderHeader {
    background: var(--surface2) !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    color: var(--heading) !important;
    border: 1px solid var(--border) !important;
}
.streamlit-expanderContent {
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
    background: var(--surface) !important;
    padding: 18px !important;
}

.stMarkdown p  { color: var(--text); font-size: 0.93rem; line-height: 1.7; }
.stMarkdown li { color: var(--text); font-size: 0.91rem; line-height: 1.7; }
.stMarkdown strong { color: var(--heading); }

.stCodeBlock pre {
    background: #090d13 !important;
    border-radius: 10px !important;
    border: 1px solid var(--border) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# UTILIDADES
# ─────────────────────────────────────────────────────────────
def img(nombre, caption=""):
    ruta = os.path.join("imagenes", nombre)
    if os.path.exists(ruta):
        if caption:
            st.markdown(f'<p class="chart-title">{caption}</p>', unsafe_allow_html=True)
        st.image(Image.open(ruta), use_container_width=True)
    else:
        st.markdown(
            f'<div style="background:#1c2330;border:1px dashed #2d3748;border-radius:10px;'
            f'padding:28px;text-align:center;color:#64748b;font-size:0.80rem;">'
            f'Imagen no encontrada: <code>{nombre}</code></div>',
            unsafe_allow_html=True
        )

def stag(tipo):
    labels = {"chart": ("tag-chart", "Gráfica"), "result": ("tag-result", "Resultados"),
              "table": ("tag-table", "Tabla"), "map": ("tag-chart", "Mapa Interactivo")}
    css, txt = labels.get(tipo, ("tag-chart", "Gráfica"))
    st.markdown(f'<span class="tag {css}">{txt}</span>', unsafe_allow_html=True)

def results(html_content):
    st.markdown(f'<div class="results-block">{html_content}</div>', unsafe_allow_html=True)

def slabel(txt):
    st.markdown(f'<div class="section-label">{txt}</div>', unsafe_allow_html=True)

def hr():
    st.markdown('<hr class="div-line">', unsafe_allow_html=True)

def best_model(txt):
    st.markdown(f'<div class="best-badge">Mejor modelo seleccionado &mdash; {txt}</div>',
                unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# DATOS GEOGRÁFICOS
# ─────────────────────────────────────────────────────────────
direcciones = [
    "VIA 11 CON CARRERA 8", "CARRERA 51B CON CALLE 79", "CALLE 30 CON CARRERA 6B",
    "CARRERA 53 ENTRE CALLE 104 Y 106", "CALLE 45 CON CARRERA 1", "CALLE 30 CON CARRERA 8",
    "CALLE 82 CON CARRERA 51B", "CARRERA 51B CON CALLE 103", "CARRERA 6 CON CALLE 72",
    "AVENIDA CIRCUNVALAR CON CARRERA 9G", "VIA 40 CON CALLE 73", "CALLE 45 CON CARRERA 20",
    "CALLE 82 CON CARRERA 56", "CALLE 45B CON CARRERA 14", "CALLE 45 CON CARRERA 21",
    "CARRERA 15 CON CALLE 21", "CALLE 72 CON CARRERA 44", "CALLE 84 ENTRE CARRERA 59 Y 59B",
    "CALLE 94 CON CARRERA 58", "CARRERA 46 CON CALLE 100", "CALLE 56 CON CARRERA 14",
    "CALLE 19 CON CARRERA 4C", "CALLE 53 CON CARRERA 45", "CALLE 87 CON CARRERA 21",
    "CALLE 76 CON CARRERA 38C-100", "CALLE 19 CON CARRERA 3D", "CARRERA 53 CON CALLE 86",
    "CALLE 70 CON CARRERA 46", "CALLE 34 CON CARRERA 45", "AVENIDA CIRCUNVALAR CON CARRERA 31",
    "CALLE 98 CON CARRERA 56", "CALLE 61 CON CARRERA 35", "CARRERA 27 CON CALLE 82C"
]
coordenadas = [
    (10.95749, -74.89345), (11.00320, -74.81055), (10.94276, -74.78356),
    (11.01742, -74.83438), (10.92959, -74.79918), (10.94667, -74.78458),
    (11.00457, -74.81435), (11.01310, -74.83406), (10.94750, -74.81622),
    (10.95670, -74.83610), (11.01211, -74.79250), (10.96134, -74.79337),
    (11.00740, -74.81254), (10.95467, -74.79734), (10.96212, -74.79308),
    (10.95356, -74.77608), (10.99261, -74.80666), (11.01113, -74.81144),
    (11.01561, -74.82071), (11.00788, -74.83351), (10.95849, -74.80349),
    (10.94252, -74.77770), (10.98771, -74.78975), (10.97017, -74.83003),
    (10.98943, -74.81432), (10.94020, -74.77858), (11.00938, -74.81841),
    (10.99322, -74.80340), (10.98383, -74.77750), (10.97849, -74.83592),
    (11.01575, -74.82514), (10.98087, -74.80040), (10.97925, -74.82361)
]
coordenadas_dict = dict(zip(direcciones, coordenadas))


# ─────────────────────────────────────────────────────────────
# CARGA DE DATOS CSV
# ─────────────────────────────────────────────────────────────
@st.cache_data
def cargar_datos_camaras(csv_path, coord_dict):
    df = pd.read_csv(csv_path)
    df['fecha_comparendo'] = pd.to_datetime(
        df['fecha_comparendo'], format='%Y %b %d %I:%M:%S %p').dt.normalize()
    df.loc[df['Camara_y_direccion'] == 'CARRERA 53 CON CALLE 104',
           'Camara_y_direccion'] = 'CARRERA 53 ENTRE CALLE 104 Y 106'
    df.loc[df['Camara_y_direccion'] == 'CALLE 84 CON CARRERA 59',
           'Camara_y_direccion'] = 'CALLE 84 ENTRE CARRERA 59 Y 59B'
    df.loc[df['Camara_y_direccion'] == 'CARRERA 45 CON CALLE 53',
           'Camara_y_direccion'] = 'CALLE 53 CON CARRERA 45'
    df.loc[df['Camara_y_direccion'] == 'CALLE 45B CARRERA 14',
           'Camara_y_direccion'] = 'CALLE 45B CON CARRERA 14'
    df = df[~((df['COD_INFRACCION'] == 'C02') & (df['Tipo Camara'] == 'Fijo'))]
    datos = []
    for direccion, grupo in df.groupby('Camara_y_direccion'):
        if direccion not in coord_dict:
            continue
        total = grupo['CANTIDAD_INFRACCIONES'].sum()
        por_codigo = grupo.groupby('COD_INFRACCION')['CANTIDAD_INFRACCIONES'].sum().to_dict()
        datos.append({
            'direccion': direccion,
            'total': total,
            'comparendos_por_codigo': por_codigo,
            'primera_fecha': grupo['fecha_comparendo'].min().strftime('%Y-%m-%d'),
            'ultima_fecha': grupo['fecha_comparendo'].max().strftime('%Y-%m-%d'),
            'coordenadas': coord_dict[direccion]
        })
    return datos


csv_path = "datos/comparendos_electronicos.csv"
datos_camaras = (cargar_datos_camaras(csv_path, coordenadas_dict)
                 if os.path.exists(csv_path) else [])


# ─────────────────────────────────────────────────────────────
# MAPAS FOLIUM
# ─────────────────────────────────────────────────────────────
def crear_mapa_camaras(datos, shp_path):
    gdf = gpd.read_file(shp_path)
    gdf_baq = gdf[gdf['mpio_cnmbr'] == 'BARRANQUILLA']

    totals = [d['total'] for d in datos]
    mn, mx = min(totals), max(totals)
    for d in datos:
        d['radius'] = 5 + (d['total'] - mn) / max(mx - mn, 1) * 30

    top5_sorted = sorted(datos, key=lambda x: x['total'], reverse=True)[:5]
    top5 = {d['direccion'] for d in top5_sorted}

    m = folium.Map(location=[10.96854, -74.78132], zoom_start=12, tiles='cartodbpositron')
    folium.GeoJson(gdf_baq).add_to(m)

    fg = folium.FeatureGroup(name="Camaras", show=True)
    for d in datos:
        lat, lon = d['coordenadas']
        color = '#10b981' if d['direccion'] in top5 else '#818cf8'
        ph = f"<b>{d['direccion']}</b><br>Comparendos: {d['total']:,}"
        folium.CircleMarker(
            [lat, lon], radius=d['radius'], color=color, weight=1.5,
            fill=True, fill_color=color, fill_opacity=0.45,
            popup=folium.Popup(ph, max_width=250),
            tooltip=ph
        ).add_to(fg)
    fg.add_to(m)

    leyenda = (
        '<div style="position:fixed;bottom:20px;right:20px;border:1px solid #334155;z-index:9999;'
        'font-size:12px;background:#1e293b;color:#e2e8f0;padding:10px;border-radius:10px;'
        'font-family:Arial;max-height:260px;overflow-y:auto;">'
        '<b style="color:#93c5fd">Top 5 Camaras</b><hr style="border-color:#334155;margin:4px 0">'
        + ''.join(
            f'<div><span style="display:inline-block;width:10px;height:10px;background:#10b981;'
            f'border-radius:50%;margin-right:5px"></span><b>{i}. {c["direccion"]}:</b> {c["total"]:,}</div>'
            for i, c in enumerate(top5_sorted, 1))
        + '<hr style="border-color:#334155;margin:4px 0">'
        '<div><span style="display:inline-block;width:10px;height:10px;background:#818cf8;'
        'border-radius:50%;margin-right:5px"></span>Otras camaras</div></div>'
    )
    m.get_root().html.add_child(folium.Element(leyenda))

    return m


def crear_mapa_localidades(datos, geojson_path):
    gdf_loc = gpd.read_file(geojson_path).to_crs('EPSG:4326')
    for d in datos:
        punto = Point(d['coordenadas'][1], d['coordenadas'][0])
        idx = np.argmin([punto.distance(g) for g in gdf_loc['geometry']])
        d['localidad_asignada'] = gdf_loc.iloc[idx]['Localidad']
    loc_total, loc_cam, loc_det = {}, {}, {}
    for d in datos:
        loc = d['localidad_asignada']
        loc_total[loc] = loc_total.get(loc, 0) + d['total']
        loc_cam[loc] = loc_cam.get(loc, 0) + 1
        if loc not in loc_det:
            loc_det[loc] = {}
        for c, v in d['comparendos_por_codigo'].items():
            loc_det[loc][c] = loc_det[loc].get(c, 0) + v
    sorted_locs = sorted(loc_total.items(), key=lambda x: x[1])
    pal = sns.color_palette("Blues", n_colors=len(sorted_locs))
    colores = {loc: '#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255))
               for (loc, _), (r, g, b) in zip(sorted_locs, pal)}
    m = folium.Map(location=[10.96854, -74.78132], zoom_start=12, tiles='cartodbpositron')
    for _, row in gdf_loc.iterrows():
        loc = row['Localidad']
        if loc not in loc_total:
            continue
        ph = (f"<div style='font-family:Arial'><b>{loc}</b><hr>"
              f"<b>Total:</b> {loc_total[loc]:,}<br><b>Camaras:</b> {loc_cam[loc]}<hr>"
              f"<b>Por codigo:</b><br>"
              + ''.join(f"<b>{c}</b>: {int(v):,}<br>" for c, v in loc_det[loc].items())
              + "</div>")
        folium.GeoJson(row['geometry'],
                       style_function=lambda f, c=colores[loc]: {
                           'fillColor': c, 'color': '#1e293b', 'weight': 2, 'fillOpacity': 0.55},
                       popup=folium.Popup(ph, max_width=300),
                       tooltip=f"<b>{loc}</b><br>Comparendos: {loc_total[loc]:,}",
                       name=f"Localidad: {loc}").add_to(m)
    fg = folium.FeatureGroup(name="Camaras", overlay=True, control=True)
    top_cam = {}
    for d in datos:
        loc = d['localidad_asignada']
        if loc not in top_cam or d['total'] > top_cam[loc]['total']:
            top_cam[loc] = d
    top_dirs = {d['direccion'] for d in top_cam.values()}
    for d in datos:
        lat, lon = d['coordenadas']
        color = '#10b981' if d['direccion'] in top_dirs else '#818cf8'
        ph = (f"<div style='font-family:Arial;min-width:200px'><b>{d['direccion']}</b><hr>"
              f"<b>Total:</b> {d['total']:,}<hr><b>Por codigo:</b><br>"
              + ''.join(f"<b>{c}</b>: {int(v):,}<br>" for c, v in d['comparendos_por_codigo'].items())
              + "</div>")
        folium.CircleMarker([lat, lon], radius=5, color=color, weight=2,
                            fill=True, fill_color=color, fill_opacity=1,
                            popup=folium.Popup(ph, max_width=300),
                            tooltip=f"<b>{d['direccion']}</b><br>Comparendos: {d['total']:,}").add_to(fg)
    fg.add_to(m)
    colormap = cm.LinearColormap(
        colors=[list(pal[0]), list(pal[-1])],
        vmin=min(loc_total.values()), vmax=max(loc_total.values()),
        caption='Comparendos por Localidad')
    colormap.add_to(m)
    leyenda = (
        '<div style="position:fixed;bottom:20px;right:20px;border:1px solid #334155;z-index:9999;'
        'font-size:12px;background:#1e293b;color:#e2e8f0;padding:10px;border-radius:10px;'
        'box-shadow:0 4px 16px rgba(0,0,0,0.4);font-family:Arial;max-height:260px;overflow-y:auto;">'
        '<b style="color:#93c5fd">Comparendos por Localidad</b>'
        '<hr style="border-color:#334155;margin:4px 0">'
        + ''.join(
            f'<div style="margin-bottom:2px"><div style="display:inline-block;width:10px;height:10px;'
            f'background:{colores[l]};margin-right:5px;border:1px solid #475569"></div>'
            f'<b>{l}:</b> {v:,}</div>'
            for l, v in sorted(loc_total.items(), key=lambda x: x[1], reverse=True))
        + '</div>'
    )
    m.get_root().html.add_child(folium.Element(leyenda))
    folium.LayerControl().add_to(m)
    folium.plugins.MeasureControl().add_to(m)
    return m


# ─────────────────────────────────────────────────────────────
# TABLAS DE MÉTRICAS
# ─────────────────────────────────────────────────────────────
def mk(modelos, rmse, mae, mape, smape, mse):
    return pd.DataFrame({"Modelo": modelos, "RMSE": rmse, "MAE": mae,
                         "MAPE": mape, "SMAPE": smape, "MSE": mse})

M_C29 = ["Holt-Winters", "ARIMA(1,1,1)", "SARIMA(1,1,1)(1,0,0)[12]", "Theta (0.50)",
         "Ridge", "Lasso", "Random Forest", "XGBoost", "LightGBM", "KNN"]
M_C02 = ["Holt-Winters (SES)", "ARIMA(1,0,0)", "SARIMA(1,0,0)(0,1,1)[12]", "Theta (0.25)",
         "Ridge", "Lasso", "Random Forest", "XGBoost", "LightGBM", "KNN"]
M_C03 = ["Holt-Winters (SES)", "ARIMA(1,0,0)", "SARIMA(2,0,0)(1,0,0)[12]", "Theta (0.75)",
         "Ridge", "Lasso", "Random Forest", "XGBoost", "LightGBM", "KNN"]
M_D04 = ["Holt-Winters (SES)", "ARIMA(2,0,0)", "SARIMA(1,0,0)(0,0,0)[12]", "Theta (1.00)",
         "Ridge", "Lasso", "Random Forest", "XGBoost", "LightGBM", "KNN"]
M_C32 = ["Holt-Winters (SES)", "ARIMA(1,0,0)", "SARIMA(1,0,1)(0,0,0)[12]", "Theta (0.25)",
         "Ridge", "Lasso", "Random Forest", "XGBoost", "LightGBM", "KNN"]

def cv_c29(): return mk(M_C29,
    [792.78,747.58,729.01,782.15,951.16,901.40,846.80,835.56,772.18,899.37],
    [649.97,552.90,559.26,638.18,778.52,731.72,702.05,678.32,603.85,757.64],
    ["25.97%","23.27%","22.94%","24.42%","31.63%","29.98%","28.41%","27.79%","24.99%","30.11%"],
    ["22.01%","19.22%","19.40%","23.77%","24.72%","23.84%","23.67%","22.69%","20.59%","24.56%"],
    [636726.65,560851.18,543221.85,4079813.03,1077595.66,893013.59,740507.32,739211.48,608431.26,953569.69])

def test_c29(): return mk(M_C29,
    [479.43,804.70,740.59,1513.74,1724.24,1769.77,1671.37,1774.74,1659.20,1622.15],
    [405.89,738.88,700.91,1445.36,1704.32,1753.09,1647.96,1758.69,1638.42,1593.19],
    ["36.52%","63.54%","58.75%","107.29%","137.52%","140.95%","130.34%","140.33%","131.95%","128.35%"],
    ["28.19%","44.57%","42.95%","68.45%","78.43%","79.78%","76.72%","79.93%","76.61%","75.19%"],
    [229851.11,647538.70,548479.12,2291415.38,2973008.36,3132083.80,2793463.64,3149689.25,2752949.51,2631373.26])

def cv_c02(): return mk(M_C02,
    [873.85,736.38,765.33,1255.68,1362.07,1118.03,991.96,1017.59,923.30,1025.66],
    [792.58,663.38,668.16,1104.01,1198.25,1011.11,894.72,886.66,798.47,957.97],
    ["2835.02%","3104.53%","3083.27%","2617.77%","3207.28%","3687.94%","2619.72%","3090.16%","3672.10%","2952.14%"],
    ["44.18%","35.71%","36.47%","75.32%","73.58%","64.45%","51.49%","54.54%","42.64%","64.14%"],
    [988929.47,699811.34,756888.85,16769092.81,2437589.15,1472271.43,1161841.80,1162859.04,1014587.43,1196070.76])

def test_c02(): return mk(M_C02,
    [351.93,380.94,402.08,383.33,522.39,557.95,535.89,384.75,382.45,408.24],
    [280.29,325.41,353.72,307.51,477.87,511.89,421.74,283.23,321.24,322.30],
    ["13.67%","14.88%","15.66%","14.69%","20.37%","21.64%","21.37%","13.64%","15.21%","13.72%"],
    ["12.75%","14.79%","16.36%","14.20%","22.16%","23.91%","17.82%","12.89%","14.62%","14.91%"],
    [123854.16,145116.53,161669.03,146945.14,272890.85,311309.35,287179.21,148034.17,146268.63,166656.13])

def cv_c03(): return mk(M_C03,
    [768.51,687.63,680.40,730.63,887.76,803.00,784.06,696.88,784.23,943.90],
    [670.29,582.29,571.10,617.26,779.80,714.98,682.97,609.51,686.82,827.30],
    ["126.25%","273.97%","103.05%","186.13%","422.50%","427.83%","346.69%","383.77%","421.30%","388.04%"],
    ["79.21%","88.99%","92.70%","100.94%","123.42%","110.49%","100.29%","99.48%","108.60%","130.19%"],
    [901216.10,695880.96,812495.44,842378.66,1010664.12,872099.58,839586.82,731829.80,854458.57,1092456.43])

def test_c03(): return mk(M_C03,
    [499.66,440.12,421.36,679.18,410.50,665.53,519.62,516.97,536.22,443.21],
    [432.80,323.02,271.51,582.47,312.55,619.67,472.24,471.37,480.50,369.73],
    ["78.88%","48.84%","31.97%","102.04%","50.91%","115.48%","87.90%","82.00%","87.96%","65.25%"],
    ["50.45%","39.96%","34.16%","61.29%","38.90%","64.02%","53.39%","52.98%","54.38%","44.74%"],
    [249657.59,193703.73,177542.77,461282.50,168510.11,442936.80,270006.41,267262.36,287527.45,196435.76])

def cv_d04(): return mk(M_D04,
    [285.63,232.13,270.24,290.10,268.34,294.92,272.49,268.48,260.19,244.22],
    [237.59,196.18,225.43,244.83,231.65,265.40,241.08,240.61,229.52,212.02],
    ["45.48%","40.09%","37.90%","49.29%","43.09%","46.08%","45.98%","50.21%","47.69%","40.46%"],
    ["39.96%","34.18%","40.82%","43.56%","41.00%","51.05%","41.97%","40.78%","39.17%","36.98%"],
    [90992.73,55255.02,84260.76,88579.15,78102.01,110410.32,78496.25,74823.33,69966.77,61379.50])

def test_d04(): return mk(M_D04,
    [250.61,295.74,98.17,390.45,303.12,314.70,331.27,312.57,297.17,310.16],
    [235.12,281.03,77.92,351.20,288.11,294.83,310.22,295.66,279.47,290.97],
    ["111.22%","130.28%","37.39%","132.70%","132.22%","133.33%","141.30%","137.06%","130.98%","133.58%"],
    ["58.52%","65.49%","26.72%","73.07%","66.56%","67.07%","69.05%","67.43%","65.08%","66.69%"],
    [62805.11,87463.66,9636.56,152450.62,91880.80,99035.21,109739.14,97697.70,88308.78,96197.92])

def cv_c32(): return mk(M_C32,
    [19.23,16.12,18.08,19.38,17.63,15.92,19.51,20.54,18.39,20.97],
    [16.33,13.69,14.71,16.07,15.16,12.70,17.25,17.53,16.05,18.28],
    ["59.94%","57.22%","40.48%","57.62%","57.59%","46.63%","64.44%","66.52%","62.73%","66.81%"],
    ["47.60%","40.75%","49.98%","52.66%","44.59%","40.49%","50.97%","49.15%","46.22%","51.62%"],
    [378.84,326.87,420.95,2642.16,322.23,257.87,390.92,454.11,356.90,474.02])

def test_c32(): return mk(M_C32,
    [18.07,20.73,7.87,31.34,18.82,18.85,26.05,21.97,18.59,22.58],
    [16.15,18.80,6.61,29.02,17.15,17.28,24.08,20.40,16.30,20.73],
    ["207.37%","235.34%","88.69%","265.39%","214.60%","213.82%","286.61%","240.94%","218.21%","251.80%"],
    ["70.24%","75.98%","43.05%","94.72%","72.79%","73.22%","85.71%","79.64%","69.89%","79.80%"],
    [326.40,429.56,61.98,981.92,354.37,355.25,678.79,482.73,345.44,509.95])


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:12px 4px 20px 4px">
        <div style="font-family:'DM Serif Display',serif;font-size:1.1rem;color:#f8fafc;line-height:1.3">
            Comparendos<br>Electrónicos
        </div>
        <div style="font-size:0.70rem;color:#64748b;margin-top:4px;font-family:'DM Sans',sans-serif">
            Barranquilla &middot; 2018–2025
        </div>
    </div>
    """, unsafe_allow_html=True)

    seccion = st.radio("", [
        "Antecedentes y Problema",
        "Justificación",
        "Objetivos",
        "Marco Teórico",
        "Metodología",
        "Resultados",
        "Conclusiones"
    ])

    st.markdown("""
    <div style="margin-top:40px;padding-top:16px;border-top:1px solid #1e293b;
                font-size:0.70rem;color:#334155;font-family:'DM Sans',sans-serif">
        Universidad del Norte<br>
        Cristian Linero &middot; David Marquez
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# ENCABEZADO PRINCIPAL
# ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Dashboard Académico</div>', unsafe_allow_html=True)
st.title("Análisis y Modelado Predictivo de Comparendos Electrónicos")
st.markdown(
    '<div style="color:#94a3b8;font-size:0.88rem;margin-bottom:1.5rem">'
    'Barranquilla, 2018–2025 &nbsp;&middot;&nbsp; '
    '<span class="pill">Series Temporales</span>'
    '<span class="pill">Machine Learning</span>'
    '<span class="pill">Georreferenciación</span>'
    '</div>', unsafe_allow_html=True)
hr()


# ═════════════════════════════════════════════════════════════
# SECCIONES
# ═════════════════════════════════════════════════════════════

# ── ANTECEDENTES Y PROBLEMA ───────────────────────────────────
if seccion == "Antecedentes y Problema":
    st.header("Antecedentes")
    st.markdown("""
    El foto-comparendo se refiere a sanciones de tránsito impuestas mediante sistemas de fotodetección.
    Barranquilla cuenta con una robusta infraestructura (**aproximadamente 50 cámaras** en el periodo
    estudiado, en crecimiento). La base de datos pública contiene **cerca de 340 000 registros** (2018–2025).

    **Importancia de los datos:**
    - Permiten analizar patrones de comportamiento infractor.
    - Facilitan la identificación de zonas de alto riesgo.
    - Sirven de base para modelos predictivos que apoyen la toma de decisiones.

    **Contexto normativo:**
    - Ley 769 de 2002 (Código Nacional de Tránsito).
    - Resoluciones locales de la Secretaría de Movilidad de Barranquilla.
    - Implementación de fotodetección como medida disuasiva.

    **Evolución del sistema:**
    - 2018: inicio con cámaras fijas y móviles.
    - 2019: expansión a corredores viales principales.
    - 2025: incorporación de cámaras tipo Carril Bus.
    """)
    hr()
    st.header("Problema")
    st.markdown("""
    La accidentalidad y el incumplimiento de normas de tránsito afectan la seguridad vial en Barranquilla.
    Aunque las cámaras tienen un efecto disuasivo, **se desconoce el comportamiento futuro** y no se ha
    realizado una **comparativa sistemática de modelos predictivos** en este contexto local.

    **Preguntas de investigación:**
    1. ¿Qué patrones temporales y espaciales presentan las infracciones?
    2. ¿Qué modelo predictivo (clásico o ML) se adapta mejor a cada tipo de infracción?
    3. ¿Cómo evolucionarán las infracciones en 2026?
    """)


# ── JUSTIFICACIÓN ─────────────────────────────────────────────
elif seccion == "Justificación":
    st.header("Justificación")
    st.markdown("""
    **Importancia práctica:**
    - Las autoridades necesitan anticipar patrones para **diseñar intervenciones efectivas**.
    - Este estudio aporta una **comparación rigurosa de 10 modelos** aplicados a datos reales.
    - Los **pronósticos para 2026** permitirán planificar recursos y presupuestos.

    **Aporte académico:**
    - Primera comparativa de este tipo en Colombia para datos de fotodetección.
    - Metodología reproducible y adaptable a otras ciudades.
    - Validación de que **modelos simples pueden superar a complejos** ante cambios estructurales.

    **Impacto social:**
    - Reducción de siniestros viales y salvaguarda de peatones, ciclistas y conductores.
    - Uso eficiente de recursos públicos basado en evidencia.
    """)


# ── OBJETIVOS ─────────────────────────────────────────────────
elif seccion == "Objetivos":
    st.header("Objetivos del Estudio")
    st.markdown("""
    **Objetivo general**
    Analizar las infracciones registradas en Barranquilla (2018–2025) y evaluar la capacidad predictiva
    de diversos modelos.

    **Objetivos específicos**
    1. Caracterizar la frecuencia, proporción y distribución espacial de las infracciones.
    2. Evaluar los patrones de tendencia y estacionalidad en las series temporales.
    3. Implementar y comparar modelos estadísticos clásicos y de aprendizaje automático.
    """)


# ── MARCO TEÓRICO ─────────────────────────────────────────────
elif seccion == "Marco Teórico":
    st.header("Marco Teórico")
    st.markdown("""
    **Métricas de evaluación**
    - **MSE:** Promedio de los errores al cuadrado. Penaliza más los errores grandes.
    - **RMSE:** Raíz cuadrada del MSE. Interpretable en las unidades originales.
    - **MAE:** Promedio de las diferencias absolutas. Menos sensible a outliers.
    - **MAPE:** Error porcentual absoluto medio.
    - **SMAPE:** Versión simétrica del MAPE, evita asimetrías cuando el valor real es cercano a cero.

    **Descomposición STL**
    Separa una serie temporal en tres componentes: tendencia (T_t), estacionalidad (S_t) y residuos (R_t):
    `Y_t = T_t + S_t + R_t`

    **Pruebas estadísticas**
    - **ADF (Dickey-Fuller Aumentada):** Evalúa estacionariedad.
    - **Ljung-Box:** Evalúa autocorrelación en residuos (H₀: ruido blanco).
    - **Shapiro-Wilk:** Prueba de normalidad.
    - **Levene:** Homogeneidad de varianzas.
    - **ANOVA / Kruskal-Wallis / Mann-Whitney U:** Comparación de grupos.

    **Modelos implementados**
    - **Clásicos:** Holt-Winters, ARIMA/SARIMA, Dynamic Optimized Theta.
    - **Regularización:** Ridge (L2) y Lasso (L1).
    - **Árboles:** Random Forest, XGBoost, LightGBM.
    - **Basado en similitud:** K-Nearest Neighbors (KNN).
    """)


# ═════════════════════════════════════════════════════════════
# METODOLOGÍA
# ═════════════════════════════════════════════════════════════
elif seccion == "Metodología":
    st.header("Metodología")

    # ══════════════════════════════════════════════════════════
    # ANÁLISIS UNIVARIADO
    # ══════════════════════════════════════════════════════════
    with st.expander("Análisis Univariado", expanded=True):

        # Tipo de cámara
        slabel("Distribución de Comparendos Electrónicos por Tipo de Cámara y Proporción por Tipo de Cámara")
        stag("chart")
        img("proporcion_tipo_camaras.png",
                "Distribución de Comparendos por Tipo de Cámara")
        hr()

        # Infracción
        slabel("Distribución de Comparendos Electrónicos por Infracción")
        stag("chart")
        img("comparendos_por_infraccion.png",
            "Distribución de Comparendos Electrónicos por Infracción")
        hr()

        # Servicio del vehículo
        slabel("Distribución y Proporción por Servicio del Vehículo")
        stag("chart")
        img("comparendos_por_serivicio.png",
                "Distribución de Comparendos por Servicio del Vehículo")
        hr()

        # Clase del vehículo
        slabel("Distribución de Comparendos Electrónicos por Clase del Vehículo")
        stag("chart")
        img("comparendos_por_tipo_vehiculo.png",
            "Distribución de Comparendos por Clase del Vehículo")
        hr()

        # Cámara de mal parqueo
        slabel("Distribución de Comparendos Electrónicos por Cámara de Mal Parqueo")
        stag("chart")
        img("distribucion_camaras_moviles.png",
            "Distribución por Cámara de Mal Parqueo")
        hr()

        # Top 5 cámaras
        slabel("Top 5 de la Distribución de Comparendos Electrónicos por Cámara con Dirección")
        stag("chart")
        img("distribucion_camaras_fijas.png",
            "Top 5 – Cámara con Dirección")
        hr()

        # Evolución mensual
        slabel("Evolución Mensual de Comparendos Electrónicos")
        stag("chart")
        img("comparendos_por_mes.png", "Evolución Mensual de Comparendos Electrónicos")
        hr()

        # Por mes + resultados
        slabel("Distribución de Comparendos Electrónicos por Mes")
        col1, col2 = st.columns(2)
        with col1:
            stag("chart")
            img("boxplot_infracciones_mes.png",
                "Distribución de Comparendos por Mes")
        with col2:
            stag("result")
            results(
                '<span class="hdr">Prueba de Normalidad (Shapiro-Wilk)</span>\n'
                'Enero:      p = 4.4047e-01  <span class="ok">Normal</span>\n'
                'Febrero:    p = 6.0271e-01  <span class="ok">Normal</span>\n'
                'Marzo:      p = 5.8562e-01  <span class="ok">Normal</span>\n'
                'Abril:      p = 7.3115e-01  <span class="ok">Normal</span>\n'
                'Mayo:       p = 5.6190e-01  <span class="ok">Normal</span>\n'
                'Junio:      p = 2.0412e-01  <span class="ok">Normal</span>\n'
                'Julio:      p = 6.7018e-01  <span class="ok">Normal</span>\n'
                'Agosto:     p = 4.4654e-01  <span class="ok">Normal</span>\n'
                'Septiembre: p = 8.2598e-01  <span class="ok">Normal</span>\n'
                'Octubre:    p = 5.7897e-02  <span class="ok">Normal</span>\n'
                'Noviembre:  p = 5.8083e-01  <span class="ok">Normal</span>\n'
                'Diciembre:  p = 5.6147e-01  <span class="ok">Normal</span>\n'
                '<span class="ok">Normalidad en todos los meses: Si</span>\n\n'
                'Levene p = 3.5003e-01  <span class="ok">Varianzas iguales: Si</span>\n'
                '<span class="ok">Supuestos cumplidos → ANOVA</span>\n\n'
                'Estadistico F: 0.2150\n'
                'P-valor:       9.9615e-01\n'
                '<span class="ok">Estacionalidad: No\n'
                'Diferencias entre meses: No</span>'
            )
        hr()

        # Por día de semana + resultados
        slabel("Distribución de Comparendos Electrónicos por Día de la Semana")
        col1, col2 = st.columns(2)
        with col1:
            stag("chart")
            img("boxplot_dias_semana.png",
                "Distribución por Día de la Semana")
        with col2:
            stag("result")
            results(
                '<span class="hdr">Prueba de Normalidad (Shapiro-Wilk)</span>\n'
                'Lunes:     p = 6.6881e-02  <span class="ok">Normal</span>\n'
                'Martes:    p = 2.7028e-02  <span class="fail">No normal</span>\n'
                'Miercoles: p = 1.5207e-03  <span class="fail">No normal</span>\n'
                'Jueves:    p = 2.9750e-03  <span class="fail">No normal</span>\n'
                'Viernes:   p = 5.4349e-01  <span class="ok">Normal</span>\n'
                'Sabado:    p = 4.5476e-01  <span class="ok">Normal</span>\n'
                'Domingo:   p = 2.5946e-01  <span class="ok">Normal</span>\n'
                '<span class="fail">Normalidad en todos los dias: No</span>\n\n'
                'Levene p = 6.0183e-04  <span class="fail">Varianzas iguales: No</span>\n'
                '<span class="warn">Supuestos no cumplidos → Kruskal-Wallis</span>\n\n'
                'Estadistico H: 131.1884\n'
                'P-valor:       7.2235e-26\n'
                '<span class="ok">Diferencias por dia de semana: Si\n'
                'Diferencias significativas entre dias: Si</span>\n\n'
                '<span class="hdr">Post-hoc Dunn (Bonferroni)</span>\n'
                'Domingo difiere significativamente del resto.'
            )
        hr()

        # Tipo cámara y día + resultados
        slabel("Total y Proporción de Infracciones por Tipo de Cámara y Día")
        col1, col2 = st.columns(2)
        with col1:
            stag("chart")
            img("propor_tipo_camara_dia.png",
                "Infracciones por Tipo de Cámara y Día")
        with col2:
            stag("result")
            results(
                '<span class="hdr">Prueba de Normalidad (Shapiro-Wilk)</span>\n'
                'Domingo: W=0.9967, p=5.7101e-01  <span class="ok">Normal</span>\n'
                'Resto:   W=0.9659, p=7.9722e-24  <span class="fail">No normal</span>\n\n'
                '<span class="hdr">Mann-Whitney U</span>\n'
                'H0: Infracciones domingo <= resto de dias\n'
                'H1: Infracciones domingo > resto de dias\n'
                'Estadistico U: 731 115.5\n'
                'P-valor (unilateral): 7.4871e-43\n'
                '<span class="ok">Conclusion: Domingo es significativamente mayor</span>\n\n'
                '<span class="hdr">Estadisticos Descriptivos</span>\n'
                'Domingo: media=177  mediana=176  n=414\n'
                'Resto:   media=134  mediana=130  n=2489'
            )

    # ══════════════════════════════════════════════════════════
    # ANÁLISIS BIVARIADO
    # ══════════════════════════════════════════════════════════
    with st.expander("Análisis Bivariado", expanded=True):

        slabel("Distribución de Comparendos Electrónicos por Código de Infracción y Tipo de Cámara")
        stag("chart")
        img("codigo_inf_vs_tipo_camara.png",
            "Comparendos por Código de Infracción y Tipo de Cámara")
        hr()

        slabel("Distribución de Comparendos por Servicio del Vehículo y Código de Infracción")
        stag("chart")
        img("codigo_vs_servicio.png",
            "Comparendos por Servicio del Vehículo y Código de Infracción")
        hr()

        slabel("Distribución de Comparendos por Clase del Vehículo y Código de Infracción")
        stag("chart")
        img("codigo_vs_tipo.png",
            "Comparendos por Clase del Vehículo y Código de Infracción")
        hr()

        slabel("Evolución Mensual de Comparendos Electrónicos por Tipo de Cámara")
        stag("chart")
        img("evoc_mensual_vs_tipo_camara.png",
            "Evolución Mensual por Tipo de Cámara")
        hr()

        # Cámara Fija mensual + resultados
        slabel("Distribución de Comparendos Electrónicos por Mes – Cámara Fijo")
        col1, col2 = st.columns(2)
        with col1:
            stag("chart")
            img("boxplot_mensual_camara_fija.png",
                "Distribución por Mes – Cámara Fijo")
        with col2:
            stag("result")
            results(
                '<span class="hdr">Prueba de Normalidad (Shapiro-Wilk)</span>\n'
                'Enero:      p = 5.6635e-01  <span class="ok">Normal</span>\n'
                'Febrero:    p = 6.8655e-01  <span class="ok">Normal</span>\n'
                'Marzo:      p = 8.7740e-01  <span class="ok">Normal</span>\n'
                'Abril:      p = 4.5477e-01  <span class="ok">Normal</span>\n'
                'Mayo:       p = 2.9897e-01  <span class="ok">Normal</span>\n'
                'Junio:      p = 1.4495e-01  <span class="ok">Normal</span>\n'
                'Julio:      p = 2.6510e-01  <span class="ok">Normal</span>\n'
                'Agosto:     p = 9.4652e-01  <span class="ok">Normal</span>\n'
                'Septiembre: p = 5.5549e-01  <span class="ok">Normal</span>\n'
                'Octubre:    p = 3.2284e-01  <span class="ok">Normal</span>\n'
                'Noviembre:  p = 9.9640e-01  <span class="ok">Normal</span>\n'
                'Diciembre:  p = 9.8976e-01  <span class="ok">Normal</span>\n'
                '<span class="ok">Normalidad en todos los meses: Si</span>\n\n'
                'Levene p = 3.1942e-01  <span class="ok">Varianzas iguales: Si</span>\n'
                '<span class="ok">Supuestos cumplidos → ANOVA</span>\n\n'
                'Estadistico F: 0.2820\n'
                'P-valor:       9.8770e-01\n'
                '<span class="ok">Diferencias entre meses: No</span>'
            )
        hr()

        # Cámara Móvil mensual + resultados
        slabel("Distribución de Comparendos Electrónicos por Mes – Cámara Móvil")
        col1, col2 = st.columns(2)
        with col1:
            stag("chart")
            img("boxplot_mensual_camara_movil.png",
                "Distribución por Mes – Cámara Móvil")
        with col2:
            stag("result")
            results(
                '<span class="hdr">Prueba de Normalidad (Shapiro-Wilk)</span>\n'
                'Enero:      p = 5.1447e-01  <span class="ok">Normal</span>\n'
                'Febrero:    p = 8.2329e-01  <span class="ok">Normal</span>\n'
                'Marzo:      p = 4.2095e-01  <span class="ok">Normal</span>\n'
                'Abril:      p = 1.0021e-01  <span class="ok">Normal</span>\n'
                'Mayo:       p = 9.5293e-01  <span class="ok">Normal</span>\n'
                'Junio:      p = 5.6304e-01  <span class="ok">Normal</span>\n'
                'Julio:      p = 4.4217e-01  <span class="ok">Normal</span>\n'
                'Agosto:     p = 7.8314e-01  <span class="ok">Normal</span>\n'
                'Septiembre: p = 8.0455e-01  <span class="ok">Normal</span>\n'
                'Octubre:    p = 7.1071e-01  <span class="ok">Normal</span>\n'
                'Noviembre:  p = 8.1396e-01  <span class="ok">Normal</span>\n'
                'Diciembre:  p = 7.9826e-01  <span class="ok">Normal</span>\n'
                '<span class="ok">Normalidad en todos los meses: Si</span>\n\n'
                'Levene p = 9.6198e-01  <span class="ok">Varianzas iguales: Si</span>\n'
                '<span class="ok">Supuestos cumplidos → ANOVA</span>\n\n'
                'Estadistico F: 0.3436\n'
                'P-valor:       9.7274e-01\n'
                '<span class="ok">Diferencias entre meses: No</span>'
            )

    # ══════════════════════════════════════════════════════════
    # GEORREFERENCIACIÓN
    # ══════════════════════════════════════════════════════════
    with st.expander("Georreferenciación", expanded=True):
        slabel("Visualización Geoespacial de Cámaras de Fotodetección en Barranquilla")
        stag("map")
        shp = "datos/MGN_ADM_MPIO_GRAFICO.shp"
        if os.path.exists(shp) and datos_camaras:
            folium_static(crear_mapa_camaras(datos_camaras, shp), width=1050, height=620)
        else:
            st.warning("Shapefile no encontrado o sin datos de cámaras.")
        hr()

        slabel("Visualización de la Distribución de Comparendos Electrónicos por Localidad de Barranquilla")
        stag("map")
        geo = "datos/localidades.geojson"
        if os.path.exists(geo) and datos_camaras:
            folium_static(crear_mapa_localidades(datos_camaras, geo), width=1050, height=620)
        else:
            st.warning("GeoJSON no encontrado o sin datos de cámaras.")
    # ══════════════════════════════════════════════════════════
    # DESCOMPOSICIÓN TEMPORAL
    # ══════════════════════════════════════════════════════════
    with st.expander("Descomposición Temporal (STL)", expanded=True):

        # ─── C29 ───────────────────────────────────────────────
        st.markdown("#### Código C29 – Exceso de velocidad")
        slabel("Tendencia de Comparendos – Código C29")
        col1, col2 = st.columns(2)
        with col1:
            stag("chart")
            img("tendencia_c29.png", "Tendencia – C29")
        with col2:
            stag("result")
            results(
                'Pendiente: <span class="fail">-18.9062</span> comparendos/mes\n'
                'R²: 0.5793\n\n'
                'P-valor tendencia: 2.2758e-19\n'
                '<span class="ok">Tendencia significativa: Si</span>'
            )

        slabel("Estacionalidad de Comparendos – Código C29")
        col1, col2 = st.columns(2)
        with col1:
            stag("chart")
            img("estacionalidad_c29.png", "Estacionalidad – C29")
        with col2:
            stag("result")
            results(
                'Amplitud estacional: 1 321.8176 comparendos\n'
                'Variabilidad explicada: 5.6552%\n\n'
                '<span class="hdr">ADF – Serie original</span>\n'
                'Estadistico: -2.1101   P-valor: 2.4046e-01\n'
                'Criticos: 1%=-3.5019  5%=-2.8928  10%=-2.5835\n'
                '<span class="fail">Serie original: NO estacionaria</span>\n\n'
                '<span class="hdr">ADF – Residuos</span>\n'
                'Estadistico: -6.4165   P-valor: 1.8358e-08\n'
                'Criticos: 1%=-3.5011  5%=-2.8925  10%=-2.5833\n'
                '<span class="ok">Residuos: estacionarios</span>\n\n'
                '<span class="ok">→ STL capturo correctamente tendencia y estacionalidad</span>'
            )

        slabel("Residuos de Comparendos – Código C29")
        col1, col2 = st.columns(2)
        with col1:
            stag("chart")
            img("residuos_c29.png", "Residuos – C29")
        with col2:
            stag("result")
            results(
                '<span class="hdr">Prueba Ljung-Box</span>\n'
                'Lag  6: lb_stat=25.0726  p=3.31e-04\n'
                'Lag 12: lb_stat=36.4836  p=2.71e-04\n'
                'Lag 18: lb_stat=46.2694  p=2.71e-04\n'
                '<span class="fail">Residuos ruido blanco: No</span>\n\n'
                'Prueba t (media cero) p=4.1680e-01\n'
                '<span class="ok">Centrados en cero: Si</span>\n\n'
                'Shapiro-Wilk p=3.3907e-09\n'
                '<span class="fail">Residuos normales: No</span>'
            )

        slabel("Distribución de Residuos – Código C29")
        stag("chart")
        img("distribucion_residuos_c29.png", "Distribución de Residuos – C29")
        hr()

        # ─── C02 ───────────────────────────────────────────────
        st.markdown("#### Código C02 – Estacionamiento prohibido")
        slabel("Tendencia de Comparendos – Código C02")
        col1, col2 = st.columns(2)
        with col1:
            stag("chart")
            img("tendencia_c02.png", "Tendencia – C02")
        with col2:
            stag("result")
            results(
                'Pendiente: -2.0906 comparendos/mes\n'
                'R²: 0.0125\n\n'
                'P-valor tendencia: 2.7847e-01\n'
                '<span class="warn">Tendencia significativa: No</span>'
            )

        slabel("Estacionalidad de Comparendos – Código C02")
        col1, col2 = st.columns(2)
        with col1:
            stag("chart")
            img("estacionalidad_c02.png", "Estacionalidad – C02")
        with col2:
            stag("result")
            results(
                'Amplitud estacional: 1 100.6443 comparendos\n'
                'Variabilidad explicada: 5.1749%\n\n'
                '<span class="hdr">ADF – Serie original</span>\n'
                'Estadistico: -3.5602   P-valor: 6.5685e-03\n'
                'Criticos: 1%=-3.5011  5%=-2.8925  10%=-2.5833\n'
                '<span class="ok">Serie original: estacionaria</span>\n\n'
                '<span class="hdr">ADF – Residuos</span>\n'
                'Estadistico: -4.5151   P-valor: 1.8461e-04\n'
                'Criticos: 1%=-3.5011  5%=-2.8925  10%=-2.5833\n'
                '<span class="ok">Residuos: estacionarios</span>\n\n'
                '<span class="ok">→ Serie original y residuos son estacionarios</span>'
            )

        slabel("Residuos de Comparendos – Código C02")
        col1, col2 = st.columns(2)
        with col1:
            stag("chart")
            img("residuos_c02.png", "Residuos – C02")
        with col2:
            stag("result")
            results(
                '<span class="hdr">Prueba Ljung-Box</span>\n'
                'Lag  6: lb_stat=63.7624  p=7.72e-12\n'
                'Lag 12: lb_stat=101.8207 p=2.45e-16\n'
                'Lag 18: lb_stat=111.7505 p=1.48e-15\n'
                '<span class="fail">Residuos ruido blanco: No</span>\n\n'
                'Prueba t (media cero) p=2.7945e-01\n'
                '<span class="ok">Centrados en cero: Si</span>\n\n'
                'Shapiro-Wilk p=5.6708e-09\n'
                '<span class="fail">Residuos normales: No</span>'
            )

        slabel("Distribución de Residuos – Código C02")
        stag("chart")
        img("distribucion_residuos_c02.png", "Distribución de Residuos – C02")
        hr()

        # ─── C03 ───────────────────────────────────────────────
        st.markdown("#### Código C03 – Bloquear calzada")
        slabel("Tendencia de Comparendos – Código C03")
        col1, col2 = st.columns(2)
        with col1:
            stag("chart")
            img("tendencia_c03.png", "Tendencia – C03")
        with col2:
            stag("result")
            results(
                'Pendiente: <span class="ok">+10.3194</span> comparendos/mes\n'
                'R²: 0.5151\n\n'
                'P-valor tendencia: 1.8978e-16\n'
                '<span class="ok">Tendencia significativa: Si (creciente)</span>'
            )

        slabel("Estacionalidad de Comparendos – Código C03")
        col1, col2 = st.columns(2)
        with col1:
            stag("chart")
            img("estacionalidad_c03.png", "Estacionalidad – C03")
        with col2:
            stag("result")
            results(
                'Amplitud estacional: 1 507.8096 comparendos\n'
                'Variabilidad explicada: 10.9346%\n\n'
                '<span class="hdr">ADF – Serie original</span>\n'
                'Estadistico: -3.2061   P-valor: 1.9636e-02\n'
                'Criticos: 1%=-3.5011  5%=-2.8925  10%=-2.5833\n'
                '<span class="ok">Serie original: estacionaria</span>\n\n'
                '<span class="hdr">ADF – Residuos</span>\n'
                'Estadistico: -2.8452   P-valor: 5.2103e-02\n'
                'Criticos: 1%=-3.5088  5%=-2.8958  10%=-2.5850\n'
                '<span class="fail">Residuos: NO estacionarios</span>\n\n'
                '<span class="warn">→ Descomposicion no elimino toda la no estacionariedad</span>'
            )

        slabel("Residuos de Comparendos – Código C03")
        col1, col2 = st.columns(2)
        with col1:
            stag("chart")
            img("residuos_c03.png", "Residuos – C03")
        with col2:
            stag("result")
            results(
                '<span class="hdr">Prueba Ljung-Box</span>\n'
                'Lag  6: lb_stat=75.9732  p=2.42e-14\n'
                'Lag 12: lb_stat=84.4605  p=5.78e-13\n'
                'Lag 18: lb_stat=97.7879  p=5.62e-13\n'
                '<span class="fail">Residuos ruido blanco: No</span>\n\n'
                'Prueba t (media cero) p=5.9627e-03\n'
                '<span class="fail">Centrados en cero: No</span>\n\n'
                'Shapiro-Wilk p=1.4336e-11\n'
                '<span class="fail">Residuos normales: No</span>'
            )

        slabel("Distribución de Residuos – Código C03")
        stag("chart")
        img("distribucion_residuos_c03.png", "Distribución de Residuos – C03")
        hr()

        # ─── D04 ───────────────────────────────────────────────
        st.markdown("#### Código D04 – No detenerse ante semáforo rojo")
        slabel("Tendencia de Comparendos – Código D04")
        col1, col2 = st.columns(2)
        with col1:
            stag("chart")
            img("tendencia_d04.png", "Tendencia – D04")
        with col2:
            stag("result")
            results(
                'Pendiente: <span class="fail">-2.1003</span> comparendos/mes\n'
                'R²: 0.1403\n\n'
                'P-valor tendencia: 1.7046e-04\n'
                '<span class="ok">Tendencia significativa: Si (decreciente)</span>'
            )

        slabel("Estacionalidad de Comparendos – Código D04")
        col1, col2 = st.columns(2)
        with col1:
            stag("chart")
            img("estacionalidad_d04.png", "Estacionalidad – D04")
        with col2:
            stag("result")
            results(
                'Amplitud estacional: 598.3417 comparendos\n'
                'Variabilidad explicada: <span class="ok">25.8901%</span> (mas alta del analisis)\n\n'
                '<span class="hdr">ADF – Serie original</span>\n'
                'Estadistico: -4.4109   P-valor: 2.8387e-04\n'
                'Criticos: 1%=-3.5011  5%=-2.8925  10%=-2.5833\n'
                '<span class="ok">Serie original: estacionaria</span>\n\n'
                '<span class="hdr">ADF – Residuos</span>\n'
                'Estadistico: -7.9684   P-valor: 2.8244e-12\n'
                'Criticos: 1%=-3.5011  5%=-2.8925  10%=-2.5833\n'
                '<span class="ok">Residuos: estacionarios</span>\n\n'
                '<span class="ok">→ Serie original y residuos son estacionarios</span>'
            )

        slabel("Residuos de Comparendos – Código D04")
        col1, col2 = st.columns(2)
        with col1:
            stag("chart")
            img("residuos_d04.png", "Residuos – D04")
        with col2:
            stag("result")
            results(
                '<span class="hdr">Prueba Ljung-Box</span>\n'
                'Lag  6: lb_stat=5.1894  p=0.5198\n'
                'Lag 12: lb_stat=15.6806 p=0.2063\n'
                'Lag 18: lb_stat=16.9703 p=0.5252\n'
                '<span class="ok">Residuos ruido blanco: Si</span>\n\n'
                'Prueba t (media cero) p=9.5766e-01\n'
                '<span class="ok">Centrados en cero: Si</span>\n\n'
                'Shapiro-Wilk p=1.3525e-06\n'
                '<span class="fail">Residuos normales: No</span>'
            )

        slabel("Distribución de Residuos – Código D04")
        stag("chart")
        img("distribucion_residuos_d04.png", "Distribución de Residuos – D04")
        hr()

        # ─── C32 ───────────────────────────────────────────────
        st.markdown("#### Código C32 – No respetar paso de peatones")
        slabel("Tendencia de Comparendos – Código C32")
        col1, col2 = st.columns(2)
        with col1:
            stag("chart")
            img("tendencia_c32.png", "Tendencia – C32")
        with col2:
            stag("result")
            results(
                'Pendiente: -0.0389 comparendos/mes\n'
                'R²: 0.0127\n\n'
                'P-valor tendencia: 2.7430e-01\n'
                '<span class="warn">Tendencia significativa: No</span>'
            )

        slabel("Estacionalidad de Comparendos – Código C32")
        col1, col2 = st.columns(2)
        with col1:
            stag("chart")
            img("estacionalidad_c32.png", "Estacionalidad – C32")
        with col2:
            stag("result")
            results(
                'Amplitud estacional: 35.8702 comparendos\n'
                'Variabilidad explicada: 10.7016%\n\n'
                '<span class="hdr">ADF – Serie original</span>\n'
                'Estadistico: -3.2768   P-valor: 1.5947e-02\n'
                'Criticos: 1%=-3.5019  5%=-2.8928  10%=-2.5835\n'
                '<span class="ok">Serie original: estacionaria</span>\n\n'
                '<span class="hdr">ADF – Residuos</span>\n'
                'Estadistico: -3.4300   P-valor: 9.9776e-03\n'
                'Criticos: 1%=-3.5027  5%=-2.8932  10%=-2.5836\n'
                '<span class="ok">Residuos: estacionarios</span>\n\n'
                '<span class="ok">→ Serie original y residuos son estacionarios</span>'
            )

        slabel("Residuos de Comparendos – Código C32")
        col1, col2 = st.columns(2)
        with col1:
            stag("chart")
            img("residuos_c32.png", "Residuos – C32")
        with col2:
            stag("result")
            results(
                '<span class="hdr">Prueba Ljung-Box</span>\n'
                'Lag  6: lb_stat=58.0164  p=1.14e-10\n'
                'Lag 12: lb_stat=63.3545  p=5.48e-09\n'
                'Lag 18: lb_stat=69.0569  p=6.52e-08\n'
                '<span class="fail">Residuos ruido blanco: No</span>\n\n'
                'Prueba t (media cero) p=3.2421e-02\n'
                '<span class="fail">Centrados en cero: No</span>\n\n'
                'Shapiro-Wilk p=7.8795e-12\n'
                '<span class="fail">Residuos normales: No</span>'
            )

        slabel("Distribución de Residuos – Código C32")
        stag("chart")
        img("distribucion_residuos_c32.png", "Distribución de Residuos – C32")

    # ══════════════════════════════════════════════════════════
    # MODELADO PREDICTIVO – C29
    # ══════════════════════════════════════════════════════════
    with st.expander("Modelado Predictivo de la Infracción C29 – Exceso de velocidad", expanded=True):
        best_model("Holt-Winters con tendencia amortiguada")

        slabel("Tabla 1 – Métricas Promedio en Validación Cruzada")
        stag("table")
        st.dataframe(cv_c29(), use_container_width=True, hide_index=True)

        slabel("Tabla 2 – Métricas en Test (2025)")
        stag("table")
        st.dataframe(test_c29(), use_container_width=True, hide_index=True)

        col1, col2 = st.columns(2)
        with col1:
            stag("chart")
            img("c29_holt_prediccion_vs_real.png",
                "C29 – Holt con tendencia amortiguada: Predicción vs Real")
        with col2:
            stag("chart")
            img("c29_holt_prediccion_2026.png",
                "C29 – Holt con tendencia amortiguada: Predicción 2026")

    # ══════════════════════════════════════════════════════════
    # MODELADO PREDICTIVO – C02
    # ══════════════════════════════════════════════════════════
    with st.expander("Modelado Predictivo de la Infracción C02 – Estacionamiento prohibido", expanded=True):
        best_model("Holt-Winters SES (Suavización Exponencial Simple)")

        slabel("Tabla 1 – Métricas Promedio en Validación Cruzada")
        stag("table")
        st.dataframe(cv_c02(), use_container_width=True, hide_index=True)

        slabel("Tabla 2 – Métricas en Test (2025)")
        stag("table")
        st.dataframe(test_c02(), use_container_width=True, hide_index=True)

        col1, col2 = st.columns(2)
        with col1:
            stag("chart")
            img("c02_ses_prediccion_vs_real.png",
                "C02 – SES (Simple): Predicción vs Real")
        with col2:
            stag("chart")
            img("c02_ses_prediccion_2026.png",
                "C02 – Suavización Exponencial Simple (SES): Predicción 2026")

    # ══════════════════════════════════════════════════════════
    # MODELADO PREDICTIVO – C03
    # ══════════════════════════════════════════════════════════
    with st.expander("Modelado Predictivo de la Infracción C03 – Bloquear calzada", expanded=True):
        best_model("Ridge Regression")

        slabel("Tabla 1 – Métricas Promedio en Validación Cruzada")
        stag("table")
        st.dataframe(cv_c03(), use_container_width=True, hide_index=True)

        slabel("Tabla 2 – Métricas en Test (2025)")
        stag("table")
        st.dataframe(test_c03(), use_container_width=True, hide_index=True)

        col1, col2 = st.columns(2)
        with col1:
            stag("chart")
            img("c03_ridge_prediccion_vs_real.png",
                "C03 – Ridge Regression: Predicción vs Real")
        with col2:
            stag("chart")
            img("c03_ridge_prediccion_2026.png",
                "C03 – Ridge Regression: Predicción 2026")

    # ══════════════════════════════════════════════════════════
    # MODELADO PREDICTIVO – D04
    # ══════════════════════════════════════════════════════════
    with st.expander("Modelado Predictivo de la Infracción D04 – Semáforo rojo", expanded=True):
        best_model("SARIMA(1,0,0)(0,0,0)[12]")

        slabel("Tabla 1 – Métricas Promedio en Validación Cruzada")
        stag("table")
        st.dataframe(cv_d04(), use_container_width=True, hide_index=True)

        slabel("Tabla 2 – Métricas en Test (2025)")
        stag("table")
        st.dataframe(test_d04(), use_container_width=True, hide_index=True)

        col1, col2 = st.columns(2)
        with col1:
            stag("chart")
            img("d04_sarima_prediccion_vs_real.png",
                "D04 – SARIMA(1,0,0)(0,0,0)[12]: Predicción vs Real")
        with col2:
            stag("chart")
            img("d04_sarima_prediccion_2026.png",
                "D04 – SARIMA(1,0,0)(0,0,0)[12]: Predicción 2026")

    # ══════════════════════════════════════════════════════════
    # MODELADO PREDICTIVO – C32
    # ══════════════════════════════════════════════════════════
    with st.expander("Modelado Predictivo de la Infracción C32 – Paso de peatones", expanded=True):
        best_model("SARIMA(1,0,1)(0,0,0)[12]")

        slabel("Tabla 1 – Métricas Promedio en Validación Cruzada")
        stag("table")
        st.dataframe(cv_c32(), use_container_width=True, hide_index=True)

        slabel("Tabla 2 – Métricas en Test (2025)")
        stag("table")
        st.dataframe(test_c32(), use_container_width=True, hide_index=True)

        col1, col2 = st.columns(2)
        with col1:
            stag("chart")
            img("c32_sarima_prediccion_vs_real.png",
                "C32 – SARIMA(1,0,1)(0,0,0)[12]: Predicción vs Real")
        with col2:
            stag("chart")
            img("c32_sarima_prediccion_2026.png",
                "C32 – SARIMA(1,0,1)(0,0,0)[12]: Predicción 2026")


# ── RESULTADOS ────────────────────────────────────────────────
elif seccion == "Resultados":
    st.header("Síntesis de Resultados Relevantes")

    st.markdown("#### Distribución de infracciones")
    st.markdown("""
    - **C29 (exceso de velocidad):** 46.35% del total — principal problema.
    - **C02 (estacionamiento prohibido):** 33.36% — problema persistente.
    - **C03 (bloqueo de calzada):** 10.62% — tendencia creciente.
    - **D04 (semáforo rojo):** 8.84% y **C32 (peatones):** 0.55% — menor incidencia.
    """)
    hr()
    st.markdown("#### Perfil del infractor")
    st.markdown("""
    - **Vehículo:** automóvil (52.4%), camioneta (21.1%), motocicleta (16.7%).
    - **Servicio:** particular (82.6%), público (14.4%).
    """)
    hr()
    st.markdown("#### Geografía")
    st.markdown("""
    - Cámaras fijas concentran el 66.6% de los comparendos.
    - Top 5 cámaras: Vía 11 con carrera 8 (52 029), Carrera 51B con calle 79 (33 293).
    - Localidades con mayor actividad: Norte-Centro Histórico y Suroriente.
    """)
    hr()
    st.markdown("#### Tendencias temporales")
    st.markdown("""
    - **C03** es la única con tendencia creciente (+10.3/mes, p<0.001).
    - **C29** y **D04** decrecen significativamente.
    - **C02** y **C32** se mantienen estables.
    - Estacionalidad más fuerte en **D04** (25.9% varianza explicada).
    """)
    hr()
    st.markdown("#### Desempeño de modelos en test 2025")
    st.dataframe(pd.DataFrame({
        "Infracción": ["C29", "C02", "C03", "D04", "C32"],
        "Mejor modelo": ["Holt-Winters (tend. amort.)", "Holt-Winters (SES)",
                         "Ridge Regression", "SARIMA(1,0,0)(0,0,0)[12]",
                         "SARIMA(1,0,1)(0,0,0)[12]"],
        "RMSE": [479.4, 351.9, 410.5, 98.2, 7.9],
        "MAE":  [405.9, 280.3, 312.6, 77.9, 6.6]
    }), use_container_width=True, hide_index=True)
    hr()
    st.markdown("#### Pronóstico 2026")
    st.markdown("""
    - **C29:** descenso de 989 a 803 comparendos mensuales.
    - **C02:** estable en ~1 940.
    - **C03:** crecimiento hacia 850.
    - **D04:** descenso acelerado (262 → 141).
    - **C32:** muy bajo (3–5).
    """)
    hr()
    st.markdown("#### Lecciones aprendidas")
    st.markdown("""
    - Los modelos clásicos superaron a los de ML ante cambios estructurales.
    - No existe un modelo único: cada infracción requiere un enfoque específico.
    - La validación cruzada no siempre predice el desempeño futuro.
    """)


# ── CONCLUSIONES ──────────────────────────────────────────────
elif seccion == "Conclusiones":
    st.header("Conclusiones")

    st.markdown("#### Hallazgos fundamentales")
    st.markdown("""
    - C29 (exceso de velocidad) es la más frecuente pero muestra tendencia decreciente,
      sugiriendo un efecto disuasivo de las cámaras.
    - **C03 (bloquear calzada) es la única con tendencia creciente**, convirtiéndola en prioridad.
    - D04 (semáforo rojo) presenta la estacionalidad más marcada y es la más predecible.
    - C02 (estacionamiento prohibido) es estable y masivo; requiere intervenciones estructurales.
    - C32 (peatones) tiene volumen muy bajo, pero cualquier aumento debe atenderse con urgencia.
    """)
    hr()
    st.markdown("#### Contribución metodológica")
    st.markdown("""
    - La comparativa de 10 modelos demostró que los **modelos estadísticos clásicos superan a los de ML**
      en contextos con cambios estructurales no anticipados.
    - El mejor modelo en validación cruzada no siempre fue el mejor en test 2025.
    - La descomposición STL fue valiosa para entender la dinámica de cada infracción.
    """)
    hr()
    st.markdown("#### Limitaciones")
    st.markdown("""
    - Datos sin hora real ni coordenadas exactas de las cámaras.
    - Modelos univariados: no se incorporaron variables externas (clima, eventos, flujo vehicular).
    - El cambio abrupto de 2025 no fue anticipado por ningún modelo.
    """)
    hr()
    st.markdown("#### Recomendaciones")
    st.markdown("""
    - Incorporar modelos multivariados (flujo vehicular, clima, calendario festivo).
    - Georreferenciar con precisión para análisis espacial avanzado.
    - Evaluar el impacto causal de nuevas cámaras mediante diferencias en diferencias.
    - Vincular comparendos con siniestros para medir efectividad real.
    """)
    hr()
    st.markdown("#### Implicaciones para la gestión pública")
    st.markdown("""
    - Priorizar controles de bloqueo de calzada (C03) en horas y zonas críticas.
    - Mantener la presión sobre exceso de velocidad (C29) para consolidar la tendencia decreciente.
    - Reforzar campañas de estacionamiento prohibido (C02) en zonas comerciales y residenciales.
    - Monitorear el desplome de D04 para confirmar si es mejora real o reducción de operatividad.
    - Los pronósticos 2026 deben actualizarse anualmente con nuevos datos.
    """)
