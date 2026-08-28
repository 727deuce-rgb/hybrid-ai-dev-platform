#!/usr/bin/env python3
"""
Mini-Stack Coordinator
Unifies all 5 applications under single control
"""

import asyncio
from typing import Dict, Any
from app_1_perceptron import App1Perceptron
from app_2_comparator import App2Comparator
from app_3_validator import App3Validator
from app_4_draco_hub import App4DracoHub
from app_5_expander import App5Expander


class MiniStackCoordinator:
    """Central coordinator for all 5 mini-stack apps"""

    def __init__(self):
        self.app1 = App1Perceptron()
        self.app2 = App2Comparator()
        self.app3 = App3Validator()
        self.app4 = App4DracoHub()
        self.app5 = App5Expander()
        self.total_executions = 0

    async def execute_workflow(self, data: Dict[str, Any]) -> Dict:
        """Execute complete workflow through all apps"""
        results = {}

        # App 1: Simple decision
        result1 = await self.app1.decide([data.get("value", 0.5)])
        results["app1_decision"] = result1["decision"]

        # App 2: Comparison
        result2 = await self.app2.compare([0.6], [0.4])
        results["app2_winner"] = result2["winner"]

        # App 3: Triangulated validation
        result3 = await self.app3.triangulate([0.5, 0.6, 0.7])
        results["app3_consensus"] = result3["consensus"]

        # App 4: Route through hub
        result4 = await self.app4.route_task({"type": "fast", "priority": 8})
        results["app4_routed"] = result4["status"]

        # App 5: Distributed processing
        result5 = await self.app5.distribute_task([0.2, 0.4, 0.6, 0.8, 1.0])
        results["app5_consensus"] = result5["consensus"]

        self.total_executions += 1
        results["execution_id"] = self.total_executions

        return results

    def get_all_status(self) -> Dict:
        """Get status of all apps"""
        return {
            "coordinator_executions": self.total_executions,
            "apps": {
                "app1": self.app1.get_status(),
                "app2": self.app2.get_status(),
                "app3": self.app3.get_status(),
                "app4": self.app4.get_status(),
                "app5": self.app5.get_status()
            }
        }


async def main():
    coordinator = MiniStackCoordinator()

    # Run workflow
    result = await coordinator.execute_workflow({"value": 0.65})
    print(f"Workflow Result: {result}")

    # Get overall status
    status = coordinator.get_all_status()
    print(f"\nAll Apps Status: {status}")


if __name__ == "__main__":
    asyncio.run(main())
