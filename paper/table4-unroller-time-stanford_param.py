#!/usr/bin/env python2
# -*- coding: utf-8 -*-

packets = 100000
Brange = [5]
Lrange = [20]
detections = [1,2,4]

genloops = False
genpaths = False
topoloops = True
topopaths = False
lbasedpaths = True

topoparser = 'stanford'
topofile = (
	"topologies/stanford-backbone/port_map.txt",
	"topologies/stanford-backbone/backbone_topology.tf")

enunroller = True
enbloomfilter = False

brange = [3,4,5,6,7,8]
cHrange = [(1,1),(2,1),(4,1)]
zrange = [32]
