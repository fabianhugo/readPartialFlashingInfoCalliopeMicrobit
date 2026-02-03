
import asyncio
from bleak import BleakClient

DEVICE_UUID = "789D4083-0845-5E16-5FB0-990948081D97"
PF_SERVICE = "e97dd91d-251d-470a-a062-fa1922dfa9a8"
PF_CHAR = "e97d3b10-251d-470a-a062-fa1922dfa9a8"

async def read_metadata():
    async with BleakClient(DEVICE_UUID) as client:
        print(f"Connected to {client.address}")
        
        def notification_handler(sender, data):
            hex_str = ' '.join(f'{b:02X}' for b in data)
            print(f"Response: {hex_str}")
            
        await client.start_notify(PF_CHAR, notification_handler)
        
        # Query DAL region
        print("\nQuerying DAL region (command: 00 01)...")
        await client.write_gatt_char(PF_CHAR, bytes([0x00, 0x01]))
        await asyncio.sleep(1)
        
        # Query PROGRAM region  
        print("\nQuerying PROGRAM region (command: 00 02)...")
        await client.write_gatt_char(PF_CHAR, bytes([0x00, 0x02]))
        await asyncio.sleep(1)
        
        await client.stop_notify(PF_CHAR)

asyncio.run(read_metadata())
