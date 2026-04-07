from __future__ import annotations

import argparse

from lab_utils import verify_file_signature


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verificar firma digital")
    parser.add_argument("--manifest", default="SHA256SUMS.txt")
    parser.add_argument("--public-key", default="medisoft_pub.pem")
    parser.add_argument("--signature", default="SHA256SUMS.sig")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    is_valid = verify_file_signature(args.manifest, args.public_key, args.signature)
    if is_valid:
        print("Firma valida: el manifiesto fue emitido por MediSoft y no ha cambiado.")
    else:
        print("Firma invalida: el manifiesto o la firma fueron alterados.")


if __name__ == "__main__":
    main()
