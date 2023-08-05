"""
Misc utility functions
"""

import random
import os
import platform
from Crypto.Cipher import ChaCha20_Poly1305
import numpy as np

# encryption configuration
KEY = bytes([i for i in range(32)])
NONCE = bytes([i for i in range(12)])
HEADER = b"IDUNIDUNIDUNIDUNIDUNIDUNIDUNIDUNc22"


def check_platform():
    """
    Check if the script is running on a cross platform

    Returns:
        bool: True if running on cross platform
    """
    if platform.system() == "Darwin":
        return "Darwin"
    elif platform.system() == "Linux":
        return "linux"
    elif platform.system() == "Windows":
        return "Windows"
    else:
        raise Exception("Unsupported platform")


def check_valid_mac(mac_address: str) -> bool:
    """Check if mac address is valid

    Args:
        mac_address (str): Mac address

    Returns:
        bool: True if mac address is valid
    """
    if len(mac_address) != 17:
        return False
    if mac_address.count(":") != 5:
        return False
    print("Mac address is valid")
    return True


def check_valid_uuid(uuid: str) -> bool:
    """Check if uuid is valid

    Args:
        uuid (str): UUID
    """
    if len(uuid) != 36:
        return False
    if uuid.count("-") != 4:
        return False
    return True


def generate_mock_data_array():
    """
    Generate mock data for GDK 1.0

    Returns:
        dict: Dictionary with mock data of two channels and counter
    """
    return {
        "idx": "1",
        "ch1": random.randint(3, 10000),
        "ch2": random.randint(3, 10000),
        "imu": [
            random.randint(3, 10000),
            random.randint(3, 10000),
            random.randint(3, 10000),
        ],
    }


def convert_bbox_v1_data(bbox_data: bytes) -> dict:
    """Convert GDK 1.0 brainbox data from bytes to dict
    Args:
        bbox_data (bytes): _description_

    Returns:
        dict: _description_
    """

    gdk_data = {"ch1": [], "ch2": [], "counter": []}
    for bbox_package in range(8):
        offset = bbox_package * 16
        gdk_data["ch1"].append(
            int.from_bytes(
                bytes=bbox_data[offset + 2 : offset + 5],
                byteorder="big",
                signed=True,
            )
        )
        gdk_data["ch2"].append(
            int.from_bytes(
                bytes=bbox_data[offset + 5 : offset + 8],
                byteorder="big",
                signed=True,
            )
        )
        gdk_data["counter"].append(
            int.from_bytes(bytes=bbox_data[offset + 1 : offset + 2], byteorder="big")
        )
    return gdk_data
