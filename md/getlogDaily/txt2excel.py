import pandas as pd
import numpy
import os
import xlrd
path='/media/ztc/Data/work/LOG/2022-06-12/20/chhs/'
filelist = os.listdir(path)
for filename in filelist:
	if filename.endswith(".txt"):
		df=pd.read_csv(
			f'/media/ztc/Data/work/LOG/2022-06-12/20/chhs/{filename}',
			sep=',',
			header=None,
			engine='python',
			encoding="utf-8"
		)
		df=df.T
		df.to_excel(f'/media/ztc/Data/work/LOG/2022-06-12/20/chhs/{filename}.xls', index=False)
