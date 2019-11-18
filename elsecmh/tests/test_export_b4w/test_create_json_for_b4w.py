from elsecmh.tests.test_base_cmh import TestBaseCmh
from elsecommon import marshalling
from unittest.mock import (
    Mock,
    patch,
)
from elsecommon.tests.helpers import RouterMock

from elsecmh.operations.export_b4w.create_json_for_b4w import CreateJSONForB4WOp
from elsepublic.elsecmh.dto.create_json_for_b4w import CreateJSONForB4WParamsDTO

from elsepublic.elserender.interfaces.export_b4w import ExportB4WOpInterface
from elsepublic.elserender.dto.export_b4w import ExportB4WParamsDTO

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


class TestCreateJSONForB4W(TestBaseCmh):

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
        self.dto = CreateJSONForB4WParamsDTO(
            material_implementation_uuid=self.material_implementation.uuid,
            camera='some_camera',
        )
        self.material_revision_without_asset = MaterialRevision.objects.create(material=material, material_info='')
        self.material_implementation_no_asset_revision = MaterialImplementation.objects.create(
            name="implementation_for_revision_without_asset",
            material_revision=self.material_revision_without_asset
        )
        self.without_asset_dto = CreateJSONForB4WParamsDTO(
            material_implementation_uuid=self.material_implementation_no_asset_revision.uuid,
            camera='some_camera',
        )

        self.missed_revision_dto = CreateJSONForB4WParamsDTO(uuid='43659c08-1594-11e9-ab14-d663bd873d93')

        self.op = CreateJSONForB4WOp()

        self.router_mock = RouterMock()
        self.router_mock[ExportB4WOpInterface] = Mock(spec=marshalling.ElseOperation)
        self.patch = patch(
            'elsecmh.operations.export_b4w.create_json_for_b4w.Router',
            new=self.router_mock,
        )

    def test_create_json_for_b4w(self):
        """
        Test create json for b4w
        """
        with self.patch:
            create_b4w_json_result = self.op(self.dto)

        self.assertIsInstance(create_b4w_json_result, ExportB4WParamsDTO)
        self.assertEqual(
            DamAssetInfoSerializer(create_b4w_json_result.dam_asset_info).data,
            DamAssetInfoSerializer(self.material_asset).data,
        )
        self.assertEqual(create_b4w_json_result.camera, self.dto.camera)
        self.assertEqual(create_b4w_json_result.export_type, AssetExtensions.JSON)

        export_mock = self.router_mock[ExportB4WOpInterface]
        self.assertEqual(export_mock.call_count, 1)
        export_dto, context = export_mock.call_args
        self.assertEqual(
            DamAssetInfoSerializer(export_dto[0].dam_asset_info).data,
            DamAssetInfoSerializer(self.material_asset).data,
        )
        self.assertEqual(export_dto[0].camera, self.dto.camera)
        self.assertEqual(export_dto[0].export_type, AssetExtensions.JSON)
        self.assertEqual(context['material_implementation_uuid'], self.material_implementation.uuid)
        self.assertEqual(context['asset_type'], MaterialImplementationAsset.JSON_ASSET)

    def test_create_json_for_b4w_without_asset(self):
        """
        Test create json for b4w without asset
        """
        with self.patch:
            with self.assertRaises(MissingMaterialAssetException):
                self.op(self.without_asset_dto)
        export_mock = self.router_mock[ExportB4WOpInterface]
        self.assertFalse(export_mock.called)

    def test_create_json_for_b4w_for_missed_implementation(self):
        """
        Test create json for b4w for missed implementation
        """
        with self.patch:
            with self.assertRaises(MissingMaterialImplementationException):
                self.op(self.missed_revision_dto)
        export_mock = self.router_mock[ExportB4WOpInterface]
        self.assertFalse(export_mock.called)
