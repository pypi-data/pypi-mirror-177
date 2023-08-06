import pandas as pd
from enum import Enum
from itertools import chain
from difflib import SequenceMatcher
from typing import List, Optional

from pydantic import BaseModel
from inspect import signature


class TType(str, Enum):
    Pandas = 'Pandas'
    DataFrame = 'DataFrame'
    Series = 'Series'
    Grouped = 'Grouped'
    Index = 'Index'
    MultiIndex = 'MultiIndex'
    SeriesStr = 'Series.str'
    SeriesDate = 'Series.dt'


__mapping = {
    TType.DataFrame: ('pd.DataFrame', 100),
    TType.Series: ('pd.Series', 90),
    TType.SeriesStr: ('pd.core.strings.StringMethods', 90),
    TType.SeriesDate: ('pd.Series.dt', 90),
    TType.Pandas: ('pd', 80),
    TType.Grouped: ('pd.core.groupby.DataFrameGroupBy', 80),
    TType.Index: ('pd.Index', 40),
    TType.MultiIndex: ('pd.MultiIndex', 30),
}


_mapping_weight = {
    k: w
    for k, (_, w) in __mapping.items()
}


_mapping_name = {
    k:  v
    for k, (v, w) in __mapping.items()
}


_mapping_type = {
    k: eval(v)
    for k, v in _mapping_name.items()
}


class _MothodMsg(BaseModel):
    type: TType
    method: str


_methods_mapping = {
    k: [_MothodMsg(type=k, method=m)
        for m in dir(v) if m[0] != '_' and m[:1] != '__']
    for k, v in _mapping_type.items()
}

_type2doc_mapping = {
    k:  str(v) + '.{}.__doc__'
    for k, v in _mapping_name.items()
}


class _TMatcher(BaseModel):
    target: str
    method: _MothodMsg
    matched: bool
    score: float = 0


def _match(sm: SequenceMatcher, target: str, method: _MothodMsg):
    target_len = len(target)
    sm.set_seq2(method.method)
    blocks = sm.get_matching_blocks()

    ratio = sm.ratio()

    if ratio <= 0.7 and (blocks[0].a != 0 or blocks[0].size <= target_len * 0.9):
        return _TMatcher(target=target, method=method, matched=False)

    score = ratio * (1.8 if blocks[0].size == target_len else 1)

    score = score * (1.4 if blocks[0].b == 0 else 1)
    return _TMatcher(target=target, method=method, matched=True, score=score)


def _finder(input, collection):
    input = input.replace(' ', '_')
    input_len = len(input)
    sm = SequenceMatcher(lambda x: x in [' '], a=input)

    matches = (
        _match(sm, input, m)
        for m in collection
    )

    filters = (

        dict(type=m.method.type,
             method=m.method.method,
             score=m.score)
        for m in matches
        if m.matched
    )

    filters = sorted(filters, key=lambda v: (
        _mapping_weight[v['type']], v['score']), reverse=True)

    return filters


def get_methods(target, obj_types: List[TType]):
    if TType.Series in obj_types:
        if (TType.SeriesStr not in obj_types):
            obj_types.append(TType.SeriesStr)
        if (TType.SeriesDate not in obj_types):
            obj_types.append(TType.SeriesDate)

    if TType.Pandas not in obj_types:
        obj_types.append(TType.Pandas)

    methods = [_methods_mapping[t] for t in obj_types]
    methods = chain(*methods)

    return _finder(
        target, methods)


def get_doc(type: TType, method: str):
    template = _type2doc_mapping[type]
    code = template.format(method)
    doc = eval(code)

    method_obj = f'{_mapping_name[type]}.{method}'
    method_obj = eval(method_obj)

    sign = f'\n{_mapping_name[type]}.{method}{signature(method_obj)}'

    res = f'''<span style="color: rgb(197, 84, 84);">signature:</span>{sign}
<span style="color: rgb(197, 84, 84);">Docstring:</span>{doc}'''

    return res
