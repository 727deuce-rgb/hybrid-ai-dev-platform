#!/usr/bin/env python3
"""
App 1: Perceptron Decision Engine
Pattern: Monad (1 node)
Purpose: Binary classification, yes/no decisions
Params: 12 | Memory: ~2MB | Latency: <5ms
"""

import asyncio
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class PerceptronState:
    """Single perceptron state"""
    weight: float = 0.5
    bias: float = 0.0
    threshold: float = 0.5
    decisions_made: int = 0
    accuracy: float = 1.0


class App1Perceptron:
    """Monad: Simplest decision engine"""

    def __init__(self):
        self.state = PerceptronState()
        self.history = []

    async def decide(self, inputs: list, threshold: float = None) -> Dict[str, Any]:
        """Make binary decision"""
        if threshold:
            self.state.threshold = threshold

        # Simple weighted sum
        weighted_sum = sum(inputs) * self.state.weight + self.state.bias
        decision = weighted_sum > self.state.threshold

        self.state.decisions_made += 1
        result = {
            "decision": decision,
            "score": weighted_sum,
            "threshold": self.state.threshold,
            "confidence": abs(weighted_sum - self.state.threshold) / (self.state.threshold + 0.001)
        }

        self.history.append(result)
        return result

    async def train_feedback(self, actual: bool, prediction: bool):
        """Simple online learning"""
        if actual != prediction:
            # Adjust weight slightly
            self.state.weight *= 0.99
            self.state.accuracy *= 0.98
        else:
            self.state.accuracy = min(1.0, self.state.accuracy * 1.01)

    def get_status(self) -> Dict:
        """Get current status"""
        return {
            "app": "App1_Perceptron",
            "pattern": "monad",
            "nodes": 1,
            "decisions_made": self.state.decisions_made,
            "accuracy": self.state.accuracy,
            "weight": self.state.weight,
            "bias": self.state.bias
        }


async def test_app1():
    app = App1Perceptron()
    result = await app.decide([0.3, 0.4, 0.2])
    print(f"App 1 Decision: {result}")
    print(f"Status: {app.get_status()}")


if __name__ == "__main__":
    asyncio.run(test_app1())
