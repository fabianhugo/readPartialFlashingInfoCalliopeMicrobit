# readPartialFlashingInfoCalliopeMicrobit

A python script using bleak and asncio to read partial flashing info.
Result is e.g. 

```
DAL REGION (CODAL Runtime)
============================================================
Raw: 00 01 00 01 C0 00 00 04 64 B4 EF 8A BE DB FE 0A 6B F5 00 00
Start Address: 0x0001C000 (114688)
End Address:   0x000464B4 (287924)
DAL Hash:      EF8ABEDBFE0A6BF5

============================================================
PROGRAM REGION (User Code)
============================================================
Raw: 00 02 00 04 70 00 00 07 30 00 85 00 6E 00 D6 00 64 00 00 00
Code Start:    0x00047000 (290816)
Code End:      0x00073000 (471040)
Program Hash:  85006E00D6006400
```
