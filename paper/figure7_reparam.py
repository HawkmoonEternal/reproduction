import csv
import os,shutil,tempfile
from multiprocessing import Manager,Pool
from functools import partial

params_to_write=['detections=[2]', 'Lrange=xrange(3,100)', 'Brange=[2,5]']
brange=[3,4,5,6,7,8]
Brange=[2,5]

class temporary_copy(object):

    def __init__(self,original_path, prefix):
        self.original_path = original_path
        self.prefix=prefix

    def __enter__(self):
        temp_dir = tempfile.gettempdir()
        base_path = os.path.basename(self.original_path)
        self.path = os.path.join(temp_dir,base_path[:-3]+self.prefix+'.py')
        shutil.copy2(self.original_path, self.path)
        return self.path

    def __exit__(self,exc_type, exc_val, exc_tb):
        os.remove(self.path)

manager=Manager()
d=manager.dict()

def multip(name):
    print("starting runs for b="+str(name))
    global d
    global manager
    with temporary_copy('figure7.py',str(name)) as temporary_path_to_copy:
        with open(temporary_path_to_copy,'a') as f:
            #f.write("brange=["+str(param_dict[name][0])+"]\n")
            f.write("packets=100000\n")
            f.write('brange=['+str(name)+']\n')
            for param in params_to_write:
                f.write(param+"\n")
        print(temporary_path_to_copy)
        stream = os.popen("./loops-simulator.py "+temporary_path_to_copy)
        lines=stream.readlines()
        assert(len(lines)>=2)
        index_dict={}
        header=lines[0].split(',')
        for i in range(len(header)):
            if header[i].strip()=='AvgL' or header[i].strip()=='AvgTime' or header[i].strip()=='Th' or header[i].strip()=='AvgB':
                index_dict[header[i].strip()]=i
        assert('Th' in index_dict and 'AvgL' in index_dict and 'AvgTime' in index_dict and 'AvgB' in index_dict)
        d[name]=manager.dict() #one dict per process
        for line in lines[1:]:
            line_split=line.split(',')
            if len(line_split)>=index_dict['AvgTime']:
                B=int(float(line_split[index_dict['AvgB']]))
                if B not in d[name]:
                    d[name][B]=manager.dict()  #one dict per B value
                if int(line_split[index_dict['Th']]) not in d[name][B]:
                    item=manager.list()
                    item.append(manager.list())
                    item.append(manager.list())
                    d[name][B][int(line_split[index_dict['Th']])]=item #one double list per Th 
                if int(line_split[index_dict['Th']]) in d[name][B]:
                    d[name][B][int(line_split[index_dict['Th']])][0].append(float(line_split[index_dict['AvgL']]))
                    d[name][B][int(line_split[index_dict['Th']])][1].append(float(line_split[index_dict['AvgTime']]))

p = Pool(processes = len(brange))
async_result = p.map_async(multip, brange)
async_result.get()
p.close()
p.join()
with open("figure7_reparam.csv", "w+") as csvfile:
    csvwriter=csv.writer(csvfile)
    csvwriter.writerow(['b','AvgB','Th','AvgL', 'AvgTime'])
    for b in brange:
        for B in Brange:
            for Th in d[b][B].keys():
                for L,t in zip(d[b][B][Th][0], d[b][B][Th][1]):
                    csvwriter.writerow([str(b),str(B),str(Th), str(L), str(t)])




