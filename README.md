<!---
lambadmi/lambadmi is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->
Install the VMware to deploy the EVE-NG lab.

VMware deploys eve-ng on the local server.

Need to download netmiko, paramiko packages beforehand.

As the tool uses ntc templates:

Need to download them from the author's github;  "https://github.com/networktocode/ntc-templates"

Download the all the files and try not to change the file directories as the flask requires a specific setup.


----Setting up the topology ------

The network is simulated on the EVE-NG software, which has all the the functionalities of original networking devices.

Need to run the EVE VM from VMware workstation.

Unzip the EVE.zip 

Upload the EVE-COMM-VM-DISK1 virtual disk file in the VM and then start the VM. Need to make sure the VMEM is in the same folder as Virtual Disk File.

The server will be deployed on the LAN and the IP to access the server will be in the running VM


--- Running the code ---

Need to manaully set some environment variables:

SET NTC_TEMPLATES_DIR=/path/to/new/location/templates

SET FLASK_APP = app.py

python -m flask run// Starts the code.

Provide the Source and Desitination IP to start the analysis.
