import unittest

# Local imports
from core.providers.base import ParameterMetadata

class TestBaseProvider(unittest.TestCase):
    def test_run(self):
        #TODO:
        raise NotImplementedError()
 
    def test_validate(self):
        #TODO:
        raise NotImplementedError()

    def test_discover_parameters(self):
        #TODO:
        raise NotImplementedError()

class TestParameterMetadata(unittest.TestCase):
    def test_required(self):
        # Arrange
        descr = "description goes here"
        parameter_metadata = ParameterMetadata(descr, False)

        # Act & Assert
        self.assertEqual(parameter_metadata.description, descr)
 
    def test_description(self):
        # Arrange
        required = True
        parameter_metadata = ParameterMetadata("description goes here", required)

        # Act & Assert
        self.assertEqual(parameter_metadata.required, required)
 
if __name__ == '__main__':
    unittest.main()