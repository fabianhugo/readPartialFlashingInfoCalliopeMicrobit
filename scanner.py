import asyncio
from bleak import BleakScanner

async def scan():
    devices = await BleakScanner.discover()
    for d in devices:
        name = d.name or "Unknown"
        if "calliope" in name.lower() or "micro:bit" in name.lower() or "bbc" in name.lower():
            print(f"{name}: {d.address}")

asyncio.run(scan())
