import os
from json_source_map import calculate
from blendedUx.blendedcli.settings import BLENDED_DIR as theme_path

UNDEFINED_ERROR = "undefined_pointer"

def getErrorFileInfo(ref_path, project_object):
    temp = project_object
    filePath = ''
    jsonPointer = ''
    for i,sub_path in enumerate(ref_path): 
        if sub_path.endswith('.json'):
            filePath = temp['_meta_'+sub_path]['location']
            temp = temp[sub_path]
            if i < len(ref_path)-1: 
                jsonPointer = '/' + '/'.join(ref_path[i+1:])
                break
        else: 
            temp = temp[sub_path]
                
    errorFileInfo = {
        "filePath": filePath,
        "jsonPointer": jsonPointer
    }
    return errorFileInfo

def formatErrorPath(location):
    location = os.path.relpath(location,theme_path)
    location = location.split(os.sep)        
    if location[1] == 'src':
        accountSlug, theme = location[0], location[2]
        location = f'/'.join(location[3:])
        # location = os.path.join('-'.join([accountSlug, theme]),location)
    elif location[1] == 'lib':
        location =  os.path.join(location[3],f'{os.sep}'.join(location[5:]) )
        location = os.path.join('_package.json','dependencies', location )
    return location

def getFileContent(location):
    content = ''
    lines = [] 
    with open(location, 'r') as f : 
        content = f.read()
    with open(location, 'r') as f:
        lines = f.readlines()
    return content, lines

def getFormattedError(line, column, fileName, lineTxt):
    newError = {
        "type": UNDEFINED_ERROR,
        "message": "there is a undefined pointer error for ",
        "location": {
            "line": line+1, 
            "column": column+1,
            "templatePath": fileName, 
            "lineTxt": lineTxt
        }
    }
    return newError    
    
def nullUndefinedError(ref_path, project_object):
    errorFileInfo = getErrorFileInfo(ref_path, project_object)
    errorFileName = formatErrorPath(errorFileInfo['filePath'])
    errorJsonPointer = errorFileInfo['jsonPointer']
    jsonFileContent, jsonLineByLine = getFileContent(errorFileInfo['filePath'])
    jsonLineInfo = calculate(jsonFileContent)
    jsonLineInfo = jsonLineInfo[errorJsonPointer+'/$ref'].value_start  # 0-based indexing for line no and column no 
    jsonLineTxt = jsonLineByLine[jsonLineInfo.line].strip()
    error = getFormattedError(jsonLineInfo.line, jsonLineInfo.column, errorFileName, jsonLineTxt)
    return error
    
            
    