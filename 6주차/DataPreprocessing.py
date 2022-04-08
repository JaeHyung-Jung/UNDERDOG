from tqdm import tqdm
from encodings import utf_8
import sys
import os
import os.path
import time
import json

label_path = "./라벨링데이터"
source_path = "./원천데이터"

del_list = []
class_keys = ['01', '02', '03', '04', '05', '06', '07', '08', '09']

def read_json(path):
    with open(path, 'r', encoding="utf-8") as file:
        data = json.load(file)
        # print(data["annotations"])
        len_data = len(data["annotations"])
        # print(len_data)
        # class_list = []
        flag = False
        for idx in range(len_data):
            # class_list.append(data["annotations"][idx]["class"])
            if any(class_key in data["annotations"][idx]["class"] for class_key in class_keys):
                flag = True
                break
        if flag == False:
            del_path = path.rstrip('.json')
            del_list.append(del_path)
        # print(class_list)
        # class_list.clear()
        
    # return data
    
def search_file(dir):
    files = os.listdir(dir)
    
    for data in files:
        if os.path.isdir(dir + r"/"+data) == True:
            search_file(dir+r"/"+data)
        else:
            read_json(dir+r"/"+data)
            # print(dir+r"/"+data)
            
def del_file(path):
    #label
    if os.path.exists(path + ".json"):
        #pass
        #sys.stdout.write(path + ".json\r")
        #sys.stdout.flush()
        #print(path + ".json", flush=True)
        os.remove(path + ".json")
    #source
    if os.path.exists(source_path + r"/" + path.lstrip(label_path) + ".jpg"):
        #pass
        #sys.stdout.write(source_path + r"/" + path.lstrip(label_path) + ".jpg\r")
        #sys.stdout.flush()
        #print(source_path + r"/" + path.lstrip(label_path) + ".jpg", flush=True)
        os.remove(source_path + r"/" + path.lstrip(label_path) + ".jpg")

# 2020-02-105.공사현장안정장비인식_sample-test

def main():
    top_path = label_path
    search_file(top_path)
    
    for path in tqdm(del_list, unit="항목", desc="전처리 중"):
        #time.sleep(0.01)
        del_file(path)
    
    
if __name__ == "__main__":
    main()