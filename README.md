# Bitcoin Block & Merkle Tree Assignment

## Overview

This submission covers two tasks:
1. **Task 1** — Inspection of a real Bitcoin block using blockchain explorer data
2. **Task 2** — Construction and visualization of a Merkle tree from 4 transaction hashes

---

## Task 1: Block Inspection

See [`block-inspection.md`](./block-inspection.md) for full findings.

**Block used:** Height **942,323**  
**Source:** Data verified via learnmeabitcoin.com / Bitcoin CLI

---

## Task 2: Merkle Tree

See [`merkle-tree-diagram.md`](./merkle-tree-diagram.md) for the full diagram and step-by-step calculation.

Python source code in [`code/merkle_tree.py`](./code/merkle_tree.py) computes and verifies the Merkle root using double-SHA256, matching Bitcoin's actual algorithm.

---

## Key Learnings

- Every block references its predecessor via `previousblockhash`, forming an immutable chain.
- The **Merkle root** is a compact 32-byte fingerprint of every transaction in the block — changing even one transaction byte invalidates it.
- Merkle trees allow **SPV (Simplified Payment Verification)**: a wallet can prove a transaction is in a block using only O(log n) hashes, not all ~1,500 transactions.
- Bitcoin uses **double-SHA256** (`SHA256(SHA256(data))`) at every hashing step for extra security.
