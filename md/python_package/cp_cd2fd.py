from genericpath import exists
import os
import shutil

start_path='/media/ztc/Elements_SE/chhs_batch8/'

dests = ['LA', 'LB', 'UA', 'UB']
nps = ['N', 'P']
target_start_path='/media/ztc/Data/Falldown/'
for dest in dests:
    for np in nps:
        second_path=os.path.join(start_path, f'{dest}/sorted/Falldown/{np}')
        events = os.listdir(second_path)
        for event in events:
            third_path = os.path.join(second_path, event)
            if 'dat' in os.listdir(third_path):
                source_path_dat = os.path.join(third_path, 'dat')
                target_path_dat = os.path.join(target_start_path, f'{dest}/dat1/{np}/{event}')
                shutil.copytree(source_path_dat, target_path_dat)
            for gif in os.listdir(third_path):
                if gif.endswith('.gif'):
                    gif_file = gif
                    source_path_gif = os.path.join(third_path, gif_file)
                    target_path_gif = os.path.join(target_start_path, f'{dest}/gif/{np}')
                    print(source_path_gif)
                    print(target_path_gif)
            
                    shutil.copy(source_path_gif, target_path_gif)
            
            

