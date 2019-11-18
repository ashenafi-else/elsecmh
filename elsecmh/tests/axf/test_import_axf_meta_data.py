import os
from unittest.mock import (
    Mock,
    patch,
)

from elsecommon import marshalling
from django.conf import settings
from elsecmh.models import (
    Material,
    MaterialAsset,
    MaterialRevision,
)
from elsecmh.tests.test_base_cmh import TestBaseCmh
from elsecmh.tests.fixtures.utils import get_put_assets_to_buff_result_dto
from elsecommon.transports.router import Router
from elsepublic.dto.dam_asset_info import DamAssetInfoDTO
from elsepublic.elsedam.resource_types import ResourceTypes
from elsecommon.transports.transportabc import TransportABC
from elsepublic.elsedam.asset_extensions import AssetExtensions
from elsecommon.transports.operation_type import OperationType
from elsepublic.elsecmh.dto.import_axf_meta_data import (
    ImportAxFMetaDataParamsDTO,
)
from elsepublic.elsedam.buffering_assets.serializers import (
    PutAssetsToBufferResultSerializer,
)
from elsepublic.elsecmh.interfaces.import_axf_meta_data import (
    ImportAxFMetaDataOpInterface,
)
from elsepublic.elsedam.interfaces.put_assets_to_buffer_operation import (
    PutAssetsToBufferOpInterface,
)


class TestImportAxFMetaData(TestBaseCmh):

    def setUp(self):
        super().setUp()
        material = Material.objects.create(
            name='existed_material', material_group=self.root)
        self.material_revision = MaterialRevision.objects.create(
            material=material, material_info={})
        self.material_asset_dto = DamAssetInfoDTO(
            dam_uuid='7dcf73d0-020e-11e9-8eb2-f2801f1b9fd1',
            filename='axf_file_name',
            size=256,
            extension=AssetExtensions.AXF,
            brand_id='1',
            url='https://www.test.com/',
            state='state',
            resource_type=ResourceTypes.MATERIAL_AXF,
            meta_info='',
        )
        self.import_axf_meta_data_dto = ImportAxFMetaDataParamsDTO(
            material_revision_uuid=self.material_revision.uuid,
            dam_asset_info=self.material_asset_dto,
        )
        Router[ImportAxFMetaDataOpInterface] = OperationType(
            expose=False, producer=TransportABC)
        self.import_op = Router[ImportAxFMetaDataOpInterface.uri]

        input_file = os.path.join(self.fixtures_path, 'test_preview.axf')
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

    def test_import_axf_meta_data(self):
        """
        Test import AxF meta data
        """
        with self.put_asset_to_buff_patch:
            import_result = self.import_op(self.import_axf_meta_data_dto)
            self.assertIsNone(import_result)
            material_revision = MaterialRevision.objects.filter(
                uuid=self.material_revision.uuid).first()
            axf_asset = material_revision.assets.filter(
                asset_type=MaterialAsset.AXF_ASSET).first()
            self.assertIsNotNone(axf_asset)
            self.assertEqual(str(axf_asset.dam_uuid),
                             self.material_asset_dto.dam_uuid)
            self.assertEqual(
                axf_asset.filename,
                self.material_asset_dto.filename)
            # TODO (f.gaponenko@invento.by): fix test
            # self.assertEqual(axf_asset.size, self.material_asset_dto.size)
            self.assertEqual(
                axf_asset.extension,
                self.material_asset_dto.extension)
            self.assertEqual(
                axf_asset.brand_id,
                self.material_asset_dto.brand_id)
            self.assertEqual(axf_asset.url, self.material_asset_dto.url)
            self.assertEqual(axf_asset.state, self.material_asset_dto.state)
            self.assertEqual(
                axf_asset.resource_type,
                self.material_asset_dto.resource_type)
            self.assertEqual(
                axf_asset.meta_info,
                self.material_asset_dto.meta_info)

    def test_import_with_wrong_extension(self):
        """
        Test import with wrong extension
        """
        with self.put_asset_to_buff_patch:
            with self.assertRaises(RuntimeError):
                self.import_axf_meta_data_dto.dam_asset_info.extension =\
                    AssetExtensions.BLEND
                self.import_op(self.import_axf_meta_data_dto)

    def test_import_with_wrong_resource_type(self):
        """
        Test import with wrong resource type
        """
        with self.put_asset_to_buff_patch:
            with self.assertRaises(RuntimeError):
                self.import_axf_meta_data_dto.dam_asset_info.resource_type =\
                    ResourceTypes.BLENDER_MODEL
                self.import_op(self.import_axf_meta_data_dto)
