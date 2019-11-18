import uuid

from elsecmh.models import Material, MaterialRevision
from elsecmh.tests.test_base_cmh import TestBaseCmh
from elsecommon.transports.router import Router
from elsecommon.transports.operation_type import OperationType
from elsecommon.transports.transportabc import TransportABC

from elsepublic.elsecmh.dto.remove_material import RemoveMaterialParamsDTO
from elsepublic.elsecmh.interfaces.remove_material import RemoveMaterialOpInterface


class TestRemoveMaterial(TestBaseCmh):

    def setUp(self):
        super().setUp()
        self.material = Material.objects.create(name='test_mat', material_group=self.root)
        self.material_revision = MaterialRevision.objects.create(material=self.material)

        self.remove_material_dto = RemoveMaterialParamsDTO(uuid=self.material.uuid)
        self.remove_missed_material_dto = RemoveMaterialParamsDTO(uuid=uuid.uuid4())
        Router[RemoveMaterialOpInterface] = OperationType(expose=False, producer=TransportABC)

    def test_remove_material(self):
        """
        Test remove material
        """
        rem_op = Router[RemoveMaterialOpInterface.uri]
        remove_result = rem_op(self.remove_material_dto)
        self.assertIsNone(remove_result)
        self.assertIsNone(Material.objects.filter(uuid=self.material.uuid).first())

    def test_remove_missed_material(self):
        """
        Test remove missed material
        """
        with self.assertRaises(RuntimeError):
            rem_op = Router[RemoveMaterialOpInterface.uri]
            rem_op(self.remove_missed_material_dto)
