from django.test import TestCase
from unittest.mock import MagicMock

from photos.processors import PhotoUploadPipeline, AbstractPhotoProcessor
from app.photos.upload_context import PhotoUploadContext


class MockProcessor(AbstractPhotoProcessor):
    def process(self, context):
        pass

class PhotoUploadPipelineTests(TestCase):
    def test_mock_pipeline_runs_processors(self):
        context = PhotoUploadContext(
            user=None,
            tags=[],
            serializer=MagicMock(),
            photo=None
        )

        mock_processor_1 = MagicMock()
        mock_processor_2 = MagicMock()

        mock_processor_1.process.return_value = context
        mock_processor_2.process.return_value = context

        pipeline = PhotoUploadPipeline()
        pipeline.processors = [mock_processor_1, mock_processor_2]


        pipeline.execute(context=context)

        mock_processor_1.process.assert_called_once_with(context)
        mock_processor_2.process.assert_called_once_with(context)

