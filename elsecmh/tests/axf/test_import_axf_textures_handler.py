from elsecmh.models import (
    Material,
    MaterialAsset,
    MaterialRevision,
)
from elsecmh.tests.test_base_cmh import TestBaseCmh
from elsepublic.dto.dam_asset_info import (
    DamAssetInfoDTO,
    DamAssetsInfoDTO,
)
from elsepublic.elsedam.asset_tags import AssetTags
from elsepublic.elsedam.put_assets import DamAssetBatchDTO
from elsepublic.elsedam.resource_types import ResourceTypes
from elsepublic.elsedam.asset_extensions import AssetExtensions
from elsecmh.operations.axf_operations.import_axf_textures import (
    ImportAxfTexturesHandler,
)


class TestImportAxFTexturesHandler(TestBaseCmh):

    def setUp(self):
        super().setUp()
        material = Material.objects.create(
            name='existed_material', material_group=self.root)
        self.material_revision = MaterialRevision.objects.create(
            material=material, material_info={})
        self.dam_asset_info = DamAssetInfoDTO(
            dam_uuid='642bbbe6-d21b-11e8-a8d5-f2801f1b9fc1',
            filename='texture roughness',
            size=10,
            extension=AssetExtensions.JPG,
            brand_id='13',
            url='http://url.else',
            state='test_state',
            resource_type=ResourceTypes.MATERIAL_TEXTURE,
            meta_info='',
            tags=(AssetTags.TEXTURE, AssetTags.TEXTURE_ROUGHNESS)
        )
        self.dam_assets_info_dto = DamAssetsInfoDTO(
            dam_assets_info=[self.dam_asset_info],
            dam_asset_batch=DamAssetBatchDTO(
                resource_type=ResourceTypes.MATERIAL_TEXTURE,
                uuid='642bbbe6-d21b-11e8-a8d5-f2801f1b9fc1',
                initiator='init',
                description='axf textures',
            ),
        )
        self.context = dict(
            material_uuid=str(self.material_revision.uuid)
        )

    def test_import_axf_textures_handler(self):
        """
        Test import axf textures handler
        """
        import_op_handler = ImportAxfTexturesHandler()
        self.assertIsNotNone(import_op_handler)

        import_result = import_op_handler(
            self.dam_assets_info_dto, **self.context)
        asset_uuid = import_result.assets_uuids[0]
        self.assertIsNotNone(asset_uuid)
        asset = MaterialAsset.objects.get(pk=asset_uuid)
        self.assertIsNotNone(asset)
        self.assertEqual(asset.asset_type, MaterialAsset.TEXTURE_ASSET)
        self.assertEqual(asset.material_revision, self.material_revision)
        self.assertEqual(str(asset.dam_uuid), self.dam_asset_info.dam_uuid)
        self.assertEqual(asset.tags, self.dam_asset_info.tags)
