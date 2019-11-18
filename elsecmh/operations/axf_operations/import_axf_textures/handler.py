from elsecommon import marshalling
from elsecmh.models import (
    MaterialAsset,
    MaterialRevision,
)
from elsepublic.exceptions import MissingMaterialRevisionException
from elsepublic.dto.dam_asset_info import DamAssetsInfoDTO
from elsepublic.serializers.dam_asset_info import DamAssetsInfoSerializer
from elsepublic.elsecmh.axf.import_textures import (
    ImportAxFTexturesResultDTO,
    ImportAxfTexturesResultSerializer,
)


class ImportAxfTexturesHandler(marshalling.ElseOperation):
    """
        Handler for import AxF textures asset.

        Attributes
        ----------
        expect_serializer_class : DamAssetsInfoSerializer
            Expect serializer.
        expose_serializer_class : ImportAxfTexturesResultSerializer
            Expose serializer.
        """

    expect_serializer_class = DamAssetsInfoSerializer
    expose_serializer_class = ImportAxfTexturesResultSerializer

    def __call__(self, data: DamAssetsInfoDTO, **
                 context) -> ImportAxFTexturesResultDTO:
        material_uuid = context.get('material_uuid')
        self.material_revision = MaterialRevision.objects.get(pk=material_uuid)

        if not self.material_revision:
            raise MissingMaterialRevisionException
        assets = list(map(self._dam_asset_info2asset, data.dam_assets_info))
        assets_uuids = list(map(lambda x: x.uuid, assets))

        result = ImportAxFTexturesResultDTO(
            assets_uuids=assets_uuids,
            **context)

        return result

    def _dam_asset_info2asset(self, dam_asset_info) -> MaterialAsset:
        asset = MaterialAsset.objects.create(
            material_revision=self.material_revision,
            asset_type=MaterialAsset.TEXTURE_ASSET,
            dam_uuid=dam_asset_info.dam_uuid,
            filename=dam_asset_info.filename,
            size=dam_asset_info.size,
            extension=dam_asset_info.extension,
            brand_id=dam_asset_info.brand_id,
            url=dam_asset_info.url,
            state=dam_asset_info.state,
            resource_type=dam_asset_info.resource_type,
            meta_info=dam_asset_info.meta_info,
            tags=dam_asset_info.tags,
        )

        return asset
