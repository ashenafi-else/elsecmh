from elsecommon import marshalling
from elsecommon.transports.router import Router

from elsepublic.elserender.interfaces.compose import ComposeOpInterface
from elsepublic.elserender.dto.compose import ComposeParamsDTO
from elsepublic.dto.dam_asset_info import DamAssetInfoDTO

from elsepublic.elsecmh.serializers.create_html_for_b4w import CreateHTMLForB4WParamsSerializer
from elsepublic.elsecmh.dto.create_html_for_b4w import CreateHTMLForB4WParamsDTO
from elsecmh.models import (
    MaterialAsset,
    MaterialImplementation,
    MaterialImplementationAsset,
)
from elsepublic.exceptions import (
    MissingMaterialImplementationException,
    MissingMaterialAssetException,
)


class CreateHTMLForB4WOp(marshalling.ElseOperation):
    """
    Operation to create HTML for b4w.

    Attributes
    ----------
    expect_serializer_class : elsepublic.elsecmh.serializers.create_html_for_b4w.CreateHTMLForB4WParamsSerializer
        Expect serializer.

    Raises
    ------
    MissingMaterialImplementationException
        If material implementation does not exist.
    MissingMaterialAssetException
        If there are no assets in revision corresponding to implementation given.
    """
    expect_serializer_class = CreateHTMLForB4WParamsSerializer

    def __call__(self, data: CreateHTMLForB4WParamsDTO, **context) -> None:
        """
        Parameters
        ----------
        data : elsepublic.elsecmh.dto.create_html_for_b4w.CreateHTMLForB4WParamsDTO
            Operation input parameters
        context : dict
            context data

        Returns
        -------
        None
        """
        material_implementation = MaterialImplementation.objects.filter(uuid=data.material_implementation_uuid).first()
        if not material_implementation:
            raise MissingMaterialImplementationException

        material_revision = material_implementation.material_revision
        asset = material_revision.assets.filter(asset_type=MaterialAsset.MODEL_ASSET).first()
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
                export_camera=data.camera,
                asset_type=MaterialImplementationAsset.HTML_ASSET,
                material_implementation_uuid=material_implementation.uuid,
            ),
        )
