from elsecommon import marshalling
from elsepublic.elsecmh.dto.get_material_implementation import (
    GetMaterialImplementationParamsDTO,
    GetMaterialImplementationResultDTO,
)
from elsepublic.elsecmh.serializers.get_material_implementation import (
    GetMaterialImplementationParamsSerializer,
    GetMaterialImplementationResultSerializer,
)


class GetMaterialImplementationOp(marshalling.ElseOperation):
    """
    Operation to get material implementation. This operation is created for handler purpose. 

    Attributes
    ----------
    expect_serializer_class : elsepublic.elsecmh.dto.get_material_implementation.GetMaterialImplementationParamsSerializer
        Expect serializer.
    expose_serializer_class : elsepublic.elsecmh.dto.get_material_implementation.GetMaterialImplementationResultSerializer
        Expose serializer.
    """
    expect_serializer_class = GetMaterialImplementationParamsSerializer
    expose_serializer_class = GetMaterialImplementationResultSerializer

    def __call__(self, data: GetMaterialImplementationParamsDTO, **context) -> GetMaterialImplementationResultDTO:
        """
        Parameters
        ----------
        data : elsepublic.elsecmh.dto.get_material.GetMaterialParamsDTO
            Operation input parameters
        context : dict
            context data

        Returns
        -------
        elsepublic.elsecmh.dto.get_material_implementation.GetMaterialImplementationResultDTO
            Operation result object
        """
        return GetMaterialImplementationResultDTO(uuid=data.uuid)

