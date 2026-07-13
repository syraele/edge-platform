from edge.core.kernel import Kernel


def test_event(data):

    print(
        f"Evento ricevuto: {data}"
    )


def main():

    kernel = Kernel()


    kernel.events.subscribe(
        "market.price",
        test_event
    )


    kernel.events.publish(
        "market.price",
        {
            "symbol": "XAUUSD",
            "price": 3350
        }
    )


    print(
        kernel.registry.has("events")
    )


if __name__ == "__main__":
    main()