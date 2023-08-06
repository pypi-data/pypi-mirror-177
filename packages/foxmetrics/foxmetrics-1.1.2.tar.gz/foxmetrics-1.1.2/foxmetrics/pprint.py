from typing import Iterable, TypeVar, overload, Union, Any, Dict, Sequence

import numpy as np
import torch
from torch import Tensor

__all__ = ["item2str"]

PrintableVar = TypeVar("PrintableVar", float, int, str)

__dict_bracket__ = ""
__iter_bracket__ = "[]"


def _torch_is_scalar(v: 'Tensor') -> bool:
    return v.numel() == 1


@overload
def is_scalar(v: 'np.ndarray') -> bool:
    ...


@overload
def is_scalar(v: 'Tensor') -> bool:
    ...


@overload
def is_scalar(v: Union[float, int]) -> bool:
    ...


def is_scalar(v) -> bool:
    """if v is a scalar"""
    if isinstance(v, (int, float)):
        return True
    if isinstance(v, np.ndarray):
        return np.isscalar(v)
    if isinstance(v, Tensor):
        return _torch_is_scalar(v)
    else:
        return False


def is_iterable(v):
    """if v is an iterable, except str"""
    if isinstance(v, str):
        return False
    if isinstance(v, np.ndarray):
        return False
    if isinstance(v, Tensor):
        return False
    return isinstance(v, Iterable)


def is_mapping(v):
    return isinstance(v, Dict)


def is_leaf_node(v):
    if is_iterable(v) or is_mapping(v):
        return False
    return True


def __num2str2(v: PrintableVar):
    """only accept int, float and str"""
    if isinstance(v, int):
        return f"{v}"
    return f"{v:#.3g}"


def leaf_node2str(v) -> str:
    """
    print a leaf node, including str, scalar, torch tensor and ndarray
    :param v:
    :return:
    """
    if is_scalar(v):
        return __num2str2(v)
    if isinstance(v, str):
        return v
    if isinstance(v, Tensor):
        return iter2str(v.tolist())
    if isinstance(v, np.ndarray):
        return iter2str(v.tolist())  # noqa
    return str(v)


def iter2str(item: Iterable[Any]):
    """A list or a tuple"""
    global __iter_bracket__
    bracket = __iter_bracket__
    if bracket == "":
        return ", ".join([leaf_node2str(x) if is_leaf_node(x) else item2str(x) for x in item])
    if len(bracket) == 2:
        return bracket[0] + ", ".join([leaf_node2str(x) if is_leaf_node(x) else item2str(x) for x in item]) + bracket[1]
    raise RuntimeError(bracket)


def _generate_pair(k, v):
    """generate str for non iterable k v"""
    return f"{k}:{leaf_node2str(v)}"


def dict2str(dictionary: Dict[str, Any]):
    global __dict_bracket__

    def create_substring(k: str, v: Any):
        if is_leaf_node(v):
            return _generate_pair(k, v)
        return f"{str(k)}:" + item2str(v)

    strings = [create_substring(k, v) for k, v in dictionary.items()]

    bracket = __dict_bracket__
    if bracket == "":
        return ", ".join(strings)
    if len(bracket) == 2:
        return bracket[0] + ", ".join(strings) + bracket[1]
    raise RuntimeError(bracket)


def item2str(item: Union[Dict[str, Any], Sequence[Any], PrintableVar], *, dict_bracket: str = None,
             iter_bracket: str = None) -> str:
    global __dict_bracket__, __iter_bracket__
    __dict_bracket__ = dict_bracket or __dict_bracket__
    __iter_bracket__ = iter_bracket or __iter_bracket__
    if is_scalar(item):
        return __num2str2(item)
    if isinstance(item, Dict):
        return dict2str(item)
    if is_iterable(item):
        return iter2str(item)
    raise NotImplementedError(item)


if __name__ == "__main__":
    a = {"a": {1: 2, 2: {3, 4}, 5: [1, 2, 0.00000398948329483]},
         "ofds": ["123", "23", torch.tensor(1), torch.Tensor([1, 2, 3])]}
    from foxmetrics.utils import flatten_dict

    print(flatten_dict(a))
    print(item2str(flatten_dict(a), dict_bracket=None, iter_bracket="||"))
