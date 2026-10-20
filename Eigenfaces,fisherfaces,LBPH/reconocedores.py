import cv2 as cv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_SET = Path("/home/likcos/pruebacaras")

CASCADE_PATH = (
    cv.data.haarcascades + "haarcascade_frontalface_alt2.xml"
)

PERSONAS = sorted(
    carpeta.name
    for carpeta in DATA_SET.iterdir()
    if carpeta.is_dir()
) if DATA_SET.is_dir() else []

CONFIGURACION = {
    "eigenfaces": {
        "nombre": "Eigenfaces",
        "archivo": BASE_DIR / "Eigenfaces" / "laloEigenface.xml",
        "umbral": 2800,
        "creador": "EigenFaceRecognizer_create"
    },
    "fisherfaces": {
        "nombre": "Fisherfaces",
        "archivo": BASE_DIR / "Fisherfaces" / "laloFisherFace.xml",
        "umbral": 500,
        "creador": "FisherFaceRecognizer_create"
    },
    "lbph": {
        "nombre": "LBPH",
        "archivo": BASE_DIR / "LBPH" / "laloLBPHFace.xml",
        "umbral": 70,
        "creador": "LBPHFaceRecognizer_create"
    }
}


def cargar_modelo(tipo):

    if not hasattr(cv, "face"):
        raise RuntimeError(
            "Instala opencv-contrib-python para utilizar cv.face."
        )

    config = CONFIGURACION[tipo]
    archivo = config["archivo"]

    if not archivo.is_file():
        raise FileNotFoundError(
            f"No existe el modelo: {archivo}. "
            "Ejecuta primero su entrenamiento."
        )

    creador = getattr(cv.face, config["creador"])
    modelo = creador()
    modelo.read(str(archivo))

    return modelo


def reconocer(algoritmos):

    if not PERSONAS:
        print("No se encontraron carpetas de personas.")
        return

    try:
        modelos = {
            tipo: cargar_modelo(tipo)
            for tipo in algoritmos
        }
    except (RuntimeError, FileNotFoundError, cv.error) as error:
        print("No se pudieron cargar los modelos:", error)
        return

    cascade = cv.CascadeClassifier(CASCADE_PATH)

    if cascade.empty():
        print("No se pudo cargar el clasificador Haar.")
        return

    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("No se pudo abrir la camara.")
        cap.release()
        return

    comparar_modelos = len(algoritmos) > 1
    titulo = (
        "Comparacion de reconocedores"
        if comparar_modelos
        else CONFIGURACION[algoritmos[0]]["nombre"]
    )

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

                roi = gray[y:y + h, x:x + w]

                roi = cv.resize(
                    roi,
                    (100, 100),
                    interpolation=cv.INTER_CUBIC
                )

                cv.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (255, 255, 0),
                    2
                )

                for indice, tipo in enumerate(algoritmos):

                    config = CONFIGURACION[tipo]
                    label_id, distancia = modelos[tipo].predict(roi)

                    reconocido = (
                        0 <= label_id < len(PERSONAS)
                        and distancia < config["umbral"]
                    )

                    nombre = (
                        PERSONAS[label_id]
                        if reconocido
                        else "Desconocido"
                    )

                    color = (
                        (0, 255, 0)
                        if reconocido
                        else (0, 0, 255)
                    )

                    texto = (
                        f"{config['nombre']}: {nombre} "
                        f"({distancia:.0f})"
                        if comparar_modelos
                        else f"{nombre} ({distancia:.0f})"
                    )

                    if comparar_modelos:
                        texto_y = y + h + 22 + indice * 23

                        if texto_y > frame.shape[0] - 10:
                            texto_y = max(
                                20,
                                y - 12 - (len(algoritmos) - indice) * 23
                            )
                    else:
                        texto_y = max(y - 12, 20)

                    cv.putText(
                        frame,
                        texto,
                        (x, texto_y),
                        cv.FONT_HERSHEY_SIMPLEX,
                        0.55 if comparar_modelos else 0.7,
                        color,
                        2,
                        cv.LINE_AA
                    )

            cv.imshow(titulo, frame)

            # ESC para volver al menu
            if cv.waitKey(1) & 0xFF == 27:
                break

    finally:
        cap.release()
        cv.destroyAllWindows()


def eigenfaces():
    reconocer(["eigenfaces"])


def fisherfaces():
    reconocer(["fisherfaces"])


def lbph():
    reconocer(["lbph"])


def comparar():
    reconocer(["eigenfaces", "fisherfaces", "lbph"])