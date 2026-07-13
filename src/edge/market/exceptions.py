class MarketError(Exception):
    """Base Market Exception."""


class ProviderDisconnected(MarketError):
    """Provider is disconnected."""