'''
Created on Sep 27, 2012

@author: imaveek
'''

from Sim.gridmap import GridMap
import DrunkWalk.drunkwalk as dw
import numpy as np
import os
import random

from xbee import XBee
import serial
from time import sleep

#from apiWrapper import clients

DES_THRESHOLD = 0.5

clients = None
data = None

round = 0



States = ["Unregistered","Registered", "GroundTruth", "Directions", "Rotating", "Rotated", "Moving", "Moved"]

class Controller(object):
    '''
    Simulation Engine
    '''

    def __init__(self, arena):
        '''
        Constructor
        Params: arena - Arena object for the simulation
        '''
        self.arena = arena
        self.explorers = list()
        self.anchors = list()
        self.base = [1, 1]
        self.deltick = []
        
        #added by xinlei
        self.state = "Unregistered"
       
        

    def addExplorer(self, sf):
        '''
        Add a SensorFly to the simulation
        '''
        self.explorers.append(sf)


    def addExplorers(self, explorers):
        '''
        Add list of SensorFly objects in the simulation
        '''
        for sf in explorers:
            self.explorers.append(sf)


    def removeExplorer(self, name):
        '''
        Remove a SensorFly from the simulation
        '''
        self.explorers = filter(lambda sf: sf.name != name, self.explorers)


    def setExplorerStartLocation(self, base):
        # this function sets start locations of explorers around the given
        # "base" and "radius"
        self.base = base
        sfnum = len(self.explorers)
        radius = sfnum * 2

        # get x range
        if base[0] < radius / 2 + 2:
            x_range = range(1, radius)
        elif base[0] > self.arena.gridmap.gridlength - 2 - radius / 2:
            x_range = range(self.arena.gridmap.gridlength -
                            radius - 1, self.arena.gridmap.gridlength - 2)
        else:
            x_range = range(base[0] - radius / 2, base[0] + radius / 2 - 1)

        # get y range
        if base[1] < radius / 2 + 2:
            yrange = range(1, radius)
        elif base[1] > self.arena.gridmap.gridbreadth - 2 - radius / 2:
            yrange = range(self.arena.gridmap.gridbreadth -
                           radius - 1, self.arena.gridmap.gridbreadth - 2)
        else:
            yrange = range(base[1] - radius / 2, base[1] + radius / 2 - 1)

        for sf in self.explorers:
            i = 0
            while i < 100:
                x = random.sample(set(x_range), 1)[0]
                y = random.sample(set(yrange), 1)[0]
                if self.arena.gridmap.map[x][y] != self.arena.gridmap.v_obstacle:
                    sf.x = x
                    sf.y = y
                    break
                i += 1
            if i >= 100:
                return False
        return True

    
    def addAnchor(self, sf):
        '''
        Add a SensorFly to the simulation
        '''
        self.anchors.append(sf)


    def addAnchors(self, anchors):
        '''
        Add list of SensorFly objects in the simulation
        '''
        for sf in anchors:
            self.anchors.append(sf)


    def removeAnchor(self, name):
        '''
        Remove a SensorFly from the simulation
        '''
        self.anchors = filter(lambda sf: sf.name != name, self.anchors)
        
        
    def getExplorers(self):
        return self.explorers
    
    
    def getAnchors(self):
        return self.anchors
    
    
    # added by xinlei
    def _state_cnt(self,xbee,algo,record):
        
        
        for sf in self.explorers:
            #print sf.state,"explorer no.", sf.id
            
            #print clients[sf.id]
            #print data[sf.id]
            if sf.is_goal_reached:
                sf.state = "Moved"
            
            if sf.state == "Unregistered":
                
                #for print
                if sf.p_flag_1:
                    print "explorer",sf.id,',',sf.state
                    sf.p_flag_1 = False
                    sf.p_flag_2 = True
                
            elif sf.state == "Registered":
                
                #for print
                if sf.p_flag_2:
                    print "explorer",sf.id,',',sf.state
                    sf.p_flag_2 = False
                    sf.p_flag_1 = True
                    
                sf.rssi_rcving_flag = True
                sf.gnd_trth_rcd_flag = False
                sf.real_updated = False
                sf.pf_updated_flag = False
                sf.cmd_set_flag = False
                
                
                
            elif sf.state == "GroundTruth":
                
                #for print
                if sf.p_flag_1:
                    print "explorer",sf.id,',',sf.state
                    sf.p_flag_1 = False
                    sf.p_flag_2 = True
                    
                    
                #receive sf.xy
                #print self.state
                
                #sf.is_moving = False
                
                self.updateReal(sf)
                if sf.rssi_rcving_flag:
                    sf.reset_rssi()
                    sf.get_rssi(xbee)
                #print "getting rssi for explorer no.", sf.id
                
                
                #if sf.rssi_rcv_all and sf.cmd_set_flag == False:
                algo.update(clients,sf)   #needed to be changed
                algo.command(clients,sf)
                
                    
                
                sf.file_rcd_flag = False
                    
                #print "explorer no.", sf.id,"[",   sf.command.velocity,sf.command.turn, "}"
                
            elif sf.state == "Directions":
                #for print
                if sf.p_flag_2:
                    print "explorer",sf.id,',',sf.state
                    sf.p_flag_2 = False
                    sf.p_flag_1 = True
                
                
                if not sf.file_rcd_flag:
                    
                        
                    record_str = str(1)+','+ sf.name+','+str(sf.xy[0])+','+ str(sf.xy[1])+','+ \
                               str(sf.pf_estimated_xy[0])+','+str(sf.pf_estimated_xy[1])+','+ \
                               str(sf.dr_estimated_xy[0])+','+str(sf.dr_estimated_xy[1])+','+str(pct_covered)+','+\
                               str(sig_match_cnt)+','+str(sf.certainty)+','+str(sf.rssi[0])+','+str(sf.rssi[1])+','+str(sf.rssi[2])+'\n'
                    with open(filestr,'a') as myfile:
                        myfile.write(record_str)
                    print "Recording"
                    sf.file_rcd_flag = True
     
                
                sf.mag_rcving_flag = True
                sf.mag_rcd_flag = True
                
            elif sf.state == "Rotating":
                
                #for print
                if sf.p_flag_1:
                    print "explorer",sf.id,',',sf.state
                    sf.p_flag_1 = False
                    sf.p_flag_2 = True
                
                #start Rotating
               # print self.state
                
                #sf.is_moving = True
                
                print data
                
                sf.get_opt_mag(xbee, data)
                sf.mag_rcving_flag = True
                sf.mag_rcd_flag = True
                
                
                
                
            elif sf.state == "Rotated":
                
                #for print
                if sf.p_flag_2:
                    print "explorer",sf.id,',',sf.state
                    sf.p_flag_2 = False
                    sf.p_flag_1 = True
                
                #stop rotating
                #print self.state
                
                #sf.is_moving = False
                
                sf.get_opt_mag(xbee,data)
                if sf.mag_rcd_flag:
                    print sf.mag_dir
                sf.mag_rcving_flag = False
                sf.mag_rcd_flag = False
                sf.rst_opt_flag = True
                
                
                #print sf.mag_dir
                #get sf.mag_dir and update
                
            elif sf.state == "Moving":
                
                #for print
                if sf.p_flag_1:
                    print "explorer",sf.id,',',sf.state
                    sf.p_flag_1 = False
                    sf.p_flag_2 = True
                #start moving
                #print self.state
                print data

                #sf.is_moving = True
                
                sf.send_rst_opt(xbee)   #reset px4flow distance calculation
                sf.get_opt_mag(xbee, data)
                sf.opt_rcving_flag = True
                sf.opt_rcd_flag = True
                
            elif sf.state == "Moved":
                
                #for print
                if sf.p_flag_2:
                    print "explorer",sf.id,',',sf.state
                    sf.p_flag_2 = False
                    sf.p_flag_1 = True
                
                sf.gnd_trth_rcd_flag = False
                sf.rssi_rcving_flag = True
                sf.real_updated = False
                sf.cmd_set_flag = False
                sf.pf_updated_flag = False
                
                #sf.is_moving = False
                #sf.has_turned = False
                
                sf.get_opt_mag(xbee,data)
                if sf.opt_rcd_flag:
                    print sf.opt
                sf.opt_rcving_flag =False
                sf.opt_rcd_flag = False
                
               
                
                #print sf.opt
                #get sf.mag_dir and update
                
        
        
    def run(self, num_ticks, case, pbar, it,inputClients, inputData,systemRunning,inputfile_str):
        '''
        Run the simulation
        Params: runtime - time to run in seconds
                deltick - one tick in seconds
        '''
        global clients
        global data
        global filestr
        clients = inputClients
        data = inputData
        filestr = inputfile_str
        #added by xinlei for human experiment    
        ser = serial.Serial('/dev/tty.usbserial-DA017KHH',38400)
        xbee = XBee(ser)
        
        
        #infostr = case.name +','+ str(case.num_explorers) +','+ str(case.num_anchors), case.num_particles, case.max_iterations, \
        #                 case.noise_radio, case.noise_velocity, case.noise_turn, case.noise_mag]
        
        self.c_map = GridMap(np.zeros(self.arena.gridmap.map.shape))
        self.deltick = case.deltick

        # Change the algorithm here
        algo = dw.DrunkWalk(self.explorers, self.c_map, case)
        # Display
        if case.is_display_on_real:
            self.arena.gridmap.displayInit()
        record = []
        
        # Main loop
        state_counter =3
        
        #for tick in range(0, num_ticks):
        while systemRunning[0]:
            
         #   self.state = clients[0]["state"]
            
            
            #pbar.update((num_ticks * it) + tick)
            
            #algo.command()  #get command and set command for each explorer
            #self.updateReal()   #execute command and update SensorFly location in real arena
            #algo.update()   #Update the estimates as per command 
            
            '''
            if (tick%100==0):
                if (state_counter<7):
                    state_counter +=1  
                else:
                    state_counter = 4
            
            self.state = States[state_counter]
            
            self.state = States[4]
            '''
            #update state
            for sf in self.explorers:
                sf.state = clients[sf.id]["state"]
                #sf.state = self.state
            
            
            self._state_cnt(xbee,algo,record)
            
            #sleep(.05)
            
            global pct_covered
            global is_all_covered
            # Record data
            if case.goal_graph:
                [pct_covered, is_all_covered] = case.goal_graph.getCoverage()
            else:
                pct_covered = 0
            
