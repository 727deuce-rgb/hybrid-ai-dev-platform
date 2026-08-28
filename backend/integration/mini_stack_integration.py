#!/usr/bin/env python3
"""
Integration module: Connects mini-stack apps to DRACO-4 orchestrator
"""

import asyncio
from typing import Dict, Any

# Import mini-stack apps
import sys
sys.path.insert(0, '../mini-stacks')
from app_1_perceptron import App1Perceptron
from app_2_comparator import App2Comparator
from app_3_validator import App3Validator
from app_4_draco_hub import App4DracoHub
from app_5_expander import App5Expander


class MiniStackIntegration:
    """Integration layer connecting mini-stacks to DRACO-4"""

    def __init__(self):
        self.app1 = App1Perceptron()
        self.app2 = App2Comparator()
        self.app3 = App3Validator()
        self.app4 = App4DracoHub()
        self.app5 = App5Expander()

    async def execute_app1(self, payload: Dict[str, Any]) -> Dict:
        """Execute App 1: Perceptron"""
        data = payload.get('data', [0.5])
        threshold = payload.get('threshold')
        return await self.app1.decide(data, threshold)

    async def execute_app2(self, payload: Dict[str, Any]) -> Dict:
        """Execute App 2: Comparator"""
        path_a = payload.get('path_a', [0.5])
        path_b = payload.get('path_b', [0.5])
        return await self.app2.compare(path_a, path_b)

    async def execute_app3(self, payload: Dict[str, Any]) -> Dict:
        """Execute App 3: Validator"""
        data = payload.get('data', [0.5])
        return await self.app3.triangulate(data)

    async def execute_app4(self, payload: Dict[str, Any]) -> Dict:
        """Execute App 4: DRACO Hub"""
        task = payload.get('task', {'type': 'default'})
        return await self.app4.route_task(task)

    async def execute_app5(self, payload: Dict[str, Any]) -> Dict:
        """Execute App 5: Expander"""
        features = payload.get('features', [0.1, 0.2, 0.3])
        return await self.app5.distribute_task(features)

    async def execute_workflow(self, payload: Dict[str, Any]) -> Dict:
        """Execute complete workflow through all apps"""
        results = {}
        
        # Sequential execution
        results['app1'] = await self.execute_app1(payload)
        results['app2'] = await self.execute_app2(payload)
        results['app3'] = await self.execute_app3(payload)
        results['app4'] = await self.execute_app4(payload)
        results['app5'] = await self.execute_app5(payload)
        
        return results

    def get_all_status(self) -> Dict:
        """Get status of all integrated apps"""
        return {
            "app1": self.app1.get_status(),
            "app2": self.app2.get_status(),
            "app3": self.app3.get_status(),
            "app4": self.app4.get_status(),
            "app5": self.app5.get_status()
        }


# Singleton instance
integration = MiniStackIntegration()


async def test():
    """Test integration"""
    payload = {
        'data': [0.5, 0.6, 0.7],
        'path_a': [0.7],
        'path_b': [0.3],
        'features': [0.1, 0.2, 0.3, 0.4, 0.5]
    }
    result = await integration.execute_workflow(payload)
    print(f"Workflow result: {result}")


if __name__ == "__main__":
    asyncio.run(test())
