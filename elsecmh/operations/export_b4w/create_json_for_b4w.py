from elsecommon import marshalling
from elsecommon.transports.router import Router
from elsepublic.elsecmh.serializers.create_json_for_b4w import CreateJSONForB4WParamsSerializer
from elsepublic.elserender.interfaces.export_b4w import ExportB4WOpInterface
from elsepublic.elsecmh.dto.create_json_for_b4w import CreateJSONForB4WParamsDTO
from elsepublic.elsedam.asset_extensions import AssetExtensions
from elsepublic.elserender.dto.export_b4w import ExportB4WParamsDTO
from elsepublic.elserender.serializers.export_b4w import ExportB4WParamsSerializer
from elsepublic.dto.dam_asset_info import DamAssetInfoDTO
from elsecmh.models import (
    MaterialAsset,
    MaterialImplementation,
    MaterialImplementationAsset,
)
from elsepublic.exceptions import (
    MissingMaterialImplementationException,
    MissingMaterialAssetException,
)


class CreateJSONForB4WOp(marshalling.ElseOperation):
    """
    Operation to create JSON for b4w.

    Attributes
    ----------
    expect_serializer_class : elsepublic.elsecmh.serializers.create_json_for_b4w.CreateJSONForB4WParamsSerializer
        Expect serializer.
    expose_serializer_class : elsepublic.elserender.serializers.export_b4w.ExportB4WParamsSerializer
        Expose serializer.

    Raises
    ------
    MissingMaterialImplementationException
        If material implementation does not exist.
    MissingMaterialAssetException
        If there are no assets in revision corresponding to implementation given.
    """
    expect_serializer_class = CreateJSONForB4WParamsSerializer
    expose_serializer_class = ExportB4WParamsSerializer

    def __call__(self, data: CreateJSONForB4WParamsDTO, **context) -> ExportB4WParamsDTO:
        """
        Parameters
        ----------
        data : elsepublic.elsecmh.dto.create_json_for_b4w.CreateJSONForB4WParamsDTO
            Operation input parameters
        context : dict
            context data

        Returns
        -------
        elsepublic.elsedam.dto.export_b4w.ExportB4WParamsDTO
            Operation output result
        """
        material_implementation = MaterialImplementation.objects.filter(uuid=data.material_implementation_uuid).first()
        if not material_implementation:
            raise MissingMaterialImplementationException

        material_revision = material_implementation.material_revision
        asset = material_revision.assets.filter(asset_type=MaterialAsset.MODEL_ASSET).first()
        if not asset:
            raise MissingMaterialAssetException

        export_b4w_op = Router[ExportB4WOpInterface]
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
        export_b4w_op(
            export_b4w_dto,
            **dict(
                **context,
                material_implementation_uuid=material_implementation.uuid,
                asset_type=MaterialImplementationAsset.JSON_ASSET,
            ),
        )
        return export_b4w_dto
