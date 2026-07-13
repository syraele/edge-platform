from edge.core.kernel import Kernel


def main():
    kernel = Kernel()

    kernel.config.set("symbol", "XAUUSD")
    kernel.config.set("risk", 0.01)

    print(kernel.config.get("symbol"))
    print(kernel.config.get("risk"))
    print(kernel.config.has("broker"))

    kernel.start()
    kernel.stop()


if __name__ == "__main__":
    main()