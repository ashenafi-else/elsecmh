from elsecommon import marshalling
from elsecommon.transports.router import Router
from elsepublic.dto.dam_asset_info import DamAssetInfoDTO
from elsepublic.elsecmh.dto.validate_material_revision import ValidateMaterialRevParamsDTO
from elsepublic.elsecmh.serializers.validate_material_revision import ValidateMaterialRevParamsSerializer
from elsepublic.elserender.dto.validate_file import ValidateFileParamsDTO
from elsepublic.elserender.interfaces.validate_file import ValidateFileOpInterface
from elsepublic.exceptions import (
    MissingMaterialRevisionException,
    MissingMaterialAssetException,
)
from elsecmh.models import (
    MaterialRevision,
    MaterialAsset,
)


class ValidateMaterialRevisionOp(marshalling.ElseOperation):
    """
    Operation for validate material revision.

    Attributes
    ----------
    expect_serializer_class : elsepublic.elsecmh.serializers.validate_material_revision.ValidateMaterialRevParamsSerializer
        Expect serializer.
    expose_serializer_class : None
        Expose serializer.

    Raises
    ------
    MissingMaterialRevisionException
        If material revision does not exist.
    MissingMaterialAssetException
        If material revision does not have model asset.
    """
    expect_serializer_class = ValidateMaterialRevParamsSerializer
    expose_serializer_class = None

    def __call__(self, data: ValidateMaterialRevParamsDTO, **context) -> None:
        """
        Parameters
        ----------
        data : elsepublic.elsecmh.dto.validate_material_revision.ValidateMaterialRevParamsSerializer
            Operation input parameters
        context : dict
            context data
        Returns
        -------
        None
        """
        material_revision = MaterialRevision.objects.filter(uuid=data.uuid).first()
        if not material_revision:
            raise MissingMaterialRevisionException
        asset = material_revision.assets.filter(asset_type=MaterialAsset.MODEL_ASSET).first()
        if not asset:
            raise MissingMaterialAssetException

        validate_file_op = Router[ValidateFileOpInterface.uri]
        validate_file_dto = ValidateFileParamsDTO(
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
            ))
        context['material_revision_uuid'] = str(material_revision.uuid)
        material_revision.status = MaterialRevision.STATUS_VALIDATING
        material_revision.save()
        validate_file_op(validate_file_dto, **context)
