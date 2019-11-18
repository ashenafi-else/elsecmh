import os

from elsecmh.models import (
    Material,
    MaterialRevision,
    MaterialImplementation,
    MaterialImplementationAsset,
)
from elsecmh.operations.get_material.get_material_implementation_success import GetMaterialImplementationSuccessHandler
from elsecmh.tests.test_base_cmh import TestBaseCmh
from elsepublic.elsecmh.dto.get_material_implementation import GetMaterialImplementationResultDTO
from elsepublic.elsecmh.dto.material_implementation import MaterialImplementationDTO


class TestGetMaterialImplementationSuccessHandler(TestBaseCmh):
    test_path = os.path.dirname(os.path.realpath(__file__))
    fixtures_path = os.path.join(test_path, '..', 'fixtures')
    fixtures_models_path = os.path.join(test_path, '..', 'fixtures', 'common_test_data.json')
    fixtures_implementation_models_path = os.path.join(test_path, '..', 'fixtures', 'material_implementation_data.json')
    fixtures = (fixtures_models_path, fixtures_implementation_models_path)

    def setUp(self):
        super().setUp()
        self.material = Material.objects.get(uuid='642bbbe6-d21b-11e8-a8d5-f2801f1b9fa0')
        self.material_revision = MaterialRevision.objects.get(uuid='642bbbe6-d21b-11e8-a8d5-f2801f1b9fb0')
        self.material.active_revision = self.material_revision
        self.material.save()
        self.material_implementation = MaterialImplementation.objects.get(uuid='642bbbe6-d21b-11e8-a8d5-f2801f1b9fc0')
        self.preview_asset = MaterialImplementationAsset.objects.get(uuid='642bbbe6-d21b-11e8-a8d5-f2801f1b9fe1')
        self.json_asset = MaterialImplementationAsset.objects.get(uuid='642bbbe6-d21b-11e8-a8d5-f2801f1b9fe2')
        self.html_asset = MaterialImplementationAsset.objects.get(uuid='642bbbe6-d21b-11e8-a8d5-f2801f1b9fe3')

        self.dto = GetMaterialImplementationResultDTO(uuid=self.material_implementation.uuid)
        self.op = GetMaterialImplementationSuccessHandler()

    def test_get_material_implementation(self):
        """
        Test get material implementation
        """
        handler_result = self.op(self.dto)
        self.assertTrue(isinstance(handler_result, MaterialImplementationDTO))
        self.assertEqual(handler_result.group_name, self.root.name)
        self.assertEqual(handler_result.material_name, self.material.name)
        self.assertEqual(handler_result.material_info, self.material_revision.material_info)
        self.assertEqual(handler_result.color_name, self.material_implementation.name)

