import matplotlib.pyplot as plt
import csv

############################# Parmeters ################################

inputname="figure7.csv"
outputname="figure7.pdf"

##################

x_axis="AvgL"
y_axis="AvgTime"
varied_param="Th"
fixed_param='AvgB'
fixed_param_val=5

###################
fig_width=10
fig_height=5
label_size=15
x_label="L (# hops)"
y_label="Avg Time (#hops/X)"
varied_param_label="Th"

###################
xlim_min=0
xlim_max=30
ylim_min=0.95
ylim_max=6
y_scale='linear'
leg_pos="upper left"
with_lines=False

########################################################################

val_dict={}
index_dict={}

with open(inputname) as csvfile:
    csvreader=csv.reader(csvfile)
    header=next(csvreader)
    for i in range(len(header)):
        if header[i].strip()==x_axis or header[i].strip()==y_axis or header[i].strip()==varied_param or header[i].strip()==fixed_param:
            index_dict[header[i].strip()]=i
    assert(x_axis in index_dict and y_axis in index_dict and varied_param in index_dict)

    for row in csvreader:
        if len(row)>2 and row[index_dict[varied_param]] != "":
                if not row[index_dict[varied_param]] in val_dict:
                    val_dict[row[index_dict[varied_param]]]=[[],[]]

                val_dict[row[index_dict[varied_param]]][0].append(float(row[index_dict[x_axis]]))
                val_dict[row[index_dict[varied_param]]][1].append(float(row[index_dict[y_axis]]))

plt.figure(figsize=[10,5])
plt.rc('axes', axisbelow=True)
markerstyles=['x','s','o', 'v', '*', '.', '1','2']
line_index=0
for param, vals in val_dict.items():
    if with_lines:
        facecolor='none' if line_index==2 else 'full'
        plt.plot(vals[0], vals[1], linestyle=':',marker=markerstyles[line_index], color='k', fillstyle=facecolor, label=varied_param_label+"="+param, markersize=8)
    else:
        facecolor='none' if line_index==2 else 'k'
        size=16 if line_index==1 else 32
        plt.scatter(vals[0], vals[1],marker=markerstyles[line_index], color='k', facecolors=facecolor, label=varied_param_label+"="+param, s=size)
    line_index+=1

plt.xlim(xlim_min,xlim_max)
plt.ylim(ylim_min, ylim_max)
plt.xlabel(x_label, fontsize=label_size)
plt.xticks(fontsize=label_size)
plt.ylabel(y_label, fontsize=label_size)
plt.yticks(fontsize=label_size)
plt.yscale(y_scale)
plt.grid()
plt.legend(loc=leg_pos, fontsize="large")
plt.savefig('plots/'+outputname)
plt.show()
                        
    

