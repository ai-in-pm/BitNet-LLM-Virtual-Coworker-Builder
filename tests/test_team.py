"""
Tests for BitNetTeam class.
"""

import unittest
from unittest.mock import MagicMock, patch

from bitnet_vc_builder.core.team import BitNetTeam, CollaborationMode, TaskStatus, Task
from bitnet_vc_builder.core.virtual_coworker import BitNetVirtualCoworker

class TestBitNetTeam(unittest.TestCase):
    """
    Test BitNetTeam class.
    """
    
    def setUp(self):
        """
        Set up test fixtures.
        """
        # Create mock virtual co-workers
        self.mock_coworker1 = MagicMock(spec=BitNetVirtualCoworker)
        self.mock_coworker1.name = "Coworker1"
        self.mock_coworker1.run.return_value = "Coworker1 response"
        
        self.mock_coworker2 = MagicMock(spec=BitNetVirtualCoworker)
        self.mock_coworker2.name = "Coworker2"
        self.mock_coworker2.run.return_value = "Coworker2 response"
        
        self.mock_coworker3 = MagicMock(spec=BitNetVirtualCoworker)
        self.mock_coworker3.name = "Coworker3"
        self.mock_coworker3.run.return_value = "Coworker3 response"
        
        # Create team
        self.team = BitNetTeam(
            agents=[self.mock_coworker1, self.mock_coworker2, self.mock_coworker3],
            name="TestTeam",
            description="A test team",
            collaboration_mode=CollaborationMode.SEQUENTIAL
        )
    
    def test_init(self):
        """
        Test initialization.
        """
        self.assertEqual(self.team.name, "TestTeam")
        self.assertEqual(self.team.description, "A test team")
        self.assertEqual(len(self.team.agents), 3)
        self.assertEqual(self.team.collaboration_mode, CollaborationMode.SEQUENTIAL)
        self.assertEqual(len(self.team._agent_map), 3)
        self.assertIn("Coworker1", self.team._agent_map)
        self.assertIn("Coworker2", self.team._agent_map)
        self.assertIn("Coworker3", self.team._agent_map)
    
    def test_add_agent(self):
        """
        Test add_agent method.
        """
        new_coworker = MagicMock(spec=BitNetVirtualCoworker)
        new_coworker.name = "NewCoworker"
        
        self.team.add_agent(new_coworker)
        
        self.assertEqual(len(self.team.agents), 4)
        self.assertEqual(len(self.team._agent_map), 4)
        self.assertIn("NewCoworker", self.team._agent_map)
        self.assertEqual(self.team._agent_map["NewCoworker"], new_coworker)
    
    def test_remove_agent(self):
        """
        Test remove_agent method.
        """
        result = self.team.remove_agent("Coworker1")
        
        self.assertTrue(result)
        self.assertEqual(len(self.team.agents), 2)
        self.assertEqual(len(self.team._agent_map), 2)
        self.assertNotIn("Coworker1", self.team._agent_map)
        
        # Test removing non-existent virtual co-worker
        result = self.team.remove_agent("NonExistentCoworker")
        self.assertFalse(result)
    
    def test_get_agent(self):
        """
        Test get_agent method.
        """
        coworker = self.team.get_agent("Coworker1")
        
        self.assertEqual(coworker, self.mock_coworker1)
        
        # Test getting non-existent virtual co-worker
        coworker = self.team.get_agent("NonExistentCoworker")
        self.assertIsNone(coworker)
    
    def test_create_task(self):
        """
        Test create_task method.
        """
        task_id = self.team.create_task(
            description="Test task",
            assigned_agent="Coworker1",
            priority=3
        )
        
        self.assertIn(task_id, self.team.tasks)
        task = self.team.tasks[task_id]
        self.assertEqual(task.description, "Test task")
        self.assertEqual(task.assigned_agent, "Coworker1")
        self.assertEqual(task.priority, 3)
        self.assertEqual(task.status, TaskStatus.PENDING)
    
    def test_get_task(self):
        """
        Test get_task method.
        """
        task_id = self.team.create_task(description="Test task")
        
        task = self.team.get_task(task_id)
        
        self.assertEqual(task.description, "Test task")
        
        # Test getting non-existent task
        task = self.team.get_task("non_existent_task")
        self.assertIsNone(task)
    
    def test_run_sequential(self):
        """
        Test run method with sequential collaboration mode.
        """
        self.team.collaboration_mode = CollaborationMode.SEQUENTIAL
        
        result = self.team.run("Test task")
        
        # Check that all virtual co-workers were called
        self.mock_coworker1.run.assert_called_once()
        self.mock_coworker2.run.assert_called_once()
        self.mock_coworker3.run.assert_called_once()
        
        # Check that the result is the last virtual co-worker's response
        self.assertEqual(result, "Coworker3 response")
    
    @patch('json.loads')
    def test_run_parallel(self, mock_json_loads):
        """
        Test run method with parallel collaboration mode.
        """
        self.team.collaboration_mode = CollaborationMode.PARALLEL
        
        # Mock the JSON parsing of the plan
        mock_json_loads.return_value = [
            {
                "subtask": "Subtask 1",
                "agent_name": "Coworker1",
                "depends_on": []
            },
            {
                "subtask": "Subtask 2",
                "agent_name": "Coworker2",
                "depends_on": [0]
            },
            {
                "subtask": "Subtask 3",
                "agent_name": "Coworker3",
                "depends_on": [1]
            }
        ]
        
        # Mock the coordinator's response to include a JSON plan
        self.mock_coworker1.run.return_value = "[{...plan...}]"
        
        result = self.team.run("Test task")
        
        # Check that the coordinator was called to create a plan
        self.mock_coworker1.run.assert_called()
        
        # Check that all virtual co-workers were called to execute their subtasks
        self.assertTrue(self.mock_coworker1.run.call_count >= 1)
        self.mock_coworker2.run.assert_called()
        self.mock_coworker3.run.assert_called()
    
    @patch('json.loads')
    def test_run_hierarchical(self, mock_json_loads):
        """
        Test run method with hierarchical collaboration mode.
        """
        self.team.collaboration_mode = CollaborationMode.HIERARCHICAL
        
        # Mock the JSON parsing of the plan
        mock_json_loads.return_value = [
            {
                "subtask": "Subtask 1",
                "agent_name": "Coworker2"
            },
            {
                "subtask": "Subtask 2",
                "agent_name": "Coworker3"
            }
        ]
        
        # Mock the coordinator's response to include a JSON plan
        self.mock_coworker1.run.return_value = "[{...plan...}]"
        
        result = self.team.run("Test task")
        
        # Check that the coordinator was called to create a plan
        self.mock_coworker1.run.assert_called()
        
        # Check that the other virtual co-workers were called to execute their subtasks
        self.mock_coworker2.run.assert_called()
        self.mock_coworker3.run.assert_called()
    
    def test_run_consensus(self):
        """
        Test run method with consensus collaboration mode.
        """
        self.team.collaboration_mode = CollaborationMode.CONSENSUS
        
        result = self.team.run("Test task")
        
        # Check that all virtual co-workers were called
        self.mock_coworker1.run.assert_called()
        self.mock_coworker2.run.assert_called()
        self.mock_coworker3.run.assert_called()
    
    def test_get_performance_metrics(self):
        """
        Test get_performance_metrics method.
        """
        # Run a task to generate some performance metrics
        self.team.run("Test task")
        
        metrics = self.team.get_performance_metrics()
        
        self.assertIn("Coworker1", metrics)
        self.assertIn("Coworker2", metrics)
        self.assertIn("Coworker3", metrics)
        self.assertIn("tasks_completed", metrics["Coworker1"])
        self.assertIn("tasks_failed", metrics["Coworker1"])
        self.assertIn("avg_time", metrics["Coworker1"])
    
    def test_get_agent_performance(self):
        """
        Test get_agent_performance method.
        """
        # Run a task to generate some performance metrics
        self.team.run("Test task")
        
        metrics = self.team.get_agent_performance("Coworker1")
        
        self.assertIn("tasks_completed", metrics)
        self.assertIn("tasks_failed", metrics)
        self.assertIn("avg_time", metrics)
        
        # Test getting performance for non-existent virtual co-worker
        metrics = self.team.get_agent_performance("NonExistentCoworker")
        self.assertIsNone(metrics)

if __name__ == "__main__":
    unittest.main()
