# Week 12-13 - Part B: Hands-on Blockchain Lab
# CS 475 Introduction to Computer Security

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
import time


@dataclass
class Transaction:
    sender: str
    recipient: str
    amount: float


@dataclass
class Block:
    index: int
    timestamp: float
    transactions: list[Transaction]
    previous_hash: str
    nonce: int = 0
    hash: str = ""

    def compute_hash(self) -> str:
        payload = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [t.__dict__ for t in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


@dataclass
class ToyBlockchain:
    difficulty_prefix: str = "0000"
    chain: list[Block] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.chain:
            genesis = Block(
                index=0,
                timestamp=time.time(),
                transactions=[Transaction("network", "genesis", 0.0)],
                previous_hash="0" * 64,
            )
            self.mine_block(genesis)
            self.chain.append(genesis)

    def mine_block(self, block: Block) -> None:
        while True:
            digest = block.compute_hash()
            if digest.startswith(self.difficulty_prefix):
                block.hash = digest
                return
            block.nonce += 1

    def add_block(self, txs: list[Transaction]) -> Block:
        prev = self.chain[-1]
        block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=txs,
            previous_hash=prev.hash,
        )
        self.mine_block(block)
        self.chain.append(block)
        return block

    def is_valid(self) -> tuple[bool, str]:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.previous_hash != previous.hash:
                return False, f"Block {i} previous_hash mismatch"

            if current.compute_hash() != current.hash:
                return False, f"Block {i} content hash mismatch"

            if not current.hash.startswith(self.difficulty_prefix):
                return False, f"Block {i} proof-of-work prefix invalid"

        return True, "Chain is valid"


def print_chain(chain: ToyBlockchain, header: str) -> None:
    print(f"\n{header}")
    print(f"  {'idx':<4} {'nonce':<8} {'prev_hash[:12]':<15} {'hash[:12]':<15} tx_count")
    print(f"  {'-'*3} {'-'*7} {'-'*14} {'-'*14} {'-'*8}")
    for b in chain.chain:
        print(
            f"  {b.index:<4} {b.nonce:<8} {b.previous_hash[:12]:<15} "
            f"{b.hash[:12]:<15} {len(b.transactions)}"
        )


def run_lab() -> None:
    print("Part B-1: Build and run a toy blockchain")
    chain = ToyBlockchain(difficulty_prefix="0000")

    chain.add_block([
        Transaction("alice", "bob", 2.5),
        Transaction("bob", "charlie", 1.0),
    ])
    chain.add_block([
        Transaction("charlie", "dana", 0.25),
    ])

    ok, msg = chain.is_valid()
    print_chain(chain, "State after normal mining")
    print(f"\nValidation result: {ok} - {msg}")

    print("\nPart B-2: Deliberately break the chain")
    chain.chain[1].transactions[0].amount = 2500.0

    ok2, msg2 = chain.is_valid()
    print(f"Validation after tampering: {ok2} - {msg2}")

    print("\nPart B-3: Attempt local attacker repair")
    chain.mine_block(chain.chain[1])
    ok3, msg3 = chain.is_valid()
    print(f"Validation after re-mining only block 1: {ok3} - {msg3}")

    print(
        "\nInterpretation: an attacker must re-mine all subsequent blocks and outrun honest "
        "participants, which demonstrates why proof-of-work raises attack cost."
    )


if __name__ == "__main__":
    run_lab()
