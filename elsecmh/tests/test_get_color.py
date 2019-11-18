from elsecmh.tests.test_base_cmh import TestBaseCmh
from elsecmh.operations.get_color import GetColorOp
from elsecmh.models import (
    ColorGroup,
    Color,
)
from elsepublic.elsecmh.get_color import (
    GetColorParamsDTO,
    GetColorResultDTO,
)


class TestGetColor(TestBaseCmh):

    def setUp(self):
        super().setUp()

        color_group = ColorGroup.add_root(name='test_color_group')

        self.color = Color.objects.create(
            name='test_color',
            color_group=color_group,
            color_space='RGB',
            value='255, 0, 0',
            description='test color',
        )

        self.dto = GetColorParamsDTO(uuid=self.color.uuid)

        self.op = GetColorOp()

    def test_get_color(self):
        """
        Test get color
        """
        color_info = self.op(self.dto)

        self.assertIsInstance(color_info, GetColorResultDTO)
        self.assertEqual(color_info.name, self.color.name)
        self.assertEqual(color_info.uuid, self.color.uuid)
        self.assertEqual(
            color_info.color_group_uuid,
            self.color.color_group.uuid,
        )
        self.assertEqual(color_info.color_space, self.color.color_space)
        self.assertEqual(color_info.value, self.color.value)
        self.assertEqual(color_info.description, self.color.description)
