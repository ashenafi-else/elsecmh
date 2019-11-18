from elsecommon import marshalling
from elsecmh.models import (
    MaterialAsset,
    MaterialRevision,
)
from elsepublic.exceptions import MissingMaterialRevisionException
from elsepublic.dto.dam_asset_info import DamAssetsInfoDTO
from elsepublic.elsecmh.axf.import_preview import (
    ImportAxFPreviewResultDTO,
    ImportAxfPreviewResultSerializer,
)
from elsepublic.serializers.dam_asset_info import DamAssetsInfoSerializer


class ImportAxfPreviewHandler(marshalling.ElseOperation):
    """
        Handler for import AxF preview asset.

        Attributes
        ----------
        expect_serializer_class : DamAssetsInfoSerializer
            Expect serializer.
        expose_serializer_class : ImportAxfPreviewResultSerializer
            Expose serializer.
        """

    expect_serializer_class = DamAssetsInfoSerializer
    expose_serializer_class = ImportAxfPreviewResultSerializer

    def __call__(self, data: DamAssetsInfoDTO, **
                 context) -> ImportAxFPreviewResultDTO:
        material_uuid = context.get('material_uuid')
        dam_asset_info = data.dam_assets_info[0]
        material_revision = MaterialRevision.objects.get(pk=material_uuid)

        if not material_revision:
            raise MissingMaterialRevisionException

        asset = MaterialAsset.objects.create(
            material_revision=material_revision,
            asset_type=MaterialAsset.PREVIEW_ASSET,
            dam_uuid=dam_asset_info.dam_uuid,
            filename=dam_asset_info.filename,
            size=dam_asset_info.size,
            extension=dam_asset_info.extension,
            url=dam_asset_info.url,
            state=dam_asset_info.state,
            resource_type=dam_asset_info.resource_type,
            meta_info=dam_asset_info.meta_info,
            tags=dam_asset_info.tags,
        )

        result = ImportAxFPreviewResultDTO(
            asset_uuid=asset.uuid,
            **context)

        return result
