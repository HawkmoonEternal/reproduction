import csv
import os,shutil,tempfile
from multiprocessing import Manager,Pool
from functools import partial

outputname='topos_opt_time.csv'
Th=1
#if true use optimal b value else use b_fixed
b_opt=True
b_fixed=4

topos=['attmpls', 'bellsouth','fattree4','geant', 'stanford', 'uscarrier']

params_to_write=['detections=['+str(Th)+']']
class temporary_copy(object):

    def __init__(self,original_path):
        self.original_path = original_path

    def __enter__(self):
        temp_dir = tempfile.gettempdir()
        base_path = os.path.basename(self.original_path)
        self.path = os.path.join(temp_dir,base_path)
        shutil.copy2(self.original_path, self.path)
        return self.path

    def __exit__(self,exc_type, exc_val, exc_tb):
        os.remove(self.path)

manager=Manager()
d=manager.dict()
def multip(name,param_dict):
    print("starting runs for "+name)
    global d
    with temporary_copy('paper/table4-unroller-time-'+name+'.py') as temporary_path_to_copy:
        with open(temporary_path_to_copy,'a') as f:
            f.write("brange=["+str(param_dict[name][0])+"]\n")
            f.write("packets=3000000\n")
            for param in params_to_write:
                f.write(param+"\n")
        stream = os.popen("./loops-simulator.py "+temporary_path_to_copy)
        lines=stream.readlines()

        assert(len(lines)>=2)
        for index in range(len(lines[0].split(','))):
            if lines[0].split(',')[index].strip()=='AvgTime':
                d[name]=float(lines[1].split(',')[index])


param_dict={}
index_dict={}
for topo in topos:
    with open('outputs/topo_params_'+topo+'.csv') as csvfile:
        csvreader=csv.reader(csvfile)
        header=next(csvreader)
        for i in range(len(header)):
            if header[i].strip()=='b' or header[i].strip()=='AvgTime' or header[i].strip()=='Th' or header[i].strip()=='c':
                index_dict[header[i].strip()]=i
        assert('b' in index_dict and 'AvgTime' in index_dict and 'Th' in index_dict)
        for row in csvreader:
            if len(row)>0 and int(row[index_dict['Th']]) ==Th  and int(row[index_dict['c']]) ==1:
                if not topo in param_dict:
                    param_dict[topo]=(-1,-1)
                if param_dict[topo][0]==-1 or float(row[index_dict['AvgTime']])<param_dict[topo][1]:
                    if b_opt:
                        param_dict[topo]=(int(row[index_dict['b']]),float(row[index_dict['AvgTime']]))
                    else:
                        param_dict[topo]=(b_fixed,1.0)

p = Pool(processes = len(topos))
async_result = p.map_async(partial(multip, param_dict=param_dict), topos)
async_result.get()
p.close()
p.join()

with open("outputs/"+outputname, "w+") as csvfile:
    csvwriter=csv.writer(csvfile)
    for topo in topos:
        csvwriter.writerow([topo,param_dict[topo][0], d[topo]])




