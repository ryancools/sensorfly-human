'''
Created on Sep 27, 2012

@author: imaveek
'''

from odometer import Odometer
from radio import Radio
from magnetometer import Magnetometer
import math
import random
import numpy as np
import copy

from numpy import zeros, int16
import binascii
from xbee import XBee
from __builtin__ import False


#from apiWrapper import data

DES_THRESHOLD = 1.5
TYPE_RSSI = 1
TYPE_OPT = 2
TYPE_MAG =3

class SensorFly(object):
    '''
    SensorFly node
    '''
    #def __init__(self, name, init_xy, init_dir, init_battery, \
    #             noise_vel, noise_turn, noise_radio, noise_mag, fail_prob, controller, case=None):
    def __init__(self, id, init_xy, init_dir, init_battery, \
                 noise_vel, noise_turn, noise_radio, noise_mag, fail_prob, controller, case=None):
    
        '''
        Params: length in no. of cells
                breadth in no. of cells
        '''
        self.name = str(id)
        self.id = id
        
        self.xy = [float(i) for i in init_xy] # In meters
        self.dir = float(init_dir)
        #self.mag_dir = float(init_dir)
        
        self.is_alive = True 
        #self.is_moving = False
        self.is_backing_off = False
        #self.has_turned = False
        
        self.command = Command(0,0,0)
        #self.last_command = Command(0,0,0)
        #self.__real_command = Command(0,0,0)
        #self.command_time_cnt = 0
        
        
        self.noise_velocity = float(noise_vel)
        self.noise_turn = float(noise_turn)
        self.noise_radio = float(noise_radio)
        self.noise_mag = float(noise_mag)
        self.noise_fingerprint = [[self.noise_radio/2,0],[0,self.noise_radio/2]]
        
        '''
        self.odometer = Odometer(self.noise_velocity, self.noise_turn)
        self.radio = Radio(self)
        self.mag = Magnetometer(self)
        '''
        
        self.has_collided = False
        self.is_goal_reached = False
        self.fail_prob = fail_prob
        self.collision_count = 0
        
        # Records estimated location
        self.pf_estimated_xy = np.zeros([1, 2], dtype=np.float32)
        self.dr_estimated_xy = np.zeros([1, 2], dtype=np.float32)
        
        self.pf_particles_xy = np.ones([100, 2], dtype=float) * self.xy
        
        self.sig_match_cnt = 0
        
        # Add references to the central controller
        self.controller = controller
        
        self.last_goal_dir = np.zeros([1, 2], dtype=np.float32)
        self.backoff_time_cnt = 0
        
        if case is not None:
            self.sig_db = case.rf_signature_db
            
        #added by xinlei
        self.des = case.end
        self.certainty = 0
        self.case = case
        
        #added by xinlei for human experiment
        self.id = id
        self.n_anchors = case.num_anchors
        
        self.rssi= zeros(self.n_anchors)
        self.rssi_rcving_flag = False
        #self.rssi_rcv_all = False
        self.rssi_cnt_stop = 10
        
        self.mag_dir = float(init_dir)
        
        self.mag_rcving_flag = False    #flag for getting mag data from explorer and forward to phone
        self.mag_rcd_flag = False       #flag for recording mag data
        
        self.map_init_dir = 0                #direction from magnetometer for X+ (just for offset)
        
        self.opt = 0
        self.opt_rcving_flag = False    #flag for getting opt data from explorer and forward to phone
        self.opt_rcd_flag = False       #flag for recording opt data
        
        self.real_updated = False       #flag for update position in real arena
        
        self.gnd_trth_rcd_flag = False      #flag for recording ground truth position
        self.rst_opt_flag = False       #flag for reseting optical flow
        self.des_addr = '\x01'+chr(self.id)
        
        self.pf_updated_flag = False    #flag for updating particle filter
        self.cmd_set_flag = False       #flag for setting command for explorers
        
        self.state = "Unregistered"     #sensorfly state
        
        self.file_rcd_flag = False      # flag for put the record to file
        
        
        
        # flag for print state
        self.p_flag_1 = True
        self.p_flag_2 = True
        
        self.sig_xy = [float(i) for i in init_xy]   #the location for matching signature
        
    def setMoveCommand(self, command_params):
        '''
        Params: turn - the angle to turn in degrees
                time - the time to setMoveCommand in seconds
        '''
        self.is_moving = True
        [turn, time, velocity] = command_params 
        # Set the command_params to be executed now
        self.command.time = float(time)
        self.command.turn = float(turn)
        self.command.velocity = float(velocity)
        
        #self.__real_command = copy.deepcopy(self.command)
        #self.__real_command.velocity = self.odometer.velocity(velocity)
        #self.__real_command.turn = self.odometer.turn(turn)
        #self.command_time_cnt = self.__real_command.time
        
        # Store the last executed command_params
        #self.last_command = copy.deepcopy(self.__real_command)
        
        
    def update(self, deltick, arena):
        '''
        Params: deltick - the time tick in seconds
        '''
        # Move
        #if self.is_moving:
            # Turn instantly in first tick
            #if (self.command_time_cnt == self.__real_command.time):
        if self.has_turned == False:
            self.dir = (self.dir + self.__real_command.turn) % 360
            self.has_turned = True
        #self.has_turned = True
        #    else:
                #self.has_turned = False
                
            # Get the magnetometer reading for direction
         #   self.mag_dir = self.mag.getDirection()
                
            # Set the time taking into account the tick size    
         #   if (self.command_time_cnt - deltick <= 0):
         #       deltime = self.command_time_cnt
         #       self.command_time_cnt = 0
         #   else:
          #      self.command_time_cnt = self.command_time_cnt - deltick
          #      deltime = deltick
                
            
        oldpos = self.xy
        newx = self.xy[0] + ((self.__real_command.velocity * deltime) * \
                             math.cos(math.radians(self.dir)))
        newy = self.xy[1] + ((self.__real_command.velocity * deltime) * \
                             math.sin(math.radians(self.dir)))
        newpos = [newx, newy]
                        
        is_collision = self.isCollision(oldpos,newpos,arena)
            
            # If no collision setMoveCommand to new point
        if is_collision == False:
            self.xy = [newx, newy]
        else: # Else stop at object boundary
            self.is_moving = False
            self.command_time_cnt = 0
            self.is_backing_off = False
             
            # If the movement is complete
        #if (self.command_time_cnt == 0):
        #    self.is_moving = False
        #    self.is_backing_off = False
                
            #added by xinlei
        if np.linalg.norm(np.array(self.xy) - np.array(self.des)) < DES_THRESHOLD:
            self.is_goal_reached = True 
            
        
        
    
    def isCollision(self, oldpos, newpos, arena):
        '''
        Compute if collision
        '''        
        [oldX, oldY] = arena.gridmap.xytocell(oldpos)
        [newX, newY] = arena.gridmap.xytocell(newpos)
        covCells = self.bresenhamLine(oldX, oldY, newX, newY)
        for c in covCells:
            if arena.gridmap.map[c[0]][c[1]] == arena.gridmap.v_obstacle: # hit obstacle
                self.has_collided = True
                self.collision_count += 1
              #  print "collision "  #added by xinlei
              #  print self.name #added by xinlei
                p = random.random()
                if (p < self.fail_prob):
                    self.is_alive = False
                return True
        self.has_collided = False
        return False


    def bresenhamLine(self,x,y,x2,y2):
        # Brensenham line algorithm
        steep = 0
        coords = []
        dx = abs(x2 - x)
        if (x2 - x) > 0: sx = 1
        else: sx = -1
        dy = abs(y2 - y)
        if (y2 - y) > 0: sy = 1
        else: sy = -1
        if dy > dx:
            steep = 1
            x,y = y,x
            dx,dy = dy,dx
            sx,sy = sy,sx
        d = (2 * dy) - dx
        for _ in range(0,dx):
            if steep: coords.append((y,x))
            else: coords.append((x,y))
            while d >= 0:
                y = y + sy
                d = d - (2 * dx)
            x = x + sx
            d = d + (2 * dy)
        coords.append((x2,y2))
        return coords
    
    
    def getRadioSignature(self):
        # modified by xinlei, using the real signature instead of distance
       # anchors = [1,2,3,4]#,5,6]
        anchors = [1,2,3,4]
        signature = np.zeros(self.case.num_anchors,np.float32)
        for i in range(1,self.case.num_anchors+1):
            [x,y] = self.xytocell(self.xy)
            signature[i-1] = self.sig_db[(x-1,y-1,i)]+np.random.randn()*self.noise_radio/2
             
        return signature
