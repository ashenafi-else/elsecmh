import os

from elsecommon import marshalling
from elsecommon.transports.router import Router
from elsepublic.elsedam.asset_tags import AssetTags
from elsepublic.elsedam.put_assets import (
    PutAssetsParams,
    PutAssetParameters,
)
from elsepublic.elsedam.resource_types import ResourceTypes
from elsepublic.elsecmh.axf.import_textures import (
    ImportAxFTexturesParamsDTO,
    ImportAxFTexturesParamsSerializer,
)
from elsepublic.elsedam.interfaces.put_assets_operation import (
    PutAssetsOpInterface,
)
from elsecmh.operations.axf_operations.import_axf_textures.utils import (
    TextureExtractor,
    get_files_with_tagged_textures,
)


class ImportAxFTexturesOp(marshalling.ElseOperation):
    """
       Operation for import AxF textures.

       Attributes
       ----------
       expect_serializer_class : ImportAxFTexturesParamsSerializer
           Expect serializer.
       expose_serializer_class : None
           Expose serializer.
       """

    expect_serializer_class = ImportAxFTexturesParamsSerializer
    expose_serializer_class = None

    def __call__(self, params: ImportAxFTexturesParamsDTO, **context) -> None:
        """
               Parameters
               ----------
               params :
               elsepublic.elsecmh.dto.import_axf_textures.ImportAxFTexturesParamsDTO
                   Operation input parameters
               context : dict
                   context data
               Returns
               -------
               None
        """

        texture_extractor = TextureExtractor(params.file_name)
        tagged_textures_iterable = texture_extractor.extract_tagged_textures()
        tagged_files = get_files_with_tagged_textures(tagged_textures_iterable)
        material_revision_uuid = params.material_revision_uuid
        self.brand_id = params.brand_id

        put_to_dam_op = Router[PutAssetsOpInterface]
        assets = list(map(self._tagged_file2asset, tagged_files))
        put_to_dam_dto = PutAssetsParams(
            base_assets=assets,
            resource_type=ResourceTypes.MATERIAL_TEXTURE,
            initiator=f'update material {material_revision_uuid}',
        )
        put_to_dam_op(
            put_to_dam_dto,
            material_uuid=str(material_revision_uuid),
            **context,
        )

    def _tagged_file2asset(self, tagged_file):
        tag, out_file = tagged_file
        with open(os.path.abspath(out_file.name), 'rb') as file:
            asset = PutAssetParameters(
                filename=os.path.basename(file.name),
                tags=[AssetTags.TEXTURE, tag],
                brand_id=self.brand_id,
                file=file,
                temporary=False,
            )

        assert asset is not None

        return asset
