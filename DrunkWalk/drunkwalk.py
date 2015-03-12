'''
Created on 2012-10-4

@author: Administrator
'''
from robotpf import RobotPF
import math
import numpy as np
from cmdalgo import CmdBiased
# from cmdalgo import CmdRandom
from landmark import LandmarkDB

class DrunkWalk(object):
    '''
    DrunkWalk deployment algorithm
    '''

    def __init__(self, sflist, c_map, case):
        '''
        Constructor
        '''
        self.sflist = sflist
        self.noise_model = [case.noise_turn, case.noise_velocity]
        
        self.c_map = c_map
        self.goal_graph = case.goal_graph
                
        # Command algo
        self.cmd_algo = CmdBiased(case, c_map)
#         self.cmd_algo = CmdRandom(case, c_map)

        self.deltick = case.deltick
        
        # Initialize particle filters for each SensorFly dir
        self.pfilters = {}
        for sf in self.sflist:
            pf = RobotPF(sf, case.num_particles, case.init_p_wt, \
                                       self.noise_model, case.deltick)
            self.pfilters[sf.name] = pf
            sf.pf_estimated_xy = np.array(sf.xy, np.float32)
            
        # record the actual position without pf correction
        self.dr_estimated_pos = {}
        for sf in sflist:
            self.dr_estimated_pos[sf.name] = [sf.xy, sf.dir]
            sf.dr_estimated_xy = np.array(sf.xy, np.float32)
        
        # Iniitialize a landmark database    
        self.landmark_db = LandmarkDB(case)

            
           
    def command(self,clients,sf):
        '''
        Command as per the planning algorithm
        '''
        

        
        #for sf in self.sflist:
        if (not sf.is_goal_reached) and (not sf.cmd_set_flag):  #this if condition is added by xinlei
            print "Running command"
            cmd = self.cmd_algo.getCommand(sf)
            
            print sf.id, cmd
            #added by xinlei for human experiment testing
            sf.cmd_set_flag = True
            # send the command by wifi
            
            clients[sf.id]['directions']['rotate']=cmd[0]
            clients[sf.id]['directions']['move']=cmd[1]*cmd[2]
            clients[sf.id]['directions']['valid'] = True
            
            if cmd:
                sf.setMoveCommand(cmd)
    
    
    def update(self,clients,sf):
        '''
        Update the estimates as per command 
        '''
        

        #for sf in self.sflist:
        if (not sf.is_goal_reached) and (not sf.pf_updated_flag):  #this if condition is added by xinlei
            # Particle filter update
            print "Running update"
            if not sf.has_collided:
                pf = self.pfilters[sf.name]
                # Predict
                pf.predict(sf.command)
                # Correct
                #pf.correct(self.landmark_db)
                entropy_not_done = pf.correct(self.landmark_db,sf) #modified by xinlei
                
                
                #added by xinlei
                pf.normalizeWts()   
                if entropy_not_done:
                    pf.certainty = pf.getEntropy(pf.weights)
                
                #print pf.certainty
                
                # Resample
                pf.resample_fast()
                # Record estimated location
                sf.pf_estimated_xy = pf.getEstimate()
                sf.pf_particles_xy = pf.particles_xy
                
                #added by xinlei
                sf.certainty =  pf.certainty
                    
            # Dead reckoning update
            if not sf.has_collided:
                pos = self.dr_estimated_pos[sf.name]
                # Get direction from magnetometer
                
                pos[1] = (pos[1] + sf.command.turn) % 360
                    # Compute new poses
#                    pos[1] = sf.mag_dir

                # Update location on all ticks
                pos[0][0] = pos[0][0] + (sf.command.velocity * self.deltick) * math.cos(math.radians(pos[1]))
                pos[0][1] = pos[0][1] + (sf.command.velocity * self.deltick) * math.sin(math.radians(pos[1]))
                self.dr_estimated_pos[sf.name] = pos
                sf.dr_estimated_xy = np.array(pos[0], np.float32)    
                #print "update deadreckning!"
                #print sf.dr_estimated_xy,pos,sf.command.velocity,sf.command.turn
        # added by xinlei for human experiments
        sf.pf_updated_flag = True
