import argparse
import sys
import unittest
from io import BytesIO
from typing import ClassVar, Optional, Sequence, Tuple
from unittest import skipIf
from unittest.mock import MagicMock, patch

SequenceType = Sequence
TupleType = Tuple

if sys.version_info >= (3, 9):
    from collections.abc import Sequence  # pylint: disable=reimported
    from typing import Annotated, Literal

    Tuple = tuple  # type: ignore
else:
    from typing_extensions import Annotated, Literal

import corgy
from corgy import Corgy, CorgyHelpFormatter, corgyparser
from corgy._corgy import BooleanOptionalAction

if sys.version_info >= (3, 11):
    import tomllib as tomli
else:
    try:
        import tomli
    except ImportError:
        tomli = None  # type: ignore


class TestCorgyMeta(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        class _CorgyCls(Corgy):
            x1: Sequence[int]
            x2: Annotated[int, "x2 docstr"]
            x3: int = 3
            x4: Annotated[str, "x4 docstr"] = "4"

        cls._CorgyCls = _CorgyCls

    def test_corgy_cls_has_properties_from_type_hints(self):
        for _x in ["x1", "x2", "x3", "x4"]:
            with self.subTest(var=_x):
                self.assertTrue(hasattr(self._CorgyCls, _x))
                self.assertIsInstance(getattr(self._CorgyCls, _x), property)

    def test_corgy_instance_returns_correct_defaults(self):
        corgy_inst = self._CorgyCls()
        for _x, _d in zip(["x3", "x4"], [3, "4"]):
            with self.subTest(var=_x):
                _x_default = getattr(corgy_inst, _x)
                self.assertEqual(_x_default, _d)

    def test_corgy_instance_raises_on_unset_attr_access_without_default(self):
        corgy_inst = self._CorgyCls()
        for _x in ["x1", "x2"]:
            with self.subTest(var=_x):
                with self.assertRaises(AttributeError):
                    _x_default = getattr(corgy_inst, _x)

    def test_corgy_cls_adds_hint_metadata_as_property_docstrings(self):
        for _x in ["x1", "x2", "x3", "x4"]:
            with self.subTest(var=_x):
                _x_prop = getattr(self._CorgyCls, _x)
                if _x in ["x1", "x3"]:
                    self.assertIsNone(_x_prop.__doc__)
                else:
                    self.assertEqual(_x_prop.__doc__, f"{_x} docstr")

    def test_corgy_cls_properties_have_correct_type_annotations(self):
        for _x, _type in zip(["x1", "x2", "x3", "x4"], [Sequence[int], int, int, str]):
            with self.subTest(var=_x):
                _x_prop = getattr(self._CorgyCls, _x)
                self.assertEqual(_x_prop.fget.__annotations__["return"], _type)

                self.assertEqual(
                    len(_x_prop.fget.__annotations__),
                    1,
                    f"spurious annotations: {_x_prop.fget.__annotations__}",
                )

                self.assertEqual(_x_prop.fset.__annotations__["val"], _type)
                self.assertEqual(
                    len(_x_prop.fset.__annotations__),
                    1,
                    f"spurious annotations: {_x_prop.fset.__annotations__}",
                )

    def test_corgy_cls_raises_if_help_annotation_not_str(self):
        with self.assertRaises(TypeError):

            class _(Corgy):
                x: Annotated[int, 1]

    def test_corgy_cls_raises_if_flags_not_list(self):
        with self.assertRaises(TypeError):

            class _(Corgy):
                x: Annotated[int, "x help", "x"]

    def test_corgy_cls_raises_if_flag_list_empty(self):
        with self.assertRaises(TypeError):

            class _(Corgy):
                x: Annotated[int, "x help", []]

    def test_add_args_raises_if_custom_flags_on_group(self):
        with self.assertRaises(TypeError):

            class G(Corgy):
                x: int

            class _(Corgy):
                g: Annotated[G, "group G", ["-g", "--grp"]]

    def test_corgy_cls_allows_dunder_defaults_as_var_name(self):
        class C(Corgy):
            __defaults: int  # pylint: disable=unused-private-member
            x: int = 0

        self.assertTrue(hasattr(C, "__defaults"))
        self.assertIsInstance(getattr(C, "__defaults"), dict)
        self.assertTrue(hasattr(C, "_C__defaults"))
        self.assertIsInstance(getattr(C, "_C__defaults"), property)
        self.assertEqual(C().x, 0)

    def test_corgy_cls_raises_if_var_name_is_dunder_another_var(self):
        with self.assertRaises(TypeError):

            class _C(Corgy):  # pylint: disable=unused-variable
                x: int = 0
                __x = 2  # pylint: disable=unused-private-member

        with self.assertRaises(TypeError):

            class _C(Corgy):  # pylint: disable=unused-variable
                x: int
                __x: int  # pylint: disable=unused-private-member

    def test_corgy_cls_can_have_dunder_name(self):
        self.assertTrue(hasattr(self._CorgyCls, "_CorgyCls__x1"))

        class __C(Corgy):
            x: int

        self.assertTrue(hasattr(__C, "_C__x"))
        c = __C()
        c.x = 3
        self.assertEqual(c.x, 3)

    def test_corgy_cls_raises_on_setting_undefined_attribute(self):
        c = self._CorgyCls()
        with self.assertRaises(AttributeError):
            c.z = 0

    def test_corgy_cls_allows_custom_slots(self):
        class C(Corgy):
            __slots__ = ("y",)
            x: int

        c = C()
        c.y = 1
        self.assertEqual(c.y, 1)

    def test_corgy_cls_raises_on_slot_clash_with_var(self):
        with self.assertRaises(TypeError):

            class _(Corgy):
                x: int
                __slots__ = ("__x",)

    def test_corgy_cls_allows_disabling_slots_modification(self):
        class C(Corgy, corgy_make_slots=False):
            x: int

        c = C()
        c.x = 1
        c.y = 2
        self.assertEqual(c.x, 1)
        self.assertEqual(c.y, 2)

    def test_corgy_cls_raises_if_slots_modification_disabled_with_custom_slots(self):
        with self.assertRaises(TypeError):

            class _(Corgy, corgy_make_slots=False):
                __slots__ = ("y",)
                x: int

    def test_corgy_cls_modifies_slots_if_explicitly_enabled(self):
        class C(Corgy, corgy_make_slots=True):
            __slots__ = ("y",)
            x: int

        c = C()
        c.x = 1
        c.y = 2
        self.assertEqual(c.x, 1)
        self.assertEqual(c.y, 2)
        with self.assertRaises(AttributeError):
            c.z = 3

    def test_corgy_cls_disabling_slots_does_not_interfere_with_inheritance(self):
        class C1(Corgy):
            x: int

        class C2(Corgy, corgy_make_slots=False):
            x: int

        class D1(C1, corgy_make_slots=False):
            y: int

        class D2(C2):
            y: int

        for cls in (D1, D2):
            d = cls()
            d.x = 1
            d.y = 2
            d.z = 3
            self.assertEqual(d.x, 1)
            self.assertEqual(d.y, 2)
            self.assertEqual(d.z, 3)

    def test_corgy_cls_does_not_add_classvar(self):
        class C(Corgy):
            x: ClassVar[int] = 0

        self.assertEqual(C.x, 0)
        c = C()
        self.assertEqual(c.x, 0)
        with self.assertRaises(AttributeError):
            c.x = 1
        C.x = 1
        self.assertEqual(C.x, 1)
        self.assertEqual(c.x, 1)

    def test_corgy_cls_raises_if_classvar_has_no_value(self):
        with self.assertRaises(TypeError):

            class _(Corgy):
                x: ClassVar[int]

    def test_corgy_cls_inherits_classvar(self):
        class C:
            x: ClassVar[int] = 0
            y = 1
            __slots__ = ()

        class D(C, Corgy):
            z: ClassVar[str] = "0"

        class CCorgy(Corgy):
            x: ClassVar[int] = 0
            y = 1

        class DCorgy(CCorgy):
            z: ClassVar[str] = "0"

        for cls in (D, DCorgy):
            obj = cls()
            for _attr, _val in zip(("x", "y", "z"), (0, 1, "0")):
                with self.subTest(cls=cls.__name__, attr=_attr):
                    self.assertEqual(getattr(cls, _attr), _val)
                    self.assertEqual(getattr(obj, _attr), _val)
                    with self.assertRaises(AttributeError):
                        setattr(obj, _attr, "no")

    def test_corgy_cls_can_override_inherited_classvar(self):
        class C:
            x: ClassVar[int] = 0
            y = 1
            z: ClassVar[str] = "1"

        class D(C, Corgy):
            x: int  # type: ignore
            y: str = "1"
            z: ClassVar[str] = "2"

        class CCorgy(Corgy):
            x: ClassVar[int] = 0
            y = 1
            z: ClassVar[str] = "1"

        class DCorgy(CCorgy):
            x: int  # type: ignore
            y: str = "1"
            z: ClassVar[str] = "2"

        for ccls, dcls in zip((C, CCorgy), (D, DCorgy)):
            self.assertEqual(ccls.z, "1")
            self.assertEqual(dcls.z, "2")
            self.assertIsInstance(dcls.x, property)
            self.assertIsInstance(dcls.y, property)
            dobj = dcls()
            with self.assertRaises(AttributeError):
                _ = dobj.x
            self.assertEqual(dobj.y, "1")

    def test_corgy_cls_has_correct_repr_str(self):
        c = self._CorgyCls()
        c.x1 = [0, 1]
        c.x2 = 2
        c.x4 = "8"
        self.assertEqual(repr(c), "_CorgyCls(x1=[0, 1], x2=2, x3=3, x4='8')")
        self.assertEqual(str(c), "_CorgyCls(x1=[0, 1], x2=2, x3=3, x4=8)")

    def test_corgy_cls_repr_handles_unset_values(self):
        c = self._CorgyCls()
        self.assertEqual(repr(c), "_CorgyCls(x1=<unset>, x2=<unset>, x3=3, x4='4')")

    def test_corgy_cls_repr_handles_groups(self):
        class D(Corgy):
            x: int
            c: self._CorgyCls

        d = D(x=1, c=self._CorgyCls(x1=[0, 1], x2=2, x4="8"))
        self.assertEqual(repr(d), "D(x=1, c=_CorgyCls(x1=[0, 1], x2=2, x3=3, x4='8'))")

    def test_corgy_cls_as_dict(self):
        c = self._CorgyCls(x1=[0, 1], x2=2, x3=30, x4="40")
        self.assertDictEqual(c.as_dict(), {"x1": [0, 1], "x2": 2, "x3": 30, "x4": "40"})

    def test_corgy_cls_as_dict_uses_default_values(self):
        c = self._CorgyCls(x1=[0, 1], x2=2, x3=30)
        self.assertDictEqual(c.as_dict(), {"x1": [0, 1], "x2": 2, "x3": 30, "x4": "4"})

    def test_corgy_cls_as_dict_ignores_unset_attrs_without_defaults(self):
        c = self._CorgyCls(x3=30, x4="40")
        self.assertDictEqual(c.as_dict(), {"x3": 30, "x4": "40"})

    def test_corgy_cls_as_dict_handles_groups(self):
        class D(Corgy):
            x: int
            c: self._CorgyCls

        c = self._CorgyCls()
        d = D(x=1, c=c)
        self.assertDictEqual(d.as_dict(), {"x": 1, "c": c})

    def test_corgy_cls_as_dict_handles_inherited_attributes(self):
        class C:
            x1: int

        class D(C, Corgy):
            x2: int

        class CCorgy(Corgy):
            x1: int

        class DCorgy(CCorgy):
            x2: int

        for cls in (D, DCorgy):
            obj = cls(x1=1, x2=2)
            self.assertDictEqual(obj.as_dict(), {"x1": 1, "x2": 2})

    def test_corgy_cls_as_dict_handles_groups_when_recursive(self):
        class C(Corgy):
            x: int
            y: str

        class D(Corgy):
            x: int
            c: C

        class E(Corgy):
            x: int
            d: D

        e = E(x=1, d=D(x=10, c=C(x=100, y="100")))
        self.assertDictEqual(
            e.as_dict(recursive=True),
            {"x": 1, "d": {"x": 10, "c": {"x": 100, "y": "100"}}},
        )

    def test_corgy_cls_raises_if_initialized_directly(self):
        with self.assertRaises(TypeError):
            Corgy()

    def test_corgy_cls_usable_without_annotations(self):
        class C(Corgy):
            ...

        c = C()
        self.assertEqual(repr(c), "C()")
        self.assertDictEqual(c.as_dict(), {})

    def test_corgy_cls_subclasses_work_without_annotations(self):
        class D(self._CorgyCls):
            ...

        self.assertTrue(hasattr(D, "x1"))
        self.assertIsInstance(getattr(D, "x1"), property)

    def test_corgy_cls_inherits_annotations(self):
        class C:
            x1: int

        class D(Corgy, C):
            x2: int

        class CCorgy(Corgy):
            x1: int

        class DCorgy(CCorgy):
            x2: int

        for cls in (D, DCorgy):
            self.assertIn("x1", cls.__annotations__)
            self.assertIn("x2", cls.__annotations__)

    def test_corgy_cls_doesnt_inherit_annotations_if_disabled(self):
        class C:
            x1: int

        class D(Corgy, C, corgy_track_bases=False):
            x2: int

        class CCorgy(Corgy):
            x1: int

        class DCorgy(CCorgy, corgy_track_bases=False):
            x2: int

        for cls in (D, DCorgy):
            self.assertIn("x2", cls.__annotations__)
            self.assertNotIn("x1", cls.__annotations__)

    def test_corgy_cls_inherits_annotations_from_ancestors(self):
        class C:
            x1: int

        class D(Corgy, C):
            x2: str

        class E(D):
            x3: float

        for _x in ["x1", "x2", "x3"]:
            with self.subTest(var=_x):
                self.assertTrue(hasattr(E, _x))
                self.assertIsInstance(getattr(E, _x), property)

    def test_corgy_cls_overrides_inherited_annotations(self):
        class C:
            x1: int

        class D(Corgy, C):
            x1: str  # type: ignore

        class CCorgy(Corgy):
            x1: int

        class DCorgy(CCorgy):
            x1: str  # type: ignore

        for cls in (D, DCorgy):
            self.assertEqual(cls.x1.fget.__annotations__["return"], str)

    def test_corgy_cls_inherits_defaults(self):
        class C:
            x1: int = 1

        class D(Corgy, C):
            ...

        class CCorgy(Corgy):
            x1: int = 1

        class DCorgy(CCorgy):
            ...

        for cls in (D, DCorgy):
            self.assertIn("x1", getattr(cls, "__defaults"))

    def test_corgy_cls_overrides_inherited_defaults(self):
        class C:
            x1: int = 1
            x2: int = 2

        class D(Corgy, C):
            x1: int = 2
            x2: int

        class CCorgy(Corgy):
            x1: int = 1

        class DCorgy(CCorgy):
            x1: int = 2
            x2: int

        for cls in (D, DCorgy):
            self.assertIn("x1", getattr(cls, "__defaults"))
            self.assertEqual(getattr(cls, "__defaults")["x1"], 2)
            self.assertNotIn("x2", getattr(cls, "__defaults"))

    def test_corgy_cls_init_creates_correct_object(self):
        class C(Corgy):
            x1: int
            x2: str

        c = C(x1=1, x2="2")
        self.assertEqual(c.x1, 1)
        self.assertEqual(c.x2, "2")

    def test_corgy_cls_init_ignores_unknown_attrs(self):
        class C(Corgy):
            x1: int
            x2: str

        c = C(x1=1, x2="2", x3=3)
        self.assertFalse(hasattr(c, "x3"))

    def test_corgy_cls_init_allows_missing_attrs(self):
        class C(Corgy):
            x1: int
            x2: str

        c = C(x1=1)
        self.assertEqual(c.x1, 1)
        with self.assertRaises(AttributeError):
            _ = c.x2

    def test_corgy_cls_init_handles_groups(self):
        class G(Corgy):
            x1: int
            x2: str

        class C(Corgy):
            x1: int
            g: G

        c = C(x1=10, g=G(x1=1, x2="2"))
        self.assertEqual(c.x1, 10)
        self.assertEqual(c.g.x1, 1)
        self.assertEqual(c.g.x2, "2")

    def test_corgy_cls_init_handles_flat_group_args(self):
        class G(Corgy):
            x1: int
            x2: str

        class C(Corgy):
            x1: int
            g: G

        c = C(x1=10, **{"g:x1": 1, "g:x2": "2"})
        self.assertEqual(c.x1, 10)
        self.assertEqual(c.g.x1, 1)
        self.assertEqual(c.g.x2, "2")

        c = C(x1=10, **{"g:x1": 1})
        self.assertEqual(c.x1, 10)
        self.assertEqual(c.g.x1, 1)
        self.assertFalse(hasattr(c.g, "x2"))

    def test_corgy_cls_init_handles_nested_groups(self):
        class G(Corgy):
            x1: int
            x2: str

        class H(Corgy):
            x1: int
            x2: str

        class C(Corgy):
            x1: int
            g: G
            h: H

        c = C(x1=100, g=G(x1=10, x2="20"), **{"h:x2": "2"})
        self.assertEqual(c.x1, 100)
        self.assertEqual(c.g.x1, 10)
        self.assertEqual(c.g.x2, "20")
        self.assertEqual(c.h.x2, "2")

    def test_corgy_cls_init_raises_on_unknown_group_flat_args(self):
        class G(Corgy):
            x1: int
            x2: str

        class C(Corgy):
            x1: int
            g: G

        with self.assertRaises(ValueError):
            _ = C(**{"gee:x1": 1})

    def test_corgy_cls_init_raises_on_conflicting_group_args(self):
        class G(Corgy):
            x1: int
            x2: str

        class C(Corgy):
            x1: int
            g: G

        with self.assertRaises(ValueError):
            _ = C(g=G(x1=1), **{"g:x2": "2"})

    def test_corgy_cls_init_raises_on_non_corgy_group(self):
        class C(Corgy):
            x: int

        with self.assertRaises(ValueError):
            C(**{"x:": 1})
        with self.assertRaises(ValueError):
            C(**{"x:x": 1})
        with self.assertRaises(ValueError):
            C(**{"y:x": 1})

    def test_corgy_cls_from_dict(self):
        c = self._CorgyCls.from_dict({"x1": [0, 1], "x4": "four"})
        self.assertTrue(hasattr(c, "x1"))
        self.assertListEqual(c.x1, [0, 1])
        self.assertFalse(hasattr(c, "x2"))
        self.assertTrue(hasattr(c, "x3"))
        self.assertEqual(c.x3, 3)
        self.assertTrue(hasattr(c, "x4"))
        self.assertEqual(c.x4, "four")

    def test_corgy_cls_from_dict_handles_groups_as_dicts(self):
        class D(Corgy):
            x2: str = "two"
            c: self._CorgyCls
            x5: int

        d = D.from_dict({"x5": 5, "c": {"x2": 2, "x4": "four"}})
        self.assertTrue(hasattr(d, "x2"))
        self.assertEqual(d.x2, "two")
        self.assertTrue(hasattr(d, "x5"))
        self.assertEqual(d.x5, 5)
        self.assertTrue(hasattr(d, "c"))
        self.assertTrue(hasattr(d.c, "x2"))
        self.assertEqual(d.c.x2, 2)
        self.assertTrue(hasattr(d.c, "x4"))
        self.assertEqual(d.c.x4, "four")

    def test_corgy_cls_from_dict_handles_groups_as_objects(self):
        class D(Corgy):
            x2: str
            c: self._CorgyCls

        d = D.from_dict({"x2": "two", "c": self._CorgyCls(x2=2, x4="four")})
        self.assertTrue(hasattr(d, "c"))
        self.assertEqual(d.c.x2, 2)
        self.assertEqual(d.c.x4, "four")

    def test_corgy_cls_from_dict_handles_flattened_group_arguments(self):
        class D(Corgy):
            x2: str
            c: self._CorgyCls

        d = D.from_dict({"x2": "two", "c:x2": 2, "c:x4": "four"})
        self.assertTrue(hasattr(d, "c"))
        self.assertEqual(d.c.x2, 2)
        self.assertEqual(d.c.x4, "four")

    def test_corgy_cls_from_dict_raises_on_conflicting_group_arguments(self):
        class D(Corgy):
            x2: str
            c: self._CorgyCls

        with self.assertRaises(ValueError):
            D.from_dict({"x2": "two", "c": self._CorgyCls(x2=2), "c:x4": "four"})

    def test_corgy_cls_from_dict_allows_dict_as_value(self):
        class D(Corgy):
            x: dict

        d = D.from_dict({"x": {"x": 1}})
        self.assertDictEqual(d.x, {"x": 1})

    def test_corgy_cls_from_dict_ignores_unknown_arguments(self):
        self._CorgyCls.from_dict({"y1": 1, "y2": {"x1": 1}})

    def test_corgy_cls_from_dict_handles_inherited_attributes(self):
        class C(Corgy):
            x1: int

        class D(C):
            x2: str

        d = D.from_dict({"x1": 1, "x2": "two"})
        self.assertTrue(hasattr(d, "x1"))
        self.assertEqual(d.x1, 1)
        self.assertTrue(hasattr(d, "x2"))
        self.assertEqual(d.x2, "two")

    def test_corgy_cls_works_with_string_annotations(self):
        class C(Corgy):
            x1: "int"
            x2: "Annotated[str, 'x2 help']"
            x3: SequenceType["str"]

        for _x, _type in zip(["x1", "x2", "x3"], [int, str, SequenceType[str]]):
            with self.subTest(var=_x):
                self.assertIn(_x, C.__annotations__)
                self.assertEqual(C.__annotations__[_x], _type)

        self.assertEqual(getattr(C, "__helps")["x2"], "x2 help")

    def test_corgy_cls_handles_inherited_group_annotations(self):
        class C(Corgy):
            x1: "int"

        class D(C):
            x2: "str"

        class E1(D):
            x3: "float"

        class E2(D, corgy_track_bases=False):
            x3: "float"

        for _x, _type in zip(["x1", "x2", "x3"], [int, str, float]):
            with self.subTest(var=_x):
                self.assertIn(_x, E1.__annotations__)
                self.assertEqual(E1.__annotations__[_x], _type)

        self.assertNotIn("x1", E2.__annotations__)
        self.assertNotIn("x2", E2.__annotations__)
        self.assertIn("x3", E2.__annotations__)
        self.assertEqual(E2.__annotations__["x3"], float)


class TestCorgyAddArgsToParser(unittest.TestCase):
    def setUp(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument = MagicMock()
        self.parser.add_argument_group = MagicMock()

    def test_add_args_replaces_underscores_with_hyphens(self):
        class C(Corgy):
            the_x_arg: int

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--the-x-arg", type=int, required=True
        )

    def test_add_args_handles_provided_prefix(self):
        class C(Corgy):
            the_x_arg: int

        C.add_args_to_parser(self.parser, "prefix")
        self.parser.add_argument.assert_called_once_with(
            "--prefix:the-x-arg", type=int, required=True
        )

    def test_add_args_handles_custom_metavar(self):
        class T:
            __metavar__ = "T"

        class C(Corgy):
            x: T

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=T, required=True, metavar="T"
        )

    def test_add_args_handles_plain_type_annotation(self):
        class C(Corgy):
            x: int

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with("--x", type=int, required=True)

    def test_add_args_handles_default_value(self):
        class C(Corgy):
            x: int = 0

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with("--x", type=int, default=0)

    def test_add_args_handles_annotated_optional(self):
        class C(Corgy):
            x: Optional[int]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with("--x", type=int)

    @skipIf(sys.version_info < (3, 10), "`|` syntax needs Python 3.10 or higher")
    def test_add_args_handles_annotated_new_style_optional(self):
        class C(Corgy):
            x: int | None  # type: ignore # pylint: disable=unsupported-binary-operation

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with("--x", type=int)

    def test_add_args_handles_annotated_optional_with_default(self):
        class C(Corgy):
            x: Optional[int] = 0

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with("--x", type=int, default=0)

    def test_add_args_allows_incorrectly_typed_default(self):
        class C(Corgy):
            x: int = "x"

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with("--x", type=int, default="x")

    def test_add_args_uses_metadata_as_help(self):
        class C(Corgy):
            x: Annotated[int, "x docstring"]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, required=True, help="x docstring"
        )

    def test_add_args_handles_custom_flag(self):
        class C(Corgy):
            the_x_arg: Annotated[int, "x help", ["-x", "--the-x", "--the-x-arg"]]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "-x",
            "--the-x",
            "--the-x-arg",
            type=int,
            required=True,
            help="x help",
            dest="the_x_arg",
        )

    def test_add_args_uses_positional_flag(self):
        class C(Corgy):
            the_x_arg: Annotated[int, "x help", ["x"]]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "the_x_arg", type=int, help="x help"
        )

    def test_add_handles_positional_flag_with_same_name(self):
        class C(Corgy):
            the_x_arg: Annotated[int, "x help", ["the-x-arg"]]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "the_x_arg", type=int, help="x help"
        )

    def test_add_handles_positional_optional(self):
        class C(Corgy):
            the_x_arg: Annotated[Optional[int], "x help", ["the-x-arg"]]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "the_x_arg", type=int, help="x help", nargs="?"
        )

    def test_add_args_converts_literal_to_choices(self):
        class C(Corgy):
            x: Literal[1, 2, 3]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, required=True, choices=(1, 2, 3)
        )

    def test_add_args_raises_if_choices_not_same_type(self):
        class C(Corgy):
            x: Literal[1, 2, "3"]

        with self.assertRaises(TypeError):
            C.add_args_to_parser(self.parser)

    def test_add_args_uses_base_class_for_choice_type(self):
        class A:
            ...

        class A1(A):
            ...

        class A2(A):
            ...

        class B:
            ...

        class B1(B):
            ...

        class BA1(B, A2):
            ...

        class C(Corgy):
            x: Literal[A1, A2, BA1]  # type: ignore

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=A, required=True, choices=(A1, A2, BA1)
        )

        with self.assertRaises(TypeError):

            class D(Corgy):
                x: Literal[A1, A2, B1]  # type: ignore

            D.add_args_to_parser(self.parser)

    def test_add_args_uses_custom_choices(self):
        class A:
            __choices__ = (1, 2, 3)

        class C(Corgy):
            x: A

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=A, required=True, choices=(1, 2, 3)
        )

    def test_add_args_handles_user_defined_class_as_type(self):
        class T:
            ...

        class C(Corgy):
            x: T

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with("--x", type=T, required=True)

    def test_add_args_handles_user_defined_object_as_default(self):
        class T:
            ...

        t = T()

        class C(Corgy):
            x: T = t

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with("--x", type=T, default=t)

    def test_add_args_converts_bool_to_action(self):
        class C(Corgy):
            x: bool

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=bool, action=BooleanOptionalAction, required=True
        )

    def test_add_args_handles_default_for_bool_type(self):
        class C(Corgy):
            x: bool = False

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=bool, action=BooleanOptionalAction, default=False
        )

    def test_add_args_does_not_convert_bool_sequence_to_action(self):
        class C(Corgy):
            x: Sequence[bool]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=bool, required=True, nargs="*"
        )

    def test_add_args_raises_if_sequence_has_no_types(self):
        class C(Corgy):
            x: Sequence

        class D(Corgy):
            x: SequenceType

        with self.assertRaises(TypeError):
            C.add_args_to_parser(self.parser)

        with self.assertRaises(TypeError):
            D.add_args_to_parser(self.parser)

    def test_add_args_raises_if_tuple_has_no_types(self):
        class C(Corgy):
            x: Tuple

        class D(Corgy):
            x: TupleType

        with self.assertRaises(TypeError):
            C.add_args_to_parser(self.parser)

        with self.assertRaises(TypeError):
            D.add_args_to_parser(self.parser)

    def test_add_args_sets_nargs_to_asterisk_for_sequence_type(self):
        class C(Corgy):
            x: Sequence[int]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, nargs="*", required=True
        )

    def test_add_args_sets_nargs_to_asterisk_for_tuple_type(self):
        class C(Corgy):
            x: Tuple[int]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, nargs="*", required=True
        )

    def test_add_args_handles_sequence_type_as_well_as_abstract_sequence(self):
        class C(Corgy):
            x: SequenceType[int]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, nargs="*", required=True
        )

    def test_add_args_handles_tuple_type_as_well_as_abstract_tuple(self):
        class C(Corgy):
            x: TupleType[int]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, nargs="*", required=True
        )

    def test_add_args_handles_optional_sequence_type(self):
        class C(Corgy):
            x: Optional[Sequence[int]]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with("--x", type=int, nargs="*")

    def test_add_args_handles_optional_tuple_type(self):
        class C(Corgy):
            x: Optional[Tuple[int]]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with("--x", type=int, nargs="*")

    @skipIf(sys.version_info < (3, 9), "`typing.Sequence` doesn't accept multiple args")
    def test_add_args_sets_nargs_to_plus_for_non_empty_sequence_type(self):
        class C(Corgy):
            x: Sequence[int, ...]  # type: ignore

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, nargs="+", required=True
        )

    def test_add_args_sets_nargs_to_plus_for_non_empty_tuple_type(self):
        class C(Corgy):
            x: Tuple[int, ...]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, nargs="+", required=True
        )

    def test_add_args_handles_sequence_with_default(self):
        class C(Corgy):
            x: Sequence[int] = [1, 2, 3]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, nargs="*", default=[1, 2, 3]
        )

    def test_add_args_handles_tuple_with_default(self):
        class C(Corgy):
            x: Tuple[int] = [1, 2, 3]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, nargs="*", default=[1, 2, 3]
        )

    def test_add_args_converts_literal_sequence_to_choices_with_nargs(self):
        class C(Corgy):
            x: Sequence[Literal[1, 2, 3]]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, nargs="*", required=True, choices=(1, 2, 3)
        )

    def test_add_args_converts_literal_tuple_to_choices_with_nargs(self):
        class C(Corgy):
            x: Tuple[Literal[1, 2, 3]]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, nargs="*", required=True, choices=(1, 2, 3)
        )

    @skipIf(sys.version_info < (3, 9), "`typing.Sequence` doesn't accept multiple args")
    def test_add_args_handles_fixed_length_sequence_with_chocies(self):
        class C(Corgy):
            x: Sequence[Literal[1, 2, 3], Literal[1, 2, 3]]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, nargs=2, required=True, choices=(1, 2, 3)
        )

    def test_add_args_handles_fixed_length_tuple_with_chocies(self):
        class C(Corgy):
            x: Tuple[Literal[1, 2, 3], Literal[1, 2, 3]]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, nargs=2, required=True, choices=(1, 2, 3)
        )

    @skipIf(sys.version_info < (3, 9), "`typing.Sequence` doesn't accept multiple args")
    def test_add_args_raises_if_fixed_length_sequence_choices_not_all_same(self):
        class C(Corgy):
            x: Sequence[Literal[1, 2, 3], Literal[1, 2]]

        with self.assertRaises(TypeError):
            C.add_args_to_parser(self.parser)

    def test_add_args_raises_if_fixed_length_tuple_choices_not_all_same(self):
        class C(Corgy):
            x: Tuple[Literal[1, 2, 3], Literal[1, 2]]

        with self.assertRaises(TypeError):
            C.add_args_to_parser(self.parser)

    @skipIf(sys.version_info < (3, 9), "`typing.Sequence` doesn't accept multiple args")
    def test_add_args_handles_fixed_length_typed_sequence(self):
        class C(Corgy):
            x: Sequence[int, int, int]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, nargs=3, required=True
        )

    def test_add_args_handles_fixed_length_typed_tuple(self):
        class C(Corgy):
            x: Tuple[int, int, int]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, nargs=3, required=True
        )

    @skipIf(sys.version_info < (3, 9), "`typing.Sequence` doesn't accept multiple args")
    def test_add_args_handles_length_2_typed_sequence(self):
        class C(Corgy):
            x: Sequence[int, int]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, nargs=2, required=True
        )

    def test_add_args_handles_length_2_typed_tuple(self):
        class C(Corgy):
            x: Tuple[int, int]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, nargs=2, required=True
        )

    @skipIf(sys.version_info < (3, 9), "`typing.Sequence` doesn't accept multiple args")
    def test_add_args_raises_if_fixed_length_sequence_types_not_all_same(self):
        class C(Corgy):
            x: Sequence[int, str, int]

        with self.assertRaises(TypeError):
            C.add_args_to_parser(self.parser)

    def test_add_args_raises_if_fixed_length_tuple_types_not_all_same(self):
        class C(Corgy):
            x: Tuple[int, str, int]

        with self.assertRaises(TypeError):
            C.add_args_to_parser(self.parser)

    def test_add_args_converts_corgy_var_to_argument_group(self):
        class G(Corgy):
            x: int

        class C(Corgy):
            g: Annotated[G, "group G"]

        grp_parser = MagicMock()
        self.parser.add_argument_group = MagicMock(return_value=grp_parser)

        C.add_args_to_parser(self.parser)
        self.parser.add_argument_group.assert_called_once_with("g", "group G")
        grp_parser.add_argument.assert_called_once_with(
            "--g:x", type=int, required=True
        )

    def test_add_args_allows_repeated_name_in_group(self):
        class G(Corgy):
            x: int

        class C(Corgy):
            x: int
            g: G

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with("--x", type=int, required=True)
        self.parser.add_argument_group.assert_called_once_with("g", None)

    def test_add_args_handles_custom_flags_inside_group(self):
        class G(Corgy):
            the_x_arg: Annotated[int, "x help", ["-x", "--the-x", "--the-x-arg"]]

        class C(Corgy):
            the_grp: G

        grp_parser = MagicMock()
        self.parser.add_argument_group.return_value = grp_parser

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_not_called()
        self.parser.add_argument_group.assert_called_once_with("the_grp", None)
        grp_parser.add_argument.assert_called_once_with(
            "--the-grp:x",
            "--the-grp:the-x",
            "--the-grp:the-x-arg",
            type=int,
            help="x help",
            required=True,
            dest="the_grp:the_x_arg",
        )

    def test_add_args_handles_custom_flags_of_positional_args_inside_group(self):
        class G(Corgy):
            the_x_arg: Annotated[int, "x help", ["x", "the-x", "the_x_arg"]]

        grp_parser = argparse.ArgumentParser()
        grp_parser.add_argument = MagicMock()
        G.add_args_to_parser(grp_parser)
        grp_parser.add_argument.assert_called_once_with(
            "the_x_arg", type=int, help="x help"
        )

        class C(Corgy):
            the_grp: G

        grp_parser = MagicMock()
        self.parser.add_argument_group.return_value = grp_parser

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_not_called()
        self.parser.add_argument_group.assert_called_once_with("the_grp", None)
        grp_parser.add_argument.assert_called_once_with(
            "--the-grp:x",
            "--the-grp:the-x",
            "--the-grp:the_x_arg",
            type=int,
            help="x help",
            required=True,
            dest="the_grp:the_x_arg",
        )

    def test_add_args_makes_nested_groups_flat(self):
        class G2(Corgy):
            x: int

        class G1(Corgy):
            x: int
            g2: G2

        class C(Corgy):
            x: int
            g1: G1

        grp_parser = MagicMock()
        self.parser.add_argument_group.return_value = grp_parser

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with("--x", type=int, required=True)
        self.parser.add_argument_group.assert_any_call("g1", None)
        grp_parser.add_argument.assert_has_calls(
            [
                (("--g1:x",), {"type": int, "required": True}),
                (("--g1:g2:x",), {"type": int, "required": True}),
            ]
        )

    def test_add_args_handles_flatten_subgrps_arg(self):
        class G(Corgy):
            x: int

        class C(Corgy):
            x: int
            g: G

        C.add_args_to_parser(self.parser, flatten_subgrps=True)
        self.parser.add_argument.assert_has_calls(
            [
                (("--x",), {"type": int, "required": True}),
                (("--g:x",), {"type": int, "required": True}),
            ]
        )

    def test_add_args_infers_correct_base_type_from_complex_type_hint(self):
        class C(Corgy):
            x: Annotated[Optional[Sequence[str]], "x"]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=str, help="x", nargs="*"
        )

    def test_add_args_allows_function_base_type(self):
        def f(x: str) -> int:
            return int(x)

        class C(Corgy):
            x: f

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with("--x", type=f, required=True)

    def test_add_args_allows_list_base_type(self):
        class C(Corgy):
            x: Annotated[list, "x"]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=list, required=True, help="x"
        )

    def test_add_args_handles_passed_defaults(self):
        class C(Corgy):
            x: int

        C.add_args_to_parser(self.parser, defaults={"x": 42})
        self.parser.add_argument.assert_called_once_with("--x", type=int, default=42)

    def test_add_args_overrides_default_values_with_passed_defaults(self):
        class C(Corgy):
            x: int = 0

        C.add_args_to_parser(self.parser, defaults={"x": 42})
        self.parser.add_argument.assert_called_once_with("--x", type=int, default=42)

    def test_add_args_handles_passed_defaults_for_groups(self):
        class G(Corgy):
            x: int = 1
            y: str
            z: float = 2.0
            w: int

        class C(Corgy):
            g: G

        grp_parser = MagicMock()
        self.parser.add_argument_group.return_value = grp_parser

        C.add_args_to_parser(self.parser, defaults={"g": G(x=42, y="foo")})
        grp_parser.add_argument.assert_has_calls(
            [
                (("--g:x",), {"type": int, "default": 42}),
                (("--g:y",), {"type": str, "default": "foo"}),
                (("--g:z",), {"type": float, "default": 2.0}),
                (("--g:w",), {"type": int, "required": True}),
            ],
            any_order=True,
        )

    def test_add_args_handles_individually_passed_defaults_for_groups(self):
        class G(Corgy):
            x: int = 1
            y: str
            z: float = 2.0
            w: int

        class C(Corgy):
            g: G

        grp_parser = MagicMock()
        self.parser.add_argument_group.return_value = grp_parser

        C.add_args_to_parser(
            self.parser, defaults={"g": G(x=42, y="foo"), "g:x": 43, "g:w": 44}
        )
        grp_parser.add_argument.assert_has_calls(
            [
                (("--g:x",), {"type": int, "default": 43}),
                (("--g:y",), {"type": str, "default": "foo"}),
                (("--g:z",), {"type": float, "default": 2.0}),
                (("--g:w",), {"type": int, "default": 44}),
            ],
            any_order=True,
        )

    def test_add_args_raises_if_passed_defaults_for_unknown_var(self):
        class C(Corgy):
            x: int

        with self.assertRaises(ValueError):
            C.add_args_to_parser(self.parser, defaults={"y": 42})

    def test_add_args_raises_if_passed_defaults_for_unknown_group_var(self):
        class G(Corgy):
            x: int

        class C(Corgy):
            x: int
            g: G

        with self.assertRaises(ValueError):
            C.add_args_to_parser(self.parser, defaults={"g:y": 42})

    def test_add_args_raises_if_passed_non_corgy_as_group_default(self):
        class G(Corgy):
            x: int

        class C(Corgy):
            x: int
            g: G

        with self.assertRaises(ValueError):
            C.add_args_to_parser(self.parser, defaults={"g": 42})

    def test_add_args_handles_inherited_arguments(self):
        class C:
            x: int

        class D(Corgy, C):
            y: str

        class CCorgy(Corgy):
            x: int

        class DCorgy(CCorgy):
            y: str

        for cls in (D, DCorgy):
            self.parser.add_argument = MagicMock()
            cls.add_args_to_parser(self.parser)
            self.parser.add_argument.assert_has_calls(
                [
                    (("--x",), {"type": int, "required": True}),
                    (("--y",), {"type": str, "required": True}),
                ],
                any_order=True,
            )

    def test_add_args_handles_inheritance_disabling(self):
        class C:
            x: int

        class D(Corgy, C, corgy_track_bases=False):
            y: str

        class CCorgy(Corgy):
            x: int

        class DCorgy(CCorgy, corgy_track_bases=False):
            y: str

        for cls in (D, DCorgy):
            self.parser.add_argument = MagicMock()
            cls.add_args_to_parser(self.parser)
            self.parser.add_argument.assert_called_once_with(
                "--y", type=str, required=True
            )

    def test_add_args_uses_inherited_defaults(self):
        class C:
            x: int = 2

        class D(Corgy, C):
            ...

        class CCorgy(Corgy):
            x: int = 2

        class DCorgy(CCorgy):
            ...

        for cls in (D, DCorgy):
            self.parser.add_argument = MagicMock()
            cls.add_args_to_parser(self.parser)
            self.parser.add_argument.assert_called_once_with("--x", type=int, default=2)

    def test_add_args_uses_inherited_help_and_flags(self):
        class C(Corgy):
            the_x_arg: Annotated[int, "x help", ["-x", "--the-x", "--the-x-arg"]]

        class D(C):
            ...

        D.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "-x",
            "--the-x",
            "--the-x-arg",
            type=int,
            required=True,
            help="x help",
            dest="the_x_arg",
        )

    def test_add_args_raises_on_inconsistent_flags(self):
        class C(Corgy):
            x: Annotated[int, "x help", ["-x", "the-x"]]

        with self.assertRaises(TypeError):
            C.add_args_to_parser(self.parser)


