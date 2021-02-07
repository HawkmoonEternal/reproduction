import csv
import os,shutil,tempfile
from multiprocessing import Manager,Pool
from functools import partial

outputname='topos_opt_oh_Th2.csv'
Th=2
b_opt=True #use best b value
b_fixed=4
z_min=1
z_max=32
topos=['attmpls', 'bellsouth','fattree4','geant', 'stanford', 'uscarrier']

params_to_write=['detections=['+str(Th)+']', 'zrange = xrange('+str(z_max)+','+str(z_min)+',-1)']

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
    with temporary_copy('paper/table4-unroller-bits-'+name+'.py') as temporary_path_to_copy:
        with open(temporary_path_to_copy,'a') as f:
            f.write("brange=["+str(param_dict[name][0])+"]\n")
            for param in params_to_write:
                f.write(param+"\n")
        stream = os.popen("./loops-simulator.py "+temporary_path_to_copy)
        lines=stream.readlines()
        header=lines[0].split(',')
        assert(len(lines)>=2)
        index_dict={}
        for i in range(len(header)):
            if header[i].strip()=='FP%' or header[i].strip()=='Mem':
                index_dict[header[i].strip()]=i
        for line in lines[1:]:
            vals=line.split(',')
            if len(vals)>1:
                if float(vals[index_dict['FP%']])==float(0):
                    d[name]=float(vals[index_dict['Mem']])

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
    csvwriter.writerow(['topology', 'b', 'bit-overhead'])
    for topo in topos:
        csvwriter.writerow([topo,param_dict[topo][0], d[topo]])




