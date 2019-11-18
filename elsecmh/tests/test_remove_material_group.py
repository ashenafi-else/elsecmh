import uuid

from elsecmh.models import (
    Material,
    MaterialRevision,
)
from elsecmh.models import MaterialGroup
from elsecmh.tests.test_base_cmh import TestBaseCmh
from elsecommon.transports.router import Router
from elsecommon.transports.operation_type import OperationType
from elsecommon.transports.transportabc import TransportABC

from elsepublic.elsecmh.dto.remove_material_group import RemoveMaterialGroupParamsDTO
from elsepublic.elsecmh.interfaces.remove_material_group import RemoveMaterialGroupOpInterface


class TestRemoveMaterialGroup(TestBaseCmh):

    def setUp(self):
        super().setUp()
        self.child_group1 = self.root.add_child(name='child_group1')
        self.child_group11 = self.child_group1.add_child(name='child_group11')
        self.child_group12 = self.child_group1.add_child(name='child_group12')
        self.child_group2 = self.root.add_child(name='child_group2')
        self.child_group21 = self.child_group2.add_child(name='child_group21')
        self.child_group22 = self.child_group2.add_child(name='child_group22')
        self.material = Material.objects.create(name='material', material_group=self.child_group11)
        self.material_revision = MaterialRevision.objects.create(material=self.material)

        self.remove_material_group_dto = RemoveMaterialGroupParamsDTO(uuid=self.child_group11.uuid)
        self.remove_root_material_group_dto = RemoveMaterialGroupParamsDTO(uuid=self.root.uuid)
        self.remove_missed_material_group_dto = RemoveMaterialGroupParamsDTO(uuid=uuid.uuid4())
        Router[RemoveMaterialGroupOpInterface] = OperationType(expose=False, producer=TransportABC)

    def test_remove_material_group(self):
        """
        Test remove material group
        """
        rem_op = Router[RemoveMaterialGroupOpInterface.uri]
        remove_result = rem_op(self.remove_material_group_dto)
        self.assertIsNone(remove_result)
        self.assertIsNone(MaterialGroup.objects.filter(name=self.child_group11.name).first())

    def test_remove_root_material_group(self):
        """
        Test remove root material group
        """
        rem_op = Router[RemoveMaterialGroupOpInterface.uri]
        remove_result = rem_op(self.remove_root_material_group_dto)
        self.assertIsNone(remove_result)
        self.assertIsNone(MaterialGroup.objects.filter().first())
        self.assertIsNone(Material.objects.filter().first())
        self.assertIsNone(MaterialRevision.objects.filter().first())

    def test_remove_missed_material_group(self):
        """
        Test remove missed material group
        """
        with self.assertRaises(RuntimeError):
            rem_op = Router[RemoveMaterialGroupOpInterface.uri]
            rem_op(self.remove_missed_material_group_dto)
