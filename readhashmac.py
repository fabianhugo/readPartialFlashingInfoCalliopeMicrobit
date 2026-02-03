import asyncio
from bleak import BleakClient

DEVICE_ADDRESS = "789D4083-0845-5E16-5FB0-990948081D97"  # e.g., "C5:16:3C:1A:5B:AA"
PF_SERVICE = "e97dd91d-251d-470a-a062-fa1922dfa9a8"
PF_CHAR = "e97d3b10-251d-470a-a062-fa1922dfa9a8"

async def read_metadata():
    async with BleakClient(DEVICE_ADDRESS) as client:
        def notification_handler(sender, data):
            print(f"Response: {data.hex().upper()}")
            
        await client.start_notify(PF_CHAR, notification_handler)
        
        # Query DAL region
        print("Querying DAL region...")
        await client.write_gatt_char(PF_CHAR, bytes([0x00, 0x01]))
        await asyncio.sleep(1)
        
        # Query PROGRAM region  
        print("Querying PROGRAM region...")
        await client.write_gatt_char(PF_CHAR, bytes([0x00, 0x02]))
        await asyncio.sleep(1)

asyncio.run(read_metadata())
