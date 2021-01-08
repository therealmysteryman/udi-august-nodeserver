#!/usr/bin/env python3

"""
This is a NodeServer for August written by automationgeek (Jean-Francois Tremblay)
based on the NodeServer template for Polyglot v2 written in Python2/3 by Einstein.42 (James Milne) milne.james@gmail.com
"""

import polyinterface
import hashlib
import time
import json
import sys
from copy import deepcopy
from august.api import Api 
from august.authenticator import Authenticator, AuthenticationState


LOGGER = polyinterface.LOGGER
SERVERDATA = json.load(open('server.json'))
VERSION = SERVERDATA['credits'][0]['version']

def get_profile_info(logger):
    pvf = 'profile/version.txt'
    try:
        with open(pvf) as f:
            pv = f.read().replace('\n', '')
    except Exception as err:
        logger.error('get_profile_info: failed to read  file {0}: {1}'.format(pvf,err), exc_info=True)
        pv = 0
    f.close()
    return { 'version': pv }

class Controller(polyinterface.Controller):

    def __init__(self, polyglot):
        super(Controller, self).__init__(polyglot)
        self.name = 'August'
        self.initialized = False
        self.queryON = False
        self.email = ""
        self.password = ""
        self.install_id = ""
        self.tries = 0
        self.hb = 0

    def start(self):
        LOGGER.info('Started Twinkly for v2 NodeServer version %s', str(VERSION))
        self.setDriver('ST', 0)
        try:
            if 'email' in self.polyConfig['customParams']:
                self.email = self.polyConfig['customParams']['email']
            else:
                self.email = ""
                
            if 'password' in self.polyConfig['customParams']:
                self.password = self.polyConfig['customParams']['password']
            else:
                self.password = ""
            
            # Generate a UUID ( 11111111-1111-1111-1111-111111111111 )
            if 'install_id' in self.polyConfig['customParams']:
                self.install_id = self.polyConfig['customParams']['install_id']
            else:
                self.install_id = "" 

            if self.email == "" or self.password == "" or self.install_id == "":
                LOGGER.error('August requires email,password,install_id parameters to be specified in custom configuration.')
                return False
            else:
                self.check_profile()
                self.discover()
                self.query()

        except Exception as ex:
            LOGGER.error('Error starting August NodeServer: %s', str(ex))
           
    def shortPoll(self):
        self.query()

    def longPoll(self):
        self.heartbeat()

    def query(self):
        self.setDriver('ST', 1)
        for node in self.nodes:
            if self.nodes[node].queryON == True :
                self.nodes[node].query()
            self.nodes[node].reportDrivers()

    def heartbeat(self):
        LOGGER.debug('heartbeat: hb={}'.format(self.hb))
        if self.hb == 0:
            self.reportCmd("DON",2)
            self.hb = 1
        else:
            self.reportCmd("DOF",2)
            self.hb = 0

    def discover(self, *args, **kwargs):
        count = 1
        
        api = Api(timeout=20)
        authenticator = Authenticator(api, "email", self.email, self.password, install_id=self.install_id, access_token_cache_file="augustToken.txt")
        authentication = authenticator.authenticate()
        if ( authentication.state is AuthenticationState.AUTHENTICATED ) :
            locks = api.get_locks(authentication.access_token)
            for lock in locks:
                myhash =  str(int(hashlib.md5(locks.device_id.encode('utf8')).hexdigest(), 16) % (10 ** 8))
                self.addNode(AugustLock(self,myhash, "lock_" + str(count) ,  "lock_" + str(count),api, authentication, lock ))
                count = count + 1
        else :
            LOGGER.error('August requires validation')
        
    def delete(self):
        LOGGER.info('Deleting August')

    def check_profile(self):
        self.profile_info = get_profile_info(LOGGER)
        # Set Default profile version if not Found
        cdata = deepcopy(self.polyConfig['customData'])
        LOGGER.info('check_profile: profile_info={0} customData={1}'.format(self.profile_info,cdata))
        if not 'profile_info' in cdata:
            cdata['profile_info'] = { 'version': 0 }
        if self.profile_info['version'] == cdata['profile_info']['version']:
            self.update_profile = False
        else:
            self.update_profile = True
            self.poly.installprofile()
        LOGGER.info('check_profile: update_profile={}'.format(self.update_profile))
        cdata['profile_info'] = self.profile_info
        self.saveCustomData(cdata)

    def install_profile(self,command):
        LOGGER.info("install_profile:")
        self.poly.installprofile()

    id = 'controller'
    commands = {
        'QUERY': query,
        'DISCOVER': discover,
        'INSTALL_PROFILE': install_profile,
    }
    drivers = [{'driver': 'ST', 'value': 1, 'uom': 2}]

class AugustLock(polyinterface.Node):

    def __init__(self, controller, primary, address, name, api, authentication, lock):

        super(TwinklyLight, self).__init__(controller, primary, address, name)
        self.queryON = True
        self.api = api
        self.authentication = authentication
        self.lock = lock

    def start(self):
        self.query()

    def setOn(self, command):
        self.myTwinkly.set_mode('movie')
        self.setDriver('ST', 100,True)
        
    def setOff(self, command):
        self.myTwinkly.set_mode('off')
        self.setDriver('ST', 0,True)
        
    def setBrightness(self, command):
        intBri = int(command.get('value'))
        self.myTwinkly.set_brightness(intBri)
        self.setDriver('GV1', intBri,True)
 
    def query(self):
        if ( self.myTwinkly.getMode() != 'off' ) :
           self.setDriver('ST', 100,True) 
        else :
           self.setDriver('ST', 0,True) 
        
        self.setDriver('GV1', self.myTwinkly.get_brightness() , True)
        pass
                        
    drivers = [{'driver': 'ST', 'value': 0, 'uom': 78},
               {'driver': 'GV1', 'value': 0, 'uom': 51}]

    id = 'TWINKLY_LIGHT'
    commands = {
                    'DON': setOn,
                    'DOF': setOff,
                    'SET_BRI': setBrightness
                }

if __name__ == "__main__":
    try:
        polyglot = polyinterface.Interface('TwinklyNodeServer')
        polyglot.start()
        control = Controller(polyglot)
        control.runForever()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
