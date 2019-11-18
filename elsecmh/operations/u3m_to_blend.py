from elsecmh.models import (
    MaterialAsset,
    MaterialRevision,
)
from elsecommon.marshalling import async_marshall
from elsecommon.transports.router import Router
from elsepublic.dto.dam_asset_info import DamAssetInfoDTO
from elsepublic.elsecmh.import_u3m import (
    U3mToBlendAssetParams,
    U3mToBlendAssetResult,
    U3mToBlendAssetParamsSerializer,
    U3mToBlendAssetResultSerializer,
)
from elsepublic.elserender.import_u3m import (
    ImportU3mParams,
    ImportU3mOpInterface,
)


@async_marshall(
    expect=U3mToBlendAssetParamsSerializer,
    expose=U3mToBlendAssetResultSerializer,
)
async def import_u3m_asset(
        params: U3mToBlendAssetParams,
        **context,
) -> U3mToBlendAssetResult:
    """
    Operation which get u3m assets related to revision
    import these assets to blender model

    Parameters
    ----------
    params: elsepublic.elsecmh.import_u3m.U3mToBlendAssetParams
        Input operation params
    context: dict
        Keyword arguments

    Returns
    -------
    elsepublic.elsecmh.import_u3m.U3mToBlendAssetResult
        Operation result DTO
    """
    material_revision = MaterialRevision.objects.select_related(
        'material',
    ).get(pk=params.revision_uuid)
    u3m_assets = material_revision.assets.filter(
        asset_type=MaterialAsset.U3M_ASSET,
    ).values()
    dam_assets = [DamAssetInfoDTO(**u3m_asset) for u3m_asset in u3m_assets]
    import_op = Router[ImportU3mOpInterface]
    import_params = ImportU3mParams(
        name=material_revision.material.name,
        assets=dam_assets,
    )
    imported_assets = await import_op(import_params, **context)
    model_dam_asset = imported_assets.dam_assets_info[0]
    model_asset = MaterialAsset.objects.create(
        asset_type=MaterialAsset.MODEL_ASSET,
        material_revision=material_revision,
        resource_type=imported_assets.dam_asset_batch.resource_type,
        dam_uuid=model_dam_asset.uuid,
        filename=model_dam_asset.filename,
        size=model_dam_asset.size,
        extension=model_dam_asset.extension,
        brand_id=model_dam_asset.brand_id,
        url=model_dam_asset.url,
        state=model_dam_asset.state,
        meta_info=model_dam_asset.meta_info,
        tags=model_dam_asset.tags,
    )

    return U3mToBlendAssetResult(asset_uuid=model_asset.pk)
