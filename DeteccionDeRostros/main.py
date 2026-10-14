
import cv2 as cv
from pathlib import Path

# Archivos y carpetas
detector = cv.CascadeClassifier(
    "haarcascade_frontalface_alt.xml"
)

video_path = "caras.mp4"
output_dir = Path("dataset/luna")
output_dir.mkdir(parents=True, exist_ok=True)

if detector.empty():
    raise RuntimeError("No se pudo cargar el archivo XML")

cap = cv.VideoCapture(video_path)

if not cap.isOpened():
    raise RuntimeError("No se pudo abrir el video")

count = 0
max_images = 1000
frame_number = 0

while count < max_images:
    ret, frame = cap.read()

    if not ret:
        print("El video terminó.")
        break

    frame_number += 1
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    rostros = detector.detectMultiScale(
        gray, scaleFactor=1.3, minNeighbors=5
    )

    for (x, y, w, h) in rostros:
        # Evitar guardar todos los fotogramas consecutivos
        if frame_number % 3 != 0:
            continue

        cara = frame[y:y+h, x:x+w]
        cara = cv.resize(cara, (100, 100))

        count += 1
        nombre = output_dir / f"luna_{count:04d}.jpg"

        if not cv.imwrite(str(nombre), cara):
            count -= 1
            print("No se pudo guardar la imagen")
            continue

        print(f"Imagen guardada: {count}/{max_images}")

        cv.rectangle(
            frame, (x, y), (x+w, y+h), (0, 255, 0), 2
        )

        if count >= max_images:
            break

    cv.imshow("Deteccion de rostros", frame)

    if cv.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv.destroyAllWindows()

print(f"Total de imagenes guardadas: {count}")
