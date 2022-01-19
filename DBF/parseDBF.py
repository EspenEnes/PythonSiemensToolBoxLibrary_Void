# import pandas as pd
from dbfread import DBF


class ParseDBF(DBF):
    def __init__(self, file, encoding=None):
        if encoding:
            super(ParseDBF, self, ).__init__(file, encoding=encoding)
        else:
            super(ParseDBF, self, ).__init__(file, raw=True)

    def getColumns(self, columns, encoding=None):
        for column in columns:
            if not self.isPresent(column):
                return None
        result = list()
        for record in self.records:
            newColumns = {}
            for column in columns:
                if encoding:
                    newColumns[column] = record[column]  # .decode(encoding).strip()
                else:
                    newColumns[column] = record[column]
            result.append(newColumns)
        return iter(result)

    # def toPandasDataFrame(self, deleted=False, encoding=None):
    #     df = pd.DataFrame(self.__iter__())
    #     df["DELETED_FLAG"] = b"False"
    #     if deleted:
    #         df = df.append(self.getDeletedPandasDataFrame())
    #     if encoding:
    #         df = df.apply(lambda x: x.str.decode(encoding=encoding))
    #     return df
    #
    # def getDeletedPandasDataFrame(self, flag="DELETED_FLAG"):
    #     df = pd.DataFrame(iter(self.deleted))
    #
    #     if not df.empty:
    #         df[flag] = b"True"
    #     return df

    def isPresent(self, name):
        return name in self.field_names or False


