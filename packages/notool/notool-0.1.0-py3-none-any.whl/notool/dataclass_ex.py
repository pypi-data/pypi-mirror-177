import functools
from dataclasses import dataclass
import typing as t
from enum import EnumMeta

import orjson
from dacite import from_dict, core, UnionMatchError

_T = t.TypeVar("_T")


def _transform_value(type_hooks, cast, target_type, value):
    args = t.get_args(target_type)
    target_type = t.get_origin(target_type) or target_type
    try:
        if target_type is dict and args and (key_type := args[0]):
            # key_type_args = t.get_args(key_type)
            # key_type = t.get_origin(key_type) or key_type
            if key_type is str:
                pass
            # TODO orjson not supported tuple as dict keys
            # elif key_type is tuple and key_type_args:
            #     if len(key_type_args) > 1 or \
            #             (key_type_args := key_type_args[0]) not in (int, float, str):
            #         raise NotImplementedError
            #     return {tuple(map(key_type_args, key[1:-1].split(','))): val
            #             for key, val in value.items()}
            elif key_type in (int, float):
                return {key_type(key): val for key, val in value.items()}
            else:
                raise NotImplementedError
        elif hasattr(target_type, '_asdict'):  # for namedtuple
            return target_type(**value)
        elif isinstance(target_type, EnumMeta) or target_type is tuple:
            return target_type(value)
    except ValueError:
        raise KeyError

    return super_transform_value(type_hooks, cast, target_type, value)


def _build_value(type_, data, config):
    try:
        return super_build_value(type_, data, config)
    except UnionMatchError:
        raise KeyError


super_transform_value = getattr(core, 'transform_value')
setattr(core, 'transform_value', _transform_value)
super_build_value = getattr(core, '_build_value')
setattr(core, '_build_value', _build_value)


def _orjson_default(obj):
    if hasattr(obj, '_asdict'):
        return obj._asdict()


_encoder = functools.partial(orjson.dumps, default=_orjson_default, option=orjson.OPT_NON_STR_KEYS)
_decoder = orjson.loads


class Serializable:
    @classmethod
    def loads(cls: t.Type[_T],
              obj: t.Union[bytes, bytearray, memoryview, str],
              decoder: t.Callable = None) -> _T:
        return from_dict(cls, decoder or _decoder(obj))

    def dumps(self, encoder: t.Callable = None) -> t.Union[bytes, bytearray, memoryview, str]:
        return encoder or _encoder(self)


if __name__ == '__main__':

    def _tests():
        from notool.enum_ex import EnumChain
        from enum import Enum
        from dataclasses import field

        class Data1(Enum):
            data1a = 1

        class Data2(Enum):
            data2a = 16

        class Data(Data1, Data2, metaclass=EnumChain):
            ...
        Data._T = t.Union[Data, Data1, Data2]

        class EbcParams(t.NamedTuple):
            p1: float
            p2: float
            p3: float

        @dataclass
        class TestForDict:
            d1: EbcParams = EbcParams(1, 1, 1)
            d2: float = 20.20

        @dataclass
        class TestForList:
            f1: Data._T = Data2.data2a
            f2: tuple = (1, 1)
            f3: bool = True
            f4: t.Union[EbcParams, tuple[str, int]] = ('asd', 2)
            f5: dict[int, TestForDict] = field(default_factory=dict)

        @dataclass
        class TestData(Serializable):
            field1: Data._T = Data1.data1a
            field2: float = 2.0
            field3: dict = field(default_factory=lambda: {'test_field': 2})
            field4: list[TestForList] = field(default_factory=list)

        list_ = []
        for i in range(10):
            dict_ = {}
            for j in range(10):
                test_for_dict = TestForDict(EbcParams(i, i, i), j)
                dict_.update({j: test_for_dict})
            a = bool(i % 2)
            tuple_ = EbcParams(i, i, i) if a else (str(i), i)
            list_.append(TestForList(Data1.data1a, (i, i), a, tuple_, dict_))

        for test_data in (TestData(Data2.data2a, 14.2, {'test_field2': 22}),
                          TestData(Data2.data2a, 14.2, {'test_field2': 22}, list_)):
            test_data_loads = orjson.loads(orjson.dumps(test_data, default=_orjson_default, option=orjson.OPT_NON_STR_KEYS))
            test_data_dacite = from_dict(TestData, test_data_loads, )  # Config(cast=[Data], check_types=True))
            assert test_data == test_data_dacite
            assert test_data == TestData.loads(test_data.dumps())

        # a = b'\n'.join([orjson.dumps({'asd asd': '\n\t', 'a\na': 5}),
        #                orjson.dumps(['asd asd', '\n\t', 'a\na', 5])])
        # print(*a.split(b'\n'))

    _tests()
