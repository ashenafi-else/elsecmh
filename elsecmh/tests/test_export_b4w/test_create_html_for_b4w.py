from elsecmh.tests.test_base_cmh import TestBaseCmh
from elsecommon import marshalling
from unittest.mock import (
    Mock,
    patch,
)
from elsecommon.tests.helpers import RouterMock

from elsecmh.operations.export_b4w.create_html_for_b4w import CreateHTMLForB4WOp
from elsepublic.elsecmh.dto.create_html_for_b4w import CreateHTMLForB4WParamsDTO

from elsepublic.elserender.interfaces.compose import ComposeOpInterface

from elsepublic.dto.dam_asset_info import DamAssetInfoDTO
from elsepublic.serializers.dam_asset_info import DamAssetInfoSerializer
from elsepublic.elsedam.asset_extensions import AssetExtensions

from elsecmh.models import (
    Material,
    MaterialRevision,
    MaterialAsset,
    MaterialImplementation,
    MaterialImplementationAsset,
)
from elsepublic.exceptions import (
    MissingMaterialAssetException,
    MissingMaterialImplementationException,
)


class TestCreateHTMLForB4W(TestBaseCmh):

    def setUp(self):
        super().setUp()

        material = Material.objects.create(name='material', material_group=self.root)
        self.material_revision = MaterialRevision.objects.create(material=material, material_info='')
        self.material_asset = MaterialAsset.objects.create(
            material_revision=self.material_revision,
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
        self.material_implementation = MaterialImplementation.objects.create(
            name="test_implementation",
            material_revision=self.material_revision
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
        self.dto = CreateHTMLForB4WParamsDTO(
            material_implementation_uuid=self.material_implementation.uuid,
            camera='some_camera',
            environment=self.environment_dto,
        )

        self.material_revision_without_asset = MaterialRevision.objects.create(material=material, material_info='')
        self.material_implementation_no_asset_revision = MaterialImplementation.objects.create(
            name="implementation_for_revision_without_asset",
            material_revision=self.material_revision_without_asset
        )
        self.without_asset_dto = CreateHTMLForB4WParamsDTO(
            material_implementation_uuid=self.material_implementation_no_asset_revision.uuid,
            camera='some_camera',
            environment=self.environment_dto,
        )

        self.missed_revision_dto = CreateHTMLForB4WParamsDTO(uuid='43659c08-1594-11e9-ab14-d663bd873d93')

        self.op = CreateHTMLForB4WOp()

        self.router_mock = RouterMock()
        self.router_mock[ComposeOpInterface] = Mock(spec=marshalling.ElseOperation)
        self.patch = patch(
            'elsecmh.operations.export_b4w.create_html_for_b4w.Router',
            new=self.router_mock
        )

    def test_create_html_for_b4w(self):
        """
        Test create html for b4w
        """
        with self.patch:
            create_b4w_html_result = self.op(self.dto)

        self.assertIsNone(create_b4w_html_result)
        compose_mock = self.router_mock[ComposeOpInterface]
        compose_dto, context = compose_mock.call_args
        self.assertEqual(compose_mock.call_count, 1)
        self.assertEqual(compose_dto[0].dam_assets_info[0], self.environment_dto)
        self.assertEqual(DamAssetInfoSerializer(compose_dto[0].dam_assets_info[1]).data,
                         DamAssetInfoSerializer(self.material_asset).data)
        self.assertEqual(context['export_camera'], self.dto.camera)
        self.assertEqual(context['asset_type'], MaterialImplementationAsset.HTML_ASSET)

    def test_create_html_for_b4w_without_asset(self):
        """
        Test create html for b4w without asset
        """
        with self.patch:
            with self.assertRaises(MissingMaterialAssetException):
                self.op(self.without_asset_dto)
        compose_mock = self.router_mock[ComposeOpInterface]
        self.assertFalse(compose_mock.called)

    def test_create_html_for_b4w_for_missed_implementation(self):
        """
        Test create html for b4w for missed implementation
        """
        with self.patch:
            with self.assertRaises(MissingMaterialImplementationException):
                self.op(self.missed_revision_dto)
        compose_mock = self.router_mock[ComposeOpInterface]
        self.assertFalse(compose_mock.called)
