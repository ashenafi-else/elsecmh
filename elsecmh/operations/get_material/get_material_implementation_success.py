from elsecommon import marshalling
from elsecmh.models import (
    MaterialImplementation,
    MaterialImplementationAsset,
)
from elsepublic.dto.dam_asset_info import DamAssetInfoDTO
from elsepublic.elsecmh.dto.get_material_implementation import GetMaterialImplementationResultDTO
from elsepublic.elsecmh.dto.material_implementation import MaterialImplementationDTO
from elsepublic.elsecmh.serializers.get_material_implementation import GetMaterialImplementationResultSerializer
from elsepublic.elsecmh.serializers.material_implementation import MaterialImplementationSerializer
from elsepublic.elsedam.asset_extensions import AssetExtensions
from elsepublic.helpers.asset_to_dto import asset_to_dto


class GetMaterialImplementationSuccessHandler(marshalling.ElseOperation):
    """
    Handler for success get material implementation. 

    Attributes
    ----------
    expect_serializer_class : elsepublic.elsecmh.dto.get_material_implementation.GetMaterialImplementationParamsSerializer
        Expect serializer.
    expose_serializer_class : elsepublic.elsecmh.serializers.material_implementation.MaterialImplementationSerializer
        Expose serializer.
    """
    expect_serializer_class = GetMaterialImplementationResultSerializer
    expose_serializer_class = MaterialImplementationSerializer

    def __call__(self, data: GetMaterialImplementationResultDTO, **context) -> MaterialImplementationDTO:
        """
        Parameters
        ----------
        data : elsepublic.elsecmh.dto.get_material.GetMaterialParamsDTO
            Operation input parameters
        context : dict
            context data

        Returns
        -------
        elsepublic.elsecmh.dto.material_implementation.MaterialImplementationDTO
            Operation result object
        """
        material_impl = MaterialImplementation.objects.get(uuid=data.uuid)
        preview_asset = material_impl.assets.filter(
            asset_type=MaterialImplementationAsset.PREVIEW_ASSET
        ).first()
        json_asset = material_impl.assets.filter(
            asset_type=MaterialImplementationAsset.JSON_ASSET,
            extension=AssetExtensions.JSON,
        ).first()
        html_asset = material_impl.assets.filter(
            asset_type=MaterialImplementationAsset.HTML_ASSET,
            extension=AssetExtensions.HTML,
        ).first()
        return MaterialImplementationDTO(
            group_name=material_impl.material_revision.material.material_group.name,
            material_name=material_impl.material_revision.material.name,
            material_info=material_impl.material_revision.material_info,
            color_name=material_impl.name,
            preview_asset=asset_to_dto(preview_asset),
            json_asset=asset_to_dto(json_asset),
            html_asset=asset_to_dto(html_asset),
        )
