from elsecmh.tests.test_base_cmh import TestBaseCmh
from elsecmh.operations.publish_material_revision.utils import get_default_color_implementation

from elsecmh.models import (
    MaterialImplementation,
    MaterialRevision,
    Material,
)


class TestPublishMaterialRevisionUtils(TestBaseCmh):

    def setUp(self):
        super().setUp()
        material = Material.objects.create(name='material', material_group=self.root)
        self.material_revision = MaterialRevision.objects.create(material=material, material_info='')
        self.material_implementation = MaterialImplementation.objects.create(material_revision=self.material_revision)

    def test_get_default_color_implementation(self):
        """
        Test get default color implementation
        """
        # todo: implement test
        result = get_default_color_implementation(self.material_revision)
        self.assertEqual(result, self.material_implementation)
