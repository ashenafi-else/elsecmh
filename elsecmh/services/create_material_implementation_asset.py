from typing import Optional

from elsecmh.models import (
    MaterialImplementation,
    MaterialImplementationAsset,
    MaterialRevision,
)
from elsepublic.dto.dam_asset_info import DamAssetsInfoDTO
from elsepublic.elsecmh.dto.get_material_implementation import GetMaterialImplementationResultDTO
from elsepublic.helpers.asset_dto_to_dict import asset_dto_to_dict

PUBLISHED_TYPES = [
    MaterialImplementationAsset.MODEL_ASSET,
    MaterialImplementationAsset.PREVIEW_ASSET,
    MaterialImplementationAsset.JSON_ASSET,
    MaterialImplementationAsset.HTML_ASSET,
]


def create_material_implementation_asset(data: DamAssetsInfoDTO, material_implementation_uuid, asset_type) -> Optional[GetMaterialImplementationResultDTO]:
    """
    Service which save material implementation asset

    Parameters
    ----------
    data : elsepublic.dto.dam_asset_info.DamAssetsInfoDTO
        Operation input parameters
    material_implementation_uuid : str
        uuid of material implementation
    asset_type : str
        asset type of material implementation asset

    Returns
    -------
    elsepublic.elsecmh.dto.get_material_implementation.GetMaterialImplementationResultDTO or None
        Service output result. Returns DTO in case if the material implementation 
        has asset of all the types from PUBLISHED_TYPES 
    """
    material_implementation = MaterialImplementation.objects.filter(uuid=material_implementation_uuid).first()
    asset_list = []
    for dam_asset in data.dam_assets_info:
        asset_list.append(MaterialImplementationAsset(
            material_implementation=material_implementation,
            asset_type=asset_type,
            **asset_dto_to_dict(dam_asset)))

    MaterialImplementationAsset.objects.bulk_create(asset_list)

    asset_type_count = material_implementation.assets.filter(
        asset_type__in=PUBLISHED_TYPES).distinct('asset_type').count()
    if asset_type_count == len(PUBLISHED_TYPES):
        return GetMaterialImplementationResultDTO(uuid=material_implementation.uuid)
