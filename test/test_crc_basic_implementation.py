from src.crc_utils import *

data = b"Hello World!"
crc = calculate_basic_crc_standard(data)
print(f"CRC-32: 0x{crc:08X}")
crc = calculate_basic_crc_optimized(data)
print(f"CRC-32: 0x{crc:08X}")