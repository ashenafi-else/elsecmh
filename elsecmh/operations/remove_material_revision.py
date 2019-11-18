from elsecmh.models import MaterialRevision
from elsecommon import marshalling

from elsepublic.elsecmh.dto.remove_material_revision import RemoveMaterialRevParamsDTO
from elsepublic.elsecmh.serializers.remove_material_revision import RemoveMaterialRevParamsSerializer
from elsepublic.exceptions import MissingMaterialRevisionException


class RemoveMaterialRevisionOp(marshalling.ElseOperation):
    """
    Operation for remove material revision.

    Attributes
    ----------
    expect_serializer_class : RemoveMaterialRevParamsSerializer
        Expect serializer.
    expose_serializer_class : None
        Expose serializer.

    Raises
    ------
    MaterialExistsException
        If material instance already exists.
    """
    expect_serializer_class = RemoveMaterialRevParamsSerializer
    expose_serializer_class = None

    def __call__(self, data: RemoveMaterialRevParamsDTO, **context) -> None:
        """
        Parameters
        ----------
        data : elsepublic.elsecmh.dto.remove_material_revision.RemoveMaterialRevisionParamsDTO
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
        material_revision.delete()
