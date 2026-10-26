"""密钥存储：Windows DPAPI 优先，失败时退回本地受限文件。"""

from __future__ import annotations

import base64
import ctypes
import json
import os
from ctypes import wintypes
from pathlib import Path

_CRYPTPROTECT_UI_FORBIDDEN = 0x01
_CRYPTPROTECT_LOCAL_MACHINE = 0x04


class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]


def _blob(data: bytes) -> tuple[DATA_BLOB, ctypes.Array]:
    buffer = ctypes.create_string_buffer(data, len(data))
    return DATA_BLOB(len(data), ctypes.cast(buffer, ctypes.POINTER(ctypes.c_char))), buffer


def _dpapi_protect(data: bytes, machine: bool = False) -> bytes | None:
    if os.name != "nt":
        return None
    crypt = ctypes.windll.crypt32
    kernel = ctypes.windll.kernel32
    in_blob, in_buffer = _blob(data)
    out_blob = DATA_BLOB()
    flags = _CRYPTPROTECT_UI_FORBIDDEN | (_CRYPTPROTECT_LOCAL_MACHINE if machine else 0)
    if not crypt.CryptProtectData(
        ctypes.byref(in_blob), None, None, None, None, flags, ctypes.byref(out_blob)
    ):
        return None
    try:
        return ctypes.string_at(out_blob.pbData, out_blob.cbData)
    finally:
        kernel.LocalFree(out_blob.pbData)


def _dpapi_unprotect(data: bytes) -> bytes | None:
    if os.name != "nt":
        return None
    crypt = ctypes.windll.crypt32
    kernel = ctypes.windll.kernel32
    in_blob, in_buffer = _blob(data)
    out_blob = DATA_BLOB()
    if not crypt.CryptUnprotectData(
        ctypes.byref(in_blob), None, None, None, None,
        _CRYPTPROTECT_UI_FORBIDDEN, ctypes.byref(out_blob),
    ):
        return None
    try:
        return ctypes.string_at(out_blob.pbData, out_blob.cbData)
    finally:
        kernel.LocalFree(out_blob.pbData)


class SecretStore:
    """把 API Key 加密后存到用户配置目录；读取时解密。"""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.backend = "plain" if os.name != "nt" else "dpapi"

    def set(self, key: str, value: str) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps({key: value}, ensure_ascii=False).encode("utf-8")
        if self.backend == "dpapi":
            protected = _dpapi_protect(payload)
            if protected is not None:
                self.path.write_bytes(protected)
                return
            self.backend = "plain"
        self.path.write_text(
            json.dumps({key: value, "_plain": True}, ensure_ascii=False), encoding="utf-8"
        )
        try:
            os.chmod(self.path, 0o600)
        except OSError:
            pass

    def get(self, key: str) -> str:
        if not self.path.exists():
            return ""
        raw = self.path.read_bytes()
        if self.backend == "dpapi":
            decrypted = _dpapi_unprotect(raw)
            if decrypted is not None:
                try:
                    return json.loads(decrypted.decode("utf-8")).get(key, "")
                except Exception:  # noqa: BLE001
                    return ""
        try:
            data = json.loads(raw.decode("utf-8"))
        except Exception:  # noqa: BLE001
            return ""
        return data.get(key, "")

    def has(self, key: str) -> bool:
        return bool(self.get(key))
