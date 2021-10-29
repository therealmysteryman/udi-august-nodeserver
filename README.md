## This nodeserver has been converted to run on PG3. The code has been moved to https://github.com/UniversalDevicesInc-PG3/udi-august-nodeserver


# AugustLock NodeServer

This Poly provides an interface between August Connect and Polyglot v2 server. This is very rough polyglot, but does work to control one lock. Has only been tested on Polisy. The status will update based on the shortPoll value.
*Experimental use at your own risk*

#### Installation

You can install manually or the store:

1. Install from Polyglot Store
2. In polyglot on the nodesever AugustLock create the following configuration variable
   - email - email to access August Account
   - password - password to access August Account
   - install_id - generate a random uuid (11111111-1111-1111-1111-111111111111)
   - tokenFilePath - Path and Filename were the tokenFile should be generated ( /var/polyglot/nodeservers/AugustLock/token.txt )
                     The directory must exist and the user running polyglot must have read/write access
3. First time your run the nodeserver, you should receive a validation code by email, enter the validation code on August Node in ISY994 and click Send Validation. 
4. Once your get a message in the log saying it has been validated, restart the node server and your lock should appear.
