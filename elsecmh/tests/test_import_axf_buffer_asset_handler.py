import os
from unittest.mock import Mock

from django.conf import settings

from elsecmh.models import (
    Material,
    MaterialRevision,
    MaterialMetaData,
)
from elsecmh.tests.fixtures.utils import get_put_assets_to_buff_result_dto
from elsecmh.tests.test_base_cmh import TestBaseCmh
from elsecommon.transports.operation_type import OperationType
from elsecommon.transports.router import Router
from elsecommon.transports.transportabc import TransportABC
from elsepublic.elsecmh.handler_interfaces.import_axf_buffer_asset_success import (
    ImportAxFBufferAssetSuccessHandlerInterface,
)


class TestImportAxFBufferAssetHandler(TestBaseCmh):
    test_path = os.path.dirname(os.path.realpath(__file__))
    fixtures_path = os.path.join(test_path, 'fixtures')

    def setUp(self):
        super().setUp()
        test_material = Material.objects.create(name='test_material1', material_group=self.root)
        self.material_revision = MaterialRevision.objects.create(material=test_material, material_info={})
        test_material.active_revision = self.material_revision
        test_material.save()

        Router[ImportAxFBufferAssetSuccessHandlerInterface] = OperationType(expose=False, producer=TransportABC)
        self.import_axf_handler_op = Router[ImportAxFBufferAssetSuccessHandlerInterface.uri]
        input_file = os.path.join(self.fixtures_path, 'REMOVEME.axf')
        settings.BUFFER_SERVICE.copy_to_buffer = Mock(return_value=input_file)
        settings.BUFFER_SERVICE.open_buffer_file = Mock(return_value=open(input_file, 'rb'))
        settings.BUFFER_SERVICE.get_buffer_file_path = Mock(input_file)
        settings.BUFFER_SERVICE.copy_to_temp = Mock(return_value=input_file)
        self.put_asset_to_buff_result = get_put_assets_to_buff_result_dto(open(input_file, 'rb'))

    def test_import_axf_buffer_asset_handler(self):
        """
        Test import axf buffer asset handler
        """
        context = {'material_revision_uuid': self.material_revision.uuid}
        validate_result = self.import_axf_handler_op(self.put_asset_to_buff_result, **context)
        self.assertIsNone(validate_result)
        material_revision = MaterialRevision.objects.filter(uuid=self.material_revision.uuid).first()
        raw_data = material_revision.meta_data.filter(category=MaterialMetaData.AXF_RAW_DATA).first()
        self.assertEqual(raw_data.key, 'data')
        meta_data = material_revision.meta_data.filter(category=MaterialMetaData.AXF_META_DATA).first()
        self.assertIsNotNone(meta_data)
