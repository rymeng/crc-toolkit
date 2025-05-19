from src.crc_utils import *

data = b"Hello World!"
crc = calculate_crc32_standard(data)
print(f"CRC-32: 0x{crc:08X}")
crc = calculate_crc32_optimized(data)
print(f"CRC-32: 0x{crc:08X}")