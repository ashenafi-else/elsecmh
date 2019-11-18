from elsecmh.models import MaterialGroup
from elsecommon import marshalling
from elsepublic.exceptions import MissingMaterialGroupException
from elsepublic.elsecmh.dto.create_material_group import (
    CreateMaterialGroupParamsDTO,
    CreateMaterialGroupResultDTO,
)
from elsepublic.elsecmh.serializers.create_material_group import (
    CreateMaterialGroupParamsSerializer,
    CreateMaterialGroupResultSerializer,
)


class CreateMaterialGroupOp(marshalling.ElseOperation):
    """
    Operation for create material group instance.

    Attributes
    ----------
    expect_serializer_class : CreateMaterialGroupParamsSerializer
        Expect serializer.
    expose_serializer_class : CreateMaterialGroupResultSerializer
        Expose serializer.

    Raises
    ------
    MaterialExistsException
        If material instance already exists.
    """
    expect_serializer_class = CreateMaterialGroupParamsSerializer
    expose_serializer_class = CreateMaterialGroupResultSerializer

    def __call__(self, data: CreateMaterialGroupParamsDTO, **context) -> CreateMaterialGroupResultDTO:
        """
        Parameters
        ----------
        data : elsepublic.elsecmh.dto.create_material_group.CreateMaterialGroupParamsDTO
            Operation input parameters
        context : dict
            context data
        Returns
        -------
        elsepublic.elsecmh.dto.create_material_group.CreateMaterialGroupResultDTO
            Operation result object
        """
        if not data.parent_uuid:
            material_group = MaterialGroup.add_root(name=data.name)
        else:
            parent_group = MaterialGroup.objects.filter(uuid=data.parent_uuid).first()
            if not parent_group:
                raise MissingMaterialGroupException
            material_group = parent_group.add_child(name=data.name)
        return CreateMaterialGroupResultDTO(
            uuid=material_group.uuid,
            name=material_group.name,
            parent_uuid=material_group.get_parent().uuid if data.parent_uuid else None,
        )
