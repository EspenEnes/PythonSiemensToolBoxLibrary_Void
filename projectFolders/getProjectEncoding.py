import codecs

def getProjectEncoding(parent=None, projectFolder=None):
    # if projectFolder, use projectfolder, else use parent.projectFolder
    if projectFolder:
        pass
    elif hasattr(parent, "projectFolder"):
        projectFolder = parent.projectFolder
    else:
        return None

    file = fr"{projectFolder}\Global\Language"
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