from datetime import UTC, datetime
import MetaTrader5 as mt5

print("Initialize:", mt5.initialize())
print("Version:", mt5.version())
print("Last error:", mt5.last_error())

print("\n=== Simboli XAU disponibili ===")

for s in mt5.symbols_get():
    if "XAU" in s.name.upper():
        print(s.name)

symbol = "XAUUSD"

rates = mt5.copy_rates_range(
    symbol,
    mt5.TIMEFRAME_M1,
    datetime(2026, 4, 20, tzinfo=UTC),
    datetime(2026, 4, 22, tzinfo=UTC),
)

print("\n=== Download ===")
print("Last error:", mt5.last_error())

if rates is None:
    print("rates = None")
else:
    print("Numero barre:", len(rates))
    if len(rates):
        print("Prima:", rates[0])
        print("Ultima:", rates[-1])

mt5.shutdown()