import os
import json
import re
class FileHandler:
    path = ""
    files_in_path = []
    current_file_content =""
    current_file =""
    temp_file =""
    temp_file_name = "temp.json"
    line = 0
    dict_all =  {}
    dict_temp = {}
    arr_temp = []
    words = []
    exclode_words = []
    exclode_fun = []
    pattern=r'["\'](.*?)["\']'
    def __init__(self,path,exclode_words=[],exclode_fun=[],pattern=r'["\'](.*?)["\']' ) -> None:
        self.path = path
        self.exclode_fun = exclode_fun
        self.exclode_words = exclode_words
        self.dict_all["root"] = path
        self.pattern = pattern
        self.set_temp_file()
        self.get_files()
        pass
    def pattern_cal_fun(self,fun):
        return fun+r'\s*\(([^)]*)\)'
    def get_paths(self,path=""):
        if(path == ""):
            path = self.path
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                self.files_in_path.append(os.path.join(root, name))
                # print(os.path.join(root, name))
            for name in dirs:
                pass
    def get_files(self):
        self.get_paths()
                # print(os.path.join(root, name))
        self.dict_all["files_in_root"] = self.files_in_path
        self.get_file_data()
        self.dump_json()
    def read_file(self,path):
        self.current_file = open(path, "r") 
        self.current_file_content = self.current_file.read()
        self.current_file.close()
    def set_temp_file(self):
        self.temp_file = open(self.temp_file_name, "w")
    def dump_json(self):
        json_object = json.dumps(self.dict_all)
        self.temp_file.write(json_object)
    def get_file_data(self):
        for path in self.files_in_path :
            try:
                self.read_file(path)
            except:
                continue
            self.get_words_pattern()
            if(len(self.words) > 0):
                self.dict_temp["path"] = path
                self.dict_temp["words"] = self.words
                self.arr_temp.append(self.dict_temp)
            self.words = []
        self.dict_all["data"] = self.arr_temp
    
    def extract_arguments(self,fun,call):
        match = re.search(self.pattern_cal_fun(fun), call)
        if match:
            arguments_string = match.group(1)
            return [arg.strip() for arg in arguments_string.split(',')]
        else:
            return []
    def get_words_pattern(self):
        file_str = self.current_file_content
        self.words = re.findall(self.pattern,  file_str) 
        arguments = []
        [  arguments.extend(self.extract_arguments(arg,file_str)) for arg in self.exclode_fun ]
        arguments = list(dict.fromkeys(arguments))
        arguments2 = []
        [arguments2.extend(re.findall(r'["\'](.*?)["\']',  arg)) for arg in arguments ]
        arr = [arg.replace("'",'') for arg in arguments2]
        arr.extend([arg.replace('"','') for arg in arguments2])
        arguments2 = list(dict.fromkeys(arr))
        w = [arg.replace("'",'') for arg in self.words]
        w.extend([arg.replace('"','') for arg in self.words])
        w2 = list(dict.fromkeys(w))
        w2 = [arg for arg in w2 if arg not in arguments2]
        w2 = [arg for arg in w2 if arg not in self.exclode_words]
        self.words = {"words":w2}
    