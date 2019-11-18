from elsecommon import marshalling

from elsepublic.elsecmh.get_color import (
    GetColorParamsDTO,
    GetColorResultDTO,
    GetColorParamsSerializer,
    GetColorResultSerializer,
)

from elsecmh.models import Color


class GetColorOp(marshalling.ElseOperation):
    """
    Operation to get color.

    Attributes
    ----------
    expect_serializer_class : elsepublic.elsecmh.get_color.GetColorParamsSerializer
        Expect serializer.
    expose_serializer_class : elsepublic.elsecmh.get_color.GetColorResultSerializer
        Expose serializer.
    """
    expect_serializer_class = GetColorParamsSerializer
    expose_serializer_class = GetColorResultSerializer

    def __call__(self, data: GetColorParamsDTO, **context) -> GetColorResultDTO:
        """
        Parameters
        ----------
        data : elsepublic.elsecmh.get_color.GetColorParamsDTO
            Operation input parameters
        context : dict
            context data

        Returns
        -------
        elsepublic.elsecmh.get_color.GetColorResultDTO
            Operation result object
        """

        color = Color.objects.get(uuid=data.uuid)

        return GetColorResultDTO(
            uuid=color.uuid,
            name=color.name,
            color_group_uuid=color.color_group.uuid,
            color_space=color.color_space,
            value=color.value,
            description=color.description,
        )
