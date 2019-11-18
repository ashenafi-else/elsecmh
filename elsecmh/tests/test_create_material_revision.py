import os
from unittest.mock import (
    Mock,
    patch,
)

from elsecommon import marshalling
from elsecmh.models import (
    Color,
    Material,
    MaterialRevision,
    MaterialImplementation,
)
from elsepublic.exceptions import (
    MissingColorException,
    MissingMaterialException,
)
from elsecommon.tests.helpers import RouterMock
from elsecmh.tests.test_base_cmh import TestBaseCmh
from elsecmh.tests.fixtures.utils import get_create_material_revision_dto
from elsepublic.dto.dam_asset_info import DamAssetInfoDTO
from elsepublic.helpers.asset_to_dto import asset_to_dto
from elsepublic.elsedam.resource_types import ResourceTypes
from elsepublic.elsedam.asset_extensions import AssetExtensions
from elsepublic.helpers.asset_dto_to_dict import asset_dto_to_dict
from elsecmh.operations.create_material_revision import (
    CreateMaterialRevisionOp,
)
from elsepublic.elsecmh.create_material_revision.dto import (
    CreateMaterialRevResult,
)
from elsepublic.elsecmh.interfaces.validate_material_revision import (
    ValidateMaterialOpInterface,
)


class TestCreateMaterialRevision(TestBaseCmh):
    test_path = os.path.dirname(os.path.realpath(__file__))
    fixtures_path = os.path.join(test_path, 'fixtures')
    fixtures_models_path = os.path.join(
        test_path, 'fixtures', 'common_test_data.json')
    fixtures_implementation_models_path = os.path.join(
        test_path, 'fixtures', 'color_test_data.json')
    fixtures = (fixtures_models_path, fixtures_implementation_models_path)

    def setUp(self):
        super().setUp()
        self.material_asset_dto = DamAssetInfoDTO(
            dam_uuid='7dcf73d0-020e-11e9-8eb2-f2801f1b9fd1',
            filename='material_file_name',
            size=256,
            extension=AssetExtensions.PNG,
            brand_id='1',
            url='https://www.test.com/',
            state='state',
            resource_type=ResourceTypes.BLENDER_MODEL,
            meta_info='',
        )
        self.colors = [
            Color.objects.get(uuid='e29dcd47-6965-4d01-a208-7a0418716c90'),
            Color.objects.get(uuid='642bbbe6-d21b-11e8-a8d5-f2801f1b9fe3'),
        ]
        color_uuids = [color.uuid for color in self.colors]
        test_material1 = Material.objects.create(
            name='test_material1', material_group=self.root)
        self.create_material_revision_dto = get_create_material_revision_dto(
            test_material1.uuid,
            self.material_asset_dto,
            color_uuids,
        )

        self.create_missing_material_revision_dto = \
            get_create_material_revision_dto(
                test_material1.uuid,
                self.material_asset_dto,
                color_uuids,
            )
        self.create_missing_material_revision_dto.uuid = \
            'd9548b20-ed76-11e8-8eb2-f2801f1b9fd1'

        self.create_missing_color_revision_dto = \
            get_create_material_revision_dto(
                test_material1.uuid,
                self.material_asset_dto,
                color_uuids,
            )
        self.create_missing_color_revision_dto.color_uuids.add(
            'd9548b20-ed76-11e8-8eb2-f2801f1b9fd1')

        self.router_mock = RouterMock()
        self.router_mock[ValidateMaterialOpInterface] = Mock(
            spec=marshalling.ElseOperation,
        )
        self.patch = patch(
            'elsecmh.operations.create_material_revision.Router',
            new=self.router_mock,
        )
        self.op = CreateMaterialRevisionOp()

    def test_create_material_revision(self):
        """
        Test create material revision
        """
        with self.patch:
            create_result = self.op(self.create_material_revision_dto)
        self.assertIsInstance(create_result, CreateMaterialRevResult)
        self.assertEqual(
            create_result.material_info,
            self.create_material_revision_dto.info,
        )
        validate_mock = self.router_mock[ValidateMaterialOpInterface.uri]
        self.assertEqual(validate_mock.call_count, 1)
        validate_mat_dto, context = validate_mock.call_args
        self.assertEqual(create_result.uuid, validate_mat_dto[0].uuid)
        material_revision = MaterialRevision.objects.filter(
            uuid=create_result.uuid,
        ).first()
        dam_asset = self.material_asset_dto
        material_asset = asset_to_dto(material_revision.assets.first())
        self.assertEqual(
            asset_dto_to_dict(material_asset),
            asset_dto_to_dict(dam_asset),
        )
        for color in self.colors:
            implementation = MaterialImplementation.objects.filter(
                color=color,
            ).first()
            self.assertIsNotNone(implementation)
            self.assertEqual(
                implementation.material_revision,
                material_revision,
            )

    def test_create_missing_material_revision(self):
        """
        Test create material revision for missing material
        """
        with self.patch:
            with self.assertRaises(MissingMaterialException):
                self.op(self.create_missing_material_revision_dto)
        validate_mock = self.router_mock[ValidateMaterialOpInterface.uri]
        self.assertFalse(validate_mock.called)

    def test_create_missing_color_revision(self):
        """
        Test create material revision with missing color
        """
        with self.patch:
            with self.assertRaises(MissingColorException):
                self.op(self.create_missing_color_revision_dto)
        validate_mock = self.router_mock[ValidateMaterialOpInterface.uri]
        self.assertFalse(validate_mock.called)
