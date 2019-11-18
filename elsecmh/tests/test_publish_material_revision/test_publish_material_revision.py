from elsecmh.tests.test_base_cmh import TestBaseCmh
from elsecommon import marshalling
from unittest.mock import (
    Mock,
    patch,
)
from elsecommon.tests.helpers import RouterMock

from elsecmh.operations.publish_material_revision.publish_material_revision import PublishMaterialRevisionOp
from elsepublic.elsecmh.dto.publish_material_revision import PublishMaterialRevisionParamsDTO

from elsepublic.elsecmh.interfaces.create_preview import CreatePreviewOpInterface
from elsepublic.elsecmh.interfaces.create_html_for_b4w import CreateHTMLForB4WOpInterface
from elsepublic.elsecmh.interfaces.create_json_for_b4w import CreateJSONForB4WOpInterface

from elsepublic.dto.dam_asset_info import DamAssetInfoDTO
from elsepublic.serializers.dam_asset_info import DamAssetInfoSerializer
from elsepublic.elsedam.asset_extensions import AssetExtensions
from elsepublic.elsedam.resource_types import ResourceTypes

from elsecmh.models import (
    Material,
    MaterialRevision,
    MaterialAsset,
    MaterialImplementationAsset,
    MaterialImplementation,
)
from elsepublic.exceptions import (
    MissingMaterialRevisionException,
    NotValidatedRevisionException,
)


