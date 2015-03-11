'''
Created on Nov 3, 2013

@author: imaveek
'''
import random
from numpy import arctan2, degrees, arctan
from unittest import case
from math import atan

CERTAIN_THRESHOLD = 4.5

class CmdBiased():
    
    def __init__(self, case, c_map):
        self.c_map = c_map
        self.goal_graph = case.goal_graph

    def getCommand(self, sf):
        # Biased walk
        # Find current location estimate
        real_cell = self.c_map.xytocell(sf.xy)
        if self.goal_graph:
            self.goal_graph.markCovered(real_cell)
        # if collided backup randomly jump to a new location
        if sf.has_collided:
            command = self.__computeBackoff(sf)
            return command
        # If old command is complete execute new
        if not sf.is_moving:
            est_pos = sf.pf_estimated_xy#sf.dr_estimated_xy##np.array(sf.xy)#
#             est_cell = self.c_map.xytocell(est_pos)
            est_cells = self.c_map.xytocellArray(sf.pf_particles_xy)
            
            
            return self.__getCommandFromGraph(sf, est_cells, est_pos)
        # Return none if no movement is needed
        return None
    
    def __getCommandFromGraph(self, sf, est_cells, est_pos):
        # modified by xinlei, add the direction guidance
        if sf.certainty < CERTAIN_THRESHOLD:        
            if self.goal_graph is None:
                next_dir= self.__getNextDirToDesSample(sf,est_pos)
            else:
                next_dir = self.goal_graph.getNextDirSample(est_cells) 
            
            #added by xinlei, for debugging
#            print sf.name, sf.xy[0], sf.xy[1], est_pos[0], est_pos[1], sf.last_goal_dir, next_dir, sf.dir#, command[0], sf.certainty    

        else: # Randomly pick a direction
            next_dir = random.randrange(0,360,20)
         # modification end  
            
        #print "next_dir",next_dir
            
        if next_dir is None:
            next_dir = sf.last_goal_dir
        sf.last_goal_dir = next_dir
        # Command the sensorfly to move
        command = self.__getTurnTimeVel(sf, est_pos, next_dir)
        
 #       if sf.certainty < CERTAIN_THRESHOLD:        
 #           print command[0]
        
        return command
        
        
    def __getCommandRandom(self, sf, est_cell, est_pos):
        next_pos = random.randrange(0,360,20)
        turn = next_pos - sf.dir
        if (turn < 0):
            turn = turn + 360
        velocity = 1
        time = random.randint(1,10)
        return [turn, time, velocity]
    
    # added by xinlei, get direction to the destination
    def __getNextDirToDesSample(self,sf,est_pos):
        dx = sf.des[0]-est_pos[0]
        dy = sf.des[1]-est_pos[1]
        next_dir = degrees(arctan(dy/dx))
        if dx<0:
            next_dir += 180
        elif dy<0:
            next_dir += 360
        
        return next_dir
            
    
    
    def __computeBackoff(self, sf):
        '''
        Compute backoff on collision
        '''
        # Randomly pick a direction
        sf.is_backing_off = True
        new_dir = random.choice(list(xrange(0,360,20)))
        turn = new_dir - sf.dir
        if (turn < 0):
            turn = turn + 360
        velocity = 1
        time = 2 ** sf.backoff_time_cnt
        return [turn, time, velocity]
    
    
    def __getTurnTimeVel(self, sf, pos, next_dir):
        '''
        Compute the turn time vel
        '''
        if pos is None or next_dir is None:
            return None
        turn = next_dir - sf.dir
        if (turn < 0):
            turn = turn + 360
        velocity = 5#1.0  
        time = 1#5      #modified by xinlei
        
        
        
        return [turn, time, velocity]
        

class CmdRandom():
    
    def __init__(self, case, c_map):
        self.c_map = c_map
        self.goal_graph = case.goal_graph

    def getCommand(self, sf):
        '''
        Compute the command to SensorFly for random walk
        '''
        real_cell = self.c_map.xytocell(sf.xy)
        if self.goal_graph:
            self.goal_graph.markCovered(real_cell)
        # Randomly pick a direction
        if sf.is_moving == False:
            newpose = random.randrange(0,360,20)
            turn = newpose - sf.dir
            if (turn < 0):
                turn = turn + 360
            velocity = 1
            time = random.randint(1,5)
            return [turn, time, velocity]
        return None 
        return [turn, time, velocity]