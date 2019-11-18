from elsecommon import marshalling
from elsecommon.transports.router import Router
from elsepublic.dto.dam_asset_info import DamAssetsInfoDTO
from elsepublic.serializers.dam_asset_info import (
    DamAssetInfoSerializer,
    DamAssetsInfoSerializer,
)
from elsecmh.services.preview_render_settings import get_preview_settings
from elsepublic.elserender.render_operations.render_frame.dto import (
    RenderFrameOpParams,
)
from elsepublic.elserender.render_operations.render_frame.interface import (
    RenderFrameOpInterface,
)
from elsepublic.elserender.render_operations.render_frame.serializers import (
    RenderFrameOpParamsSerializer,
)


class CreatePreviewComposeSuccessHandler(marshalling.ElseOperation):
    """
    Handler which responds to put assets operation called by
    compose operation after create preview operation

    Attributes
    ----------
    expect_serializer_class : elsepublic.serializers.dam_asset_info.DamAssetsInfoSerializer
        Expect serializer.
    expose_serializer_class : elsepublic.elserender.serializers.render_frame_serializer.RenderFrameOpParamsSerializer
        Expose serializer.
    """
    expect_serializer_class = DamAssetsInfoSerializer
    expose_serializer_class = RenderFrameOpParamsSerializer

    def __call__(self, data: DamAssetsInfoDTO, **
                 context) -> RenderFrameOpParams:
        """
        Parameters
        ----------
        data : elsepublic.dto.dam_asset_info.DamAssetsInfoDTO
            Operation input parameters
        context : dict
            context data {render_data{settings_dam_asset_info, camera}, material_implementation_uuid}

        Returns
        -------
        elsepublic.elsedam.dto.put_assets_operation.PutAssetsResult
            Operation output result
        """
        scene_dam_asset_info = data.dam_assets_info[0]
        render_data = context.pop('render_data')
        settings_asset_info_serializer = DamAssetInfoSerializer(
            data=render_data['settings_dam_asset_info'])
        settings_asset_info_serializer.is_valid(raise_exception=True)
        settings_asset_info_dto = settings_asset_info_serializer.to_entity()

        render_settings = get_preview_settings()
        render_frame_op = Router[RenderFrameOpInterface]
        render_frame_dto = RenderFrameOpParams(
            settings_asset_info=settings_asset_info_dto,
            scene_asset_info=scene_dam_asset_info,
            camera=render_data['camera'],
            **render_settings
        )
        render_frame_op(render_frame_dto, **context)
        return render_frame_dto
