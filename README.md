# AugustLock NodeServer

This Poly provides an interface between August Connect and Polyglot v2 server. This is very rough polyglot, but does work to control one lock. If anyone want to take over this nodeserver for futher enhancement is welcome. Has only been tested on Polisy.

#### Installation

You can install manually or the store:

1. cd ~/.polyglot/nodeservers
2. git clone https://github.com/therealmysteryman/udi-august-nodeserver.git
3. run ./install.sh to install the required dependency.
4. Create a custom variable named email, password ,install_id (generate your own UUID 11111111-1111-1111-1111-111111111111 ), tokenFilePath (Path and Filename were the tokenFile should be generated).
5. First time your run the nodeserver, you should receive a validation code by email, enter the validation code in August Node and click Send Validation. 
   Once your get a message in the log saying it has been validated, restart the node server and your lock should appear.
