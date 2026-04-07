from __future__ import annotations

import hashlib
import hmac
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


ALGORITHMS = {
    "MD5": "md5",
    "SHA-1": "sha1",
    "SHA-256": "sha256",
    "SHA3-256": "sha3_256",
}

HIBP_RANGE_URL = "https://api.pwnedpasswords.com/range/{prefix}"

PASSWORD_HASHER = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=4,
    hash_len=32,
    salt_len=16,
)


@dataclass
class VerificationResult:
    path: Path
    expected_hash: str
    actual_hash: str | None
    status: str


def digest_text(algorithm: str, text: str) -> str:
    hasher = hashlib.new(algorithm)
    hasher.update(text.encode("utf-8"))
    return hasher.hexdigest()


def file_sha256(path: str | Path, chunk_size: int = 65536) -> str:
    hasher = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def count_changed_bits(hex_a: str, hex_b: str) -> int:
    return (int(hex_a, 16) ^ int(hex_b, 16)).bit_count()


def build_hash_rows(text: str) -> list[dict[str, str | int]]:
    rows = []
    for label, algorithm in ALGORITHMS.items():
        digest = digest_text(algorithm, text)
        rows.append(
            {
                "algorithm": label,
                "bits": len(bytes.fromhex(digest)) * 8,
                "hex_length": len(digest),
                "hash": digest,
            }
        )
    return rows


def sha1_hex(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest().upper()


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def hibp_breach_count(password: str, timeout: int = 10) -> int:
    sha1_hash = sha1_hex(password)
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]
    request = urllib.request.Request(
        HIBP_RANGE_URL.format(prefix=prefix),
        headers={"Add-Padding": "true", "User-Agent": "medisoft-lab/1.0"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read().decode("utf-8")
    for line in body.splitlines():
        candidate_suffix, count = line.split(":")
        if candidate_suffix == suffix:
            return int(count)
    return 0


def hash_password(password: str) -> str:
    return PASSWORD_HASHER.hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    try:
        return PASSWORD_HASHER.verify(password_hash, password)
    except VerifyMismatchError:
        return False


def hmac_sha256(secret: bytes, message: bytes) -> str:
    return hmac.new(secret, message, hashlib.sha256).hexdigest()


def verify_hmac(secret: bytes, message: bytes, signature: str) -> bool:
    return hmac.compare_digest(hmac_sha256(secret, message), signature)


def insecure_prefix_mac(secret: bytes, message: bytes) -> str:
    return hashlib.sha256(secret + message).hexdigest()


def generate_manifest_entries(files: list[str | Path]) -> list[tuple[str, str]]:
    entries = []
    for file_path in files:
        path = Path(file_path)
        entries.append((file_sha256(path), path.name))
    return entries


def append_manifest(files: list[str | Path], manifest_path: str | Path) -> list[tuple[str, str]]:
    manifest = Path(manifest_path)
    entries = generate_manifest_entries(files)
    with manifest.open("a", encoding="utf-8") as handle:
        for digest, filename in entries:
            handle.write(f"{digest} {filename}\n")
    return entries


def read_manifest(manifest_path: str | Path) -> list[tuple[str, str]]:
    entries = []
    with Path(manifest_path).open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            digest, filename = stripped.split(maxsplit=1)
            entries.append((digest, filename))
    return entries


def verify_manifest(manifest_path: str | Path, base_dir: str | Path = ".") -> list[VerificationResult]:
    results = []
    root = Path(base_dir)
    for expected_hash, filename in read_manifest(manifest_path):
        file_path = root / filename
        if not file_path.exists():
            results.append(VerificationResult(file_path, expected_hash, None, "MISSING"))
            continue
        actual_hash = file_sha256(file_path)
        status = "OK" if actual_hash == expected_hash else "ALTERADO"
        results.append(VerificationResult(file_path, expected_hash, actual_hash, status))
    return results


def generate_rsa_keypair(private_key_path: str | Path, public_key_path: str | Path, bits: int = 2048) -> None:
    key = RSA.generate(bits)
    Path(private_key_path).write_bytes(key.export_key())
    Path(public_key_path).write_bytes(key.publickey().export_key())


def sign_file(file_path: str | Path, private_key_path: str | Path, signature_path: str | Path) -> bytes:
    private_key = RSA.import_key(Path(private_key_path).read_bytes())
    payload = Path(file_path).read_bytes()
    signature = pkcs1_15.new(private_key).sign(SHA256.new(payload))
    Path(signature_path).write_bytes(signature)
    return signature


def verify_file_signature(file_path: str | Path, public_key_path: str | Path, signature_path: str | Path) -> bool:
    public_key = RSA.import_key(Path(public_key_path).read_bytes())
    payload = Path(file_path).read_bytes()
    signature = Path(signature_path).read_bytes()
    try:
        pkcs1_15.new(public_key).verify(SHA256.new(payload), signature)
        return True
    except (ValueError, TypeError):
        return False
