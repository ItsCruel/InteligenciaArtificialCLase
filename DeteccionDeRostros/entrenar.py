
import cv2 as cv
import numpy as np
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"
MODEL_PATH = BASE_DIR / "modelo_rostros.yml"
LABELS_PATH = BASE_DIR / "labels.json"

rostros = []
etiquetas = []
nombres = {}

# Buscar una carpeta por cada persona
carpetas = sorted(
    carpeta for carpeta in DATASET_DIR.iterdir()
    if carpeta.is_dir()
)

for etiqueta, carpeta in enumerate(carpetas):
    nombres[str(etiqueta)] = carpeta.name
    cantidad = 0

    for archivo in carpeta.glob("*.jpg"):
        imagen = cv.imread(
            str(archivo),
            cv.IMREAD_GRAYSCALE
        )

        if imagen is None:
            continue

        imagen = cv.resize(imagen, (100, 100))
        rostros.append(imagen)
        etiquetas.append(etiqueta)
        cantidad += 1

    print(f"{carpeta.name}: {cantidad} imágenes")

if not rostros:
    raise RuntimeError(
        "No se encontraron imágenes válidas en dataset."
    )

# Crear y entrenar el reconocedor LBPH
modelo = cv.face.LBPHFaceRecognizer_create()
modelo.train(
    rostros,
    np.array(etiquetas, dtype=np.int32)
)

# Guardar el modelo y sus etiquetas
modelo.write(str(MODEL_PATH))

with open(LABELS_PATH, "w", encoding="utf-8") as archivo:
    json.dump(nombres, archivo, ensure_ascii=False, indent=4)

print("\nEntrenamiento terminado.")
print(f"Modelo guardado en: {MODEL_PATH}")
print(f"Etiquetas guardadas en: {LABELS_PATH}")
