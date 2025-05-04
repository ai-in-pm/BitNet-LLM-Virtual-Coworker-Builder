"""
Tests for API server.
"""

import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

import sys
import os

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bitnet_vc_builder.api.server import app
from bitnet_vc_builder.models.bitnet_wrapper import BitNetModel
from bitnet_vc_builder.core.virtual_coworker import BitNetVirtualCoworker
from bitnet_vc_builder.core.team import BitNetTeam, CollaborationMode

class TestAPIServer(unittest.TestCase):
    """
    Test API server.
    """
    
    def setUp(self):
        """
        Set up test fixtures.
        """
        # Create a test client
        self.client = TestClient(app)
        
        # Mock the models, virtual co-workers, and teams
        app.models = {}
        app.virtual_coworkers = {}
        app.teams = {}
        app.tasks = {}
    
    def test_root(self):
        """
        Test root endpoint.
        """
        response = self.client.get("/")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Welcome to BitNet Virtual Co-worker Builder API"})
    
    def test_get_models(self):
        """
        Test get_models endpoint.
        """
        # Add some models
        app.models = {
            "model1": MagicMock(spec=BitNetModel),
            "model2": MagicMock(spec=BitNetModel)
        }
        
        response = self.client.get("/models")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"models": ["model1", "model2"]})
    
    def test_create_model(self):
        """
        Test create_model endpoint.
        """
        # Mock BitNetModel.__init__ to avoid loading a real model
        with patch("bitnet_vc_builder.models.bitnet_wrapper.BitNetModel.__init__", return_value=None):
            response = self.client.post(
                "/models",
                json={
                    "name": "test_model",
                    "model_path": "models/test_model",
                    "kernel_type": "i2_s"
                }
            )
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"message": "Model test_model created successfully"})
            self.assertIn("test_model", app.models)
    
    def test_delete_model(self):
        """
        Test delete_model endpoint.
        """
        # Add a model
        app.models = {
            "test_model": MagicMock(spec=BitNetModel)
        }
        
        response = self.client.delete("/models/test_model")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Model test_model deleted successfully"})
        self.assertNotIn("test_model", app.models)
        
        # Try to delete a non-existent model
        response = self.client.delete("/models/non_existent_model")
        
        self.assertEqual(response.status_code, 404)
    
    def test_get_virtual_coworkers(self):
        """
        Test get_virtual_coworkers endpoint.
        """
        # Add some virtual co-workers
        app.virtual_coworkers = {
            "coworker1": MagicMock(spec=BitNetVirtualCoworker),
            "coworker2": MagicMock(spec=BitNetVirtualCoworker)
        }
        
        response = self.client.get("/virtual-coworkers")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"virtual_coworkers": ["coworker1", "coworker2"]})
    
    def test_create_virtual_coworker(self):
        """
        Test create_virtual_coworker endpoint.
        """
        # Add a model
        app.models = {
            "test_model": MagicMock(spec=BitNetModel)
        }
        
        # Mock BitNetVirtualCoworker.__init__ to avoid loading a real model
        with patch("bitnet_vc_builder.core.virtual_coworker.BitNetVirtualCoworker.__init__", return_value=None):
            response = self.client.post(
                "/virtual-coworkers",
                json={
                    "name": "test_coworker",
                    "model_name": "test_model",
                    "description": "A test virtual co-worker"
                }
            )
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"message": "Virtual co-worker test_coworker created successfully"})
            self.assertIn("test_coworker", app.virtual_coworkers)
    
    def test_delete_virtual_coworker(self):
        """
        Test delete_virtual_coworker endpoint.
        """
        # Add a virtual co-worker
        app.virtual_coworkers = {
            "test_coworker": MagicMock(spec=BitNetVirtualCoworker)
        }
        
        response = self.client.delete("/virtual-coworkers/test_coworker")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Virtual co-worker test_coworker deleted successfully"})
        self.assertNotIn("test_coworker", app.virtual_coworkers)
        
        # Try to delete a non-existent virtual co-worker
        response = self.client.delete("/virtual-coworkers/non_existent_coworker")
        
        self.assertEqual(response.status_code, 404)
    
    def test_run_virtual_coworker(self):
        """
        Test run_virtual_coworker endpoint.
        """
        # Add a virtual co-worker
        mock_coworker = MagicMock(spec=BitNetVirtualCoworker)
        mock_coworker.run.return_value = "Coworker response"
        
        app.virtual_coworkers = {
            "test_coworker": mock_coworker
        }
        
        response = self.client.post(
            "/virtual-coworkers/test_coworker/run",
            json={
                "task": "Test task"
            }
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("task_id", response.json())
        self.assertEqual(response.json()["status"], "pending")
        
        # Try to run a non-existent virtual co-worker
        response = self.client.post(
            "/virtual-coworkers/non_existent_coworker/run",
            json={
                "task": "Test task"
            }
        )
        
        self.assertEqual(response.status_code, 404)
    
    def test_get_teams(self):
        """
        Test get_teams endpoint.
        """
        # Add some teams
        app.teams = {
            "team1": MagicMock(spec=BitNetTeam),
            "team2": MagicMock(spec=BitNetTeam)
        }
        
        response = self.client.get("/teams")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"teams": ["team1", "team2"]})
    
    def test_create_team(self):
        """
        Test create_team endpoint.
        """
        # Add some virtual co-workers
        app.virtual_coworkers = {
            "coworker1": MagicMock(spec=BitNetVirtualCoworker),
            "coworker2": MagicMock(spec=BitNetVirtualCoworker)
        }
        
        # Mock BitNetTeam.__init__ to avoid loading real virtual co-workers
        with patch("bitnet_vc_builder.core.team.BitNetTeam.__init__", return_value=None):
            response = self.client.post(
                "/teams",
                json={
                    "name": "test_team",
                    "description": "A test team",
                    "virtual_coworker_names": ["coworker1", "coworker2"],
                    "collaboration_mode": "SEQUENTIAL"
                }
            )
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"message": "Team test_team created successfully"})
            self.assertIn("test_team", app.teams)
    
    def test_delete_team(self):
        """
        Test delete_team endpoint.
        """
        # Add a team
        app.teams = {
            "test_team": MagicMock(spec=BitNetTeam)
        }
        
        response = self.client.delete("/teams/test_team")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Team test_team deleted successfully"})
        self.assertNotIn("test_team", app.teams)
        
        # Try to delete a non-existent team
        response = self.client.delete("/teams/non_existent_team")
        
        self.assertEqual(response.status_code, 404)
    
    def test_run_team(self):
        """
        Test run_team endpoint.
        """
        # Add a team
        mock_team = MagicMock(spec=BitNetTeam)
        mock_team.run.return_value = "Team response"
        
        app.teams = {
            "test_team": mock_team
        }
        
        response = self.client.post(
            "/teams/test_team/run",
            json={
                "task": "Test task"
            }
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("task_id", response.json())
        self.assertEqual(response.json()["status"], "pending")
        
        # Try to run a non-existent team
        response = self.client.post(
            "/teams/non_existent_team/run",
            json={
                "task": "Test task"
            }
        )
        
        self.assertEqual(response.status_code, 404)
    
    def test_get_task(self):
        """
        Test get_task endpoint.
        """
        # Add a task
        app.tasks = {
            "task_1": {
                "task": "Test task",
                "status": "completed",
                "result": "Task result"
            }
        }
        
        response = self.client.get("/tasks/task_1")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "task": "Test task",
            "status": "completed",
            "result": "Task result"
        })
        
        # Try to get a non-existent task
        response = self.client.get("/tasks/non_existent_task")
        
        self.assertEqual(response.status_code, 404)
    
    def test_get_tasks(self):
        """
        Test get_tasks endpoint.
        """
        # Add some tasks
        app.tasks = {
            "task_1": {
                "task": "Test task 1",
                "status": "completed",
                "result": "Task 1 result"
            },
            "task_2": {
                "task": "Test task 2",
                "status": "pending",
                "result": None
            }
        }
        
        response = self.client.get("/tasks")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "tasks": {
                "task_1": {
                    "task": "Test task 1",
                    "status": "completed",
                    "result": "Task 1 result"
                },
                "task_2": {
                    "task": "Test task 2",
                    "status": "pending",
                    "result": None
                }
            }
        })

if __name__ == "__main__":
    unittest.main()
