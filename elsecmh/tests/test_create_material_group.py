import uuid

from elsecmh.tests.test_base_cmh import TestBaseCmh
from elsecommon.transports.router import Router
from elsecommon.transports.operation_type import OperationType
from elsecommon.transports.transportabc import TransportABC

from elsepublic.elsecmh.dto.create_material_group import (
    CreateMaterialGroupParamsDTO,
    CreateMaterialGroupResultDTO,
)
from elsepublic.elsecmh.interfaces.create_material_group import CreateMaterialGroupOpInterface


class TestCreateMaterialGroup(TestBaseCmh):

    def setUp(self):
        super().setUp()
        self.create_material_dto = CreateMaterialGroupParamsDTO(name='group')
        self.create_child_material_dto = CreateMaterialGroupParamsDTO(name='group', parent_uuid=self.root.uuid)
        self.create_material_group_with_wrong_parent_dto = CreateMaterialGroupParamsDTO(
            name='group', parent_uuid=uuid.uuid4())
        Router[CreateMaterialGroupOpInterface] = OperationType(expose=False, producer=TransportABC)

    def test_create_material_group(self):
        """
        Test create material group
        """
        cre_op = Router[CreateMaterialGroupOpInterface.uri]
        create_result = cre_op(self.create_material_dto)
        self.assertIsInstance(create_result, CreateMaterialGroupResultDTO)
        self.assertEqual(create_result.name, self.create_material_dto.name)
        self.assertIsNone(create_result.parent_uuid)

    def test_create_child_material_group(self):
        """
        Test create child material group
        """
        cre_op = Router[CreateMaterialGroupOpInterface.uri]
        create_result = cre_op(self.create_child_material_dto)
        self.assertIsInstance(create_result, CreateMaterialGroupResultDTO)
        self.assertEqual(create_result.name, self.create_child_material_dto.name)
        self.assertEqual(create_result.parent_uuid, self.root.uuid)

    def test_create_material_group_with_wrong_parent(self):
        """
        Test create material group with wrong parent
        """
        with self.assertRaises(RuntimeError):
            cre_op = Router[CreateMaterialGroupOpInterface.uri]
            cre_op(self.create_material_group_with_wrong_parent_dto)

