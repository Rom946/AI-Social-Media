import unittest
from unittest.mock import patch, MagicMock
from app.utils.image_generation import ImageGenerator
from app.utils.text_generation import TextGenerator

class TestImageGenerator(unittest.TestCase):
    def setUp(self):
        self.image_generator = ImageGenerator()

    @patch('app.utils.image_generation.pipeline')
    @patch('app.utils.image_generation.StableDiffusionPipeline')
    def test_generate_random_images(self, mock_stable_diffusion, mock_pipeline):
        # Mock the text generator
        mock_pipeline.return_value = MagicMock()
        mock_pipeline.return_value.return_value = [{'generated_text': 'Test prompt'}]

        # Mock the image generator
        mock_image = MagicMock()
        mock_image.resize.return_value = mock_image
        mock_stable_diffusion.return_value = MagicMock()
        mock_stable_diffusion.return_value.return_value.images = [mock_image]

        # Test the generate_random_images method
        images = self.image_generator.generate_random_images(num_images=1, size=(512, 512), prompt='Test prompt')
        self.assertEqual(len(images), 1)
        self.assertIn('url', images[0])
        self.assertIn('description', images[0])

    @patch('app.utils.image_generation.pipeline')
    def test_generate_text(self, mock_pipeline):
        # Mock the text generator
        mock_pipeline.return_value = MagicMock()
        mock_pipeline.return_value.return_value = [{'generated_text': 'Generated text'}]

        # Test the generate_text method
        text = self.image_generator.generate_text('Test prompt')
        self.assertEqual(text, 'Generated text')

    @patch('app.utils.text_generation.pipeline')
    def test_generate_comment(self, mock_pipeline):
        # Mock the text generator
        mock_pipeline.return_value = MagicMock()
        mock_pipeline.return_value.return_value = [{'generated_text': 'Generated comment'}]

        # Test the generate_comment method
        comment = self.image_generator.generate_comment('Test caption', 'Test image description')
        self.assertEqual(comment, 'Generated comment')

    @patch('app.utils.text_generation.pipeline')
    def test_generate_random_post(self, mock_pipeline):
        # Mock the text generator
        mock_pipeline.return_value = MagicMock()
        mock_pipeline.return_value.return_value = [{'generated_text': 'Generated post'}]

        # Test the generate_random_post method
        post = self.image_generator.generate_random_post()
        self.assertIn('url', post)
        self.assertIn('description', post)

if __name__ == '__main__':
    unittest.main()