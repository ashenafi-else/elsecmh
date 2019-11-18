from elsecmh.models import (
    MaterialImplementation,
    MaterialRevision,
)
from elsecommon import marshalling
from elsepublic.elsecmh.dto.get_material_implementation import GetMaterialImplementationResultDTO
from elsepublic.elsecmh.serializers.get_material_implementation import GetMaterialImplementationResultSerializer

from elsepublic.elsecmh.dto.validate_material_revision import ValidateMaterialRevParamsDTO
from elsepublic.elsecmh.serializers.validate_material_revision import ValidateMaterialRevParamsSerializer


class PublishMaterialRevisionSuccessHandler(marshalling.ElseOperation):
    """
    Handler which responds to publish material revision operation. It sets revision status to published
    and updates corresponding material's active revision.

    Attributes
    ----------
    expect_serializer_class : elsepublic.elsecmh.serializers.get_material_implementation.GetMaterialImplementationResultSerializer
        Expect serializer.
    expose_serializer_class : elsepublic.elsecmh.serializers.validate_material_revision.ValidateMaterialRevParamsSerializer
        Expose serializer.
    """
    expect_serializer_class = GetMaterialImplementationResultSerializer
    expose_serializer_class = ValidateMaterialRevParamsSerializer

    def __call__(self, data: GetMaterialImplementationResultDTO, **context) -> ValidateMaterialRevParamsDTO:
        """
        Parameters
        ----------
        data : elsepublic.elsedam.dto.put_assets_operation.PutAssetsResult
            Operation input parameters
        context : dict
            context data

        Returns
        -------
        elsepublic.elsecmh.dto.validate_material_revision.ValidateMaterialRevParamsDTO
            Operation output result.
        """
        material_revision = MaterialImplementation.objects.get(uuid=data.uuid).material_revision
        material_revision.status = MaterialRevision.STATUS_PUBLISHED
        material_revision.save(update_fields=['status'])
        material_revision.material.active_revision = material_revision
        material_revision.material.save()

        return ValidateMaterialRevParamsDTO(uuid=material_revision.uuid)
