import os
import clr
import pandas as pd
import collections
import mozartpy.dataconverter as dc

filedir = os.path.dirname(os.path.abspath(__file__))
dllFolder = os.path.join(filedir, 'dlls')
clr.AddReference(os.path.join(dllFolder, 'Mozart.Task.Model.dll'))
clr.AddReference(os.path.join(dllFolder, 'Mozart.DataActions.dll'))

from Mozart.Task.Model import ModelEngine
from Mozart.DataActions import ILocalAccessor

class Model:
    """
    Baseclass for mozart model object. Return the Input/Output DataItem with Pandas DataFrame object

    :properties
        name(string) : File name of the vmodel file
        inputs(list<string>) : String list of the Input DataItem names(from input data schema)
        outputs(list<string>) : String list of the Output DataItem names(from output data schema)
        path(string) : Full path for the vmodel file
        experiments(list<string>) : String list of the output Experiment names
        results : Dictionary of output result for each experiment

    """
    def __init__(self, path):
        self.__engine = None
        self.name = ''
        self.results = []
        self.inputs = []
        self.outputs = []
        self.path = path
        self.resultDic = collections.defaultdict(list)
        self.__readModel()

    def __readModel(self):
        ''' Initialize by reading the model

        '''
        self.__engine = ModelEngine.Load(self.path)
        self.name = self.__engine.Name

        for item in self.__engine.Inputs.ItemArray:
            self.inputs.append(item.Name)

        for experiment in self.__engine.Experiments:
            for result in experiment.ResultList:
                self.resultDic[experiment.Name].append(result.Key)

        for result in self.__engine.Experiments[0].ResultList:
            self.results.append(result.Key)

        for item in self.__engine.Outputs.ItemArray:
            self.outputs.append(item.Name)

    def GetInputItem(self, key):
        """
        Return the Input DataItem with Pandas DataFrame object

        :param key: Input DataItem name which is the same as vdat file name under Data folder
        :return: Converted Pandas DataFrame from Input DataItem whose table name is the parameter (key)
        """
        acc = ILocalAccessor(self.__engine.LocalAccessorFor(key))
        dt = acc.QueryTable('', -1, -1)
        df = dc.TableToDataFrame(dt)
        return df

    def GetOutputItem(self, key, exp_name='Experiment 1', rst_name='Result 0'):
        """
        Return the Output DataItem with Pandas DataFrame object for a given table name (key) under Experiment (exp_name) and Result (rst_name)

        :param key: Output DataItem name(string)
        :param exp_name: Output Experiment name(string, defaultValue = 'Experiment 1')
        :param rst_name: Output Result name(string, defaultvalue='Result 0')
        :return: Converted Pandas DataFrame from Output DataItem whose table name is the parameter (key) under Experiment (exp_name) and Result (rst_name)
        """

        if key == '':
            print('{0} is not found key'.format(key))
            pass

        if not self.outputs.__contains__(key):
            print('{0} is not found output item name'.format(key))
            pass

        result = self.__GetResult(exp_name, rst_name)
        if result is None:
            print('{0} is not found result'.format(rst_name))
            pass

        try:
            acc = ILocalAccessor(result.LocalAccessorFor(key))
            dt = acc.QueryTable('', -1, -1)
            df = dc.TableToDataFrame(dt)
            return df
        except Exception as err:
            print(str(err))

    def __GetResult(self, exp_name, key):
        for exp in self.__engine.Experiments:
            if exp.Name != exp_name:
                continue
            for result in exp.ResultList:
                if result.Key == key:
                    return result
        # for result in self.__engine.Experiments[0].ResultList:
        #     if result.Key == key:
        #         return result

    # def GetOutputItemByCvs(self, exp_name, rname, key):
    #     if key == '':
    #         print('{0} is empty'.format(key))
    #         pass
    #
    #     if not self.outputs.__contains__(key):
    #         print('{0} is not found key'.format(key))
    #         pass
    #
    #     result = self.__GetResult(exp_name, rname)
    #     if result is None:
    #         print('{0} is not found result'.format(rname))
    #         pass
    #
    #     try:
    #         acc = ILocalAccessor(result.LocalAccessorFor(key))
    #         filepath = os.path.join(acc.DataDirectory, key)
    #         df = pd.read_csv(filepath + '.csv')
    #         return df
    #     except Exception as err:
    #         print(str(err))
