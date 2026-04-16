# Merkle Tree Visualization

## Input: 4 Transaction Hashes

These are example transaction IDs (shortened for readability; full 64-char hex below).

| Label | Full TXID (64 hex chars) |
|-------|--------------------------|
| TxA   | `a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2` |
| TxB   | `b2c3d4e5f6a7b2c3d4e5f6a7b2c3d4e5f6a7b2c3d4e5f6a7b2c3d4e5f6a7b2c3` |
| TxC   | `c3d4e5f6a7b8c3d4e5f6a7b8c3d4e5f6a7b8c3d4e5f6a7b8c3d4e5f6a7b8c3d4` |
| TxD   | `d4e5f6a7b8c9d4e5f6a7b8c9d4e5f6a7b8c9d4e5f6a7b8c9d4e5f6a7b8c9d4e5` |

> **Note:** Bitcoin uses *internal byte order* (little-endian) for TXIDs in Merkle computation. The Python script in `code/merkle_tree.py` handles this correctly.

---

## Tree Structure

```
                        ┌─────────────────────────┐
                        │       MERKLE ROOT        │
                        │  Hash(Hash_AB + Hash_CD)  │
                        └────────────┬────────────┘
                                     │
               ┌─────────────────────┴─────────────────────┐
               │                                           │
    ┌──────────┴──────────┐                   ┌──────────┴──────────┐
    │       Hash_AB        │                   │       Hash_CD        │
    │  Hash(TxA + TxB)    │                   │  Hash(TxC + TxD)    │
    └──────┬──────┬───────┘                   └──────┬──────┬───────┘
           │      │                                   │      │
        ┌──┴─┐  ┌─┴──┐                            ┌──┴─┐  ┌─┴──┐
        │ TxA│  │ TxB│                            │ TxC│  │ TxD│
        └────┘  └────┘                            └────┘  └────┘

  Level 0 (Leaves):   TxA        TxB        TxC        TxD
  Level 1 (Pairs):        Hash_AB                Hash_CD
  Level 2 (Root):              Merkle Root
```

---

## Step-by-Step Calculation

Bitcoin's hashing function at each step is **double-SHA256**:

```
Hash(x) = SHA256( SHA256( x ) )
```

### Step 1 — Hash the leaf transactions

```
Hash_A  = dSHA256( TxA )
Hash_B  = dSHA256( TxB )
Hash_C  = dSHA256( TxC )
Hash_D  = dSHA256( TxD )
```

*(In practice these ARE the TXIDs themselves — a TXID is already the double-SHA256 of the serialised transaction.)*

### Step 2 — Pair and hash at Level 1

```
Hash_AB = dSHA256( Hash_A  ||  Hash_B )
Hash_CD = dSHA256( Hash_C  ||  Hash_D )
```

Where `||` means byte-concatenation of the two 32-byte values.

### Step 3 — Compute the Merkle Root (Level 2)

```
Merkle Root = dSHA256( Hash_AB  ||  Hash_CD )
```

---

## Computed Values (from `code/merkle_tree.py`)

Run `python3 code/merkle_tree.py` to reproduce these results.

```
TxA     = a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2
TxB     = b2c3d4e5f6a7b2c3d4e5f6a7b2c3d4e5f6a7b2c3d4e5f6a7b2c3d4e5f6a7b2c3
TxC     = c3d4e5f6a7b8c3d4e5f6a7b8c3d4e5f6a7b8c3d4e5f6a7b8c3d4e5f6a7b8c3d4
TxD     = d4e5f6a7b8c9d4e5f6a7b8c9d4e5f6a7b8c9d4e5f6a7b8c9d4e5f6a7b8c9d4e5

Hash_AB = 2fd2927910b621f164a787f3ba7ede243d12684fb8ac2c9dcfb07837d462b0fb
Hash_CD = 6401351b7ec7ac7ff9060263220727185531f2a14c663c57e9992a6b48b6290d

Merkle Root = 42d15bbecbb6aa29245f48a2aedabfad30a42e626a612f0217c666120a8a3ff7
```

---

## The Odd-Transaction Rule

If a block has an **odd** number of transactions, Bitcoin duplicates the last TXID to make the count even before pairing:

```
Odd case (3 txs):   TxA   TxB   TxC   TxC  ← TxC duplicated
                      └─AB─┘     └─CC─┘
                           └─Root─┘
```

---

## Why Merkle Trees Matter

| Property | Benefit |
|----------|---------|
| **Tamper detection** | Changing any transaction changes the root → invalidates the block header |
| **Efficient proofs** | Prove a tx is in a block with only O(log₂ n) hashes, not all n TXIDs |
| **SPV wallets** | Light clients verify payments without downloading the full blockchain |
| **Compact commitment** | 1,513 transactions summarised in just 32 bytes |
