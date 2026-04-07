from __future__ import annotations

import argparse

from lab_utils import sign_file


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Firmar manifiesto")
    parser.add_argument("--manifest", default="SHA256SUMS.txt")
    parser.add_argument("--private-key", default="medisoft_priv.pem")
    parser.add_argument("--signature", default="SHA256SUMS.sig")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    sign_file(args.manifest, args.private_key, args.signature)
    print(f"Firma generada en: {args.signature}")


if __name__ == "__main__":
    main()
