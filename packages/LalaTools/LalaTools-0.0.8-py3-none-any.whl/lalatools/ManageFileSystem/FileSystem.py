import os

def delHead(path):
    if(type(path)==str):
        re_path = os.path.basename(path)
        return re_path
    elif(type(path)==list):
        re_path = [os.path.basename(_path) for _path in path]
        return re_path
    else:
        raise TypeError("Now type(path) is "+str(type(path))+". path type need to be 'list' or 'str'.")
    
def replaceSplitMark(path,mark="/"):
    if(type(path)==str):
        re_path = path.replace("\\\\","\\").replace("\\","/").replace("/",mark)
        return re_path
    elif(type(path)==list):
        re_path = [filepath.replace("\\\\","\\").replace("\\","/").replace("/",mark) for filepath in path]
        return re_path
    else:
        raise TypeError("Now type(path) is "+str(type(path))+". path type need to be 'list' or 'str'.")

def getFileList(path, isDir=True, isFile=True, abs=None, all=False, extension="", contain="", mark="/"):
    onlyfiles = []
    onlydirs = []
    if(extension!=""):
        if(extension[0]!="."):extension='.'+extension
    if(all):
        if(abs==None):abs=True
        if(isFile):onlyfiles = [os.path.join(curDir, file) for curDir, dirs, files in os.walk(path) for file in files if file.endswith(extension) if contain in file]
        if(isDir and extension==""):onlydirs = [os.path.join(curDir, dir) for curDir, dirs, files in os.walk(path) for dir in dirs if contain in dir]
    else:
        if(abs==None):abs=False
        if(isFile):onlyfiles = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) if f.endswith(extension) if contain in f]
        if(isDir and extension==""):onlydirs = [os.path.join(path, f) for f in os.listdir(path) if os.path.isdir(os.path.join(path, f)) if contain in f]
    fs = onlyfiles + onlydirs
    fs = replaceSplitMark(fs, mark=mark)
    if(abs==False):fs = [os.path.basename(_path) for _path in fs]
    fs.sort()
    return fs


# print(dir_list)
# print(onlyfiles)
# print(onlyfolders)
# print(os.walk('./')['root'])

# def getFsTree(startpath):
#     for root, dirs, files in os.walk(startpath):
#         level = root.replace(startpath, '').count(os.sep)
#         indent = ' ' * 4 * (level)
#         print('{}{}/'.format(indent, os.path.basename(root)))
#         subindent = ' ' * 4 * (level + 1)
#         for f in files:
#             print('{}{}'.format(subindent, f))
            

# import os
 
# for curDir, dirs, files in os.walk("./"):
#     for file in files:
#         if file.endswith(".py"):
#             print(os.path.join(curDir, file).replace("/","\\"))
    
# onlyfiles = [os.path.join(curDir, file).replace("/","\\") for curDir, dirs, files in os.walk("./") for file in files]
# print(type("asfafds"))


# https://www.sejuku.net/blog/63816