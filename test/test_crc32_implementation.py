#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
"""
@File    : test_crc32_implementation.py
@Created : 2025/05/19
@Author  : Rainer Meng
@Desc    : Implementation of test cases for CRC32 algorithm validation
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

from src.crc_utils import *

data = b"Hello World!"
crc = calculate_crc32_standard(data)
print(f"CRC-32: 0x{crc:08X}")
crc = calculate_crc32_optimized(data)
print(f"CRC-32: 0x{crc:08X}")