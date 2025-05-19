def bit_reflect(value: int, length: int) -> int:
    reflected_value = 0
    for _ in range(length):
        reflected_value = (reflected_value << 1) | (value & 1)
        value >>= 1
    return reflected_value

POLYNOMIAL_CRC32_STANDARD = 0x04C11DB7
POLYNOMIAL_CRC32_REFLECTED = 0xEDB88320
INITIAL_VALUE_CRC32 = 0xFFFFFFFF

def calculate_crc32_standard(raw_data: bytes) -> int:
    crc_value = INITIAL_VALUE_CRC32
    for byte in raw_data:
        reflected_byte = bit_reflect(byte, 8)
        crc_value ^= (reflected_byte << 24)
        for _ in range(8):
            if crc_value & 0x80000000:
                crc_value = ((crc_value << 1) ^ POLYNOMIAL_CRC32_STANDARD)
            else:
                crc_value <<= 1
            crc_value &= 0xFFFFFFFF
    crc_value = bit_reflect(crc_value, 32)
    return crc_value ^ INITIAL_VALUE_CRC32

def calculate_crc32_optimized(raw_data: bytes) -> int:
    crc_value = INITIAL_VALUE_CRC32
    for byte in raw_data:
        crc_value ^= byte
        for _ in range(8):
            crc_value = (
                (crc_value >> 1) ^
                (POLYNOMIAL_CRC32_REFLECTED if (crc_value & 1) else 0)
            )
            crc_value &= 0xFFFFFFFF
    return crc_value ^ INITIAL_VALUE_CRC32

def calculate_basic_crc_standard(raw_data: bytes) -> int:
    crc_value = 0
    bit_stream = []
    for byte in raw_data:
        for i in range(7, -1, -1):
            bit_stream.append((byte >> i) & 1)
    bit_stream += [0] * 32
    for bit in bit_stream:
        if crc_value & 0x80000000:
            crc_value = ((crc_value << 1) | bit) ^ POLYNOMIAL_CRC32_STANDARD
        else:
            crc_value = (crc_value << 1) | bit
        crc_value &= 0xFFFFFFFF
    return crc_value

def calculate_basic_crc_optimized(raw_data: bytes) -> int:
    crc_value = 0
    for byte in raw_data:
        crc_value ^= (byte << 24)
        for _ in range(8):
            if crc_value & 0x80000000:
                crc_value = (crc_value << 1) ^ POLYNOMIAL_CRC32_STANDARD
            else:
                crc_value <<= 1
            crc_value &= 0xFFFFFFFF
    return crc_value