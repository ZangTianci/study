import json
import function
import os
import numpy as np 
import numpyencoder
Falldown_path = '/media/ztc/Data/Falldown/'
points = ['LA', 'LB', 'UA', 'UB']
f_or_n = ['N', 'P']
result = [[],[]]

for index, fn in enumerate(f_or_n):
    for point in points:
        print("="*20)
        name = f"{point}-{fn}"
            
        reault_path = os.path.join(Falldown_path, point, "result", fn)
        events = os.listdir(reault_path)
        for event in events:
            event_path = os.path.join(reault_path, event)
            falldown_list = function.read_json(filepath=event_path, file='Falldown.json')
            if len(falldown_list) != 0:
                for i in range(len(falldown_list)):
                    # print(event_path)        
                    # print(falldown_list[i]["id"])
                    reault99event_path = os.path.join(Falldown_path, point, "result99", fn, event)
                    # print(reault99event_path)
                    track_json = function.read_json(filepath=reault99event_path, file='tracking.json')
                    for j in range(len(track_json)):
                        if falldown_list[i]["id"] == track_json[j]["BASE"]["id"]:
                            if track_json[j]["EVENT"]["Falldown"]['delay']['enable_recover'] == 1:

                                result[index].append(np.max(track_json[j]["EVENT"]["Falldown"]["recover"]["occurrence_times"]))
                                break
with open(os.path.join(Falldown_path,"rst.json"),"w") as f:
    json.dump(result,f,indent=4,cls=numpyencoder.NumpyEncoder)