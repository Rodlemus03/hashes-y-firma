from __future__ import annotations

import argparse

from lab_utils import hash_password, verify_password


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Demo Argon2id")
    parser.add_argument("password", help="Contrasena a proteger")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    password_hash = hash_password(args.password)
    print(f"Hash Argon2id: {password_hash}")
    print(f"Verificacion correcta: {verify_password(password_hash, args.password)}")
    print(f"Verificacion incorrecta: {verify_password(password_hash, args.password + '!')}")


if __name__ == "__main__":
    main()
