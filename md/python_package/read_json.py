import json
import os
import numpy as np

def read_json():
    location = ["LA", "LB", "UA", "UB"]
    tf = ["N", "P"]
    for loc in location:
        for torf in tf:
            path1=f'/media/ztc/Data/Falldown/{loc}/result/{torf}/'
            events = os.listdir(path1)
            for event in events:
                path = os.path.join(path1, event)
                file='tracking.json'
                filepath = os.path.join(path, file)
                with open(filepath, mode='r', encoding='utf8') as js:
                    json_data = json.load(js)
                for i in range(len(json_data)):
                    arr = json_data[i]['EVENT']['Falldown']['recover']['occurrence_times']
                    n = len(arr)
                    for m in range(n):
                        for j in range(0, n-m-1):
                            if arr[j] > arr[j+1] :
                                arr[j], arr[j+1] = arr[j+1], arr[j]
                    if arr[-1]>0:
                        print(torf)
                        print(event)
                        print(f"id={i}")
                        print(f"occurrence_times_max={arr[-1]}")
                

if __name__ == '__main__':
    read_json()