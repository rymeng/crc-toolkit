#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
"""
@File    : crc_utils.py
@Created : 2025/05/19
@Author  : Rainer Meng
@Desc    : Implementation of core CRC computation functions
@License : GPL-3.0 (https://www.gnu.org/licenses/gpl-3.0.en.html)

Copyright (C) 2025  Rainer Meng

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

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