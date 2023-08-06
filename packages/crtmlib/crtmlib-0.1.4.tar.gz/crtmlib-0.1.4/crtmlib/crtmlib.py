try:
    import sys
    import boto3
    import json
    import s3fs
    import datetime
    from datetime import timedelta, date
    import pyspark.sql.types as T
    # import pandas as pd
    from pyspark.sql.types import *
    from pyspark import SparkConf, SparkContext
    from pyspark.sql import functions as F
    from pyspark.sql import SQLContext, SparkSession, Window, DataFrame, Row
    from pyspark.sql.functions import (
        col,
        coalesce,
        lit,
        concat,
        substring,
        dayofweek,
        month,
        current_date,
        substring_index,
        length,
        decode,
        to_date,
        date_format
    )
    from pyspark.sql.utils import AnalysisException
    from datetime import datetime, timedelta
    from datetime import date
    import psycopg2
    import io

    import importlib.util
    from abc import ABC, abstractmethod
    print("All Modules ok .....   ")
except Exception as e:
    print("Error :{} ".format(e))

########################################################################################################
########################################################################################################
########################################################################################################

global AWS_BUCKET_NAME
global AWS_ACCESS_KEY
global AWS_SECRET_KEY
global AWS_REGION_NAME

AWS_BUCKET_NAME = None
AWS_ACCESS_KEY = None
AWS_SECRET_KEY = None
AWS_REGION_NAME = None


class AWSS3(object):

    """Helper class to which add functionality on top of boto3 """

    def __init__(self, bucket=AWS_BUCKET_NAME):
        self.BucketName = bucket
        self.client = boto3.client("s3",
                                   aws_access_key_id=AWS_ACCESS_KEY,
                                   aws_secret_access_key=AWS_SECRET_KEY,
                                   region_name=AWS_REGION_NAME)

    def put_files(self, Response=None, Key=None):
        """
        'Intenta' poner el fichero en S3
        :return: Bool
        """
        try:

            DATA = bytes(json.dumps(Response).encode('UTF-8'))

            response = self.client.put_object(
                ACL='private',
                Body=DATA,
                Bucket = self.BucketName,
                Key=Key
            )
            return 'ok'
        except Exception as e:
            print("Error : {} ".format(e))
            return 'error'

    def item_exists(self, Key):
        """Comprueba si el key existe en AWS S3"""
        try:
            response_new = self.client.get_object(Bucket=self.BucketName, Key=str(Key))
            return True
        except Exception as e:
            return False

    def get_item(self, Key):

        """Devuelve los Data-Bytes de AWS S3"""

        try:
            response_new = self.client.get_object(Bucket=self.BucketName, Key=str(Key))
            return response_new["Body"].read()
        except Exception as e:
            print("Error", e)
            return False

    def find_one_update(self, data=None, key=None):

        """
        Función que comprueba si el key está en S3,
        si está, devuelve el dato de S3, si no está,
        la guarda en S3 y la devuelve
        """

        flag = self.item_exists(Key=key)

        if flag:
            data = self.get_item(Key=key)
            return data

        else:
            self.put_files(Key=key, Response=data)
            return data

    def get_all_keys(self ,Prefix=''):
        """
        Devuelve una lista de keys
        :param Prefix: Prefix string
        :return: Keys List
        """

        paginator = self.client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=self.BucketName, Prefix=Prefix)

        tmp = []

        for page in pages:
            for obj in page['Contents']:
                tmp.append(obj['Key'])

        return tmp

    def print_tree(self):
        keys = self.get_all_keys()
        for key in keys:
            print(key)
        return None

    def find_one_similar_key(self, searchTerm=''):
        keys = self.get_all_keys()
        return [key for key in keys if re.search(searchTerm, key)]

    def __repr__(self):
        return "AWS S3 Helper class "


class LoaderInterface(ABC):

    @abstractmethod
    def get_instance(self):
        """Fetch the Scrappers from DB """
        pass


class Loaderinterface(ABC):

    @abstractmethod
    def get_instance(self):
        pass


class Loader(Loaderinterface, AWSS3):

    #Constructor: se aporta el key del elemento script en S3
    def __init__(self, Key='script/etl/CALIDAD/QDATA_009/funciones_pruebas_lib.py'):
        self.Key = Key
        AWSS3.__init__(self)

    #Función que retorna el módulo formado al 'importar/descargar' el elemento script
    def get_instance(self, bucket, access, secret, region):
        
        #Tomando variables del establecimiento de credenciales
        AWS_BUCKET_NAME = bucket
        AWS_ACCESS_KEY = access
        AWS_SECRET_KEY = secret
        AWS_REGION_NAME = region

        response = self.get_item(Key=self.Key)
        my_name = 'my_module'
        my_spec = importlib.util.spec_from_loader(my_name, loader=None)
        my_module = importlib.util.module_from_spec(my_spec)
        exec(response, my_module.__dict__)

        return my_module

#Al crear librería, son las llamadas para la ejecución ligera (así se llama a las funciones en s3)
"""
crtm.CRTM(bucket_name, access_key, secret_key, region_name)
helper = crtm.Loader(Key='script/etl/CALIDAD/QDATA_009/funciones_pruebas_lib.py')   #Llamada al constructor de la clase
instance = helper.get_instance()   #Formación de la instancia
#instance.imprime()
"""
