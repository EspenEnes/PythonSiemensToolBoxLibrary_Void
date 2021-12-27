from dbfread import DBF
import pandas as pd
from collections import OrderedDict
from itertools import chain

class ParseDBF(DBF):
    def __init__(self, file, encoding=None):
        super(ParseDBF, self, ).__init__(file, raw=True)





    def getColumns(self, columns, encoding=None):
        for column in columns:
            if not self.isPresent(column):
                return None
        result = list()
        for record in self.records:
            newColumns = OrderedDict()
            for column in columns:
                if encoding:
                    newColumns[column] = record[column].decode(encoding).strip()
                else:
                    newColumns[column] = record[column]
            result.append(newColumns)
        return iter(result)



    def toPandasDataFrame(self, deleted=False, encoding=None):
        df = pd.DataFrame(self.__iter__())
        df["DELETED_FLAG"] = b"False"
        if deleted:
            df = df.append(self.getDeletedPandasDataFrame())
        if encoding:
            df = df.apply(lambda x: x.str.decode(encoding = encoding))
        return df

    def getDeletedPandasDataFrame(self, flag="DELETED_FLAG"):
        df = pd.DataFrame(iter(self.deleted))

        if not df.empty:
            df[flag] = b"True"
        return df

    def isPresent(self, name):
        return name in self.field_names or False




if __name__ == '__main__':
    dbf = ParseDBF("C:\\Users\\espen\\PycharmProjects\\SimaticToolbox\\tests\integration\\fixtures\\G9837_SMI_SW_Sf_20200817_Rev\\G9837_SM\\ombstx\\offline\\00000002\\BAUSTEIN.DBF")
    for x in dbf.getColumns(["ID"], "ISO-8859-1"):
        print(x)
    df = dbf.toPandasDataFrame(deleted=True, encoding="ISO-8859-1")

