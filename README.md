# August-nodeserver

This Poly provides an interface between August Connect and Polyglot v2 server. This a POC and very rough polyglot, but does work to control one lock.

#### Installation

You can install manually :

1. cd ~/.polyglot/nodeservers
2. git clone https://github.com/therealmysteryman/udi-august-nodeserver.git
3. run ./install.sh to install the required dependency.
4. Create a custom variable named email, password and install_id (generate your own UUID)
5. Generate Token file using those scripts (createToken.py,verifyToken.py)
6. Copy file containing the key has to be in this location and need to use that name ( /var/polyglot/nodeservers/AugustLock/augustToken.txt )
