from elsecommon import marshalling

from elsepublic.elsecmh.delete_color import (
    DeleteColorParamsDTO,
    DeleteColorParamsSerializer,
)

from elsecmh.models import Color


class DeleteColorOp(marshalling.ElseOperation):
    """
    Operation to delete color.

    Attributes
    ----------
    expect_serializer_class : elsepublic.elsecmh.delete_color.DeleteColorParamsSerializer
        Expect serializer.
    """
    expect_serializer_class = DeleteColorParamsSerializer

    def __call__(self, data: DeleteColorParamsDTO, **context) -> None:
        """
        Parameters
        ----------
        data : elsepublic.elsecmh.delete_color.DeleteColorParamsDTO
            Operation input parameters
        context : dict
            context data
        """
        Color.objects.get(uuid=data.uuid).delete()