class TestPublishMaterialRevision(TestBaseCmh):

    def setUp(self):
        super().setUp()

        material = Material.objects.create(name='material', material_group=self.root)
        self.material_revision = MaterialRevision.objects.create(
            material=material,
            material_info={
                "default_color": "black",
                "type": "regular",
                "available_colors": ["black", "white"],
            },
            status=MaterialRevision.STATUS_VALIDATED,
        )

        self.material_implementation = MaterialImplementation.objects.create(
            material_revision=self.material_revision,
            name='test implementation',
        )

        common_data = dict(
            filename='settings',
            size=256,
            extension=AssetExtensions.BLEND,
            brand_id='1',
            url='https://www.test.com/',
            state='state',
            resource_type=ResourceTypes.BLEND4WEB_HTML,
            meta_info='',
        )

        self.material_model_asset = MaterialAsset.objects.create(
            material_revision=self.material_revision,
            asset_type=MaterialAsset.MODEL_ASSET,
            dam_uuid='7dcf73d0-020e-11e9-8eb2-f2801f1b9fd1',
            **common_data,
        )

        self.settings_dto = DamAssetInfoDTO(
            dam_uuid='7dcf73d0-020e-11e9-8eb2-f2801f1b9fd1',
            **common_data,
        )
        self.environment_dto = DamAssetInfoDTO(
            dam_uuid='7dcf73d0-020e-11e9-8eb2-f2801f1b9fd2',
            **common_data,
        )

        common_dto_data = dict(
            camera='some_camera',
            environment=self.environment_dto,
            settings=self.settings_dto,
        )
        self.dto = PublishMaterialRevisionParamsDTO(
            material_revision_uuid=self.material_revision.uuid,
            **common_dto_data,
        )

        self.not_validated_material_revision = MaterialRevision.objects.create(
            material=material,
            material_info={
                "default_color": "black",
                "type": "regular",
                "available_colors": ["black", "white"],
            },
            status=MaterialRevision.STATUS_NEW,
        )
        self.not_validated_revision_dto = PublishMaterialRevisionParamsDTO(
            material_revision_uuid=self.not_validated_material_revision.uuid,
            **common_dto_data,
        )
        self.missing_revision_dto = PublishMaterialRevisionParamsDTO(
            material_revision_uuid='7dcf73d0-020e-11e9-8eb2-f2801f1b9fd1',
            **common_dto_data,
        )

        self.op = PublishMaterialRevisionOp()

        self.router_mock = RouterMock()
        self.router_mock[CreatePreviewOpInterface] = Mock(spec=marshalling.ElseOperation)
        self.router_mock[CreateHTMLForB4WOpInterface] = Mock(spec=marshalling.ElseOperation)
        self.router_mock[CreateJSONForB4WOpInterface] = Mock(spec=marshalling.ElseOperation)
        self.router_patch = patch(
            'elsecmh.operations.publish_material_revision.publish_material_revision.Router',
            new=self.router_mock,
        )
        self.get_default_implementation_patch = patch(
            'elsecmh.operations.publish_material_revision.publish_material_revision.get_default_color_implementation',
            return_value=self.material_implementation,
        )

    def test_publish_material_revision(self):
        """
        Test publish material revision
        """
        with self.router_patch, self.get_default_implementation_patch:
            publish_material_revision_result = self.op(self.dto)

        self.assertIsNone(publish_material_revision_result)

        material_revision = MaterialRevision.objects.filter(uuid=self.material_revision.uuid).first()
        self.assertEqual(material_revision.status, MaterialRevision.STATUS_PUBLISHING)

        created_implementation_model_asset = self.material_implementation.assets.filter(
            asset_type=MaterialImplementationAsset.MODEL_ASSET,
        ).first()
        self.assertIsNotNone(created_implementation_model_asset)

        created_environment_asset = material_revision.assets.filter(
            asset_type=MaterialAsset.ENVIRONMENT_ASSET,
            **vars(self.environment_dto),
        ).first()
        self.assertIsNotNone(created_environment_asset)

        created_settings_asset = material_revision.assets.filter(
            asset_type=MaterialAsset.SETTINGS_ASSET,
            **vars(self.settings_dto),
        )
        self.assertIsNotNone(created_settings_asset)

        create_preview_mock = self.router_mock[CreatePreviewOpInterface.uri]
        self.assertEqual(create_preview_mock.call_count, 1)

        create_preview_dto, context = create_preview_mock.call_args
        self.assertEqual(create_preview_dto[0].camera, self.dto.camera)
        self.assertEqual(DamAssetInfoSerializer(create_preview_dto[0].environment).data,
                         DamAssetInfoSerializer(self.environment_dto).data)
        self.assertEqual(DamAssetInfoSerializer(create_preview_dto[0].settings).data,
                         DamAssetInfoSerializer(self.settings_dto).data)
        self.assertEqual(create_preview_dto[0].uuid, str(self.material_implementation.uuid))

        create_html_mock = self.router_mock[CreateHTMLForB4WOpInterface.uri]
        self.assertEqual(create_html_mock.call_count, 1)

        create_html_dto, context = create_html_mock.call_args
        self.assertEqual(create_html_dto[0].camera, self.dto.camera)
        self.assertEqual(DamAssetInfoSerializer(create_html_dto[0].environment).data,
                         DamAssetInfoSerializer(self.environment_dto).data)
        self.assertEqual(create_html_dto[0].material_implementation_uuid, str(self.material_implementation.uuid))

        create_json_mock = self.router_mock[CreateJSONForB4WOpInterface.uri]
        self.assertEqual(create_json_mock.call_count, 1)

        create_json_dto, context = create_json_mock.call_args
        self.assertEqual(create_json_dto[0].camera, self.dto.camera)
        self.assertEqual(create_json_dto[0].material_implementation_uuid, str(self.material_implementation.uuid))

    def test_publish_material_revision_with_missing_revision(self):
        """
        Test publish material revision with missing revision
        """
        with self.router_patch, self.get_default_implementation_patch:
            with self.assertRaises(MissingMaterialRevisionException):
                self.op(self.missing_revision_dto)

        create_preview_mock = self.router_mock[CreatePreviewOpInterface.uri]
        self.assertFalse(create_preview_mock.called)

        create_html_mock = self.router_mock[CreateHTMLForB4WOpInterface.uri]
        self.assertFalse(create_html_mock.called)

        create_json_mock = self.router_mock[CreateJSONForB4WOpInterface.uri]
        self.assertFalse(create_json_mock.called)

    def test_publish_material_not_validated_revision(self):
        """
        Test publish material not validated revision
        """
        with self.router_patch, self.get_default_implementation_patch:
            with self.assertRaises(NotValidatedRevisionException):
                self.op(self.not_validated_revision_dto)

        create_preview_mock = self.router_mock[CreatePreviewOpInterface.uri]
        self.assertFalse(create_preview_mock.called)

        create_html_mock = self.router_mock[CreateHTMLForB4WOpInterface.uri]
        self.assertFalse(create_html_mock.called)

        create_json_mock = self.router_mock[CreateJSONForB4WOpInterface.uri]
        self.assertFalse(create_json_mock.called)
