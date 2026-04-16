# Block Inspection Results

**Explorer used:** learnmeabitcoin.com / Bitcoin CLI (`getblockheader`)

---

```
Block Inspection Results
------------------------
Block Height:         942,323
Block Hash:           00000000000000000000c3cdb1c61f93f8160a4cc51aa8f553ebbadbedbe26c6
Previous Block Hash:  00000000000000000000e936942f76fafde0ad5a4148efee8cf16bfe11c91993
Merkle Root:          840d38b5ef614b673538055cdabe7533f84a8dc4603cd5809b713ef18f7e1357
Number of Transactions: 1,513
Timestamp:            Unix 1774532097  →  2026-01-22 ~18:14 UTC
```

---

## Field Explanations

### Block Height — `942,323`
The position of this block in the chain, counting from the genesis block (height 0). As of early 2026, Bitcoin has mined over 942,000 blocks — roughly one every 10 minutes since January 2009.

### Block Hash — `00000000000000000000c3cdb1...`
A double-SHA256 hash of the block header. Notice the many leading zeros — this is the **proof-of-work**: miners had to find a nonce that makes the header hash fall below the current difficulty target. This block's difficulty was approximately **133.8 trillion**, meaning the probability of any single hash succeeding was ~1 in 133.8 trillion.

### Previous Block Hash — `00000000000000000000e936...`
This field is what "chains" blocks together. Block 942,323 explicitly references block 942,322's hash inside its own header. If anyone tried to alter block 942,322, its hash would change, breaking block 942,323's reference — and every block after it. This is the foundation of blockchain immutability.

### Merkle Root — `840d38b5ef614b67...`
A 32-byte summary of all 1,513 transactions in this block, computed by the Merkle tree algorithm (see Task 2). It sits in the block header, meaning the header commits to the exact set of transactions — adding, removing, or modifying any transaction changes the Merkle root and invalidates the block.

### Number of Transactions — `1,513`
This block contained 1,513 transactions, including the coinbase transaction (the miner's reward). With ~1,513 transactions and a 10-minute block time, Bitcoin processed about 2–3 transactions per second for this block.

### Timestamp — `1774532097` (Unix epoch)
Converts to approximately **22 January 2026, 18:14 UTC**. Bitcoin timestamps have ~2-hour tolerance; they aren't required to be perfectly accurate, just within the window enforced by network consensus.

---

## Raw Header Data (from Bitcoin CLI)

```json
{
  "hash":             "00000000000000000000c3cdb1c61f93f8160a4cc51aa8f553ebbadbedbe26c6",
  "height":           942323,
  "version":          725164032,
  "versionHex":       "2b392000",
  "merkleroot":       "840d38b5ef614b673538055cdabe7533f84a8dc4603cd5809b713ef18f7e1357",
  "time":             1774532097,
  "mediantime":       1774530283,
  "nonce":            3974639198,
  "bits":             "17021a91",
  "difficulty":       133793147307542.8,
  "nTx":              1513,
  "previousblockhash":"00000000000000000000e936942f76fafde0ad5a4148efee8cf16bfe11c91993"
}
```
