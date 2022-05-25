from operator import index
import os
import os.path
import json

class_keys = ['01', '02', '03', '04', '05', '06', '07', '08']
cnt_class_keys = [0, 0, 0, 0, 0, 0, 0, 0]
data_count = 0
data_cnt_list = []

def read_json(path, del_list):
    global data_count
    with open(path, 'r', encoding="utf-8") as file:
        data = json.load(file)
        # len_data = len(data["annotations"])
        flag = False
        for annotations in data["annotations"]:
            if any(class_key in annotations["class"] for class_key in class_keys):
                flag = True
                data_count += 1
                cnt_class_keys[int(annotations["class"]) - 1] += 1
        if flag == False:
            del_path = data["image"]["filename"].rstrip(".jpg")
            del_list.append(del_path)

def del_specific(index_list, source_path, source_dir_len, path):
    print("  ㄴ다른 장비 처리중...")
    del_list = []
    #print(index_list)
    for index in index_list:
        if index == "5.전체":
            continue
        json_list = os.listdir(path + index)
        #print(json_list)
        for data in json_list:
            del_list.append(data.rstrip(".json"))
        for file in del_list:
            #label
            if os.path.exists(path + index + r"/" + file + ".json"):
                pass
                #print(path + index + r"/" + file + ".json")
                os.remove(path + index + r"/" + file + ".json")
            
            #source
            if source_dir_len == 0:
                if os.path.exists(source_path + r"/" + file + ".jpg"):
                    #pass
                    #print(source_path + r"/" + file + ".jpg")
                    os.remove(source_path + r"/" + file + ".jpg")
            else:
                if os.path.exists(path.replace("[라벨]", "[원천]") + file + ".jpg"):
                    #pass
                    #print(path.replace("[라벨]", "[원천]") + file + ".jpg")
                    os.remove(path.replace("[라벨]", "[원천]") + file + ".jpg")
        
        if os.path.exists(path + index):
            os.rmdir(path + index)
        
        del_list.clear()
    print("  ㄴ완료.")
    # print(del_list)

def del_all(index_list, source_path, source_dir_len, path):
    if "5.전체" not in index_list:
        return
    print("  ㄴ선별 처리 중...")
    del_list = []
    index = "5.전체"
    json_list = os.listdir(path + index)
    #print(json_list)
    for data in json_list:
        read_json(path + index + r"/" + data, del_list)
    #print(del_list)
    for file in del_list:
        #label
        if os.path.exists(path + index + r"/" + file + ".json"):
            #pass
            #print(path + index + r"/" + file + ".json")
            os.remove(path + index + r"/" + file + ".json")
        
        #source
        if source_dir_len == 0:
            if os.path.exists(source_path + r"/" + file + ".jpg"):
                #pass
                #print(source_path + r"/" + file + ".jpg")
                os.remove(source_path + r"/" + file + ".jpg")
        else:
            if os.path.exists(path.replace("[라벨]", "[원천]") + file + ".jpg"):
                #pass
                #print(path.replace("[라벨]", "[원천]") + file + ".jpg")
                os.remove(path.replace("[라벨]", "[원천]") + file + ".jpg")
    del_list.clear()
    print("  ㄴ완료.")
    # print(del_list)

def delete(label_list, path):
    global data_count
    for iter in label_list:
        print(iter.lstrip("[라벨]") + " 처리중...")
        location_list = os.listdir(path + iter)
        #print(location_list)
        source_path = "[원천]" + iter.lstrip("[라벨]")
        source_dir_len = 0
        source_file_list = os.listdir(path + source_path)
        for file in source_file_list:
            if os.path.isdir(path + source_path + r"/" + file) == True:
                source_dir_len += 1
        #print(source_path)
        for location in location_list:
            print("ㄴ" + location + " 처리 중...")
            index_list = os.listdir(path + iter + r"/" + location)
            #print(index_list)
            if "1.안전장비만" in index_list:
                safety = index_list.pop(index_list.index("1.안전장비만"))
                safety_list = os.path.listdir(path + iter + r"/" + location + r"/" + safety)
                data_count += len(safety_list)
            del_specific(index_list, path + source_path, source_dir_len, path + iter + r"/" + location + r"/")
            del_all(index_list, path + source_path, source_dir_len, path + iter + r"/" + location + r"/")
            
        print("")

def processing(dir):
    print("Processing for %s" % (dir))
    file_list = os.listdir("./" + dir)
    for data in file_list:
        if os.path.isfile("./" + dir + r"/" + data) == True:
            file_list.pop(file_list.index(data))
    if "키포인트" in file_list:
        file_list.pop(file_list.index("키포인트"))
    #print(file_list)
    label_list = list(filter(lambda x: x.startswith("[라벨]"), file_list))
    #print(label_list)
    delete(label_list, "./" + dir + r"/")

def main():
    global data_count
    root_dir = "."
    root_list = os.listdir(root_dir)
    #print(root_list)
    root_list.pop(root_list.index("DataPreprocessing.py"))
    for data in root_list:
        if os.path.isdir(root_dir + r"/" + data) == False:
            root_list.pop(root_list.index(data))
    #print(root_list)
    for dir in root_list:
        processing(dir)
        data_cnt_list.append(data_count)
        data_count = 0
    
    print("전체 데이터 수: %d" % (data_cnt_list[0] + data_cnt_list[1]))
    print("훈련 데이터 수: %d" % (data_cnt_list[0]))
    print("검증 데이터 수: %d" % (data_cnt_list[1]))
    print("데이터 비율 : 훈련/검증 %.2f/%.2f "% (data_cnt_list[0]/(data_cnt_list[0] + data_cnt_list[1])*100, data_cnt_list[1]/(data_cnt_list[0] + data_cnt_list[1])*100))
    
    print("")
    
    for i, v in enumerate(cnt_class_keys):
        print("class %d : %d"%(i+1, v))

if __name__ == "__main__":
    main()