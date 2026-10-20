import cv2 as cv
import os

# ==========================================
# CONFIGURACION
# ==========================================

DATA_SET = "/home/likcos/pruebacaras"

# Utilizar el clasificador Haar incluido en OpenCV
CASCADE_PATH = (
    cv.data.haarcascades + "haarcascade_frontalface_alt2.xml"
)

# Verificar que OpenCV tenga los reconocedores disponibles
if not hasattr(cv, "face"):
    raise SystemExit(
        "Error: falta cv.face. Instala opencv-contrib-python."
    )

# Nombres de las personas.
# Deben conservar el mismo orden utilizado al entrenar los modelos.
caras = sorted(
    carpeta
    for carpeta in os.listdir(DATA_SET)
    if os.path.isdir(os.path.join(DATA_SET, carpeta))
)

if not caras:
    raise SystemExit("No se encontraron carpetas de personas.")

# Modelos, archivos y umbrales
CONFIGURACION = [
    {
        "opcion": "1",
        "nombre": "Eigenfaces",
        "archivo": "laloEigenface.xml",
        "umbral": 2800,
        "crear": cv.face.EigenFaceRecognizer_create
    },
    {
        "opcion": "2",
        "nombre": "Fisherfaces",
        "archivo": "laloFisherFace.xml",
        "umbral": 500,
        "crear": cv.face.FisherFaceRecognizer_create
    },
    {
        "opcion": "3",
        "nombre": "LBPH",
        "archivo": "laloLBPHFace.xml",
        "umbral": 70,
        "crear": cv.face.LBPHFaceRecognizer_create
    }
]

# ==========================================
# CARGAR LOS MODELOS
# ==========================================

modelos = {}

for config in CONFIGURACION:
    archivo = config["archivo"]

    if not os.path.isfile(archivo):
        print(f"No se encontro el modelo: {archivo}")
        continue

    try:
        reconocedor = config["crear"]()
        reconocedor.read(archivo)

        modelos[config["nombre"]] = reconocedor

        print(f"Modelo cargado: {config['nombre']}")

    except cv.error as error:
        print(f"Error al cargar {archivo}: {error}")

# ==========================================
# DETECTOR DE ROSTROS
# ==========================================

cascade = cv.CascadeClassifier(CASCADE_PATH)

if cascade.empty():
    raise SystemExit(
        "Error: no se pudo cargar el clasificador Haar."
    )

# ==========================================
# FUNCION PARA RECONOCER UN ROSTRO
# ==========================================

def reconocer_rostro(reconocedor, umbral, roi):
    label_id, distancia = reconocedor.predict(roi)

    if 0 <= label_id < len(caras) and distancia < umbral:
        nombre = caras[label_id]
        reconocido = True
    else:
        nombre = "Desconocido"
        reconocido = False

    return nombre, distancia, reconocido

# ==========================================
# RECONOCIMIENTO EN VIVO
# ==========================================

def reconocer_en_vivo(seleccionados):

    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("Error: no se pudo abrir la camara.")
        cap.release()
        return

    comparar = len(seleccionados) > 1

    if comparar:
        titulo = "Comparacion de reconocedores"
    else:
        titulo = f"Reconocimiento - {seleccionados[0]['nombre']}"

    print("\nCamara iniciada.")
    print("Presiona ESC para regresar al menu.")

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("No se pudo obtener imagen de la camara.")
                break

            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            rostros = cascade.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=3
            )

            for (x, y, w, h) in rostros:

                # Recortar y normalizar el rostro
                roi = gray[y:y + h, x:x + w]

                roi = cv.resize(
                    roi,
                    (100, 100),
                    interpolation=cv.INTER_CUBIC
                )

                # ----------------------------------
                # COMPARACION DE LOS TRES MODELOS
                # ----------------------------------

                if comparar:

                    cv.rectangle(
                        frame,
                        (x, y),
                        (x + w, y + h),
                        (255, 255, 0),
                        2
                    )

                    resultados = []

                    for config in seleccionados:
                        reconocedor = modelos[config["nombre"]]

                        nombre, distancia, reconocido = reconocer_rostro(
                            reconocedor,
                            config["umbral"],
                            roi
                        )

                        resultados.append(
                            (
                                config["nombre"],
                                nombre,
                                distancia,
                                reconocido
                            )
                        )

                    # Mostrar una prediccion por cada metodo
                    for i, resultado in enumerate(resultados):

                        metodo, nombre, distancia, reconocido = resultado

                        color = (
                            (0, 255, 0)
                            if reconocido
                            else (0, 0, 255)
                        )

                        texto = (
                            f"{metodo}: {nombre} "
                            f"({distancia:.0f})"
                        )

                        texto_y = y + h + 22 + i * 23

                        # Si no hay espacio debajo del rostro,
                        # mostrar los resultados encima.
                        if texto_y > frame.shape[0] - 10:
                            texto_y = max(
                                20,
                                y - 15 - (len(resultados) - 1 - i) * 23
                            )

                        cv.putText(
                            frame,
                            texto,
                            (x, texto_y),
                            cv.FONT_HERSHEY_SIMPLEX,
                            0.55,
                            color,
                            2,
                            cv.LINE_AA
                        )

                # ----------------------------------
                # RECONOCIMIENTO CON UN SOLO MODELO
                # ----------------------------------

                else:
                    config = seleccionados[0]

                    reconocedor = modelos[config["nombre"]]

                    nombre, distancia, reconocido = reconocer_rostro(
                        reconocedor,
                        config["umbral"],
                        roi
                    )

                    color = (
                        (0, 255, 0)
                        if reconocido
                        else (0, 0, 255)
                    )

                    texto = f"{nombre} ({distancia:.0f})"

                    cv.rectangle(
                        frame,
                        (x, y),
                        (x + w, y + h),
                        color,
                        2
                    )

                    cv.putText(
                        frame,
                        texto,
                        (x, max(y - 12, 20)),
                        cv.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        color,
                        2,
                        cv.LINE_AA
                    )

            cv.imshow(titulo, frame)

            # ESC termina la camara
            if cv.waitKey(1) & 0xFF == 27:
                break

    finally:
        cap.release()
        cv.destroyAllWindows()

# ==========================================
# MENU PRINCIPAL
# ==========================================

def mostrar_menu():

    while True:
        print("\n================================")
        print(" SISTEMA DE RECONOCIMIENTO FACIAL")
        print("================================")
        print("1. Reconocer con Eigenfaces")
        print("2. Reconocer con Fisherfaces")
        print("3. Reconocer con LBPH")
        print("4. Comparar los tres algoritmos")
        print("0. Salir")
        print("================================")

        opcion = input("Selecciona una opcion: ").strip()

        if opcion == "0":
            print("Programa finalizado.")
            break

        elif opcion in ("1", "2", "3"):
            config = next(
                item for item in CONFIGURACION
                if item["opcion"] == opcion
            )

            if config["nombre"] not in modelos:
                print(
                    f"No se puede utilizar {config['nombre']}. "
                    "Revisa su archivo XML."
                )
                continue

            reconocer_en_vivo([config])

        elif opcion == "4":

            nombres = [
                config["nombre"]
                for config in CONFIGURACION
            ]

            faltantes = [
                nombre for nombre in nombres
                if nombre not in modelos
            ]

            if faltantes:
                print(
                    "No se pueden comparar los tres. "
                    "Faltan modelos: " + ", ".join(faltantes)
                )
                continue

            reconocer_en_vivo(CONFIGURACION)

        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    mostrar_menu()