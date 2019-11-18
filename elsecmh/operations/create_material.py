from elsecmh.models import (
    Material,
    MaterialGroup,
    Brand,
)
from elsecommon import marshalling
from elsepublic.elsecmh.create_material.dto import (
    CreateMaterialParamsDTO,
    CreateMaterialResultDTO,
)
from elsepublic.elsecmh.create_material.serializer import (
    CreateMaterialParamsSerializer,
    CreateMaterialResultSerializer,
)
from elsepublic.exceptions import MaterialExistsException


class CreateMaterialOp(marshalling.ElseOperation):
    """
    Operation for create material instance.
    
    Attributes
    ----------
    expect_serializer_class : CreateMaterialParamsSerializer
        Expect serializer.
    expose_serializer_class : CreateMaterialResultSerializer
        Expose serializer.

    Raises
    ------
    MaterialExistsException
        If material instance already exists.
    """
    expect_serializer_class = CreateMaterialParamsSerializer
    expose_serializer_class = CreateMaterialResultSerializer

    def __call__(self, data: CreateMaterialParamsDTO, **context) -> CreateMaterialResultDTO:
        """
        Parameters
        ----------
        data : elsepublic.elsecmh.dto.create_material.CreateMaterialParamsDTO
            Operation input parameters
        context : dict
            context data
        Returns
        -------
        elsepublic.elsecmh.dto.create_material.CreateMaterialResultDTO
            Operation result object
        """
        material_group = MaterialGroup.objects.get(uuid=data.material_group_uuid)
        brand = Brand.objects.get(brand_external_id=data.brand_uuid)
        material, created = Material.objects.get_or_create(name=data.name, material_group=material_group, brand=brand)
        if not created:
            raise MaterialExistsException
        return CreateMaterialResultDTO(
            uuid=material.uuid,
            name=material.name,
            material_group_uuid=material.material_group.uuid,
        )
