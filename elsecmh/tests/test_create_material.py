from elsecmh.models import Material
from elsecmh.tests.test_base_cmh import TestBaseCmh
from elsecommon.transports.operation_type import OperationType
from elsecommon.transports.router import Router
from elsecommon.transports.transportabc import TransportABC
from elsepublic.elsecmh.create_material.dto import (
    CreateMaterialParamsDTO,
    CreateMaterialResultDTO,
)
from elsepublic.elsecmh.create_material.interface import CreateMaterialOpInterface


class TestCreateMaterial(TestBaseCmh):

    def setUp(self):
        super().setUp()
        self.create_material_dto = CreateMaterialParamsDTO(
            name='test_material', material_group_uuid=self.root.uuid, brand_uuid=self.brand.brand_external_id)
        material = Material.objects.create(
            name='existed_material',
            material_group=self.root,
            brand=self.brand,
        )
        self.create_existed_material_dto = CreateMaterialParamsDTO(
            name=material.name,
            material_group_uuid=material.material_group.uuid,
            brand_uuid=self.brand.brand_external_id,
        )
        Router[CreateMaterialOpInterface] = OperationType(expose=False, producer=TransportABC)

    def test_create_material(self):
        """
        Test create material
        """
        cre_op = Router[CreateMaterialOpInterface.uri]
        create_result = cre_op(self.create_material_dto)
        self.assertIsInstance(create_result, CreateMaterialResultDTO)
        self.assertEqual(create_result.name, self.create_material_dto.name)
        self.assertEqual(create_result.material_group_uuid, str(self.create_material_dto.material_group_uuid))

    def test_create_existed_material_revision(self):
        """
        Test create existed material
        """
        cre_op = Router[CreateMaterialOpInterface.uri]
        with self.assertRaises(RuntimeError):
            cre_op(self.create_existed_material_dto)
