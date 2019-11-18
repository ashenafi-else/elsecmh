from elsecommon.transports.router import Router

from elsecmh.models import (
    MaterialAsset,
    MaterialImplementation,
    MaterialImplementationAsset,
)
from elsecommon import marshalling
from elsepublic.dto.dam_asset_info import DamAssetInfoDTO
from elsepublic.elsecmh.dto.create_preview import CreatePreviewParamsDTO
from elsepublic.elsecmh.serializers.create_preview import CreatePreviewParamsSerializer
from elsepublic.elserender.dto.compose import ComposeParamsDTO
from elsepublic.serializers.dam_asset_info import DamAssetInfoSerializer
from elsepublic.elserender.compose import AsyncComposeOpInterface
from elsecmh.services.preview_render_settings import get_preview_settings
from elsepublic.elserender.render import (
    AsyncRenderOpInterface,
)
from elsepublic.elserender.render_operations.render_frame.dto import (
    RenderFrameOpParams,
)
from elsepublic.helpers.asset_dto_to_dict import asset_dto_to_dict


class AsyncCreatePreviewOp(marshalling.AsyncElseOperation):
    """
    Async operation to create preview image according to values from
    elsecmh.services.preview_render_settings.get_preview_settings:
    quality, out_format, engine, device, resolution_x, resolution_y
    with environment and settings placed in input dto.

    Attributes
    ----------
    expect_serializer_class : elsepublic.elsecmh.serializers.create_preview.CreatePreviewParamsSerializer
        Expect serializer.
    """
    expect_serializer_class = CreatePreviewParamsSerializer

    async def call(self, data: CreatePreviewParamsDTO, **context) -> None:
        """
        Parameters
        ----------
        data : elsepublic.elsecmh.dto.create_preview.CreatePreviewParamsDTO
            Operation input parameters
        context : dict
            context data
        """
        material_implementation = MaterialImplementation.objects.get(
            uuid=data.uuid,
        )
        asset = material_implementation.material_revision.assets.get(
            asset_type=MaterialAsset.MODEL_ASSET,
        )

        compose_op = Router[AsyncComposeOpInterface]
        compose_dto = ComposeParamsDTO(
            dam_assets_info=[
                data.environment,
                DamAssetInfoDTO(
                    dam_uuid=asset.dam_uuid,
                    filename=asset.filename,
                    size=asset.size,
                    extension=asset.extension,
                    brand_id=asset.brand_id,
                    url=asset.url,
                    state=asset.state,
                    resource_type=asset.resource_type,
                    meta_info=asset.meta_info,
                ),
            ]
        )
        compose_result = await compose_op(
            compose_dto,
            **dict(
                **context,
                material_implementation_uuid=material_implementation.uuid,
                render_data=dict(
                    camera=data.camera,
                    settings_dam_asset_info=DamAssetInfoSerializer(
                        data.settings,
                    ).data,
                ),
                asset_type=MaterialImplementationAsset.PREVIEW_ASSET,
            ),
        )

        scene_dam_asset_info = compose_result.asset
        render_data = context.pop('render_data')
        settings_asset_info_serializer = DamAssetInfoSerializer(
            data=render_data['settings_dam_asset_info'])
        settings_asset_info_serializer.is_valid(raise_exception=True)
        settings_asset_info_dto = settings_asset_info_serializer.to_entity()

        render_settings = get_preview_settings()
        render_frame_op = Router[AsyncRenderOpInterface]
        render_frame_dto = RenderFrameOpParams(
            settings_asset_info=settings_asset_info_dto,
            scene_asset_info=scene_dam_asset_info,
            camera=render_data['camera'],
            **render_settings
        )
        render_result = await render_frame_op(
            render_frame_dto,
            **context,
        )

        asset_list = []
        for dam_asset in render_result.dam_assets:
            asset_list.append(
                MaterialImplementationAsset(
                    material_implementation=material_implementation,
                    asset_type=MaterialImplementationAsset.PREVIEW_ASSET,
                    **asset_dto_to_dict(dam_asset),
                ),
            )
        MaterialImplementationAsset.objects.bulk_create(asset_list)