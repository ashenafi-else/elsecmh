from elsecmh.models import MaterialGroup
from elsecommon import marshalling
from elsepublic.elsecmh.dto.remove_material_group import RemoveMaterialGroupParamsDTO
from elsepublic.elsecmh.serializers.remove_material_group import RemoveMaterialGroupParamsSerializer
from elsepublic.exceptions import MissingMaterialGroupException


class RemoveMaterialGroupOp(marshalling.ElseOperation):
    """
    Operation for remove material group.

    Attributes
    ----------
    expect_serializer_class : RemoveMaterialGroupParamsSerializer
        Expect serializer.
    expose_serializer_class : None
        Expose serializer.

    Raises
    ------
    MaterialExistsException
        If material instance already exists.
    """
    expect_serializer_class = RemoveMaterialGroupParamsSerializer
    expose_serializer_class = None

    def __call__(self, data: RemoveMaterialGroupParamsDTO, **context) -> None:
        """
        Parameters
        ----------
        data : elsepublic.elsecmh.dto.remove_material_group.RemoveMaterialGroupParamsDTO
            Operation input parameters
        context : dict
            context data
        Returns
        -------
        None
        """
        material_group = MaterialGroup.objects.filter(uuid=data.uuid).first()
        if not material_group:
            raise MissingMaterialGroupException
        material_group.delete()
