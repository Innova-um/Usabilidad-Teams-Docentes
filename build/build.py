import pandas as pd, json, os, sys, re

HERE = os.path.dirname(os.path.abspath(__file__))
# Carpeta con los datos crudos (por defecto, la raíz del repositorio; no se suben a GitHub)
POS = [a for a in sys.argv[1:] if not a.startswith("--")]
SRC = POS[0] if POS else os.path.dirname(HERE)
# --out=RUTA: archivo de salida (por defecto index.html en la raíz del repositorio)

TEAMS = "Usabilidad teams.csv"  # Informe «Actividad de usuarios de Teams» exportado de Microsoft 365
NOMBRES = "profesores user y nombre ocmpleto.xlsx"  # Columnas: User, nombre_profesor
# Nombres que vienen dañados en el Excel (usuario: nombre correcto)
CORREGIR = {"mcaamano": "MARIA DEL ROSARIO CAAMAÑO"}
# Rango de conexión a revisar (según la fecha de última actividad): inicio, fin
RANGO = ("2026-09-21", "2026-09-22")

# Columnas del informe, en el orden en que se envían al tablero
METRICAS = [
    "Team Chat Message Count", "Private Chat Message Count", "Call Count",
    "Meeting Count", "Meetings Organized Count", "Meetings Attended Count",
    "Ad Hoc Meetings Organized Count", "Ad Hoc Meetings Attended Count",
    "Scheduled One-time Meetings Organized Count", "Scheduled One-time Meetings Attended Count",
    "Scheduled Recurring Meetings Organized Count", "Scheduled Recurring Meetings Attended Count",
    "Audio Duration In Seconds", "Video Duration In Seconds", "Screen Share Duration In Seconds",
    "Post Messages", "Reply Messages", "Urgent Messages",
]

t = pd.read_csv(os.path.join(SRC, TEAMS), encoding="utf-8-sig")
t = t[t["Rol"].astype(str).str.strip().str.lower() == "profesor"]

nom = pd.read_excel(os.path.join(SRC, NOMBRES))
nombres = {str(u).strip().lower(): re.sub("�+", "Ñ", str(n).strip()) for u, n in zip(nom["User"], nom["nombre_profesor"]) if pd.notna(u) and pd.notna(n)}
nombres.update(CORREGIR)

teachers = []
for _, r in t.iterrows():
    la = pd.to_datetime(r["Last Activity Date"], dayfirst=True)
    u = str(r["User Principal Name"]).split("@")[0].strip().lower()
    teachers.append([
        u,
        la.strftime("%Y-%m-%d") if pd.notna(la) else "",
        1 if str(r["Has Other Action"]).strip().lower() == "yes" else 0,
        1 if "FACULTY" in str(r["Assigned Products"]).upper() else 0,
        [int(r[c]) if pd.notna(r[c]) else 0 for c in METRICAS],
        nombres.get(u, ""),
    ])

ref = pd.to_datetime(t["Report Refresh Date"].iloc[0], dayfirst=True)
dias = int(t["Report Period"].iloc[0])
data = {"ref": ref.strftime("%Y-%m-%d"), "days": dias,
        "ini": (ref - pd.Timedelta(days=dias - 1)).strftime("%Y-%m-%d"), "r0": RANGO[0], "r1": min(RANGO[1], ref.strftime("%Y-%m-%d")),  # el rango no pasa de la fecha del informe
        "t": teachers}

tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
out = tpl.replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
out = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
       '<meta name="robots" content="noindex, nofollow">\n'
       + out.replace("</style>\n", "</style>\n</head>\n<body>\n", 1) + "\n</body>\n</html>\n")
dest = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--out=")), os.path.join(os.path.dirname(HERE), "index.html"))
open(dest, "w", encoding="utf-8").write(out)
print("ok", len(teachers), "profesores,", sum(1 for x in teachers if not x[5]), "sin nombre,", len(out), dest)
