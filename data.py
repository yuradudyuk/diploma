import xarray as xr
from pandas import to_datetime as tdt
import numpy as np

names_of_conc=['no2_conc','o3_conc','so2_conc','pm2p5_conc','pm10_conc','co_conc']
names_of_files=['no_2spring.nc','ozon_spring.nc','so2_spring.nc','pm2.5_spring.nc','pm10_spring.nc','co_spring.nc']
names_of_outfiles=['no2_for_matrix.txt','o3_for_matrix.txt','so2_for_matrix.txt','pm2p5_for_matrix.txt','pm10_for_matrix.txt','co_for_matrix.txt']

class preload:
    def __init__(self,days,infile,name_chemical,outfile):
        self.days=days*6
        self.infile=infile
        self.name_chemical=name_chemical
        self.outfile=outfile
    def do_everything(self):
        days=days*6
        ds = xr.open_dataset(self.infile)
        df = ds.to_dataframe().reset_index()
        start_date = tdt('2021-03-01')
        df['time'] = start_date + df['time']
        time=np.array(df['time'])[:self.days]
        vykydy=[]
        for i in range(self.days):
            dd=df[df['time']==time[i]]
            chemical=np.array(dd[self.name_chemical])
            vykydy.append((chemical.sum()/9855))
        result_data = []
        for i in range(0,self.days,6):
            ser = (vykydy[i] + vykydy[i+1] + vykydy[i+2] +vykydy[i+3] + vykydy[i+4] + vykydy[i+5])/6
            result_data.append(ser)
        len_of_result_data=len(result_data)
        f=open(self.outfile,'w')
        for i in range (len_of_result_data):
            f.write(str(result_data[i])+'\n')
        f.close()
    def __del__(self):
        print('deleted')



ozon= preload(92,names_of_files[1],names_of_conc[1],names_of_outfiles[1])
so2=preload(92,names_of_files[2],names_of_conc[2],names_of_outfiles[2])
pm2p5=preload(92,names_of_files[3],names_of_conc[3],names_of_outfiles[3])
pm10=preload(92,names_of_files[4],names_of_conc[4],names_of_outfiles[4])
