import asyncio
from datetime import date
import asyncio
import matplotlib.pyplot as plt
from spothinta_api import SpotHinta


async def main() -> None:
    """Fetch the energy prices and plot them."""
    async with SpotHinta() as client:
        # Fetch the energy prices
        energy = await client.energy_prices()

        # Extract data from the response
        times = list(energy.prices.keys())
        prices = list(energy.prices.values())

        # Plot the data
        plt.figure(figsize=(12, 6))
        plt.plot(times, prices, marker='o', linestyle='-', label="Electricity Price")
        plt.title("Electricity Prices Over Time")
        plt.xlabel("Time")
        plt.ylabel("Price (€/kWh)")
        plt.grid(True)
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Display the plot
        plt.show()


if __name__ == "__main__":
    asyncio.run(main())
