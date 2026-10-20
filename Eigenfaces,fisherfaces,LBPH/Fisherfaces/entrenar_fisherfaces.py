import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from entrenamiento_comun import entrenar

MODELO = Path(__file__).resolve().parent / "laloFisherFace.xml"

if __name__ == "__main__":
    entrenar("fisherfaces", MODELO)