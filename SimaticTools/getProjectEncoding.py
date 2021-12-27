import codecs

def getProjectEncoding(projectfolder):
    file = projectfolder + "\\" + "Global" + "\\" + "Language"
    result = []
    try:
        f = open(file)
        languageFile = f.readlines()
        for line in languageFile:
            try:
                result.append(codecs.lookup(line))
            except LookupError:
                continue
        f.close()
    except IOError:
        result.append(codecs.lookup("ISO-8859-1"))
        result.append(codecs.lookup("ISO-8859-1"))
    return result