class TestCorgyCmdlineParsing(unittest.TestCase):
    def setUp(self):
        self.parser = argparse.ArgumentParser()
        self.orig_parse_args = argparse.ArgumentParser.parse_args

    def test_cmdline_args_are_parsed_to_corgy_cls_properties(self):
        class C(Corgy):
            x: int
            y: str
            z: Sequence[int]

        self.parser.parse_args = lambda: self.orig_parse_args(
            self.parser, ["--x", "1", "--y", "2", "--z", "3", "4"]
        )
        c = C.parse_from_cmdline(self.parser)
        self.assertEqual(c.x, 1)
        self.assertEqual(c.y, "2")
        self.assertListEqual(c.z, [3, 4])

    def test_cmdline_args_are_parsed_with_custom_flags(self):
        class C(Corgy):
            var: Annotated[int, "x help", ["-x", "--the-x", "--the-x-arg"]]

        for flag in ["-x", "--the-x", "--the-x-arg"]:
            with self.subTest(flag=flag):
                self.parser = argparse.ArgumentParser()
                self.parser.parse_args = lambda: self.orig_parse_args(
                    self.parser, ["-x", "1"]
                )
                c = C.parse_from_cmdline(self.parser)
                self.assertEqual(c.var, 1)

    def test_cmdline_positional_args_are_parsed_with_custom_flags(self):
        class C(Corgy):
            var: Annotated[int, "x help", ["x"]]

        self.parser = argparse.ArgumentParser()
        self.parser.parse_args = lambda: self.orig_parse_args(self.parser, ["1"])
        c = C.parse_from_cmdline(self.parser)
        self.assertEqual(c.var, 1)

    def test_cmdline_positional_optional_args_are_pared_without_value(self):
        class C(Corgy):
            var: Annotated[Optional[int], "x help", ["x"]]

        for args in [[], ["1"]]:
            with self.subTest(args=args):
                self.parser = argparse.ArgumentParser()
                # pylint: disable=cell-var-from-loop
                self.parser.parse_args = lambda: self.orig_parse_args(self.parser, args)
                c = C.parse_from_cmdline(self.parser)
                if not args:
                    self.assertIsNone(c.var)
                else:
                    self.assertEqual(c.var, 1)

    def test_cmdline_parsing_handles_group_arguments(self):
        class G(Corgy):
            x: int
            y: str

        class C(Corgy):
            x: int
            y: int
            g: G

        self.parser.parse_args = lambda: self.orig_parse_args(
            self.parser, ["--x", "1", "--y", "2", "--g:x", "3", "--g:y", "four"]
        )
        c = C.parse_from_cmdline(self.parser)
        self.assertEqual(c.x, 1)
        self.assertEqual(c.y, 2)
        self.assertEqual(c.g.x, 3)
        self.assertEqual(c.g.y, "four")

    def test_cmdline_parsing_handles_groups_with_positional_args(self):
        class G(Corgy):
            the_x_var: Annotated[int, "x help", ["x", "the_x", "the-x-var"]]

        grp_parser = argparse.ArgumentParser()
        grp_parser.parse_args = lambda: self.orig_parse_args(grp_parser, ["1"])
        g = G.parse_from_cmdline(grp_parser)
        self.assertEqual(g.the_x_var, 1)

        class C(Corgy):
            x: int
            g: G

        for grp_flag in ["--g:x", "--g:the-x", "--g:the-x-var"]:
            with self.subTest(grp_flag=grp_flag):
                self.setUp()
                self.parser.parse_args = lambda: self.orig_parse_args(
                    self.parser,
                    ["--x", "1", grp_flag, "2"],  # pylint: disable=cell-var-from-loop
                )
                c = C.parse_from_cmdline(self.parser)
                self.assertEqual(c.x, 1)
                self.assertEqual(c.g.the_x_var, 2)

    def test_cmdline_parsing_handles_nested_groups(self):
        class G1(Corgy):
            x: int

        class G2(Corgy):
            x: int
            g: G1

        class C(Corgy):
            x: int
            g1: G1
            g2: G2

        self.parser.parse_args = lambda: self.orig_parse_args(
            self.parser, ["--x", "1", "--g1:x", "2", "--g2:x", "3", "--g2:g:x", "4"]
        )
        c = C.parse_from_cmdline(self.parser)
        self.assertEqual(c.x, 1)
        self.assertEqual(c.g1.x, 2)
        self.assertEqual(c.g2.x, 3)
        self.assertEqual(c.g2.g.x, 4)

    def test_cmdline_parsing_handles_nested_groups_with_custom_flags(self):
        class G1(Corgy):
            var: Annotated[int, "var help", ["-v", "--var"]]

        class G2(Corgy):
            var: Annotated[int, "var help", ["-v", "--var"]]
            g: G1

        class C(Corgy):
            var: Annotated[int, "var help", ["-v", "--var"]]
            g1: G1
            g2: G2

        self.parser.parse_args = lambda: self.orig_parse_args(
            self.parser, ["-v", "1", "--g1:v", "2", "--g2:var", "3", "--g2:g:v", "4"]
        )
        c = C.parse_from_cmdline(self.parser)
        self.assertEqual(c.var, 1)
        self.assertEqual(c.g1.var, 2)
        self.assertEqual(c.g2.var, 3)
        self.assertEqual(c.g2.g.var, 4)

    def test_cmdline_parsing_handles_list_base_type(self):
        class C(Corgy):
            x: list

        self.parser.parse_args = lambda: self.orig_parse_args(
            self.parser, ["--x", "123"]
        )
        c = C.parse_from_cmdline(self.parser)
        self.assertListEqual(c.x, ["1", "2", "3"])

    def test_cmdline_parsing_handles_custom_base_type(self):
        class A:
            def __init__(self, s):
                x, y = s.split(",")
                self.x = int(x)
                self.y = float(y)

        class C(Corgy):
            a: A

        self.parser.parse_args = lambda: self.orig_parse_args(
            self.parser, ["--a", "1,2.3"]
        )
        c = C.parse_from_cmdline(self.parser)
        self.assertEqual(c.a.x, 1)
        self.assertEqual(c.a.y, 2.3)

    def test_parse_from_cmdline_passes_extra_args_to_parser_constructor(self):
        class C(Corgy):
            x: int

        self.parser.parse_args = lambda: self.orig_parse_args(self.parser, ["--x", "1"])
        with patch(
            "corgy._corgy.argparse.ArgumentParser", MagicMock(return_value=self.parser)
        ):
            C.parse_from_cmdline(
                formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=False
            )
            corgy._corgy.argparse.ArgumentParser.assert_called_once_with(
                formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=False
            )

    def test_parse_from_cmdline_uses_corgy_help_formatter_if_no_formatter_specified(
        self,
    ):
        class C(Corgy):
            x: int

        self.parser.parse_args = lambda: self.orig_parse_args(self.parser, ["--x", "1"])
        with patch(
            "corgy._corgy.argparse.ArgumentParser", MagicMock(return_value=self.parser)
        ):
            C.parse_from_cmdline(add_help=False)
            corgy._corgy.argparse.ArgumentParser.assert_called_once_with(
                formatter_class=CorgyHelpFormatter, add_help=False
            )

    def test_parse_from_cmdline_ignores_extra_arguments(self):
        class C(Corgy):
            x: int

        self.parser.add_argument("--y", type=str)
        self.parser.parse_args = lambda: self.orig_parse_args(
            self.parser, ["--x", "1", "--y", "2"]
        )
        c = C.parse_from_cmdline(self.parser, add_help=False)
        self.assertEqual(c.x, 1)
        with self.assertRaises(AttributeError):
            _ = c.y

    def test_parse_from_cmdline_handles_passed_defaults(self):
        class C(Corgy):
            x: int

        self.parser.parse_args = lambda: self.orig_parse_args(self.parser, [])
        c = C.parse_from_cmdline(self.parser, defaults={"x": 1}, add_help=False)
        self.assertEqual(c.x, 1)


