
import cv2 as cv
from pathlib import Path

# ==========================================
# CONFIGURACIÓN
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

XML_PATH = BASE_DIR / "haarcascade_frontalface_alt.xml"
OUTPUT_DIR = BASE_DIR / "dataset" / "luna"

MAX_IMAGES = 1000
SAVE_EVERY_N_FRAMES = 3

# ==========================================
# CARGAR DETECTOR FACIAL
# ==========================================

detector = cv.CascadeClassifier(str(XML_PATH))

if detector.empty():
    raise RuntimeError(
        f"No se pudo cargar el detector facial: {XML_PATH}"
    )

# ==========================================
# PREPARAR CARPETA Y CONTAR IMÁGENES EXISTENTES
# ==========================================

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

existing_files = list(OUTPUT_DIR.glob("luna_*.jpg"))

existing_numbers = []

for file in existing_files:
    suffix = file.stem.removeprefix("luna_")

    if suffix.isdigit():
        existing_numbers.append(int(suffix))

total_saved = len(existing_files)
next_number = max(existing_numbers, default=0) + 1

print(f"Imágenes existentes: {total_saved}/{MAX_IMAGES}")

# ==========================================
# INICIAR CÁMARA
# ==========================================

cap = cv.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError(
        "No se pudo abrir la cámara web. "
        "Comprueba que esté conectada y disponible."
    )

frame_number = 0
capturing = False

print("Cámara iniciada.")
print("ESPACIO: iniciar o pausar la captura.")
print("ESC: salir.")

# ==========================================
# CAPTURA Y DETECCIÓN EN TIEMPO REAL
# ==========================================

try:
    while True:
        ret, frame = cap.read()

        if not ret:
            print("No se pudo leer la imagen de la cámara.")
            break

        frame_number += 1

        # Espejar horizontalmente para facilitar el encuadre
        frame = cv.flip(frame, 1)

        # Convertir a escala de grises
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Detectar rostros
        rostros = detector.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(60, 60)
        )

        # Dibujar los rectángulos detectados
        for (x, y, w, h) in rostros:
            cv.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

        # Capturar únicamente el rostro más grande
        # cuando la captura está activada
        if (
            capturing
            and frame_number % SAVE_EVERY_N_FRAMES == 0
            and total_saved < MAX_IMAGES
            and len(rostros) > 0
        ):
            x, y, w, h = max(
                rostros,
                key=lambda r: r[2] * r[3]
            )

            cara = frame[y:y+h, x:x+w]

            if cara.size > 0:
                cara = cv.resize(cara, (100, 100))

                filename = OUTPUT_DIR / f"luna_{next_number:04d}.jpg"

                if cv.imwrite(str(filename), cara):
                    total_saved += 1
                    next_number += 1

                    print(
                        f"Imagen guardada: "
                        f"{total_saved}/{MAX_IMAGES}"
                    )

        # Detener automáticamente al alcanzar el límite
        if total_saved >= MAX_IMAGES:
            capturing = False
            estado = "LIMITE ALCANZADO"
        elif capturing:
            estado = "CAPTURANDO"
        else:
            estado = "VISTA PREVIA"

        # Mostrar estado y contador
        cv.putText(
            frame,
            f"Imagenes: {total_saved}/{MAX_IMAGES}",
            (10, 30),
            cv.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv.putText(
            frame,
            f"Estado: {estado}",
            (10, 60),
            cv.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 255, 255),
            2
        )

        cv.putText(
            frame,
            "ESPACIO: iniciar/pausar | ESC: salir",
            (10, frame.shape[0] - 15),
            cv.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1
        )

        # Mostrar la cámara en vivo
        cv.imshow("Deteccion y captura de rostros", frame)

        # Leer controles del teclado
        key = cv.waitKey(1) & 0xFF

        if key == 27:  # ESC
            break

        elif key == 32 and total_saved < MAX_IMAGES:  # ESPACIO
            capturing = not capturing

            if capturing:
                print("Captura iniciada.")
            else:
                print("Captura pausada.")

finally:
    cap.release()
    cv.destroyAllWindows()

print("\nCaptura finalizada.")
print(f"Total de imágenes: {total_saved}")
print(f"Carpeta de salida: {OUTPUT_DIR}")
