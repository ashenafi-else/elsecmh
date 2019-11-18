from elsecommon import marshalling
from elsecmh.models import (
    MaterialAsset,
    MaterialRevision,
)
from elsepublic.exceptions import (
    WrongFileExtensionException,
    ExistedMaterialAssetException,
    WrongAssetResourceTypeException,
    MissingMaterialRevisionException,
)
from elsecommon.transports.router import Router
from elsepublic.elsedam.resource_types import ResourceTypes
from elsepublic.elsedam.asset_extensions import AssetExtensions
from elsepublic.elsedam.buffering_assets.dto import PutAssetsToBufferParams
from elsepublic.elsecmh.dto.import_axf_meta_data import (
    ImportAxFMetaDataParamsDTO,
)
from elsepublic.elsecmh.serializers.import_axf_meta_data import (
    ImportAxFMetaDataParamsSerializer,
)
from elsepublic.elsedam.interfaces.put_assets_to_buffer_operation import (
    PutAssetsToBufferOpInterface,
)


class ImportAxFMetaDataOp(marshalling.ElseOperation):
    """
    Operation for import AxF meta data.

    Attributes
    ----------
    expect_serializer_class : ImportAxFMetaDataParamsDTO
        Expect serializer.
    expose_serializer_class : None
        Expose serializer.

    Raises
    ------
    MissingMaterialRevisionException
        If material revision does not exist.
    MissingMaterialAssetException
        If material revision does not have AxF asset.
    """
    expect_serializer_class = ImportAxFMetaDataParamsSerializer
    expose_serializer_class = None

    def __call__(self, data: ImportAxFMetaDataParamsDTO, **context) -> None:
        """
        Parameters
        ----------
        data : elsepublic.elsecmh.dto.import_axf_meta_data.ImportAxFMetaDataParamsDTO
            Operation input parameters
        context : dict
            context data
        Returns
        -------
        None
        """

        material_revision = MaterialRevision.objects.filter(
            uuid=data.material_revision_uuid,
        ).first()
        if not material_revision:
            raise MissingMaterialRevisionException
        dam_asset_info = data.dam_asset_info
        material_asset = material_revision.assets.filter(
            asset_type=MaterialAsset.AXF_ASSET,
        ).first()
        if material_asset:
            raise ExistedMaterialAssetException
        if dam_asset_info.extension != AssetExtensions.AXF:
            raise WrongFileExtensionException
        if dam_asset_info.resource_type != ResourceTypes.MATERIAL_AXF:
            raise WrongAssetResourceTypeException

        material_asset = MaterialAsset.objects.create(
            material_revision=material_revision,
            asset_type=MaterialAsset.AXF_ASSET,
            dam_uuid=dam_asset_info.dam_uuid,
            filename=dam_asset_info.filename,
            size=dam_asset_info.size,
            extension=dam_asset_info.extension,
            brand_id=dam_asset_info.brand_id,
            url=dam_asset_info.url,
            state=dam_asset_info.state,
            resource_type=dam_asset_info.resource_type,
            meta_info=dam_asset_info.meta_info,
            tags=dam_asset_info.tags,
        )
        put_buffer_asset_op = Router[PutAssetsToBufferOpInterface.uri]
        context['material_revision_uuid'] = material_revision.uuid
        put_buffer_asset_dto = PutAssetsToBufferParams(
            dam_asset_uuids=[material_asset.dam_uuid])
        put_buffer_asset_op(put_buffer_asset_dto, **context)
