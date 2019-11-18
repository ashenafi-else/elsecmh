from unittest.mock import (
    Mock,
    patch,
)

from elsecommon import marshalling
from django.test import TestCase
from elsecommon.tests.helpers import RouterMock
from elsepublic.dto.dam_asset_info import (
    DamAssetInfoDTO,
    DamAssetsInfoDTO,
)
from elsepublic.elsedam.resource_types import ResourceTypes
from elsepublic.elsedam.asset_extensions import AssetExtensions
from elsepublic.serializers.dam_asset_info import DamAssetInfoSerializer
from elsecmh.services.preview_render_settings import get_preview_settings
from elsepublic.elserender.render_operations.render_frame.dto import (
    RenderFrameOpParams,
)
from elsepublic.elserender.render_operations.render_frame.interface import (
    RenderFrameOpInterface,
)
from elsecmh.operations.create_preview.create_preview_compose_success import (
    CreatePreviewComposeSuccessHandler,
)


class TestCreatePreviewComposeSuccessHandler(TestCase):

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
        self.settings_serializer = DamAssetInfoSerializer(
            DamAssetInfoDTO(
                dam_uuid='7dcf73d0-020e-11e9-8eb2-f2801f1b9fd1',
                filename='settings',
                size=256,
                extension=AssetExtensions.BLEND,
                brand_id='1',
                url='https://www.test.com/',
                state='state',
                resource_type=AssetExtensions.BLEND,
                meta_info='',
            ))
        self.context = dict(
            material_implementation_uuid='7dcf73d0-020e-11e9-8eb2-f2801f1b9fd5',
            render_data=dict(
                camera='camera',
                settings_dam_asset_info=self.settings_serializer.data,
            ))

        self.op = CreatePreviewComposeSuccessHandler()

        self.router_mock = RouterMock()
        self.router_mock[RenderFrameOpInterface] = Mock(
            spec=marshalling.ElseOperation)
        self.patch = patch(
            'elsecmh.operations.create_preview.create_preview_compose_success.Router',
            new=self.router_mock)

    def test_create_preview_compose_success_handler(self):
        """
        Test create preview compose success handler
        """
        with self.patch:
            handler_result = self.op(self.dto, **self.context)
            self.assertTrue(isinstance(handler_result, RenderFrameOpParams))
            render_mock = self.router_mock[RenderFrameOpInterface]
            self.assertEqual(render_mock.call_count, 1)
            render_dto, context = render_mock.call_args
            self.assertEqual(
                DamAssetInfoSerializer(render_dto[0].settings_asset_info).data,
                self.settings_serializer.data
            )
            self.assertEqual(
                DamAssetInfoSerializer(render_dto[0].scene_asset_info).data,
                DamAssetInfoSerializer(self.dto.dam_assets_info[0]).data
            )
            render_settings = get_preview_settings()
            self.assertEqual(
                render_dto[0].camera,
                self.context['render_data']['camera'])
            self.assertEqual(
                render_dto[0].resolution_x,
                render_settings['resolution_x'])
            self.assertEqual(
                render_dto[0].resolution_y,
                render_settings['resolution_y'])
            self.assertEqual(
                render_dto[0].out_format,
                render_settings['out_format'])
            self.assertEqual(render_dto[0].engine, render_settings['engine'])
            self.assertEqual(render_dto[0].device, render_settings['device'])
            self.assertEqual(render_dto[0].quality, render_settings['quality'])
