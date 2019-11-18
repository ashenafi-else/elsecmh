from elsecmh.models import (
    MaterialImplementation,
    Material,
    MaterialRevision,
)
from elsecommon.transports.router import Router

from elsecommon import marshalling
from elsepublic.elsecmh.dto.get_material import GetMaterialParamsDTO
from elsepublic.elsecmh.dto.get_material_implementation import GetMaterialImplementationParamsDTO
from elsepublic.elsecmh.dto.publish_existed_material import PublishExistedMaterialParamsDTO
from elsepublic.elsecmh.interfaces.get_material_implementation import GetMaterialImplementationOpInterface
from elsepublic.elsecmh.interfaces.publish_existed_material import PublishExistedMaterialOpInterface
from elsepublic.elsecmh.serializers.get_material import GetMaterialParamsSerializer
from elsepublic.exceptions import MissingMaterialException


class GetMaterialOp(marshalling.ElseOperation):
    """
    Operation to get material implementation. If material implementation with input color_name
    exists it will call operation to return it, else it will check if the material with mat name
    exists and if input color is available and then call operation to publish existed material.

    Attributes
    ----------
    expect_serializer_class : elsepublic.elsecmh.serializers.get_material.GetMaterialParamsSerializer
        Expect serializer.

    Raises
    ------
    NotAvailableColorException
        If material color is not included in material_info available_colors
    MissedPublishedMaterialRevisionException
        If material with color does not exist 
    """
    expect_serializer_class = GetMaterialParamsSerializer

    def __call__(self, data: GetMaterialParamsDTO, **context) -> None:
        """
        Parameters
        ----------
        data : elsepublic.elsecmh.dto.get_material.GetMaterialParamsDTO
            Operation input parameters
        context : dict
            context data

        Returns
        -------
        None
        """
        color_name = data.color_name
        material_implementation = MaterialImplementation.objects.filter(
            name=color_name,
            material_revision__status=MaterialRevision.STATUS_PUBLISHED
        ).first()
        if material_implementation:
            get_material_op = Router[GetMaterialImplementationOpInterface.uri]
            get_material_dto = GetMaterialImplementationParamsDTO(uuid=material_implementation.uuid)
            get_material_op(get_material_dto, **context)
        else:
            *material_name_list, color_code = color_name.split('_')
            material_name = '_'.join(material_name_list)
            material = Material.objects.filter(
                name=material_name,
                active_revision__status=MaterialRevision.STATUS_PUBLISHED,
                active_revision__material_info__available_colors__contains=[color_code]
            ).first()
            if not material:
                raise MissingMaterialException
            publish_material_op = Router[PublishExistedMaterialOpInterface.uri]
            publish_material_dto = PublishExistedMaterialParamsDTO(
                uuid=material.active_revision.uuid,
                color=color_name,
            )
            publish_material_op(publish_material_dto, **context)
