import io
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile

class TestDataMixin():
    @staticmethod
    def get_mock_image():
        file_obj = io.BytesIO()
        image = Image.new('RGB', (1, 1), color='red')
        image.save(file_obj, 'jpeg')
        file_obj.seek(0)

        return SimpleUploadedFile(
            name='test_image.jpg',
            content=file_obj.read(),
            content_type='image/jpeg'
        )