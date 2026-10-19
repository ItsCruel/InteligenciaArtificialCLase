
import cv2 as cv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

XML_PATH = BASE_DIR / "haarcascade_frontalface_alt.xml"
MODEL_PATH = BASE_DIR / "modelo_rostros.yml"
LABELS_PATH = BASE_DIR / "labels.json"

# Cargar detector facial
detector = cv.CascadeClassifier(str(XML_PATH))

if detector.empty():
    raise RuntimeError("No se pudo cargar el detector facial.")

# Cargar modelo entrenado
modelo = cv.face.LBPHFaceRecognizer_create()
modelo.read(str(MODEL_PATH))

with open(LABELS_PATH, "r", encoding="utf-8") as archivo:
    nombres = json.load(archivo)

# Ajuste inicial; debe calibrarse con pruebas reales
UMBRAL = 70

cap = cv.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("No se pudo abrir la cámara.")

print("Reconocimiento facial iniciado. Presiona ESC para salir.")

try:
    while True:
        ret, frame = cap.read()

        if not ret:
            print("No se pudo leer la cámara.")
            break

        frame = cv.flip(frame, 1)
        gris = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        rostros = detector.detectMultiScale(
            gris,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(60, 60)
        )

        for (x, y, w, h) in rostros:
            cara = gris[y:y+h, x:x+w]
            cara = cv.resize(cara, (100, 100))

            etiqueta, confianza = modelo.predict(cara)

            if confianza < UMBRAL and str(etiqueta) in nombres:
                nombre = nombres[str(etiqueta)].capitalize()
            else:
                nombre = "Desconocido"

            color = (0, 255, 0) if nombre == "Irving" else (0, 0, 255)

            cv.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                color,
                2
            )

            cv.putText(
                frame,
                f"{nombre} ({confianza:.1f})",
                (x, max(y-10, 20)),
                cv.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

        cv.imshow("Reconocimiento facial", frame)

        if cv.waitKey(1) & 0xFF == 27:
            break

finally:
    cap.release()
    cv.destroyAllWindows()
