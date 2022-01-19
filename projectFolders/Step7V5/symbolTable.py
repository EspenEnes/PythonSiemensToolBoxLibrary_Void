from DBF import ParseDBF


class SymbolTable():
    def __init__(self):
        self.folder = None
        self.Name = None
        self._symbols = None
        self._loaded = False


    def load(self):
        dbf = ParseDBF(f"{self.folder}\\SYMLIST.DBF")
        sym = {}
        for row in dbf.records:
            operand = "".join(x.strip() for x in row["_OPHIST"].decode("ISO-8859-1").split())
            sym[operand] = {}

            sym[operand]["symbol"] = row["_SKZ"]
            sym[operand]["operand"] = row["_OPHIST"]
            sym[operand]["operandIEC"] = row["_OPIEC"]
            sym[operand]["dataType"] = row["_DATATYP"]
            sym[operand]["comment"] = row["_COMMENT"]
        self._symbols = sym
        self._loaded = True
        return sym

    # @property
    # def symbols(self):
    #     if not self._loaded:
    #         self.load()
    #     return self._symbols

    def __getitem__(self, item):
        if not self._loaded:
            self.load()

        try:
            return self._symbols[item]["symbol"]
        except KeyError:
            return None




