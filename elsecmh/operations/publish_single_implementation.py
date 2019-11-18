from elsecommon import marshalling
from elsecommon.transports.router import Router
import asyncio

from elsepublic.elsecmh.publish_single_implementation import (
    PublishSingleImplementationParams,
    PublishSingleImplementationParamsSerializer,
)

from elsepublic.elsecmh.create_preview.interface import AsyncCreatePreviewOpInterface
from elsepublic.elsecmh.create_html_for_b4w.interface import AsyncCreateHTMLForB4WOpInterface
from elsepublic.elsecmh.create_json_for_b4w.interface import AsyncCreateJSONForB4WOpInterface

from elsepublic.elsecmh.dto.create_json_for_b4w import CreateJSONForB4WParamsDTO
from elsepublic.elsecmh.dto.create_html_for_b4w import CreateHTMLForB4WParamsDTO
from elsepublic.elsecmh.dto.create_preview import CreatePreviewParamsDTO
from elsepublic.elserender.apply_color import (
    AsyncApplyColorParams,
    AsyncApplyColorOpInterface,
)

from elsecmh.models import (
    MaterialAsset,
    MaterialImplementationAsset,
    MaterialImplementation,
    MaterialRevision,
)
from elsepublic.exceptions import (
    NotPublishingRevisionException,
)
from elsepublic.helpers.asset_to_dto import asset_to_dto


class PublishSingleImplementationOp(marshalling.AsyncElseOperation):
    """
    Operation to publish one implementation of the revision.

    Attributes
    ----------
    expect_serializer_class : elsepublic.elsecmh.publish_single_implementation
    .PublishSingleImplementationParamsSerializer
        Expect serializer.

    Raises
    ------
    NotPublishingRevisionException
        If material revision is not being published.
    """
    expect_serializer_class = PublishSingleImplementationParamsSerializer

    async def __call__(self, data: PublishSingleImplementationParams, **context) -> None:
        """
        Parameters
        ----------
        data : elsepublic.elsecmh.publish_single_implementation.PublishSingleImplementationParams
            Operation input parameters
        context : dict
            context data
        """
        material_implementation = MaterialImplementation.objects.get(
            uuid=data.material_implementation_uuid,
        )

        material_revision = material_implementation.material_revision
        if material_revision.status != MaterialRevision.STATUS_PUBLISHING:
            raise NotPublishingRevisionException

        model_asset = material_revision.assets.filter(
            asset_type=MaterialAsset.MODEL_ASSET,
        ).first()

        apply_color_op = Router[AsyncApplyColorOpInterface]
        apply_color_params = AsyncApplyColorParams(
            dam_asset_info=asset_to_dto(model_asset),
            material_name=material_revision.material.name,
            color=material_implementation.color.value,
        )
        apply_result = await apply_color_op(apply_color_params)
        apply_result_asset = apply_result.result_asset

        MaterialImplementationAsset.objects.create(
            material_implementation=material_implementation,
            asset_type=MaterialImplementationAsset.MODEL_ASSET,
            dam_uuid=apply_result_asset.dam_uuid,
            filename=apply_result_asset.filename,
            size=apply_result_asset.size,
            extension=apply_result_asset.extension,
            brand_id=apply_result_asset.brand_id,
            url=apply_result_asset.url,
            state=apply_result_asset.state,
            resource_type=apply_result_asset.resource_type,
            meta_info=apply_result_asset.meta_info,
        )

        create_preview_op = Router[AsyncCreatePreviewOpInterface]
        create_preview_dto = CreatePreviewParamsDTO(
            uuid=material_implementation.uuid,
            camera=data.camera,
            settings=data.settings,
            environment=data.environment,
        )

        create_html_op = Router[AsyncCreateHTMLForB4WOpInterface]
        create_html_dto = CreateHTMLForB4WParamsDTO(
            material_implementation_uuid=material_implementation.uuid,
            camera=data.camera,
            environment=data.environment,
        )

        create_json_op = Router[AsyncCreateJSONForB4WOpInterface]
        create_json_dto = CreateJSONForB4WParamsDTO(
            material_implementation_uuid=material_implementation.uuid,
            camera=data.camera,
        )

        await asyncio.wait([
            create_preview_op(create_preview_dto, **context),
            create_html_op(create_html_dto, **context),
            create_json_op(create_json_dto, **context),
        ])
