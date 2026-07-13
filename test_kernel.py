import sys
from pathlib import Path

# Aggiunge la cartella "src" al percorso di ricerca dei moduli
sys.path.insert(0, str(Path(__file__).parent / "src"))

from edge.core.kernel import Kernel

kernel = Kernel()

print(kernel.started)

kernel.start()

print(kernel.started)

kernel.stop()

print(kernel.started)