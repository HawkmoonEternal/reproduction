import matplotlib.pyplot as plt
import csv

inputname="figure7_reparam.csv"
inputname_old="figure2_reparam.csv"
outputname="figure7_re_final.pdf"

x_float=True
y_float=True

x_label="L (# hops)"
y_label="Avg Time (#hops/X) with Th=2"
varied_param_label="b"

xmax=99
xmin=0
ymax=4.3
ymin=1.5

leg_pos="upper left"
plt_rel_times=False

x_axis="AvgL"
y_axis="AvgTime"
varied_param="b"
comp="Th"
fixed_param='AvgB'
fixed_param_val=2

val_dict={}
index_dict={}

val_dict_Th1={}
index_dict_Th1={}

with open(inputname) as csvfile:
    csvreader=csv.reader(csvfile)
    header=next(csvreader)
    for i in range(len(header)):
        if header[i].strip()==x_axis or header[i].strip()==y_axis or header[i].strip()==varied_param or header[i].strip()==comp or header[i].strip()==fixed_param:
            index_dict[header[i].strip()]=i
    assert(x_axis in index_dict and y_axis in index_dict and varied_param in index_dict and comp in index_dict)

    for row in csvreader:
        if len(row)>0 and row[index_dict[varied_param]] != "":
            if int(row[index_dict[fixed_param]])==fixed_param_val:
                if not row[index_dict[varied_param]] in val_dict:
                    val_dict[row[index_dict[varied_param]]]=[[],[],[],[],[]]
                if int(row[index_dict[comp]])==2:
                        val_dict[row[index_dict[varied_param]]][0].append(float(row[index_dict[x_axis]]))
                val_dict[row[index_dict[varied_param]]][int(int(row[index_dict[comp]])/2)].append(float(row[index_dict[y_axis]]))


with open(inputname_old) as csvfile:
    csvreader=csv.reader(csvfile)
    header=next(csvreader)
    for i in range(len(header)):
        if header[i].strip()==x_axis or header[i].strip()==y_axis or header[i].strip()==varied_param or header[i].strip()==comp or header[i].strip()==fixed_param:
            index_dict_Th1[header[i].strip()]=i
    assert(x_axis in index_dict_Th1 and y_axis in index_dict_Th1 and varied_param in index_dict_Th1 and comp in index_dict_Th1)
    
    for row in csvreader:
        if len(row)>0 and row[index_dict_Th1[varied_param]] != "":
            if int(float(row[index_dict_Th1[fixed_param]]))==5:
                if not row[index_dict_Th1[varied_param]] in val_dict_Th1:
                    val_dict_Th1[row[index_dict_Th1[varied_param]]]=[[],[],[],[],[]]
                if int(row[index_dict_Th1[comp]])==1:
                        val_dict_Th1[row[index_dict_Th1[varied_param]]][0].append(float(row[index_dict_Th1[x_axis]]))
                val_dict_Th1[row[index_dict_Th1[varied_param]]][int(row[index_dict_Th1[comp]])].append(float(row[index_dict_Th1[y_axis]]))

fig, ax1 = plt.subplots(figsize=[15,5])

markerstyles=['s','o', 'v', '*', '.', '1','2']
line_index=0
for param, vals in val_dict.items():
    facecolor='none' if line_index==2 else 'full'
    ax1.scatter(vals[0], vals[1],marker=markerstyles[line_index], color='k', label=varied_param_label+"="+param, s=32)
    line_index+=1

L=[x for x in val_dict_Th1.values()][0][0]
b_lists_Th2=[x[1] for x in val_dict.values()]
b_lists_Th1=[x[1] for x in val_dict_Th1.values()]

mins_Th2=[]
mins_Th1=[]
min_index_Th1=[]
min_1_Th2=[]

for i in range(0,int(max(L))-int(min(L))+1):
    mins_Th2.append(min([x[i] for x in b_lists_Th2]))
    mins_Th1.append(min([x[i] for x in b_lists_Th1]))
    min_1_Th2.append(b_lists_Th2[[x[i] for x in b_lists_Th1].index(min([x[i] for x in b_lists_Th1]))-1][i])

if plt_rel_times:
    ax2=ax1.twinx()
    ax2.plot(L, [x/y for x,y in zip(mins_Th2,mins_Th1)], linewidth=3, color='black')
    ax2.plot(L, [x/y for x,y in zip(min_1_Th2,mins_Th1)], linewidth=3, color='black', linestyle=(0,(1,1)))
    ax2.set_ylabel('Relative AvgTime Th=2 vs Th=1')
    ax2.set_ylim(ymin, ymax)

plt.xlim(xmin,xmax)
ax1.set_ylim(ymin, ymax)
plt.xlabel(x_label)
ax1.set_ylabel(y_label)

ax1.grid()
fig.legend(loc=leg_pos, fontsize="large", bbox_to_anchor=(0.075, 0.5, 0.5, 0.45))
fig.tight_layout()
plt.savefig('plots/'+outputname)

plt.show()
                        
    

