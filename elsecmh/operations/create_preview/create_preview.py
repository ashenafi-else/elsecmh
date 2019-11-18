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
from elsepublic.elserender.interfaces.compose import ComposeOpInterface
from elsepublic.exceptions import (
    MissingMaterialAssetException,
    MissingMaterialImplementationException,
)
from elsepublic.serializers.dam_asset_info import DamAssetInfoSerializer


class CreatePreviewOp(marshalling.ElseOperation):
    """
    Operation to create preview image according to values from
    elsecmh.services.preview_render_settings.get_preview_settings: 
    quality, out_format, engine, device, resolution_x, resolution_y
    with environment and settings placed in input dto.

    Attributes
    ----------
    expect_serializer_class : elsepublic.elsecmh.serializers.create_preview.CreatePreviewParamsSerializer
        Expect serializer.
    expose_serializer_class : None
        Expose serializer.

    Raises
    ------
    MissingMaterialImplementationException
        If material implementation does not exist.
    MissingMaterialAssetException
        If material revision does not have model asset.
    """
    expect_serializer_class = CreatePreviewParamsSerializer
    expose_serializer_class = None

    def __call__(self, data: CreatePreviewParamsDTO, **context) -> None:
        """
        Parameters
        ----------
        data : elsepublic.elsecmh.dto.create_preview.CreatePreviewParamsDTO
            Operation input parameters
        context : dict
            context data

        Returns
        -------
        None
        """
        material_implementation = MaterialImplementation.objects.filter(uuid=data.uuid).first()
        if not material_implementation:
            raise MissingMaterialImplementationException
        asset = material_implementation.material_revision.assets.filter(asset_type=MaterialAsset.MODEL_ASSET).first()
        if not asset:
            raise MissingMaterialAssetException

        compose_op = Router[ComposeOpInterface]
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
        compose_op(
            compose_dto,
            **dict(
                **context,
                material_implementation_uuid=material_implementation.uuid,
                render_data=dict(
                    camera=data.camera,
                    settings_dam_asset_info=DamAssetInfoSerializer(data.settings).data,
                ),
                asset_type=MaterialImplementationAsset.PREVIEW_ASSET,
            ),
        )

