import asyncio

from elsepublic.elsecmh.publish_single_implementation import (
    PublishSingleImplementationParams,
    PublishSingleImplementationOpInterface,
)
from elsepublic.elsecmh.dto.validate_material_revision import ValidateMaterialRevParamsDTO

from elsecommon import marshalling
from elsecommon.transports.router import Router

from elsepublic.elsecmh.publish_material_revision import (
    PublishMaterialRevisionParamsSerializer,
    PublishMaterialRevisionParamsDTO,
)
from elsepublic.elsecmh.serializers.validate_material_revision import ValidateMaterialRevParamsSerializer

from elsecmh.models import (
    MaterialAsset,
    MaterialRevision,
)
from elsepublic.exceptions import NotValidatedRevisionException


class AsyncPublishMaterialRevisionOp(marshalling.AsyncElseOperation):
    """
    Asynchronous operation to publish material revision.

    Attributes
    ----------
    expect_serializer_class : lsepublic.elsecmh.publish_material_revision
    .PublishMaterialRevisionParamsSerializer
        Expect serializer.
    expose_serializer_class : elsepublic.elsecmh.serializers.validate_material_revision.ValidateMaterialRevParamsSerializer
        Expose serializer.

    Raises
    ------
    NotValidatedRevisionException
        If the status of revision is not validated.
    """
    expect_serializer_class = PublishMaterialRevisionParamsSerializer
    expose_serializer_class = ValidateMaterialRevParamsSerializer

    async def __call__(self, data: PublishMaterialRevisionParamsDTO, **context) -> ValidateMaterialRevParamsDTO:
        """
        Parameters
        ----------
        data : lsepublic.elsecmh.publish_material_revision.PublishMaterialRevisionParamsDTO
            Operation input parameters
        context : dict
            context data

                Returns
        -------
        elsepublic.elsecmh.dto.validate_material_revision.ValidateMaterialRevParamsDTO
            Operation output result.
        """
        material_revision = MaterialRevision.objects.get(uuid=data.material_revision_uuid)

        if material_revision.status != MaterialRevision.STATUS_VALIDATED:
            raise NotValidatedRevisionException

        material_revision.status = MaterialRevision.STATUS_PUBLISHING
        material_revision.save(update_fields=['status'])

        MaterialAsset.objects.create(
            material_revision=material_revision,
            asset_type=MaterialAsset.SETTINGS_ASSET,
            **vars(data.settings),
        )
        MaterialAsset.objects.create(
            material_revision=material_revision,
            asset_type=MaterialAsset.ENVIRONMENT_ASSET,
            **vars(data.environment),
        )

        publish_implementation_op = Router[PublishSingleImplementationOpInterface]
        publish_implementation_params = []
        for implementation in material_revision.implementations:
            publish_implementation_params.append(
                PublishSingleImplementationParams(
                    material_implementation_uuid=implementation.uuid,
                    camera=data.camera,
                    environment=data.environment,
                    settings=data.settings,
                ),
            )

        await asyncio.wait(
            [publish_implementation_op(params)
             for params in publish_implementation_params],
        )

        material_revision.status = MaterialRevision.STATUS_PUBLISHED
        material_revision.save(update_fields=['status'])
        material_revision.material.active_revision = material_revision
        material_revision.material.save()

        return ValidateMaterialRevParamsDTO(uuid=material_revision.uuid)
