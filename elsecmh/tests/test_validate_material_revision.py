import os
from unittest.mock import (
    Mock,
    patch,
)
from elsecommon import marshalling

from elsecmh.models import (
    Material,
    MaterialRevision,
    MaterialAsset,
)
from elsecmh.tests.test_base_cmh import TestBaseCmh
from elsecommon.transports.operation_type import OperationType
from elsecommon.transports.router import Router
from elsecommon.transports.transportabc import TransportABC
from elsepublic.elsecmh.dto.validate_material_revision import ValidateMaterialRevParamsDTO
from elsepublic.elsecmh.interfaces.validate_material_revision import ValidateMaterialOpInterface
from elsepublic.elserender.interfaces.validate_file import ValidateFileOpInterface


class TestValidateMaterialRevision(TestBaseCmh):
    test_path = os.path.dirname(os.path.realpath(__file__))
    fixtures_path = os.path.join(test_path, 'fixtures')

    def setUp(self):
        super().setUp()

        material = Material.objects.create(name='material', material_group=self.root)
        self.material_revision1 = MaterialRevision.objects.create(material=material, material_info='')
        self.material_asset = MaterialAsset.objects.create(
            material_revision=self.material_revision1,
            asset_type=MaterialAsset.MODEL_ASSET,
            dam_uuid='de60c96d-56c5-4d0d-9748-e82746a44ec2',
            filename='test',
            size=256,
            extension='blend',
            brand_id='1',
            url='url.com',
            state='uploaded',
            resource_type='blend',
            meta_info='',
        )
        self.validate_material_revision_dto = ValidateMaterialRevParamsDTO(uuid=self.material_revision1.uuid)
        self.material_revision2 = MaterialRevision.objects.create(material=material, material_info='')
        self.validate_without_asset_dto = ValidateMaterialRevParamsDTO(uuid=self.material_revision2.uuid)
        self.validate_missed_revision = ValidateMaterialRevParamsDTO(uuid='43659c08-1594-11e9-ab14-d663bd873d93')

        Router[ValidateMaterialOpInterface] = OperationType(expose=False, producer=TransportABC)
        self.validate_op = Router[ValidateMaterialOpInterface.uri]

        Router[ValidateFileOpInterface] = OperationType(expose=False, producer=TransportABC)
        mock_settings = {'wrapped.return_value': None}
        self.validate_file_mock = Mock(spec=marshalling.ElseOperation, **mock_settings)
        self.validate_file_patch = patch(ValidateFileOpInterface.uri, new=self.validate_file_mock)

    def test_validate_material_revision(self):
        """
        Test validate material revision
        """
        with self.validate_file_patch:
            validate_result = self.validate_op(self.validate_material_revision_dto)
            self.assertIsNone(validate_result)
            material_revision = MaterialRevision.objects.filter(uuid=self.material_revision1.uuid).first()
            self.assertEqual(material_revision.status, MaterialRevision.STATUS_VALIDATING)
            self.assertEqual(len(self.validate_file_mock.method_calls), 1)
            dam_asset_info = self.validate_file_mock.method_calls[0][1][0]['dam_asset_info']
            self.assertEqual(self.material_asset.dam_uuid, dam_asset_info['dam_uuid'])
            self.assertEqual(self.material_asset.filename, dam_asset_info['filename'])
            self.assertEqual(self.material_asset.size, dam_asset_info['size'])
            self.assertEqual(self.material_asset.extension, dam_asset_info['extension'])
            self.assertEqual(self.material_asset.brand_id, dam_asset_info['brand_id'])
            self.assertEqual(self.material_asset.url, dam_asset_info['url'])
            self.assertEqual(self.material_asset.state, dam_asset_info['state'])
            self.assertEqual(self.material_asset.resource_type, dam_asset_info['resource_type'])
            context = self.validate_file_mock.method_calls[0][2]
            self.assertEqual(context['material_revision_uuid'], str(material_revision.uuid))

    def test_validate_without_asset(self):
        """
        Test validate without asset
        """
        with self.validate_file_patch:
            with self.assertRaises(RuntimeError):
                self.validate_op(self.validate_without_asset_dto)

    def test_validate_missed_revision(self):
        """
        Test validate missed revision
        """
        with self.validate_file_patch:
            with self.assertRaises(RuntimeError):
                self.validate_op(self.validate_missed_revision)
