import os
from unittest.mock import (
    Mock,
    patch,
)
from elsecmh.operations.create_preview.create_preview import CreatePreviewOp
from elsecommon import marshalling

from elsecmh.models import (
    Material,
    MaterialRevision,
    MaterialAsset,
    MaterialImplementation,
    MaterialImplementationAsset,
)
from elsecmh.tests.test_base_cmh import TestBaseCmh
from elsecommon.tests.helpers import RouterMock
from elsepublic.dto.dam_asset_info import DamAssetInfoDTO
from elsepublic.elsedam.asset_extensions import AssetExtensions
from elsepublic.elsecmh.dto.create_preview import CreatePreviewParamsDTO
from elsepublic.elserender.interfaces.compose import ComposeOpInterface
from elsepublic.exceptions import (
    MissingMaterialAssetException,
    MissingMaterialImplementationException,
)
from elsepublic.serializers.dam_asset_info import DamAssetInfoSerializer


class TestCreatePreview(TestBaseCmh):
    test_path = os.path.dirname(os.path.realpath(__file__))
    fixtures_path = os.path.join(test_path, '..', 'fixtures')

    def setUp(self):
        super().setUp()

        material = Material.objects.create(name='material', material_group=self.root)
        self.material_revision1 = MaterialRevision.objects.create(material=material, material_info='')
        self.material_implementation1 = MaterialImplementation.objects.create(material_revision=self.material_revision1)
        self.settings_dto = DamAssetInfoDTO(
            dam_uuid='7dcf73d0-020e-11e9-8eb2-f2801f1b9fd1',
            filename='settings',
            size=256,
            extension=AssetExtensions.BLEND,
            brand_id='1',
            url='https://www.test.com/',
            state='state',
            resource_type=AssetExtensions.BLEND,
            meta_info='',
        )
        self.environment_dto = DamAssetInfoDTO(
            dam_uuid='7dcf73d0-020e-11e9-8eb2-f2801f1b9fd2',
            filename='environment',
            size=256,
            extension=AssetExtensions.BLEND,
            brand_id='1',
            url='https://www.test.com/',
            state='state',
            resource_type=AssetExtensions.BLEND,
            meta_info='',
        )
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
        self.dto = CreatePreviewParamsDTO(
            uuid=self.material_implementation1.uuid,
            camera='some_camera',
            settings=self.settings_dto,
            environment=self.environment_dto,
        )
        self.material_revision2 = MaterialRevision.objects.create(material=material, material_info='')
        self.material_implementation2 = MaterialImplementation.objects.create(
            material_revision=self.material_revision2, name='test_name2')
        self.without_asset_dto = CreatePreviewParamsDTO(uuid=self.material_implementation2.uuid)
        self.missed_implementation_dto = CreatePreviewParamsDTO(uuid='43659c08-1594-11e9-ab14-d663bd873d93')
        self.op = CreatePreviewOp()

        self.router_mock = RouterMock()
        self.router_mock[ComposeOpInterface] = Mock(spec=marshalling.ElseOperation)
        self.patch = patch(
            'elsecmh.operations.create_preview.create_preview.Router',
            new=self.router_mock
        )

    def test_create_preview(self):
        """
        Test create preview
        """
        with self.patch:
            create_preview_result = self.op(self.dto)
            self.assertIsNone(create_preview_result)
            compose_mock = self.router_mock[ComposeOpInterface]
            self.assertEqual(compose_mock.call_count, 1)
            compose_dto, context = compose_mock.call_args
            self.assertEqual(compose_dto[0].dam_assets_info[0], self.environment_dto)
            self.assertEqual(
                DamAssetInfoSerializer(compose_dto[0].dam_assets_info[1]).data,
                DamAssetInfoSerializer(self.material_asset).data
            )
            self.assertEqual(context['render_data']['camera'], self.dto.camera)
            self.assertEqual(context['asset_type'], MaterialImplementationAsset.PREVIEW_ASSET)
            self.assertEqual(
                context['render_data']['settings_dam_asset_info'],
                DamAssetInfoSerializer(self.settings_dto).data
            )
            self.assertIsNotNone(context['material_implementation_uuid'])

    def test_create_preview_without_asset(self):
        """
        Test create preview without asset
        """
        with self.assertRaises(MissingMaterialAssetException):
            self.op(self.without_asset_dto)

    def test_create_preview_for_missed_implementation(self):
        """
        Test create preview for missed implementation
        """
        with self.assertRaises(MissingMaterialImplementationException):
            self.op(self.missed_implementation_dto)