class TestCorgyCustomParsers(unittest.TestCase):
    def test_corgyparser_raises_if_not_passed_name(self):
        with self.assertRaises(TypeError):

            @corgyparser
            def spam():
                ...

    def test_corgy_raises_if_corgyparser_target_invalid(self):
        with self.assertRaises(TypeError):

            class _(Corgy):
                x: int

                @corgyparser("y")
                def parsex(s: str):  # type: ignore # pylint: disable=no-self-argument
                    return 0

    def test_add_args_handles_corgyparser(self):
        class C(Corgy):
            x: Annotated[int, "x"]

            @corgyparser("x")
            def parsex(s: str):  # type: ignore # pylint: disable=no-self-argument
                return 0

        parser = argparse.ArgumentParser()
        parser.add_argument = MagicMock()
        C.add_args_to_parser(parser)
        parser.add_argument.assert_called_once_with(
            "--x", type=getattr(C, "__parsers")["x"], required=True, help="x"
        )

    def test_add_args_with_custom_parser_respects_default_value(self):
        class C(Corgy):
            x: int = 1

            @corgyparser("x")
            def parsex(s: str):  # type: ignore # pylint: disable=no-self-argument
                return 0

        parser = argparse.ArgumentParser()
        parser.add_argument = MagicMock()
        C.add_args_to_parser(parser)
        parser.add_argument.assert_called_once_with(
            "--x", type=getattr(C, "__parsers")["x"], default=1
        )

    def test_cmdline_parsing_calls_custom_parser(self):
        class C(Corgy):
            x: int

            @corgyparser("x")
            def parsex(s: str):  # type: ignore # pylint: disable=no-self-argument
                return 0

        getattr(C, "__parsers")["x"] = MagicMock()
        parser = argparse.ArgumentParser()
        orig_parse_args = argparse.ArgumentParser.parse_args
        parser.parse_args = lambda: orig_parse_args(parser, ["--x", "test"])

        C.parse_from_cmdline(parser)
        getattr(C, "__parsers")["x"].assert_called_once_with("test")

    def test_cmdline_parsing_returns_custom_parser_output(self):
        class C(Corgy):
            x: int

            @corgyparser("x")
            def parsex(s: str):  # type: ignore # pylint: disable=no-self-argument
                return -1

        parser = argparse.ArgumentParser()
        orig_parse_args = argparse.ArgumentParser.parse_args
        parser.parse_args = lambda: orig_parse_args(parser, ["--x", "test"])

        args = C.parse_from_cmdline(parser)
        self.assertEqual(args.x, -1)

    def test_corgyparser_allows_decorating_staticmethod(self):
        class C(Corgy):
            x: int

            @corgyparser("x")
            @staticmethod
            def parsex(s: str):
                return 0

        parser = argparse.ArgumentParser()
        orig_parse_args = argparse.ArgumentParser.parse_args
        parser.parse_args = lambda: orig_parse_args(parser, ["--x", "test"])

        c = C.parse_from_cmdline(parser)
        self.assertEqual(c.x, 0)

    def test_corgyparser_raises_if_decorating_non_staticmethod(self):
        with self.assertRaises(TypeError):

            class _(Corgy):
                x: int

                @corgyparser("x")
                @classmethod
                def parsex(cls, s: str):
                    return 0

    def test_corgyparser_functions_are_callable(self):
        class C(Corgy):
            x: int
            y: int

            @corgyparser("x")
            @staticmethod
            def parsex(s: str):
                return 0

            @corgyparser("y")
            def parsey(s: str):  # type: ignore # pylint: disable=no-self-argument
                return 1

        self.assertEqual(C.parsex("x"), 0)
        self.assertEqual(C.parsey("y"), 1)

    def test_corgyparser_decorators_can_be_chained(self):
        class C(Corgy):
            x: int
            y: int

            @corgyparser("x")
            @corgyparser("y")
            @staticmethod
            def parsexy(s: str):
                return int(s)

        self.assertEqual(C.parsexy("1"), 1)
        self.assertEqual(C.parsexy("2"), 2)

    def test_add_args_with_custom_parser_uses_custom_metavar(self):
        class T:
            __metavar__ = "T"

        class C(Corgy):
            x: T

            @corgyparser("x")
            @staticmethod
            def parsex(s: str):
                return 0

        parser = argparse.ArgumentParser()
        parser.add_argument = MagicMock()
        C.add_args_to_parser(parser)
        parser.add_argument.assert_called_once_with(
            "--x", type=C.parsex.fparse, required=True, metavar="T"
        )

    def test_corgy_cls_inherits_custom_parser(self):
        class C(Corgy):
            x: int

            @corgyparser("x")
            @staticmethod
            def parsex(s):
                return int(s) + 1

        class D(C):
            ...

        parser = argparse.ArgumentParser()
        orig_parse_args = argparse.ArgumentParser.parse_args
        parser.parse_args = lambda: orig_parse_args(parser, ["--x", "1"])

        d = D.parse_from_cmdline(parser)
        self.assertEqual(d.x, 2)


