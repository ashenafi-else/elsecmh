import os
from unittest.mock import (
    Mock,
    patch,
)

from elsecommon import marshalling
from django.conf import settings
from elsecmh.models import (
    Material,
    MaterialRevision,
)
from elsecommon.tests.helpers import RouterMock
from elsecmh.tests.test_base_cmh import TestBaseCmh
from elsecmh.tests.fixtures.utils import get_put_assets_to_buff_result_dto
from elsecommon.transports.router import Router
from elsepublic.elsedam.asset_tags import AssetTags
from elsepublic.elsedam.resource_types import ResourceTypes
from elsecommon.transports.transportabc import TransportABC
from elsecommon.transports.operation_type import OperationType
from elsepublic.elsecmh.axf.import_preview import (
    ImportAxfPreviewInterface,
    ImportAxFPreviewParamsDTO,
)
from elsepublic.elsedam.buffering_assets.serializers import (
    PutAssetsToBufferResultSerializer,
)
from elsepublic.elsedam.interfaces.put_assets_operation import (
    PutAssetsOpInterface,
)
from elsepublic.elsedam.interfaces.put_assets_to_buffer_operation import (
    PutAssetsToBufferOpInterface,
)


class TestImportAxFPreview(TestBaseCmh):

    def setUp(self):
        super().setUp()
        material = Material.objects.create(
            name='existed_material', material_group=self.root)
        self.material_revision = MaterialRevision.objects.create(
            material=material, material_info={})
        self.file_name = 'test_preview.axf'
        self.input_file = os.path.join(self.fixtures_path, self.file_name)
        self.import_axf_preview_dto = ImportAxFPreviewParamsDTO(
            material_revision_uuid=self.material_revision.uuid,
            brand_id='13',
            file_name=self.input_file,
        )
        Router[ImportAxfPreviewInterface] = OperationType(
            expose=False, producer=TransportABC)
        self.import_op = Router[ImportAxfPreviewInterface]
        input_file = self.input_file
        settings.BUFFER_SERVICE.copy_to_buffer = Mock(return_value=input_file)
        settings.BUFFER_SERVICE.open_buffer_file = Mock(
            return_value=open(input_file, 'rb'))
        settings.BUFFER_SERVICE.get_buffer_file_path = Mock(input_file)
        settings.BUFFER_SERVICE.copy_to_temp = Mock(return_value=input_file)

        Router[PutAssetsToBufferOpInterface] = OperationType(
            expose=False, producer=TransportABC)
        self.put_asset_to_buff_result = get_put_assets_to_buff_result_dto(
            open(input_file, 'rb'))
        mock_settings = {
            'wrapped.return_value': PutAssetsToBufferResultSerializer(
                self.put_asset_to_buff_result).data}
        self.put_asset_to_buff = Mock(
            spec=marshalling.ElseOperation, **mock_settings)
        self.put_asset_to_buff_patch = patch(
            PutAssetsToBufferOpInterface.uri,
            new=self.put_asset_to_buff)
        self.router_mock = RouterMock()
        self.router_mock[PutAssetsToBufferOpInterface] = Mock(
            spec=marshalling.ElseOperation)
        self.router_patch = patch(
            'elsecmh.operations.axf_operations.import_axf_preview'
            '.operation.Router',
            new=self.router_mock,
        )

    def test_import_axf_preview(self):
        """
        Test import axf preview
        """
        with self.router_patch:
            with self.put_asset_to_buff_patch:
                put_to_dam_mock = self.router_mock[PutAssetsOpInterface]

                import_op = Router[ImportAxfPreviewInterface]
                import_result = import_op(self.import_axf_preview_dto)

                self.assertIsNone(import_result)
                self.assertEqual(put_to_dam_mock.call_count, 1)
                self.assertEqual(len(put_to_dam_mock.call_args), 2)

                dam_dto, revision_uuid_dict = put_to_dam_mock.call_args
                actual_asset = dam_dto[0].base_assets[0]

                self.assertEqual(
                    revision_uuid_dict['material_uuid'],
                    str(self.material_revision.uuid))
                self.assertEqual(
                    dam_dto[0].resource_type,
                    ResourceTypes.PREVIEW)
                self.assertEqual(actual_asset.tags[0], AssetTags.PREVIEW)

                expected_file_path = os.path.join(
                    self.fixtures_path, "test_preview.png")
                actual_file_path = actual_asset.file.name
                self.assertEqual(
                    os.path.getsize(actual_file_path),
                    os.path.getsize(expected_file_path))
