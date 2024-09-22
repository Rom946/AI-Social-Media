import unittest
from unittest.mock import patch, MagicMock
from app.utils.image_generation import ImageGenerator
from app.utils.text_generation import TextGenerator

class TestImageGenerator(unittest.TestCase):
    def setUp(self):
        self.image_generator = ImageGenerator()

    @patch('app.utils.image_generation.requests.get')
    @patch('app.utils.image_generation.BeautifulSoup')
    @patch('app.utils.image_generation.TrendReq')
    def test_generate_random_images(self, mock_trends, mock_bs, mock_get):
        # Mock the trending topics
        mock_trends.return_value.trending_searches.return_value = [['Test topic']]

        # Mock the image search
        mock_bs.return_value.find_all.return_value = [{'src': 'http://test.com/image.jpg'}]

        # Mock the image download
        mock_response = MagicMock()
        mock_response.content = b'fake image content'
        mock_get.return_value = mock_response

        # Test the generate_random_images method
        images = self.image_generator.generate_random_images(num_images=1, size=(512, 512), prompt='Test prompt')
        self.assertEqual(len(images), 1)
        self.assertIn('url', images[0])
        self.assertIn('description', images[0])

    @patch('app.utils.image_generation.TrendReq')
    def test_generate_text(self, mock_trends):
        # Mock the trending topics
        mock_trends.return_value.trending_searches.return_value = [['Test topic']]

        # Test the generate_text method
        text = self.image_generator.generate_text('Test prompt')
        self.assertEqual(text, 'Test topic')

class TestTextGenerator(unittest.TestCase):
    def setUp(self):
        self.text_generator = TextGenerator()

    @patch('app.utils.text_generation.pipeline')
    def test_generate_text(self, mock_pipeline):
        # Mock the text generator
        mock_pipeline.return_value = MagicMock()
        mock_pipeline.return_value.return_value = [{'generated_text': 'Generated text'}]

        # Test the generate_text method
        text = self.text_generator.generate_text('Test prompt')
        self.assertEqual(text, 'Generated text')

    @patch('app.utils.text_generation.pipeline')
    def test_generate_comment(self, mock_pipeline):
        # Mock the text generator
        mock_pipeline.return_value = MagicMock()
        mock_pipeline.return_value.return_value = [{'generated_text': 'Generated comment'}]

        # Test the generate_comment method
        comment = self.text_generator.generate_comment('Test caption', 'Test image description')
        self.assertEqual(comment, 'Generated comment')

    @patch('app.utils.text_generation.pipeline')
    def test_generate_random_post(self, mock_pipeline):
        # Mock the text generator
        mock_pipeline.return_value = MagicMock()
        mock_pipeline.return_value.return_value = [{'generated_text': 'Generated post'}]

        # Test the generate_random_post method
        post = self.text_generator.generate_random_post()
        self.assertEqual(post, 'Generated post')

if __name__ == '__main__':
    unittest.main()