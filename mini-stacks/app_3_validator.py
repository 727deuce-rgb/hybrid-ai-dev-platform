#!/usr/bin/env python3
"""
App 3: Stable Processing Core (Triangle Validator)
Pattern: Triad (3 nodes - stable triangle)
Purpose: Triangulated decision with 3 validators
Params: 1K | Memory: ~12MB | Latency: <20ms
"""

import asyncio
from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class ValidatorNode:
    """Individual validator node"""
    node_id: int
    name: str
    threshold: float = 0.5
    bias: float = 0.0
    validations: int = 0
    agreement_rate: float = 1.0


class App3Validator:
    """Triad: Three-point validation system (stable)"""

    def __init__(self):
        self.validators = [
            ValidatorNode(0, "strict", threshold=0.7),
            ValidatorNode(1, "moderate", threshold=0.5),
            ValidatorNode(2, "lenient", threshold=0.3)
        ]
        self.consensus_decisions = 0

    async def validate_point(self, validator: ValidatorNode, data: list) -> bool:
        """Single validator point"""
        score = (sum(data) / len(data)) + validator.bias if data else 0
        validator.validations += 1
        return score > validator.threshold

    async def triangulate(self, data: list) -> Dict[str, Any]:
        """Get consensus from 3 validators"""
        votes = []
        details = []

        for validator in self.validators:
            decision = await self.validate_point(validator, data)
            votes.append(decision)
            details.append({
                "validator": validator.name,
                "decision": decision,
                "threshold": validator.threshold
            })

        # Consensus: 2+ votes
        consensus = sum(votes) >= 2
        confidence = sum(votes) / 3.0

        self.consensus_decisions += 1

        return {
            "consensus": consensus,
            "confidence": confidence,
            "votes": sum(votes),
            "validators": details,
            "stable": abs(confidence - 0.5) < 0.4  # Near-consensus is unstable
        }

    def get_status(self) -> Dict:
        return {
            "app": "App3_Validator",
            "pattern": "triad",
            "nodes": 3,
            "consensus_decisions": self.consensus_decisions,
            "validators": [
                {"name": v.name, "validations": v.validations}
                for v in self.validators
            ]
        }


async def test_app3():
    app = App3Validator()
    result = await app.triangulate([0.6, 0.7, 0.5])
    print(f"App 3 Validation: {result}")
    print(f"Status: {app.get_status()}")


if __name__ == "__main__":
    asyncio.run(test_app3())
