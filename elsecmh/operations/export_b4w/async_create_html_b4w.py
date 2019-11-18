from elsepublic.elserender.compose import AsyncComposeOpInterface
from elsepublic.elserender.dto.compose import ComposeParamsDTO
from elsepublic.dto.dam_asset_info import DamAssetInfoDTO

from elsepublic.elsecmh.serializers.create_html_for_b4w import CreateHTMLForB4WParamsSerializer
from elsepublic.elsecmh.dto.create_html_for_b4w import CreateHTMLForB4WParamsDTO
from elsecmh.models import (
    MaterialAsset,
    MaterialImplementation,
    MaterialImplementationAsset,
)
from elsecommon.transports.router import Router
from elsecommon import marshalling
from elsepublic.elserender.dto.export_b4w import ExportB4WParamsDTO
from elsepublic.elserender.export_b4w_html import AsyncExportHTMLOpInterface
from elsepublic.elsedam.asset_extensions import AssetExtensions
from elsepublic.helpers.asset_dto_to_dict import asset_dto_to_dict


class AsyncCreateHTMLForB4WOp(marshalling.AsyncElseOperation):
    """
    Async operation to create HTML for b4w.

    Attributes
    ----------
    expect_serializer_class : elsepublic.elsecmh.serializers.create_html_for_b4w.CreateHTMLForB4WParamsSerializer
        Expect serializer.
    """
    expect_serializer_class = CreateHTMLForB4WParamsSerializer

    async def __call__(self, data: CreateHTMLForB4WParamsDTO, **context) -> None:
        """
        Parameters
        ----------
        data : elsepublic.elsecmh.dto.create_html_for_b4w.CreateHTMLForB4WParamsDTO
            Operation input parameters
        context : dict
            context data
        """
        material_implementation = MaterialImplementation.objects.get(
            uuid=data.material_implementation_uuid,
        )

        material_revision = material_implementation.material_revision
        asset = material_revision.assets.get(asset_type=MaterialAsset.MODEL_ASSET)

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
                export_camera=data.camera,
                asset_type=MaterialImplementationAsset.HTML_ASSET,
                material_implementation_uuid=material_implementation.uuid,
            ),
        )

        export_dam_asset_info = compose_result.asset

        export_b4w_op = Router[AsyncExportHTMLOpInterface]
        export_b4w_dto = ExportB4WParamsDTO(
            dam_asset_info=export_dam_asset_info,
            export_type=AssetExtensions.HTML,
            camera=context.pop('export_camera'),
        )
        export_result = await export_b4w_op(export_b4w_dto, **context)

        asset_list = []
        for dam_asset in export_result.dam_assets:
            asset_list.append(
                MaterialImplementationAsset(
                    material_implementation=material_implementation,
                    asset_type=MaterialImplementationAsset.HTML_ASSET,
                    **asset_dto_to_dict(dam_asset),
                ),
            )
        MaterialImplementationAsset.objects.bulk_create(asset_list)
