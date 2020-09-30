import unittest
from wafec_wrapt_custom.wrappers import WrapperTest


class Aux(object):
    def __init__(self):
        self.item1 = Item(1)
        self.item2 = Item(2)

    def __repr__(self):
        return '<Aux(item1={}, item2={})>'.format(self.item1.value, self.item2.value)


class Item(object):
    def __init__(self, value):
        self.value = value


class TestWrapperTest(unittest.TestCase):
    def test_hello(self):
        wrapped = Aux()
        wrapper = WrapperTest(wrapped)
        self.assertTrue(isinstance(wrapper, Aux))
        self.assertTrue(isinstance(wrapper, WrapperTest))
        self.assertTrue(isinstance(wrapper.item1, WrapperTest))
        item3 = Item(3)
        wrapper.item2 = item3
        self.assertTrue(isinstance(wrapper.item2, WrapperTest))
        self.assertEqual(3, wrapper.item2.value)
        self.assertTrue(isinstance(wrapper.item2.value, int))

    def test_list(self):
        wrapped = [Aux(), Aux(), Aux()]
        wrapper = WrapperTest(wrapped)
        for item in wrapper:
            self.assertTrue(isinstance(item, WrapperTest))

    def test_dict(self):
        wrapped = {'item1': Aux(), 'item2': Aux()}
        wrapper = WrapperTest(wrapped)
        self.assertTrue(isinstance(wrapper['item1'], WrapperTest))
        self.assertTrue(isinstance(wrapper['item2'], WrapperTest))
        self.assertEqual(2, wrapper['item1'].item2.value)

    def test_kwargs(self):
        def func(item1, item2):
            self.assertTrue(isinstance(item1, WrapperTest))
            self.assertTrue(isinstance(item2, WrapperTest))

        wrapped = {'item1': Aux(), 'item2': Aux()}
        wrapper = WrapperTest.wrap_kwargs(wrapped)
        func(**wrapper)

    def test_getattr(self):
        wrapped = str('value')
        name = WrapperTest.will_wrap(wrapped)
        obj = Item(10)
        self.assertEqual(10, obj.value)
        getattr(obj, 'value')
        getattr(obj, name)

    def test_wrap_simple(self):
        def func():
            wrapped = str('value')
            WrapperTest(wrapped)

        self.assertRaises(TypeError, func)

    def test_func_wrapper(self):
        def func():
            return 10

        wrapper = WrapperTest(func)
        res = wrapper()
        self.assertEqual(10, res)

    def test_set(self):
        wrapped = {'item1', 'item2'}
        wrapper = WrapperTest(wrapped)
        for s1, s2 in zip(wrapped, wrapper):
            self.assertEqual(s1, s2)


if __name__ == '__main__':
    unittest.main()
