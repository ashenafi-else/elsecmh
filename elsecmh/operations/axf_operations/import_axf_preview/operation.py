import os

from elsecommon import marshalling
from elsecommon.transports.router import Router
from elsepublic.elsedam.asset_tags import AssetTags
from elsepublic.elsedam.put_assets import (
    PutAssetsParams,
    PutAssetParameters,
)
from elsepublic.elsedam.resource_types import ResourceTypes
from elsepublic.elsecmh.axf.import_preview import (
    ImportAxFPreviewParamsDTO,
    ImportAxFPreviewParamsSerializer,
)
from elsepublic.elsedam.interfaces.put_assets_operation import (
    PutAssetsOpInterface,
)
from elsecmh.operations.axf_operations.import_axf_preview.utils import (
    extract_preview,
    get_file_with_preview,
)


# TODO (f.gaponenko@invento.by): add handling the buffer
class ImportAxFPreviewOp(marshalling.ElseOperation):
    """
       Operation for import AxF preview.

       Attributes
       ----------
       expect_serializer_class : ImportAxFPreviewParamsSerializer
           Expect serializer.
       expose_serializer_class : None
           Expose serializer.
       """

    expect_serializer_class = ImportAxFPreviewParamsSerializer
    expose_serializer_class = None

    def __call__(self, params: ImportAxFPreviewParamsDTO, **context) -> None:
        """
               Parameters
               ----------
               params :
               elsepublic.elsecmh.dto.import_axf_preview.ImportAxFPreviewParamsDTO
                   Operation input parameters
               context : dict
                   context data
               Returns
               -------
               None
        """

        preview_image = extract_preview(params.file_name)
        out_file = get_file_with_preview(preview_image)
        material_revision_uuid = params.material_revision_uuid

        put_to_dam_op = Router[PutAssetsOpInterface]

        with open(os.path.abspath(out_file.name), 'rb') as file:
            asset = PutAssetParameters(
                filename=os.path.basename(file.name),
                brand_id=params.brand_id,
                tags=[AssetTags.PREVIEW],
                file=file,
                temporary=False,
            )
            put_to_dam_dto = PutAssetsParams(
                base_assets=[asset],
                resource_type=ResourceTypes.PREVIEW,
                initiator=f'update material {material_revision_uuid}',
            )
            put_to_dam_op(
                put_to_dam_dto,
                material_uuid=str(material_revision_uuid),
                **context,
            )