@skipIf(tomli is None, "`tomli` package not found")
class TestCorgyTomlParsing(unittest.TestCase):
    def test_toml_file_parsed_to_corgy_object(self):
        class C(Corgy):
            x: int

        f = BytesIO(b"x = 1\n")
        c = C.parse_from_toml(f)
        self.assertEqual(c.x, 1)

    def test_toml_file_parsing_handles_sequences(self):
        class C(Corgy):
            x: Sequence[int]
            y: Sequence[str]

        f = BytesIO(b"x = [1, 2, 3]\ny = ['1', '2', '3']\n")
        c = C.parse_from_toml(f)
        self.assertEqual(c.x, [1, 2, 3])
        self.assertEqual(c.y, ["1", "2", "3"])

    def test_toml_file_parsing_handles_defaults(self):
        class C(Corgy):
            x: int = 1
            y: str

        f = BytesIO(b"y = 'test'\n")
        c = C.parse_from_toml(f)
        self.assertEqual(c.x, 1)
        self.assertEqual(c.y, "test")

    def test_toml_file_parsing_handles_default_override(self):
        class C(Corgy):
            x: int = 1

        f = BytesIO(b"\n")
        c = C.parse_from_toml(f, defaults={"x": 2})
        self.assertEqual(c.x, 2)

    def test_toml_file_parsing_handles_groups(self):
        class G(Corgy):
            x: int
            y: str = "test"

        class C(Corgy):
            x: str
            g: G

        f = BytesIO(b"x = 'one'\n[g]\nx = 1\n")
        c = C.parse_from_toml(f)
        self.assertEqual(c.x, "one")
        self.assertTrue(hasattr(c, "g"))
        self.assertEqual(c.g.x, 1)
        self.assertEqual(c.g.y, "test")

    def test_toml_file_parsing_handles_subgroups(self):
        class C(Corgy):
            x: int

        class D(Corgy):
            x: str
            c: C

        class E(Corgy):
            x: int
            c: D
            d: D

        f = BytesIO(b"x = 1\n[c]\nx = 10\n[d]\nx = 'one'\n[d.c]\nx = 100\n")
        e = E.parse_from_toml(f)
        self.assertEqual(e.x, 1)
        self.assertEqual(e.c.x, 10)
        self.assertEqual(e.d.x, "one")
        self.assertEqual(e.d.c.x, 100)

    def test_toml_file_parsing_handles_inherited_attributes(self):
        class G:
            x: int

        class C(Corgy, G):
            y: str

        class GCorgy(Corgy):
            x: int

        class CCorgy(GCorgy):
            y: str

        for cls in (C, CCorgy):
            f = BytesIO(b"x = 1\ny = 'test'\n")
            c = cls.parse_from_toml(f)
            self.assertEqual(c.x, 1)
            self.assertEqual(c.y, "test")

    def test_toml_file_parsing_handles_custom_parsers(self):
        class C(Corgy):
            x: int

            @corgyparser("x")
            @staticmethod
            def parsex(s: str):
                return int(s) + 1

        f = BytesIO(b"x = 1\n")
        c = C.parse_from_toml(f)
        self.assertEqual(c.x, 2)
