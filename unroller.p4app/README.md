
# Unroller.p4app

The core part of P4 implementation of Unroller is situated in the `unroller.p4` file. It also includes other files from `includes/` defining parser, deparser, metadata or headers data structures.

Configuration file `p4app.json` defines the application in the environment of p4app tool. This file extends the standard enviroment using a custom implementation of AppController and AppProcRunner classes. Standard configuration options including the ways how to override the default controller and runner are described in the original p4app Github repository (https://github.com/p4lang/p4app).

Custom classes in `customization.py` file enables to start a tool which simulates a switch controller. The tool `tools/digest_client.py` reads and prints digest messages generated by the switch running Unroller. It utilizes `tools/bmpy_utils.py` (https://github.com/p4lang/behavioral-model/blob/master/tools/bmpy_utils.py) the original Python API of BMv2 switch implementation to communicate with the switch using the thrift interface. Finally, the custom controller implementation executes also the tool `packet_generator.py` to generate an initial packet entering the first switch. The tool than captures the output of the switch (packet with modified Unroller header) and uses it as an input for the next switch on the configured path.

You can edit parameters of the loop / path or the algorithm at the beginning of `customization.py` file:

```
# List of switch IDs visited before the loop
UNROLLER_B = [1]

# List of switch IDs of the loop
UNROLLER_L = [6, 3, 2, 7]

# The threshold for reporting a loop
UNROLLER_TH = 1
```