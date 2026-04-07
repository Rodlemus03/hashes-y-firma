from __future__ import annotations

import argparse

from lab_utils import generate_rsa_keypair


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generar claves RSA")
    parser.add_argument("--private-key", default="medisoft_priv.pem")
    parser.add_argument("--public-key", default="medisoft_pub.pem")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generate_rsa_keypair(args.private_key, args.public_key)
    print(f"Clave privada creada en: {args.private_key}")
    print(f"Clave publica creada en: {args.public_key}")


if __name__ == "__main__":
    main()
