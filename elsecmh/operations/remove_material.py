from elsecmh.models import Material

from elsecommon import marshalling
from elsepublic.exceptions import MaterialExistsException
from elsepublic.elsecmh.dto.remove_material import RemoveMaterialParamsDTO
from elsepublic.elsecmh.serializers.remove_material import RemoveMaterialParamsSerializer


class RemoveMaterialOp(marshalling.ElseOperation):
    """
    Operation for remove material instance.

    Attributes
    ----------
    expect_serializer_class : RemoveMaterialParamsSerializer
        Expect serializer.
    expose_serializer_class : None
        Expose serializer.

    Raises
    ------
    MaterialExistsException
        If material instance does not exist.
    """
    expect_serializer_class = RemoveMaterialParamsSerializer
    expose_serializer_class = None

    def __call__(self, data: RemoveMaterialParamsDTO, **context) -> None:
        """
        Parameters
        ----------
        data : elsepublic.elsecmh.dto.remove_material.RemoveMaterialParamsDTO
            Operation input parameters
        context : dict
            context data
        Returns
        -------
        None
        """
        material = Material.objects.filter(uuid=data.uuid).first()
        if not material:
            raise MaterialExistsException
        material.delete()