#             goal_reached = [sf.is_goal_reached for sf in self.explorers]
            
            global sig_match_cnt
            
            sig_match_cnt = sum([sf.sig_match_cnt for sf in self.explorers])
            
            '''
            for sf in self.explorers:
                record.append([1, int(sf.name), sf.xy[0], sf.xy[1], \
                               sf.pf_estimated_xy[0], sf.pf_estimated_xy[1], \
                               #sf.dr_estimated_xy[0], sf.dr_estimated_xy[1], pct_covered, sig_match_cnt])
                               sf.dr_estimated_xy[0], sf.dr_estimated_xy[1], pct_covered, sig_match_cnt,sf.certainty,sf.rssi])  #modified by xinlei
            '''
            # Visualize
            if case.is_display_on_real:
                self.arena.gridmap.displayUpdate()
            if case.stop_on_all_covered and case.goal_graph and is_all_covered:
                break
        #target.close()    
        return record


    def cls(self):
        os.system(['clear', 'cls'][os.name == 'nt'])
        # now, to clear the screen

    def updateReal(self,sf):
        '''
        Execute command and update SensorFly location in real arena
        '''
        

        #for sf in self.explorers:
            # If SensorFly is dead continue
        if not sf.is_alive or sf.is_goal_reached or sf.gnd_trth_rcd_flag: 
            return
        print "Running updateReal"
        xy = np.random.random_sample(2)*5
        
        pos = self.arena.gridmap.xytocell(sf.xy)
        self.arena.gridmap.markMap(pos, self.arena.gridmap.v_covered)
        oldpos = pos
        
        # Update
        sf.xy = xy
