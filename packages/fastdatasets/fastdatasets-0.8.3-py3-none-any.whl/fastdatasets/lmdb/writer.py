# @Time    : 2022/10/27 18:24
# @Author  : tk
# @FileName: kv_writer.py

import typing
import json
import pickle
import numpy as np
import data_serialize
from tfrecords import LMDB

__all__ = [
    'LMDB',
    'pickle',
    'json',
    'DataType',
    'data_serialize',
    'WriterObject',
    "StringWriter",
    "BytesWriter",
    "JsonWriter",
    "PickleWriter",
    "FeatureWriter",
    "NumpyWriter",
]

class DataType:
    int64_list = 0
    float_list = 1
    bytes_list = 2


class WriterObject:
    def __init__(self,filename,options=LMDB.LmdbOptions(env_open_flag = 0,
                env_open_mode = 0o664, # 8进制表示
                txn_flag = 0,
                dbi_flag = 0,
                put_flag = 0),
                map_size=1024 * 1024 * 1024):
        self.options = options
        self.file_writer = LMDB.Lmdb(filename,options=options,map_size=map_size)

    def __del__(self):
        self.close()

    def close(self):
        if self.file_writer is not None:
            self.file_writer.close()
            self.file_writer = None

    def put_batch(self, keys: typing.List[typing.Union[str, bytes]], values: typing.List[typing.Union[str, bytes]]):
        return self.file_writer.put_batch(keys, values)

    def put(self,key : typing.Union[bytes,str],value : typing.Union[bytes,str]):
        self.file_writer.put(key,value)

    def get(self,key : typing.Union[bytes,str],default_value=None):
        return self.file_writer.get(key,default_value)

    def remove(self,key : typing.Union[bytes,str],):
       return self.file_writer.remove(key)




class StringWriter(WriterObject):
    def put(self, key : typing.Union[bytes,str],value : typing.Union[bytes,str],*args, **kwargs):
        return self.file_writer.put(key,value)

    def put_batch(self,keys : typing.List[typing.Union[str , bytes]],values : typing.List[typing.Union[str , bytes]],*args, **kwargs):
        return self.file_writer.put_batch(keys, values)

class BytesWriter(WriterObject):
    def put(self, key : typing.Union[bytes,str],value : typing.Union[bytes,str],*args, **kwargs):
        return self.file_writer.put(key,value)

    def put_batch(self, keys: typing.List[typing.Union[str, bytes]], values: typing.List[typing.Union[str, bytes]],*args, **kwargs):
        return self.file_writer.put_batch(keys, values)

class PickleWriter(WriterObject):
    def put(self, key : typing.Union[bytes,str],value,*args, **kwargs):
        return self.file_writer.put(key,pickle.dumps(value,*args,**kwargs))

    def put_batch(self, keys: typing.List[typing.Union[str, bytes]], values: typing.List[typing.Union[str, bytes]],*args, **kwargs):
        return self.file_writer.put_batch(keys, [pickle.dumps(value,*args,**kwargs) for value in values])

class JsonWriter(WriterObject):
    def put(self,key : typing.Union[bytes,str],value : typing.Union[bytes,str],*args, **kwargs):
        return self.file_writer.put(key,json.dumps(value,*args,**kwargs))

    def put_batch(self, keys: typing.List[typing.Union[str, bytes]], values: typing.List[typing.Union[str, bytes]],*args, **kwargs):
        return self.file_writer.put_batch(keys, [json.dumps(value,*args,**kwargs) for value in values])

class FeatureWriter(WriterObject):
    def put(self,key : typing.Union[bytes,str],feature : typing.Dict,*args, **kwargs):
        assert feature is not None
        dict_data = {}
        for k,v in feature.items():
            val = v['data']
            if v['dtype'] == DataType.int64_list:
                dict_data[k] = data_serialize.Feature(int64_list=data_serialize.Int64List(value=val))
            elif v['dtype'] == DataType.float_list:
                dict_data[k] = data_serialize.Feature(float_list=data_serialize.FloatList(value=val))
            elif v['dtype'] == DataType.bytes_list:
                dict_data[k] = data_serialize.Feature(bytes_list=data_serialize.BytesList(value=val))
            else:
                raise Exception('bad dtype')

        feature = data_serialize.Features(feature=dict_data)
        example = data_serialize.Example(features=feature)
        return self.file_writer.put(key,example.SerializeToString())

    def put_batch(self, keys: typing.List[typing.Union[str, bytes]], values: typing.List[dict],*args, **kwargs):

        real_values = []
        for value in values:
            feature: dict = value
            dict_data = {}
            for k, v in feature.items():
                val = v['data']
                if v['dtype'] == DataType.int64_list:
                    dict_data[k] = data_serialize.Feature(int64_list=data_serialize.Int64List(value=val))
                elif v['dtype'] == DataType.float_list:
                    dict_data[k] = data_serialize.Feature(float_list=data_serialize.FloatList(value=val))
                elif v['dtype'] == DataType.bytes_list:
                    dict_data[k] = data_serialize.Feature(bytes_list=data_serialize.BytesList(value=val))
                else:
                    raise Exception('bad dtype')

            feature = data_serialize.Features(feature=dict_data)
            example = data_serialize.Example(features=feature)
            real_values.append(example.SerializeToString())
        return self.file_writer.put_batch(keys,real_values)




class NumpyWriter(WriterObject):
    def put(self,key: typing.Union[str, bytes],feature : typing.Dict,*args, **kwargs):
        assert feature is not None
        dict_data = {}
        for k, v in feature.items():
            assert isinstance(v, np.ndarray)
            if v.dtype.kind == 'i':
                value_key = 'int64'
                val = v.reshape((-1,)).tolist()
            elif v.dtype == np.float32:
                value_key = 'float32'
                val = v.reshape((-1,)).tolist()
            elif v.dtype == np.float or v.dtype == np.float64:
                value_key = 'float64'
                val = v.reshape((-1,)).tolist()
            elif v.dtype.kind == 'S':
                value_key = 'bytes'
                val = v.tobytes()
            else:
                raise Exception('bad dtype', k, v.dtype)
            kwargs_data = {
                "header": '',
                "dtype": str(v.dtype),
                "shape": list(v.shape),
                value_key: val,
            }
            dict_data[k] = data_serialize.NumpyObject(**kwargs_data)
        example = data_serialize.NumpyObjectMap(numpyobjects=dict_data)
        self.file_writer.put(key,example.SerializeToString())

    def put_batch(self, keys: typing.List[typing.Union[str, bytes]], values: typing.List[dict],*args, **kwargs):
        data_output = []
        for feature in values:
            dict_data = {}
            for k, v in feature.items():
                assert isinstance(v, np.ndarray)
                if v.dtype.kind == 'i':
                    value_key = 'int64'
                    val = v.reshape((-1,)).tolist()
                elif v.dtype == np.float32:
                    value_key = 'float32'
                    val = v.reshape((-1,)).tolist()
                elif v.dtype == np.float or v.dtype == np.float64:
                    value_key = 'float64'
                    val = v.reshape((-1,)).tolist()
                elif v.dtype.kind == 'S':
                    value_key = 'bytes'
                    val = v.tobytes()
                else:
                    raise Exception('bad dtype', k, v.dtype)
                kwargs_data = {
                    "header": '',
                    "dtype": str(v.dtype),
                    "shape": list(v.shape),
                    value_key: val,
                }
                dict_data[k] = data_serialize.NumpyObject(**kwargs_data)
            example = data_serialize.NumpyObjectMap(numpyobjects=dict_data)
            data_output.append(example.SerializeToString())
        self.file_writer.put_batch(keys,data_output)