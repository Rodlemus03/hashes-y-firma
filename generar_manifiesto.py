from __future__ import annotations

import argparse

from lab_utils import append_manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generar manifiesto SHA-256")
    parser.add_argument("files", nargs="+", help="Archivos a registrar")
    parser.add_argument(
        "--manifest",
        default="SHA256SUMS.txt",
        help="Ruta del manifiesto de salida",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if len(args.files) < 5:
        raise SystemExit("Debes proporcionar al menos 5 archivos.")
    entries = append_manifest(args.files, args.manifest)
    print(f"Manifiesto actualizado: {args.manifest}")
    for digest, filename in entries:
        print(f"{digest} {filename}")


if __name__ == "__main__":
    main()
