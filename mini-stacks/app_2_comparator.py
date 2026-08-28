#!/usr/bin/env python3
"""
App 2: Comparative Analyzer
Pattern: Dyad (2 nodes)
Purpose: A/B comparison, dual-path routing
Params: 256 | Memory: ~5MB | Latency: <10ms
"""

import asyncio
from dataclasses import dataclass
from typing import Dict, Any, Tuple


@dataclass
class DyadNode:
    """Individual node in dyad pair"""
    node_id: int
    bias: float = 0.0
    activation_fn: str = "sigmoid"
    feature_count: int = 0


class App2Comparator:
    """Dyad: Binary comparison system"""

    def __init__(self):
        self.node_a = DyadNode(0)
        self.node_b = DyadNode(1)
        self.comparisons = 0

    async def sigmoid(self, x: float) -> float:
        """Sigmoid activation"""
        return 1.0 / (1.0 + 2.71828 ** (-x))

    async def process_node(self, node: DyadNode, features: list) -> float:
        """Process through single node"""
        node.feature_count = len(features)
        score = sum(features) / (len(features) + 0.001) + node.bias
        if node.activation_fn == "sigmoid":
            return await self.sigmoid(score)
        return score

    async def compare(self, path_a: list, path_b: list) -> Dict[str, Any]:
        """Compare two paths"""
        score_a = await self.process_node(self.node_a, path_a)
        score_b = await self.process_node(self.node_b, path_b)

        self.comparisons += 1
        winner = "A" if score_a > score_b else "B"
        margin = abs(score_a - score_b)

        return {
            "score_a": score_a,
            "score_b": score_b,
            "winner": winner,
            "margin": margin,
            "confidence": margin / (max(score_a, score_b) + 0.001)
        }

    async def recommend(self, options: Dict[str, list]) -> str:
        """Recommend best option"""
        best = None
        best_score = -1

        for name, features in options.items():
            score = await self.process_node(self.node_a, features)
            if score > best_score:
                best_score = score
                best = name

        return best

    def get_status(self) -> Dict:
        return {
            "app": "App2_Comparator",
            "pattern": "dyad",
            "nodes": 2,
            "comparisons_total": self.comparisons
        }


async def test_app2():
    app = App2Comparator()
    result = await app.compare([0.7, 0.8, 0.6], [0.5, 0.4, 0.3])
    print(f"App 2 Comparison: {result}")
    print(f"Status: {app.get_status()}")


if __name__ == "__main__":
    asyncio.run(test_app2())
