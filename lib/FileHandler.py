import os
import json

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
    def __init__(self,path,exclode_words=[],exclode_fun=[] ) -> None:
        self.path = path
        self.dict_all["root"] = path
        self.set_temp_file()
        self.get_files()
        pass
    def get_files(self):
        for root, dirs, files in os.walk(self.path, topdown=False):
            for name in files:
                self.files_in_path.append(os.path.join(root, name))
                # print(os.path.join(root, name))
            for name in dirs:
                pass
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
            self.read_file(path)
            self.get_words_between("\"")
            self.get_words_between("\'")
            self.dict_temp["path"] = path
            self.dict_temp["words"] = self.words
            self.arr_temp.append(self.dict_temp)
            self.words = []
        self.dict_all["data"] = self.arr_temp
    def get_words_between(self,char="\""):
        i=0
        i2 = 0
        while(i != -1 and i2 != -1):
            # temp_str = self.current_file_content[i2+1:]
            i = self.current_file_content.find(char,i2+1)
            i2 = self.current_file_content.find(char,i+1) 
            word = self.current_file_content[(i+1):i2]
            if(word.find("\n")==-1):
                self.words.append({"word":word,"line":self.current_file_content.rfind("\n",0,i2+1) })
            

	

    