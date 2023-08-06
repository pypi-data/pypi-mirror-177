from typing import Iterable, TypeVar, overload, Union, Any, Dict, Sequence

import numpy as np
import torch
from torch import Tensor

PrintableVar = TypeVar("PrintableVar", float, int)


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


def _num2str2(v: PrintableVar):
    if isinstance(v, int):
        return f"{v}"
    return f"{v:#.3g}"


def _leaf2str(v) -> str:
    if is_scalar(v):
        return _num2str2(v)
    if isinstance(v, str):
        return v
    if isinstance(v, Tensor):
        return _iter2str(v.tolist())
    if isinstance(v, np.ndarray):
        return _iter2str(v.tolist())
    return str(v)


def _generate_pair(k, v):
    """generate str for non iterable k v"""
    return f"{k}:{_leaf2str(v)}"


def _dict2str(dictionary: Dict[str, Any]):
    def create_substring(k: str, v: Any):
        if not is_iterable(v):
            return _generate_pair(k, v)
        else:
            return f"{k}:" + item2str(v)

    strings = [create_substring(k, v) for k, v in dictionary.items()]
    return ", ".join(strings)


def _iter2str(item: Iterable):
    """A list or a tuple"""
    return "[" + ", ".join([_leaf2str(x) if not is_iterable(x) else item2str(x) for x in item]) + "]"


def item2str(item: Union[Dict[str, Any], Sequence[Any]]) -> str:
    """convert item to string in a pretty way.
        @param item: list, dictionary, set and tuple
        @return: pretty string
    """
    if isinstance(item, Dict):
        return _dict2str(item)
    return _iter2str(item)


if __name__ == "__main__":
    a = {"a": {1: 2, 2: {3, 4}, 5: [1, 2, 0.00000398948329483]},
         "ofds": ["123", "23", torch.tensor(1, device="cuda"), torch.Tensor([1, 2, 3]).cuda(),
                  {7: np.array([1, 2, 3, 4])}, torch.randn(3, 3)]}
    print(item2str(a))
