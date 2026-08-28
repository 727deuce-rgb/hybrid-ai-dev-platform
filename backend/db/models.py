#!/usr/bin/env python3
"""
Database models and ORM setup
"""

from datetime import datetime
from typing import Optional, List


class Task:
    """Task model"""
    def __init__(
        self,
        task_id: str,
        agent_id: str,
        status: str,
        payload: dict,
        result: Optional[dict] = None,
        created_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None
    ):
        self.task_id = task_id
        self.agent_id = agent_id
        self.status = status
        self.payload = payload
        self.result = result
        self.created_at = created_at or datetime.now()
        self.completed_at = completed_at

    def to_dict(self):
        return {
            'task_id': self.task_id,
            'agent_id': self.agent_id,
            'status': self.status,
            'payload': self.payload,
            'result': self.result,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }


class Agent:
    """Agent model"""
    def __init__(
        self,
        agent_id: str,
        role: str,
        pattern: str,
        status: str = 'active'
    ):
        self.agent_id = agent_id
        self.role = role
        self.pattern = pattern
        self.status = status
        self.tasks_processed = 0
        self.last_active = datetime.now()

    def to_dict(self):
        return {
            'agent_id': self.agent_id,
            'role': self.role,
            'pattern': self.pattern,
            'status': self.status,
            'tasks_processed': self.tasks_processed,
            'last_active': self.last_active.isoformat()
        }


class Metric:
    """Metric model"""
    def __init__(
        self,
        metric_id: str,
        agent_id: str,
        metric_type: str,
        value: float,
        timestamp: Optional[datetime] = None
    ):
        self.metric_id = metric_id
        self.agent_id = agent_id
        self.metric_type = metric_type
        self.value = value
        self.timestamp = timestamp or datetime.now()

    def to_dict(self):
        return {
            'metric_id': self.metric_id,
            'agent_id': self.agent_id,
            'metric_type': self.metric_type,
            'value': self.value,
            'timestamp': self.timestamp.isoformat()
        }
