from elsecommon import marshalling
from elsecommon.transports.router import Router
from elsepublic.elsecmh.serializers.create_json_for_b4w import CreateJSONForB4WParamsSerializer
from elsepublic.elserender.export_b4w_json import AsyncExportJSONOpInterface
from elsepublic.elsecmh.dto.create_json_for_b4w import CreateJSONForB4WParamsDTO
from elsepublic.elsedam.asset_extensions import AssetExtensions
from elsepublic.elserender.dto.export_b4w import ExportB4WParamsDTO
from elsepublic.dto.dam_asset_info import DamAssetInfoDTO
from elsecmh.models import (
    MaterialAsset,
    MaterialImplementation,
    MaterialImplementationAsset,
)
from elsepublic.helpers.asset_dto_to_dict import asset_dto_to_dict


class CreateJSONForB4WOp(marshalling.AsyncElseOperation):
    """
    Async operation to create JSON for b4w.

    Attributes
    ----------
    expect_serializer_class : elsepublic.elsecmh.serializers.
    create_json_for_b4w.CreateJSONForB4WParamsSerializer
        Expect serializer.
    """
    expect_serializer_class = CreateJSONForB4WParamsSerializer

    async def __call__(self, data: CreateJSONForB4WParamsDTO, **context) -> None:
        """
        Parameters
        ----------
        data : elsepublic.elsecmh.dto.create_json_for_b4w.CreateJSONForB4WParamsDTO
            Operation input parameters
        context : dict
            context data
        """
        material_implementation = MaterialImplementation.objects.get(
            uuid=data.material_implementation_uuid,
        )
        material_revision = material_implementation.material_revision
        asset = material_revision.assets.get(
            asset_type=MaterialAsset.MODEL_ASSET,
        )

        export_b4w_json_op = Router[AsyncExportJSONOpInterface]
        export_b4w_dto = ExportB4WParamsDTO(
            dam_asset_info=DamAssetInfoDTO(
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
            export_type=AssetExtensions.JSON,
            camera=data.camera,
        )
        export_result = await export_b4w_json_op(
            export_b4w_dto,
            **dict(
                **context,
                material_implementation_uuid=material_implementation.uuid,
                asset_type=MaterialImplementationAsset.JSON_ASSET,
            ),
        )
        asset_list = []
        for dam_asset in export_result.dam_assets:
            asset_list.append(
                MaterialImplementationAsset(
                    material_implementation=material_implementation,
                    asset_type=MaterialImplementationAsset.JSON_ASSET,
                    **asset_dto_to_dict(dam_asset),
                ),
            )
        MaterialImplementationAsset.objects.bulk_create(asset_list)