#        sf.xy = [int(clients[sf.id]['groundTruth']['x']),int(clients[sf.id]['groundTruth']['y'])]
        sf.xy = [int(clients[sf.id]['groundTruth']['x'])+1,int(clients[sf.id]['groundTruth']['y'])+1]
        sf.gnd_trth_rcd_flag = True
        
        print "explorer",sf.id," ",sf.xy
        
        newpos = sf.xy
        
        sf.has_collided = sf.isCollision(oldpos,newpos,self.arena)
        
        if (sf.has_collided):
            print "explorers ",sf.id," collision!"
        
        if np.linalg.norm(np.array(sf.xy) - np.array(sf.des)) < DES_THRESHOLD:
            sf.is_goal_reached = True 
            sf.state = "Moved"
            print "explorers ",sf.id," goal!"
        
        
        
        # Mark new position in arena
        pos = self.arena.gridmap.xytocell(sf.xy)
        self.coverAllInBetween(pos, oldpos, self.arena.gridmap)
        self.arena.gridmap.markMap(pos, self.arena.gridmap.v_node)
        
        #print "explorer ", sf.id, sf.xy
            #print pos

    def coverAllInBetween(self, loc, lastloc, lmap):
        if loc == lastloc:
            return lastloc
        [x, y] = loc
        [x2, y2] = lastloc
        cov_cells = self.bresenhamLine(x, y, x2, y2)
        for c in cov_cells:
            lmap.markMap(c, self.arena.gridmap.v_covered)


    def bresenhamLine(self, x, y, x2, y2):
        # Brensenham line algorithm
        steep = 0
        coords = []
        dx = abs(x2 - x)
        if (x2 - x) > 0:
            sx = 1
        else:
            sx = -1
        dy = abs(y2 - y)
        if (y2 - y) > 0:
            sy = 1
        else:
            sy = -1
        if dy > dx:
            steep = 1
            x, y = y, x
            dx, dy = dy, dx
            sx, sy = sy, sx
        d = (2 * dy) - dx
        for _ in range(0, dx):
            if steep:
                coords.append((y, x))
            else:
                coords.append((x, y))
            while d >= 0:
                y = y + sy
                d = d - (2 * dx)
            x = x + sx
            d = d + (2 * dy)
        coords.append((x2, y2))
        return coords