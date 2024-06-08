import os
import json
import re

from bs4 import BeautifulSoup
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
    all_words = {}
    exclode_words = []
    exclode_fun = []
    search_words = []
    pattern=r'["\'](.*?)["\']'
    def __init__(self,path,exclode_words=[],exclode_fun=[],search_words=[],pattern=r'["\'](.*?)["\']' ) -> None:
        self.path = path
        self.exclode_fun = exclode_fun
        self.exclode_words = exclode_words
        self.dict_all["root"] = path
        self.pattern = pattern
        self.search_words = search_words
        pass
    def run(self):
        self.set_temp_file()
        self.get_files()
        file = open("all_words.json", "w",encoding='utf-8')
        json_object = json.dumps(self.all_words, ensure_ascii = False)
        file.write(json_object)
    def run_blade(self):
        self.set_temp_file()
        self.get_files()
        file = open("all_words.json", "w",encoding='utf-8')
        json_object = json.dumps(self.all_words, ensure_ascii = False)
        file.write(json_object)
    def pattern_cal_fun(self):
        escaped_names = [re.escape(name) for name in self.exclode_fun]
        name_pattern = '|'.join(escaped_names)
        pattern = rf'\b({name_pattern})\s*\(([^()]*(?:\([^()]*\))*[^()]*)\)|\b\w+->({name_pattern})\s*\(([^()]*(?:\([^()]*\))*[^()]*)\)|\b\w+::({name_pattern})\s*\(([^()]*(?:\([^()]*\))*[^()]*)\)'
        return pattern
    
    def get_paths(self,path=""):
        if(path == ""):
            path = self.path
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                self.files_in_path.append(os.path.join(root, name))
            for name in dirs:
                pass
    def get_files(self,type="php"):
        self.get_paths()
        self.dict_all["files_in_root"] = self.files_in_path
        self.get_file_data(type)
        self.dump_json()
    def read_file(self,path):
        self.current_file = open(path, encoding='utf-8') 
        self.current_file_content = self.current_file.read()
        self.current_file.close()
    def set_temp_file(self):
        self.temp_file = open(self.temp_file_name, "w",encoding='utf-8')
    def dump_json(self):
        json_object = json.dumps(self.dict_all)
        self.temp_file.write(json_object)
    def get_file_data(self,type="php"):
        for path in self.files_in_path :
            try:
                self.read_file(path)
            except:
                continue
            if(type=="php"):
                self.get_words_pattern()
            elif(type == 'blade'):
                self.get_words_blade()
            self.filter_data()
            if(len(self.words) > 0):
                self.dict_temp["path"] = path
                self.dict_temp["words"] = self.words
                self.arr_temp.append(self.dict_temp)
            self.words = []
        self.dict_all["data"] = self.arr_temp
    def extract_arguments(self,call):
        matches = re.findall(self.pattern_cal_fun(), call)
        flat_matches = []
        for match in matches:
            for i in range(0, len(match), 2):  # step by 2 to skip empty captures
                if match[i]:  # check if the function/method name is not empty
                    full_call = f"{match[i]}({match[i+1]})"
                    flat_matches.append(full_call)
        d = []
        for arg in flat_matches :
            l = re.findall(r'["\']([^"\']*?)["\']',  arg)
            l2 = re.findall(r'\((.*?)\)',arg)
            if(len(l) > 0):
                d.extend(l)
            elif(len(l2)>0):
                d.extend(l2)
            else:
                d.append(arg)
        return d

    def get_words_pattern(self):
        file_str = self.current_file_content
        self.words = re.findall(self.pattern,  file_str) 
    def get_words_blade(self):
        file_str = self.current_file_content
        soup = BeautifulSoup(file_str, 'html.parser')
        self.words = [element.strip() for element in soup.stripped_strings]
    def filter_data(self):
            file_str = self.current_file_content    
            arguments = self.extract_arguments(file_str)
            arguments = list(dict.fromkeys(arguments))
            w = [arg.replace("'",'') for arg in self.words]
            w.extend([arg.replace('"','') for arg in w])
            w2 = [arg for arg in w if arg not in arguments]
            w2 = [arg for arg in w2 if arg not in self.exclode_words]
            dic_info = []
            i = 0
            # w2 = w
            for arg in w2 :
                find = [ v for v in self.search_words if arg.find(v) != -1]
                if(len(find) > 0):
                    continue
                i = file_str.find(arg,i+2)
                line = len(file_str[:i].splitlines())
                dic_info.append({"value":arg,"line":line})
                self.all_words[arg]="" 
            # w2 = list(dict.fromkeys(w2))
            self.words = dic_info
            # for arg in w2 :
    