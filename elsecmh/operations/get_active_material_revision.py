from elsecmh.models import Material
from django.forms.models import model_to_dict

from elsecommon import marshalling
from elsepublic.elsecmh.dto.get_active_material_revision import (
    GetActiveMaterialRevisionParamsDTO,
    GetActiveMaterialRevisionResultDTO,
)
from elsepublic.elsecmh.serializers.get_active_material_revision import (
    GetActiveMaterialRevisionParamsSerializer,
    GetActiveMaterialRevisionResultSerializer,
)
from elsepublic.exceptions import (
    MissingMaterialException,
    MissingActiveMaterialRevisionException,
)
from elsepublic.elsecmh.dto.color import ColorDTO

class GetActiveMaterialRevisionOp(marshalling.ElseOperation):
    """
    Operation to get active material revision. If material with given name exists and has active revision,
    returns information about the revision. Otherwise, raises an error accordingly.

    Attributes
    ----------
    expect_serializer_class : elsepublic.elsecmh.serializers.get_active_material_revision.GetActiveMaterialRevisionParamsSerializer
        Expect serializer.
    expose_serializer_class : elsepublic.elsecmh.serializers.get_active_material_revision.GetActiveMaterialRevisionResultSerializer
        Expose serializer.

    Raises
    ------
    MissingMaterialException
        If the material passed as an argument does not exist.
    MissingActiveMaterialRevisionException
        If the material passed as an argument does not have active revision.
    """
    expect_serializer_class = GetActiveMaterialRevisionParamsSerializer
    expose_serializer_class = GetActiveMaterialRevisionResultSerializer

    def __call__(self, data: GetActiveMaterialRevisionParamsDTO, **context) -> GetActiveMaterialRevisionResultDTO:
        """
        Parameters
        ----------
        data : elsepublic.elsecmh.dto.get_active_material_revision.GetActiveMaterialRevisionParamsDTO
            Operation input parameters
        context : dict
            context data

        Returns
        -------
        elsepublic.elsecmh.dto.get_active_material_revision.GetActiveMaterialRevisionResultDTO
            Operation result object
        """
        material = Material.objects.filter(name=data.material_name).first()
        if not material:
            raise MissingMaterialException

        active_revision = material.active_revision
        if not active_revision:
            raise MissingActiveMaterialRevisionException

        colors = [ColorDTO(**color) for color in active_revision.colors.values()]

        return GetActiveMaterialRevisionResultDTO(
            revision_uuid=active_revision.uuid,
            material_name=material.name,
            material_info=active_revision.material_info,
            colors=colors,
            default_color=ColorDTO(**model_to_dict(active_revision.default_color)),
        )
