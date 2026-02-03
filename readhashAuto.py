import asyncio
from bleak import BleakScanner, BleakClient

PF_SERVICE = "e97dd91d-251d-470a-a062-fa1922dfa9a8"
PF_CHAR = "e97d3b10-251d-470a-a062-fa1922dfa9a8"

async def scan_devices():
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover(timeout=5.0)
    
    # Filter for relevant devices
    relevant = []
    for d in devices:
        name = d.name or "Unknown"
        if "calliope" in name.lower() or "micro:bit" in name.lower() or "bbc" in name.lower():
            relevant.append(d)
    
    if not relevant:
        print("\nNo Calliope/micro:bit devices found!")
        print("Make sure your device is powered on and in range.")
        return None
    
    print(f"\nFound {len(relevant)} device(s):\n")
    for i, d in enumerate(relevant, 1):
        print(f"{i}. {d.name or 'Unknown'} ({d.address})")
    
    while True:
        try:
            choice = input(f"\nSelect device (1-{len(relevant)}): ")
            idx = int(choice) - 1
            if 0 <= idx < len(relevant):
                return relevant[idx]
            print("Invalid selection!")
        except ValueError:
            print("Please enter a number!")
        except KeyboardInterrupt:
            return None

async def read_metadata(device):
    print(f"\nConnecting to {device.name}...")
    
    responses = {}
    
    async with BleakClient(device.address) as client:
        print(f"✓ Connected!")
        
        def notification_handler(sender, data):
            responses['last'] = data
            
        await client.start_notify(PF_CHAR, notification_handler)
        
        # Query DAL region
        print("\n" + "="*60)
        print("DAL REGION (CODAL Runtime)")
        print("="*60)
        await client.write_gatt_char(PF_CHAR, bytes([0x00, 0x01]))
        await asyncio.sleep(0.5)
        
        if 'last' in responses:
            data = responses['last']
            hex_str = ' '.join(f'{b:02X}' for b in data)
            print(f"Raw: {hex_str}")
            
            start = int.from_bytes(data[2:6], 'big')
            end = int.from_bytes(data[6:10], 'big')
            dal_hash = ''.join(f'{b:02X}' for b in data[10:18])
            
            print(f"Start Address: 0x{start:08X} ({start})")
            print(f"End Address:   0x{end:08X} ({end})")
            print(f"DAL Hash:      {dal_hash}")
        
        # Query PROGRAM region
        responses.clear()
        print("\n" + "="*60)
        print("PROGRAM REGION (User Code)")
        print("="*60)
        await client.write_gatt_char(PF_CHAR, bytes([0x00, 0x02]))
        await asyncio.sleep(0.5)
        
        if 'last' in responses:
            data = responses['last']
            hex_str = ' '.join(f'{b:02X}' for b in data)
            print(f"Raw: {hex_str}")
            
            start = int.from_bytes(data[2:6], 'big')
            end = int.from_bytes(data[6:10], 'big')
            prog_hash = ''.join(f'{b:02X}' for b in data[10:18])
            
            print(f"Code Start:    0x{start:08X} ({start})")
            print(f"Code End:      0x{end:08X} ({end})")
            print(f"Program Hash:  {prog_hash}")
        
        print("\n" + "="*60)
        
        try:
            await client.stop_notify(PF_CHAR)
        except:
            pass  # Ignore disconnection errors

async def main():
    device = await scan_devices()
    if device:
        await read_metadata(device)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nCancelled by user")
