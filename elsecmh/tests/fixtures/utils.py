import json

from elsepublic.elsedam.asset_tags import AssetTags
from elsepublic.elsedam.put_assets.dto import (
    PutAssetResult,
    PutAssetsResult,
)
from elsepublic.elsedam.resource_types import ResourceTypes
from elsepublic.elsedam.asset_extensions import AssetExtensions
from elsepublic.elsedam.buffering_assets.dto import (
    PutAssetToBufferResult,
    PutAssetsToBufferResult,
    BufferedDamAssetParameters,
)
from elsepublic.elsecmh.create_material_revision import CreateMaterialRevParams


def get_create_material_revision_dto(
        material_uuid,
        dam_asset_info,
        color_uuids):
    return CreateMaterialRevParams(
        uuid=material_uuid,
        info=json.dumps({'data': {'a': 'a'}}),
        brand_id='1',
        assets=[dam_asset_info],
        color_uuids=color_uuids
    )


def get_put_assets_result_dto(input_file):
    return PutAssetsResult(
        dam_assets=[PutAssetResult(
            uuid='642bbbe6-d21b-11e8-a8d5-f2801f1b9fc1',
            filename='exported_model',
            file=open(input_file, 'rb'),
            size=10,
            mime_type='blob',
            extension=AssetExtensions.BLEND,
            brand_id='1',
            tags=[AssetTags.BLENDER_MODEL],
            url='http://url.else',
            state='test_state',
            resource_type=ResourceTypes.BLENDER_MODEL,
            description='test',
            temporary=True,
        )]
    )


def get_put_assets_to_buff_result_dto(file):
    return PutAssetsToBufferResult(
        dam_asset_requests=[PutAssetToBufferResult(
            uuid='2b138d8e-020e-11e9-8eb2-f2801f1b9fd1',
            created='2018-12-17 19:04:53.896428',
            buffered_asset=BufferedDamAssetParameters(
                uuid='26e8f12c-020e-11e9-8eb2-f2801f1b9fd1',
                buffer_url='https://www.google.com/',
                buffer_path='path',
                buffer_file=file,
                state='state',
                meta_info='data',
            ),
        )]
    )
