import json

import h5py
from elsecommon import marshalling
from elsepublic.elsedam.buffering_assets.dto import PutAssetsToBufferResult
from elsecmh.models import MaterialRevision, MaterialMetaData
from elsecmh.operations.axf_operations.import_axf_meta_data.utils import (
    save_meta_data,
    dict_parse_tree,
)
from elsepublic.elsedam.buffering_assets.serializers import (
    PutAssetsToBufferResultSerializer,
)


class ImportAxFBufferAssetSuccessHandler(marshalling.ElseOperation):
    """
    Handler for Import AxF buffer asset.

    Attributes
    ----------
    expect_serializer_class : PutAssetsToBufferResultSerializer
        Expect serializer.
    expose_serializer_class : None
        Expose serializer.
    """
    expect_serializer_class = PutAssetsToBufferResultSerializer
    expose_serializer_class = None

    def __call__(self, data: PutAssetsToBufferResult, **context) -> None:
        """
        Parameters
        ----------
        data : elsepublic.elsedam.dto.put_assets_to_buffer_operation.PutAssetsToBufferResult
            Operation input parameters
        context : dict
            context data
        Returns
        -------
        None
        """
        buffer_path = data.dam_asset_requests[0].buffered_asset.buffer_file.name
        axf_file = h5py.File(buffer_path, 'r')
        data = dict_parse_tree(axf_file)
        material_revision_uuid = context.get('material_revision_uuid')
        material_revision = MaterialRevision.objects.filter(
            uuid=material_revision_uuid).first()

        MaterialMetaData.add_root(
            material_revision=material_revision,
            category=MaterialMetaData.AXF_RAW_DATA,
            key='data',
            value=json.dumps(data, indent=4).encode('utf-8'),
        )
        save_meta_data(buffer_path, material_revision)
        return
