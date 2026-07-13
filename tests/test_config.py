from edge.infrastructure.config.manager import ConfigManager


config = ConfigManager(
    "config/market.yaml"
)


data = config.load()


print(data)


print(
    "SYMBOL:",
    data["market"]["symbol"]
)