# from models.methodsRouter import MethodItem
from typing import List
from fastapi import APIRouter, Query


import pandas_query_tool.models.dataModel as dataModel
from pandas_query_tool.models.dataModel import TType
from pandas_query_tool.internal.response import MyResponse
from pydantic import BaseModel


class MethodItem(BaseModel):
    type: TType
    method: str
    score: float

    @staticmethod
    def query(input: str, types: List[TType]):
        return dataModel.get_methods(input, types)


router = APIRouter(
    prefix='/api/method',
    tags=['methods'],
    default_response_class=MyResponse
)


@router.get('/', response_model=List[MethodItem])
def query(input: str, obj_types: List[TType] = Query([TType.DataFrame, TType.Series])):

    objs = dataModel.get_methods(input, obj_types)
    items = (
        MethodItem(**d)
        for d in objs
    )
    return items


class DocQueryModel(BaseModel):
    type: TType
    method: str


@router.post('/doc', response_model=str)
def get_doc(model: DocQueryModel) -> str:
    return dataModel.get_doc(model.type, model.method)
