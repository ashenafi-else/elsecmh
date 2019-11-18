from elsecommon import marshalling
from elsecommon.transports.router import Router

from elsepublic.elsecmh.publish_material_revision import (
    PublishMaterialRevisionParamsSerializer,
    PublishMaterialRevisionParamsDTO,
)

from elsepublic.elsecmh.interfaces.create_preview import CreatePreviewOpInterface
from elsepublic.elsecmh.interfaces.create_html_for_b4w import CreateHTMLForB4WOpInterface
from elsepublic.elsecmh.interfaces.create_json_for_b4w import CreateJSONForB4WOpInterface

from elsepublic.elsecmh.dto.create_json_for_b4w import CreateJSONForB4WParamsDTO
from elsepublic.elsecmh.dto.create_html_for_b4w import CreateHTMLForB4WParamsDTO
from elsepublic.elsecmh.dto.create_preview import CreatePreviewParamsDTO

from elsecmh.models import (
    MaterialAsset,
    MaterialRevision,
    MaterialImplementationAsset,
)
from elsepublic.exceptions import (
    MissingMaterialRevisionException,
    NotValidatedRevisionException,
)
from elsecmh.operations.publish_material_revision.utils import get_default_color_implementation


class PublishMaterialRevisionOp(marshalling.ElseOperation):
    """
    Operation to publish material revision.

    Attributes
    ----------
    expect_serializer_class : elsepublic.elsecmh.serializers.publish_material_revision.PublishMaterialRevisionParamsSerializer
        Expect serializer.

    Raises
    ------
    MissingMaterialRevisionException
        If material revision does not exist.
    NotValidatedRevisionException
        If the status of revision is not validated.
    """
    expect_serializer_class = PublishMaterialRevisionParamsSerializer

    def __call__(self, data: PublishMaterialRevisionParamsDTO, **context) -> None:
        """
        Parameters
        ----------
        data : elsepublic.elsecmh.dto.publish_material_revision.PublishMaterialRevisionParamsDTO
            Operation input parameters
        context : dict
            context data

        Returns
        -------
        None
        """
        material_revision = MaterialRevision.objects.filter(uuid=data.material_revision_uuid).first()
        if not material_revision:
            raise MissingMaterialRevisionException

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
        material_implementation = get_default_color_implementation(material_revision)

        model_asset = material_revision.assets.filter(asset_type=MaterialAsset.MODEL_ASSET).first()
        MaterialImplementationAsset.objects.create(
            material_implementation=material_implementation,
            asset_type=MaterialImplementationAsset.MODEL_ASSET,
            dam_uuid=model_asset.dam_uuid,
            filename=model_asset.filename,
            size=model_asset.size,
            extension=model_asset.extension,
            brand_id=model_asset.brand_id,
            url=model_asset.url,
            state=model_asset.state,
            resource_type=model_asset.resource_type,
            meta_info=model_asset.meta_info,
        )

        create_preview_op = Router[CreatePreviewOpInterface.uri]
        create_preview_dto = CreatePreviewParamsDTO(
            uuid=material_implementation.uuid,
            camera=data.camera,
            settings=data.settings,
            environment=data.environment,
        )
        create_preview_op(create_preview_dto, **context)

        create_html_op = Router[CreateHTMLForB4WOpInterface.uri]
        create_html_dto = CreateHTMLForB4WParamsDTO(
            material_implementation_uuid=material_implementation.uuid,
            camera=data.camera,
            environment=data.environment,
        )
        create_html_op(create_html_dto, **context)

        create_json_op = Router[CreateJSONForB4WOpInterface.uri]
        create_json_dto = CreateJSONForB4WParamsDTO(
            material_implementation_uuid=material_implementation.uuid,
            camera=data.camera,
        )
        create_json_op(create_json_dto, **context)
