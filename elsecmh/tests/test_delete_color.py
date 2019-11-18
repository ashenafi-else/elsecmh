from elsecmh.tests.test_base_cmh import TestBaseCmh
from elsecmh.operations.delete_color import DeleteColorOp
from elsecmh.models import (
    ColorGroup,
    Color,
)
from elsepublic.elsecmh.delete_color import DeleteColorParamsDTO


class TestDeleteColor(TestBaseCmh):

    def setUp(self):
        super().setUp()

        color_group = ColorGroup.add_root(name='test_color_group')
        color = Color.objects.create(
            name='test_color',
            color_group=color_group,
            color_space=Color.RGB,
            value='255, 0, 0',
            description='test color',
        )

        self.dto = DeleteColorParamsDTO(uuid=color.uuid)

        self.op = DeleteColorOp()

    def test_delete_color(self):
        """
        Test delete color
        """
        self.op(self.dto)
        self.assertEqual(Color.objects.filter(uuid=self.dto.uuid).count(), 0)