#        signature  = np.random.multivariate_normal(self.xy, self.noise_fingerprint)
        #self.radio.rss(self.controller.anchors)
    #return signature
    
    def xytocell(self, xy):
        X = int(round(xy[0]))
        Y = int(round(xy[1]))
        if X < 0:
            X = 0
#        elif X >= 10:
            #X = 10-1
        #    modified by xinlei
        elif X> self.case.aw:
            X = self.case.aw-1
        if Y < 0:
            Y=0
#        elif Y >= 7:
#            Y=7-1
        elif Y >= self.case.al:
            Y=self.case.al-1

        return [X,Y]
    
    #****************************************************************************************                
    #     For communication
    #****************************************************************************************
    
    def _rssi_rcv_all(self):
        for i in range(0,self.n_anchors):
            if (self.rssi[i]==0):
                return False
        return True
    
    def reset_rssi(self):
        self.rssi = zeros(self.n_anchors)
        #self.rssi_rcv_all = False
    
    
    def get_rssi(self,xbee):
        rssi_cnt=0
        while (self.rssi_rcving_flag == True and rssi_cnt<self.rssi_cnt_stop):
            try:
                response = xbee.wait_read_frame()
                #print response
                addr = response.get('source_addr')
                if (int(('0x' + binascii.hexlify(addr[0])),16)==1 and int(('0x' + binascii.hexlify(addr[1])),16)==self.id):    #get the data from explorer id 
                    rf_data = response.get('rf_data')
                    if (int(('0x' + binascii.hexlify(rf_data[0])),16)==TYPE_RSSI):   # get RSSI package
                        for i in range(0,self.n_anchors):
                            ancho_id = int(('0x' + binascii.hexlify(rf_data[2*i+1])),16)
                            #if (self.rssi[ancho_id-1] == 0):    #has not got new rssi after reset
                            rssi_get = int(('0x' + binascii.hexlify(rf_data[2*i+2])),16)
                            self.rssi[ancho_id-1] += rssi_get
                            #print "got rssi from: ", ancho_id, ' rssi: ', rssi_get
                        rssi_cnt += 1
                        print "rssi get ",rssi_cnt
        
            except KeyboardInterrupt:
                return
         
        self.rssi_rcving_flag = False
        for i in range(0,self.n_anchors):
            self.rssi[i] /=self.rssi_cnt_stop 
        self.print_rssi()            
        return
    
    def print_rssi(self):
        print "rssi"
        for i in range(0,self.n_anchors):
            print i+1,self.rssi[i]
            
            
            
    def get_opt_mag(self,xbee, data):
        #if (self.mag_rcving_flag == True or self.opt_rcving_flag == True):
        #print "running get_opt_mag outside"
        if (self.mag_rcving_flag == True or self.opt_rcving_flag == True):
            try:
        #        print "running get_opt_mag"
                response = xbee.wait_read_frame()
                addr = response.get('source_addr')
                if (int(('0x' + binascii.hexlify(addr[0])),16)==1 and int(('0x' + binascii.hexlify(addr[1])),16)==self.id):    #get the data from explorer id 
                    rf_data = response.get('rf_data')
                    if (int(('0x' + binascii.hexlify(rf_data[0])),16)==TYPE_MAG and self.mag_rcving_flag == True):   # get MAG package
                        #put parse MAG package here
                        #print "MAG package"
                        mag_data = (int(('0x' + binascii.hexlify(rf_data[1])),16) *256 + int(('0x' + binascii.hexlify(rf_data[2])),16))
                        mag_data = int16(mag_data)
                        mag_data = (mag_data+360)%360
                        
                        #data[self.id]['rotation'] = str(mag_data)
                        data[self.id]['rotation'] = float(mag_data)
                        
                        #data[self.id]['rotation'] = mag_data
                
                
                        
                        #print "magdata:",mag_data
                        #if record the data
                        if (self.mag_rcd_flag):
                            self.mag_dir = mag_data
                            self.mag_rcd_flag = False
                            # need send a reset command to Multiwii
                        #send MAG data to phone
                    elif (int(('0x' + binascii.hexlify(rf_data[0])),16)==TYPE_OPT and self.opt_rcving_flag == True):   # get opt package
                        #put parse opt package here
                        #print "OPT package"
                        opt_data = int(('0x' + binascii.hexlify(rf_data[1])),16) *256 + int(('0x' + binascii.hexlify(rf_data[2])),16)
                        #opt_data = float(opt_data)
                        #data[self.id]['distance'] = str(opt_data)
                        data[self.id]['distance'] = float(opt_data)/1000
                        
                        #data[self.id]['distance'] = opt_data

                        #print "distance:", opt_data
                         #if record the data
                        if (self.opt_rcd_flag):
                            self.opt = opt_data
                            self.opt_rcd_flag = False
                            # need send a reset command to Multiwii
                        
                        #send OPT data to phone
      
            except KeyboardInterrupt:
                return
                
        return    
    
    def send_rst_opt(self,xbee):    
        if (self.rst_opt_flag==True):
            for i in range (0,10):
                xbee.tx(dest_addr=self.des_addr,data='\x05\x01')
                self.rst_opt_flag = False
                print self.id,"reset"
#****************************************************************************************                
#     Helper Classes
#****************************************************************************************
class Command:
    '''
    Command for SensorFly nodes
    '''
    
    def __init__(self, turn, time, velocity):
        '''
        Constructor
        '''
        self.turn = turn
        self.time = time
        self.velocity = velocity
        
    @staticmethod
    def fromList((turn, time, velocity)):
        '''
        Constructor
        '''
        return Command(turn, time, velocity)
    
