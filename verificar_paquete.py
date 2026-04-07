from __future__ import annotations

import argparse

from lab_utils import verify_manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verificar un paquete")
    parser.add_argument("--manifest", default="SHA256SUMS.txt", help="Ruta del manifiesto")
    parser.add_argument(
        "--base-dir",
        default=".",
        help="Directorio base donde estan los archivos listados",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = verify_manifest(args.manifest, args.base_dir)
    print(f"{'Archivo':<40} {'Estado':<10} SHA-256 actual")
    print("-" * 130)
    for result in results:
        current = result.actual_hash if result.actual_hash is not None else "<no existe>"
        print(f"{result.path.name:<40} {result.status:<10} {current}")

    total_ok = sum(result.status == "OK" for result in results)
    print()
    print(f"Archivos verificados: {len(results)}")
    print(f"Correctos: {total_ok}")
    print(f"No correctos: {len(results) - total_ok}")


if __name__ == "__main__":
    main()
