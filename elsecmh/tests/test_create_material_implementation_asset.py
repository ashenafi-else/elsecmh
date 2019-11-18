import os

from elsecmh.services.create_material_implementation_asset import create_material_implementation_asset
from elsecmh.tests.test_base_cmh import TestBaseCmh
from elsepublic.dto.dam_asset_info import (
    DamAssetsInfoDTO,
    DamAssetInfoDTO,
)
from elsepublic.elsecmh.dto.get_material_implementation import GetMaterialImplementationResultDTO

from elsepublic.elsedam.resource_types import ResourceTypes
from elsepublic.elsedam.asset_extensions import AssetExtensions
from elsecmh.models import (
    MaterialImplementation,
    MaterialRevision,
    Material,
    MaterialImplementationAsset,
)


class TestRenderFrameExportB4WService(TestBaseCmh):
    test_path = os.path.dirname(os.path.realpath(__file__))
    fixtures_path = os.path.join(test_path, 'fixtures')

    def setUp(self):
        super().setUp()
        material = Material.objects.create(name='material', material_group=self.root)
        self.material_revision1 = MaterialRevision.objects.create(material=material, material_info='')
        self.material_implementation1 = MaterialImplementation.objects.create(material_revision=self.material_revision1)
        self.material_implementation_with_all_asset_types = MaterialImplementation.objects.create(
            material_revision=self.material_revision1,
        )
        common_data = dict(
            dam_uuid='642bbbe6-d21b-11e8-a8d5-f2801f1b9fc1',
            filename='exported_model',
            size=10,
            brand_id='1',
            url='http://url.else',
            state='test_state',
            resource_type=ResourceTypes.RENDER_RESULT,
            meta_info='',
        )
        MaterialImplementationAsset.objects.create(
            material_implementation=self.material_implementation_with_all_asset_types,
            asset_type=MaterialImplementationAsset.HTML_ASSET,
            extension=AssetExtensions.HTML,
            **common_data,
        )
        MaterialImplementationAsset.objects.create(
            material_implementation=self.material_implementation_with_all_asset_types,
            asset_type=MaterialImplementationAsset.JSON_ASSET,
            extension=AssetExtensions.JSON,
            **common_data,
        )
        MaterialImplementationAsset.objects.create(
            material_implementation=self.material_implementation_with_all_asset_types,
            asset_type=MaterialImplementationAsset.MODEL_ASSET,
            extension=AssetExtensions.JSON,
            **common_data,
        )
        self.context = dict(
            material_implementation_uuid=self.material_implementation1.uuid,
            asset_type=MaterialImplementationAsset.PREVIEW_ASSET,
        )
        self.final_context = dict(
            material_implementation_uuid=self.material_implementation_with_all_asset_types.uuid,
            asset_type=MaterialImplementationAsset.PREVIEW_ASSET,
        )
        self.dto = DamAssetsInfoDTO(
            dam_assets_info=[
                DamAssetInfoDTO(
                    dam_uuid='642bbbe6-d21b-11e8-a8d5-f2801f1b9fc1',
                    filename='exported_model',
                    size=10,
                    extension=AssetExtensions.JSON,
                    brand_id='1',
                    url='http://url.else',
                    state='test_state',
                    resource_type=ResourceTypes.RENDER_RESULT,
                    meta_info='',
                ),
                DamAssetInfoDTO(
                    uuid='642bbbe6-d21b-11e8-a8d5-f2801f1b9fc2',
                    filename='exported_model2',
                    size=10,
                    extension=AssetExtensions.HTML,
                    brand_id='1',
                    url='http://url.else',
                    state='test_state',
                    resource_type=ResourceTypes.RENDER_RESULT,
                    meta_info='test',
                ),
            ],
        )

    def test_create_material_implementation_asset(self):
        """
        Test create material implementation asset
        """
        service_result = create_material_implementation_asset(self.dto, **self.context)
        self.assertIsNone(service_result)

    def test_create_material_implementation_asset_final(self):
        """
        Test create material implementation asset final
        """
        service_result = create_material_implementation_asset(self.dto, **self.final_context)
        self.assertIsInstance(service_result, GetMaterialImplementationResultDTO)
        self.assertEqual(service_result.uuid, self.final_context['material_implementation_uuid'])
