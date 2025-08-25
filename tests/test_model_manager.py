import unittest
from unittest.mock import patch
from argparse import Namespace
import sys
from io import StringIO

# Add the 'tools' directory to the Python path to allow importing model_manager
# This is necessary because the test is run from the root directory
sys.path.insert(0, './tools')

# Now that the path is set, we can import the script's functions
from model_manager import search_models

class MockModelInfo:
    """A mock class to simulate huggingface_hub.ModelInfo for testing."""
    def __init__(self, model_id, author, tags):
        self.id = model_id
        self.author = author
        self.tags = tags

class TestModelManager(unittest.TestCase):

    @patch('model_manager.HfApi')
    def test_search_models_success(self, mock_hf_api):
        """
        Test that the search_models function correctly processes and prints successful search results.
        """
        # Arrange: Set up the mock API client and its return value
        mock_api_instance = mock_hf_api.return_value
        mock_models = [
            MockModelInfo(model_id="test/model-1", author="tester1", tags=["test", "text-generation"]),
            MockModelInfo(model_id="test/model-2", author="tester2", tags=["test", "image-generation"]),
        ]
        mock_api_instance.list_models.return_value = iter(mock_models)

        # Arrange: Prepare arguments for the function and redirect stdout to capture prints
        args = Namespace(query="test-query")
        captured_output = StringIO()
        original_stdout = sys.stdout
        sys.stdout = captured_output

        # Act: Call the function to be tested
        search_models(args)

        # Assert: Restore stdout and check if the captured output contains the expected model information
        sys.stdout = original_stdout
        output = captured_output.getvalue()

        self.assertIn("Searching the Hugging Face Hub for 'test-query'...", output)
        self.assertIn("ID: test/model-1", output)
        self.assertIn("Author: tester1", output)
        self.assertIn("ID: test/model-2", output)
        self.assertIn("Author: tester2", output)

    @patch('model_manager.HfApi')
    def test_search_models_no_results(self, mock_hf_api):
        """
        Test that the search_models function correctly handles cases where no models are found.
        """
        # Arrange: Mock the API to return an empty list
        mock_api_instance = mock_hf_api.return_value
        mock_api_instance.list_models.return_value = iter([])
        args = Namespace(query="empty-query")
        captured_output = StringIO()
        original_stdout = sys.stdout
        sys.stdout = captured_output

        # Act
        search_models(args)

        # Assert
        sys.stdout = original_stdout
        output = captured_output.getvalue()
        self.assertIn("No models found matching your query.", output)

if __name__ == '__main__':
    unittest.main()
