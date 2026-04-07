from __future__ import annotations

import argparse

from lab_utils import hmac_sha256, insecure_prefix_mac, verify_hmac


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Demo HMAC")
    parser.add_argument("--secret", default="medisoft-api-key")
    parser.add_argument("--message", default="POST:/api/releases:v2.1.0")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    secret = args.secret.encode("utf-8")
    message = args.message.encode("utf-8")
    signature = hmac_sha256(secret, message)

    print(f"Mensaje       : {args.message}")
    print(f"HMAC-SHA256   : {signature}")
    print(f"Verifica      : {verify_hmac(secret, message, signature)}")
    print(f"H(secret||m)  : {insecure_prefix_mac(secret, message)}")
    print("El patron H(secret || mensaje) no debe usarse: carece de las garantias estructurales de HMAC.")


if __name__ == "__main__":
    main()
