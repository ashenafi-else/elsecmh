from elsecmh.models import MaterialAsset
from elsepublic.elsedam.asset_extensions import AssetExtensions

ASSET_TYPE_MAPPING = {
    AssetExtensions.AXF: MaterialAsset.AXF_ASSET,
    AssetExtensions.BLEND: MaterialAsset.MODEL_ASSET,
    AssetExtensions.U3M: MaterialAsset.U3M_ASSET,
}


def get_asset_type_by_ext(asset_extension: str) -> str:
    return ASSET_TYPE_MAPPING.get(asset_extension, MaterialAsset.MODEL_ASSET)
