from __future__ import annotations

from lab_utils import build_hash_rows, count_changed_bits, digest_text


ORIGINAL = "MediSoft-v2.1.0"
VARIANT = "medisoft-v2.1.0"


def print_table(rows: list[dict[str, str | int]], title: str) -> None:
    print(title)
    print(f"{'Algoritmo':<10} {'Bits':<6} {'Hex':<6} Hash")
    print("-" * 100)
    for row in rows:
        print(f"{row['algorithm']:<10} {row['bits']:<6} {row['hex_length']:<6} {row['hash']}")
    print()


def main() -> None:
    original_rows = build_hash_rows(ORIGINAL)
    variant_rows = build_hash_rows(VARIANT)

    print_table(original_rows, f'Hashes para "{ORIGINAL}"')
    print_table(variant_rows, f'Hashes para "{VARIANT}"')

    original_sha256 = digest_text("sha256", ORIGINAL)
    variant_sha256 = digest_text("sha256", VARIANT)
    changed_bits = count_changed_bits(original_sha256, variant_sha256)

    print("Comparacion SHA-256")
    print(f"Original : {original_sha256}")
    print(f"Variante : {variant_sha256}")
    print(f"Bits distintos (XOR): {changed_bits}")


if __name__ == "__main__":
    main()
