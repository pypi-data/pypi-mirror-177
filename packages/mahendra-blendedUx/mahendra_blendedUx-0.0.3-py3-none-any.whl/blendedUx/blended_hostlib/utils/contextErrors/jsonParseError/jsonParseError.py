import os
import re 
import sys
cur_dir = os.path.dirname(os.path.abspath(__file__))
jsonLinterFilePath = os.path.join( cur_dir, 'jsonLinter.js')
file = open(jsonLinterFilePath, 'r',encoding='utf8')
jsonLinter = {'content': file.read()}
os_name = sys.platform.lower()

def createAnnotationArray(result,absolutePath):
    array = []
    for item in result['warnings']: 
        error = {
            "type": "json_parse_error",
            "message": item["message"],
            "location": {
                "line": item['line'],
                "column": item['column'],
                "templatePath": absolutePath,
                "lineTxt": re.sub("/^\s+|\s+$/g","",result['lines'][item['line']])
            }
        }
        array.append(error)
    return array

def jsonParseError(absolutePath, meta_location):
        inputs = {
            'fileContent': open(absolutePath,'r').read(),
            'absolutePath': meta_location
        }
        requireFunctionCode = '''
        function requireJsonParse() {
            const jsonLinter = %s;
            var code = `
            (function a(){
                var module = { exports: {} };
                var exports = module.exports;
                var global = {};
                
                ` +  jsonLinter['content'] + `;

                return module.exports;})()`;
            return eval(code);
        };
        
        
        const jsonParseError = requireJsonParse().jsonParseError;
        const inputs = %s; 
        '''%(jsonLinter,inputs)
        
        if os_name.startswith('linux') or os_name.startswith('darwin'):
            from py_mini_racer import py_mini_racer
            ctx = py_mini_racer.MiniRacer()
        else:
            import execjs
            ctx = execjs.get()
        code = '''(function(){ %s return jsonParseError(inputs['fileContent'], inputs['absolutePath'])})()'''%(requireFunctionCode)
        result = ctx.eval(code)    
        errors = createAnnotationArray(result,meta_location)
        return errors

        

        
        
