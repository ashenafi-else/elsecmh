import uuid

from elsecmh.models import Material, MaterialRevision
from elsecmh.tests.test_base_cmh import TestBaseCmh
from elsecommon.transports.router import Router
from elsecommon.transports.operation_type import OperationType
from elsecommon.transports.transportabc import TransportABC

from elsepublic.elsecmh.dto.remove_material_revision import RemoveMaterialRevParamsDTO
from elsepublic.elsecmh.interfaces.remove_material_revision import RemoveMaterialRevOpInterface


class TestRemoveMaterialRevision(TestBaseCmh):

    def setUp(self):
        super().setUp()
        self.material = Material.objects.create(name='test_mat', material_group=self.root)
        self.material_revision = MaterialRevision.objects.create(material=self.material)
        self.remove_material_revision_dto = RemoveMaterialRevParamsDTO(uuid=self.material_revision.uuid)
        self.remove_missed_material_revision_dto = RemoveMaterialRevParamsDTO(uuid=uuid.uuid4())
        Router[RemoveMaterialRevOpInterface] = OperationType(expose=False, producer=TransportABC)

    def test_remove_material_revision(self):
        """
        Test remove material revision
        """
        rem_op = Router[RemoveMaterialRevOpInterface.uri]
        remove_result = rem_op(self.remove_material_revision_dto)
        self.assertIsNone(remove_result)
        self.assertIsNone(MaterialRevision.objects.filter(uuid=self.material_revision.uuid).first())

    def test_remove_missed_material_revision(self):
        """
        Test remove missed material revision
        """
        with self.assertRaises(RuntimeError):
            rem_op = Router[RemoveMaterialRevOpInterface.uri]
            rem_op(self.remove_missed_material_revision_dto)
