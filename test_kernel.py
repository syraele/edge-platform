


# Aggiunge la cartella "src" al percorso di ricerca dei moduli


from edge.core.kernel import Kernel

kernel = Kernel()

print(kernel.started)

kernel.start()

print(kernel.started)

kernel.stop()

print(kernel.started)