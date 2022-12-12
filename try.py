import codecs
BLOCKSIZE = 1048576 
sourceFileName='data.csv'
targetFileName='new_data.csv'
with codecs.open(sourceFileName, 'r', 'cp1252') as sourceFile:
    with codecs.open(targetFileName,'w',"iso-8859-1") as targetFile:
        while True:
            contents = sourceFile.read(BLOCKSIZE)
            if not contents:
                break
            targetFile.write(contents)