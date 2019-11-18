from elsecommon import marshalling

from elsepublic.elsecmh.create_color import (
    CreateColorParamsDTO,
    CreateColorResultDTO,
    CreateColorParamsSerializer,
    CreateColorResultSerializer,
)

from elsecmh.models import (
    ColorGroup,
    Color,
)


class CreateColorOp(marshalling.ElseOperation):
    """
    Operation to create color.

    Attributes
    ----------
    expect_serializer_class : elsepublic.elsecmh.create_color.CreateColorParamsSerializer
        Expect serializer.
    expose_serializer_class : elsepublic.elsecmh.create_color.CreateColorResultSerializer
        Expose serializer.
    """
    expect_serializer_class = CreateColorParamsSerializer
    expose_serializer_class = CreateColorResultSerializer

    def __call__(self, data: CreateColorParamsDTO, **context) -> CreateColorResultDTO:
        """
        Parameters
        ----------
        data : elsepublic.elsecmh.create_color.CreateColorParamsDTO
            Operation input parameters
        context : dict
            context data

        Returns
        -------
        elsepublic.elsecmh.create_color.CreateColorResultDTO
            Operation result object
        """
        color_group = ColorGroup.objects.get(uuid=data.color_group_uuid)

        color = Color.objects.create(
            name=data.name,
            color_group=color_group,
            color_space=data.color_space,
            value=data.value,
            description=data.description,
        )

        return CreateColorResultDTO(
            uuid=color.uuid,
            name=color.name,
            color_group_uuid=color.color_group.uuid,
        )
