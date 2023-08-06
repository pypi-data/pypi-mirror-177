import pandas as pd
import os
import sys
def get_folder_list(main_folder):
    if os.path.exists(main_folder):
        if main_folder.endswith("/") or main_folder.endswith("\\"):
            main_folder = main_folder.replace("/","\\")
        else:
            main_folder = main_folder+"\\"
            main_folder = main_folder.replace("/","\\")
        output = []
        for i,j,k in os.walk(main_folder):
            if j != []:
                if i == main_folder:
                    output = [i+l for l in j]
        return output
    else:
        sys.exit("Path not found")
        
def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total

def get_size(path='.'):
    if os.path.isfile(path):
        return os.path.getsize(path)
    elif os.path.isdir(path):
        return get_dir_size(path)

def get_formatted_size(size = 0):
    GB = 1073741824
    MB = 1048576
    KB = 1024
    if size > 0:
        if size >= GB:
            size = str(round(size/GB,2)) + " GB"
        elif size >= MB:
            size = str(round(size/MB,2)) + " MB"
        else:
            size = str(round(size/KB,2)) + " KB"
    else:
        size = 0
        
    return size

def get_size_df(path="."):
    output = get_folder_list(path)
    folder_size = []
    total_size = 0
    for i in output:
        try:
            size = get_size(i)
            total_size += size
            formatted_size = get_formatted_size(size)

            

            folder_size.append({
                "Folder_Name":i,
                "Size":formatted_size,
                "Status":"OK"
            })
        except:
            folder_size.append({
                "Folder_Name":i,
                "Size":0,
                "Status":"Permission Error"
            })
    folder_size.append({
                "Folder_Name":"TOTAL",
                "Size":get_formatted_size(total_size),
                "Status":""
            })
    
    return folder_size

def get_df(path="."):
    df = pd.DataFrame(get_size_df(path))
    return df