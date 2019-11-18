from unittest.mock import (
    Mock,
    patch,
)
from django.test import TestCase
from elsecommon.tests.helpers import RouterMock

from elsecommon import marshalling
from elsecmh.operations.export_b4w.create_html_compose_success import CreateHTMLComposeSuccessHandler

from elsepublic.serializers.dam_asset_info import DamAssetInfoSerializer
from elsepublic.dto.dam_asset_info import (
    DamAssetInfoDTO,
    DamAssetsInfoDTO,
)

from elsepublic.elsedam.asset_extensions import AssetExtensions
from elsepublic.elsedam.resource_types import ResourceTypes

from elsepublic.elserender.dto.export_b4w import ExportB4WParamsDTO
from elsepublic.elserender.interfaces.export_b4w import ExportB4WOpInterface


class TestCreateHTMLComposeSuccessHandler(TestCase):

    def setUp(self):

        self.dto = DamAssetsInfoDTO(
            dam_assets_info=[DamAssetInfoDTO(
                dam_uuid='642bbbe6-d21b-11e8-a8d5-f2801f1b9fc1',
                filename='exported_model',
                size=10,
                extension=AssetExtensions.BLEND,
                brand_id='1',
                url='http://url.else',
                state='test_state',
                resource_type=ResourceTypes.BLENDER_MODEL,
                meta_info='',
            )]
        )
        self.context = dict(
            material_implementation_uuid='7dcf73d0-020e-11e9-8eb2-f2801f1b9fd5',
            export_camera='test_camera',
        )
        self.context_passed = {
            'material_implementation_uuid': '7dcf73d0-020e-11e9-8eb2-f2801f1b9fd5',
        }

        self.router_mock = RouterMock()
        self.router_mock[ExportB4WOpInterface] = Mock(spec=marshalling.ElseOperation)
        self.patch = patch(
            'elsecmh.operations.export_b4w.create_html_compose_success.Router',
            new=self.router_mock,
        )
        self.op = CreateHTMLComposeSuccessHandler()

    def test_create_html_compose_success_handler(self):
        """
        Test create html compose success handler
        """
        with self.patch:
            handler_result = self.op(self.dto, **self.context)
            self.assertIsInstance(handler_result, ExportB4WParamsDTO)
            self.assertEqual(
                DamAssetInfoSerializer(handler_result.dam_asset_info).data,
                DamAssetInfoSerializer(self.dto.dam_assets_info[0]).data,
            )
            self.assertEqual(handler_result.camera, self.context['export_camera'])
            self.assertEqual(handler_result.export_type, AssetExtensions.HTML)

            export_mock = self.router_mock[ExportB4WOpInterface]
            self.assertEqual(export_mock.call_count, 1)
            export_dto, context = export_mock.call_args
            self.assertEqual(
                DamAssetInfoSerializer(export_dto[0].dam_asset_info).data,
                DamAssetInfoSerializer(self.dto.dam_assets_info[0]).data,
            )
            self.assertEqual(export_dto[0].camera, self.context['export_camera'])
            self.assertEqual(export_dto[0].export_type, AssetExtensions.HTML)
            self.assertEqual(context, self.context_passed)
