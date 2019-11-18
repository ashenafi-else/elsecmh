from elsecommon import marshalling

from elsepublic.elsecmh.update_color import (
    UpdateColorParamsDTO,
    UpdateColorResultDTO,
    UpdateColorParamsSerializer,
    UpdateColorResultSerializer,
)

from elsecmh.models import (
    ColorGroup,
    Color,
)


class UpdateColorOp(marshalling.ElseOperation):
    """
    Operation to update color.

    Attributes
    ----------
    expect_serializer_class : elsepublic.elsecmh.update_color.UpdateColorParamsSerializer
        Expect serializer.
    expose_serializer_class : elsepublic.elsecmh.update_color.UpdateColorResultSerializer
        Expose serializer.
    """
    expect_serializer_class = UpdateColorParamsSerializer
    expose_serializer_class = UpdateColorResultSerializer

    def __call__(self, data: UpdateColorParamsDTO, **context) -> UpdateColorResultDTO:
        """
        Parameters
        ----------
        data : elsepublic.elsecmh.update_color.UpdateColorParamsDTO
            Operation input parameters
        context : dict
            context data

        Returns
        -------
        elsepublic.elsecmh.update_color.UpdateColorResultDTO
            Operation result object
        """
        color = Color.objects.get(uuid=data.color_uuid)

        if data.name:
            color.name = data.name
        if data.color_space:
            color.color_space = data.color_space
        if data.value:
            color.value = data.value
        if data.description is not None:
            color.description = data.description
        if data.color_group_uuid:
            color.color_group = ColorGroup.objects.get(
                uuid=data.color_group_uuid,
            )

        color.save()

        return UpdateColorResultDTO(
            uuid=color.uuid,
            name=color.name,
            color_group_uuid=color.color_group.uuid,
        )
