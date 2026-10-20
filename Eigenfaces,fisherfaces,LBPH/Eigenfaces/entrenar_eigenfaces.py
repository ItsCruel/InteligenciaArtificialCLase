import sys
from pathlib import Path

# Permitir importar el archivo comun desde la carpeta principal
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from entrenamiento_comun import entrenar

MODELO = Path(__file__).resolve().parent / "laloEigenface.xml"

if __name__ == "__main__":
    entrenar("eigenfaces", MODELO)