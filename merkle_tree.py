"""
merkle_tree.py
--------------
Constructs a Bitcoin-style Merkle tree from a list of transaction IDs
and computes the Merkle root using double-SHA256, exactly as Bitcoin does.

Usage:
    python3 merkle_tree.py

Author: Assignment submission
"""

import hashlib


# ──────────────────────────────────────────────
# Core hashing helpers
# ──────────────────────────────────────────────

def dsha256(data: bytes) -> bytes:
    """Double-SHA256: SHA256(SHA256(data)) — Bitcoin's standard hash function."""
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def hash_pair(left_hex: str, right_hex: str) -> str:
    """
    Combine two hex-encoded hashes and return their double-SHA256 as hex.

    Bitcoin stores TXIDs in internal byte order (little-endian), so we
    reverse each 32-byte hash before concatenating, then reverse the result.
    """
    left_bytes  = bytes.fromhex(left_hex)[::-1]   # to internal byte order
    right_bytes = bytes.fromhex(right_hex)[::-1]

    combined = left_bytes + right_bytes
    result   = dsha256(combined)

    return result[::-1].hex()                      # back to display byte order


# ──────────────────────────────────────────────
# Merkle tree builder
# ──────────────────────────────────────────────

def build_merkle_tree(txids: list[str]) -> tuple[str, list[list[str]]]:
    """
    Build a Merkle tree from a list of TXIDs (hex strings).

    Returns:
        merkle_root : str         — the final root hash (hex)
        levels      : list[list]  — all tree levels, bottom-up, for display
    """
    if not txids:
        raise ValueError("Transaction list cannot be empty.")

    levels = [txids[:]]   # level 0 = leaf layer
    current = txids[:]

    while len(current) > 1:
        next_level = []

        # Duplicate last element if count is odd (Bitcoin rule)
        if len(current) % 2 == 1:
            current.append(current[-1])
            print(f"  [odd-tx rule] Duplicated last hash: {current[-1][:16]}…")

        for i in range(0, len(current), 2):
            parent = hash_pair(current[i], current[i + 1])
            next_level.append(parent)
            print(f"  Hash({current[i][:12]}… , {current[i+1][:12]}…)")
            print(f"    → {parent[:16]}…")

        levels.append(next_level)
        current = next_level

    return current[0], levels


# ──────────────────────────────────────────────
# Pretty printer
# ──────────────────────────────────────────────

def print_tree(levels: list[list[str]]):
    """Print all Merkle tree levels from root down to leaves."""
    print("\n" + "=" * 70)
    print("  MERKLE TREE  (root → leaves)")
    print("=" * 70)

    for i, level in enumerate(reversed(levels)):
        label = "Root  " if i == len(levels) - 1 else f"Level {i}"
        for j, h in enumerate(level):
            print(f"  {label}  [{j}]  {h}")
    print("=" * 70)


# ──────────────────────────────────────────────
# Main — 4 example transaction IDs
# ──────────────────────────────────────────────

EXAMPLE_TXIDS = [
    "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2",
    "b2c3d4e5f6a7b2c3d4e5f6a7b2c3d4e5f6a7b2c3d4e5f6a7b2c3d4e5f6a7b2c3",
    "c3d4e5f6a7b8c3d4e5f6a7b8c3d4e5f6a7b8c3d4e5f6a7b8c3d4e5f6a7b8c3d4",
    "d4e5f6a7b8c9d4e5f6a7b8c9d4e5f6a7b8c9d4e5f6a7b8c9d4e5f6a7b8c9d4e5",
]


def main():
    print("\nBitcoin Merkle Tree Calculator")
    print("Using double-SHA256 (Bitcoin's native algorithm)\n")

    print("Input TXIDs:")
    labels = ["TxA", "TxB", "TxC", "TxD"]
    for label, txid in zip(labels, EXAMPLE_TXIDS):
        print(f"  {label}: {txid}")

    print("\nHashing pairs at each level:")
    merkle_root, levels = build_merkle_tree(EXAMPLE_TXIDS)

    print_tree(levels)

    print(f"\n✅  Merkle Root: {merkle_root}")
    print()

    # ── Demonstrate the odd-transaction rule ──
    print("\n--- Demonstrating the odd-transaction rule (3 TXIDs) ---")
    three_txids = EXAMPLE_TXIDS[:3]
    root_odd, _ = build_merkle_tree(three_txids)
    print(f"✅  Merkle Root (3 txs): {root_odd}\n")


if __name__ == "__main__":
    main()
