import os
import shutil
from unittest.mock import Mock
from django.conf import settings
from django.test import TestCase
from elsecmh.models import (
    MaterialGroup,
    Brand,
)


class TestBaseCmh(TestCase):
    test_path = os.path.dirname(os.path.realpath(__file__))
    fixtures_path = os.path.join(test_path, 'fixtures')
    fixtures_models_path = os.path.join(test_path, 'fixtures', 'common_test_data.json')
    fixtures = (fixtures_models_path,)

    def setUp(self):

        self.input_file = os.path.join(self.fixtures_path, 'test.png')
        settings.BUFFER_SERVICE.copy_to_buffer = Mock(return_value=self.input_file)
        settings.BUFFER_SERVICE.open_buffer_file = Mock(return_value=open(self.input_file, 'rb'))
        settings.BUFFER_SERVICE.get_buffer_file_path = Mock(self.input_file)
        settings.BUFFER_SERVICE.copy_to_temp = Mock(return_value=self.input_file)
        shutil.rmtree = Mock(return_value=None)

        # self.root = MaterialGroup.add_root(name='root')
        self.root = MaterialGroup.objects.filter().first()
        self.brand = Brand.objects.first()
        # print(self.root)
        # print(self.root.path)

