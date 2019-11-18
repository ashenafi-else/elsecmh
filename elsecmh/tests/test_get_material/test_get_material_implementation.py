import os
from elsecmh.operations.get_material.get_material_implementation import GetMaterialImplementationOp

from elsecmh.models import (
    Material,
    MaterialRevision,
    MaterialImplementation,
)
from elsecmh.tests.test_base_cmh import TestBaseCmh
from elsepublic.elsecmh.dto.get_material_implementation import (
    GetMaterialImplementationParamsDTO,
    GetMaterialImplementationResultDTO,
)


class TestGetMaterialImplementation(TestBaseCmh):
    test_path = os.path.dirname(os.path.realpath(__file__))
    fixtures_path = os.path.join(test_path, '..', 'fixtures')

    def setUp(self):
        super().setUp()
        material = Material.objects.create(name='mat_nappa', material_group=self.root)
        self.material_revision = MaterialRevision.objects.create(
            material=material,
            material_info=''
        )
        material.active_revision = self.material_revision
        material.save()
        self.material_implementation = MaterialImplementation.objects.create(
            material_revision=self.material_revision,
            name='mat_nappa_191A1B'
        )
        self.dto = GetMaterialImplementationParamsDTO(uuid=self.material_implementation.uuid)
        self.op = GetMaterialImplementationOp()

    def test_get_material_implementation(self):
        """
        Test get material implementation
        """
        get_material_implementation_result = self.op(self.dto)
        self.assertTrue(isinstance(get_material_implementation_result, GetMaterialImplementationResultDTO))
        self.assertEqual(get_material_implementation_result.uuid, self.material_implementation.uuid)
