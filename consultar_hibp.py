from __future__ import annotations

from lab_utils import hibp_breach_count, sha256_hex


PASSWORDS = ["admin", "123456", "hospital", "medisoft2024"]


def main() -> None:
    print(f"{'Password':<15} {'SHA-256':<64} Veces en HIBP")
    print("-" * 98)
    for password in PASSWORDS:
        count = hibp_breach_count(password)
        print(f"{password:<15} {sha256_hex(password):<64} {count}")


if __name__ == "__main__":
    main()
