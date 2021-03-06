'''
Created on Sep 27, 2012
@author: imaveek
'''

from Sim import arena, sensorfly, controller
import random
import numpy as np
from Sim.case import Case
import sys, traceback
import scipy.io
import progressbar as pb
# import time
import os 

mapsize = "9_12"

clients = None
data = None
systemRunning = None

def main(inputClients, inputData, inputSystemRunning):
#def main():

    print "Running SugarMapSim"
    
    global clients
    global data
    global systemRunning
    clients = inputClients
    data = inputData
    systemRunning = inputSystemRunning
    
    drunkWalkCase(0)
        
def drunkWalkCase(i):
#def drunkWalkCase():
    
    print "running DrunkWalk"
    case = Case("DrunkWalk", "./ArenaMaps/testbed" + mapsize + ".bmp")
    case.cov_algo = "drunkwalk"
    case.start = [1,1]
    case.end = [25,30]#[8,11]#[25,25]
    
   # case.map_array[case.end[0],case.end[1]] = 2  # added by xinlei
   
    #case.map_array[25,26] = 2  # added by xinlei
    #case.map_array[25,24] = 2  # added by xinlei
    #case.map_array[24,24] = 2  # added by xinlei
    #case.map_array[24,25] = 2  # added by xinlei
    #case.map_array[24,26] = 2  # added by xinlei
    #case.map_array[26,26] = 2  # added by xinlei
    #case.map_array[26,24] = 2  # added by xinlei
    #case.map_array[26,25] = 2  # added by xinlei
    
    
    
#     case = Case("DrunkWalk_Maps", "./ArenaMaps/7room_slam_map_small.bmp")
#     case.cov_algo = "drunkwalk_biased"
# 
# #     case = Case("DrunkWalk_BiasedRandom", "./ArenaMaps/6room_map_small/6room_map.bmp")
# #     case.cov_algo = "drunkwalk_biased"
#     case.goal_graph = goalgraph.GoalGraph()
    
    case.num_explorers = 1#1
    case.num_anchors =6#3#6
    
    # Noises
    case.noise_radio = 0.01#0.1
    case.noise_turn = 0.2    
    case.noise_velocity = 0.2
    case.noise_mag = 30
    case.fail_prob = 0
    
    #     Import the database of collected RF signatures
    '''
    raw = np.loadtxt("./ArenaMaps/testbed_sigs/sensorfly_x_y_time_id_rss.txt", delimiter=',');
    #raw = np.loadtxt("./ArenaMaps/testbed_sigs/fingerprint36*27.txt", delimiter=',');
      
    for i in range(0,9):
        for j in range(0,12):
            idxX = raw[:,0] == i
            idxY = raw[:,1] == j
            idx = idxX & idxY
            id_sigs = raw[idx,:][:,[2,3]]
            for k in range(1, case.num_anchors+1):
                idxK = id_sigs[:,0] == k
                if idxK.size != 0:
                    rss = id_sigs[idxK,1]
                else:
                    rss = np.array([0])
                case.rf_signature_db[(i,j,k)] = rss

    '''
    # Particle filter settings
    case.stop_on_all_covered = True
    case.num_particles = 100
    
    # Display
    case.is_display_on_real = False
    
    # Run case
    case.num_total_run = 14000#360
    case.max_iterations = 1#5
    case.deltick = 1
    
    runCase(case)
    
    
def runCase(case):
    '''
    Run the case for computing S for the first room
    '''
    print "Running runCase"

    
    record_list = []
    widgets = ['Case: ', pb.Percentage(), ' ', pb.Bar(),' ',pb.ETA()]
    num_ticks = int(case.num_total_run / case.deltick)
    pbar = pb.ProgressBar(widgets=widgets, maxval=case.max_iterations * num_ticks).start()  
    for it in range(case.max_iterations):
        
        case.reset()
        _arena = arena.Arena(case.map_array)
        
        # Create simulator engine
        _cnt = controller.Controller(_arena)
        _cnt.sm_num_particles = case.num_particles
            
        # Create SensorFly Explorer
        for i in range(case.num_explorers): #@UnusedVariable
            
            if case.goal_graph is not None:
#                 loc_count = len(case.goal_graph.start)
                rnd_loc = random.randint(0, 1)        
                sf_xy = case.goal_graph.start[rnd_loc]
            else:
                sf_xy = case.start
            
            
            ### need to set up initial values for each sf
            '''
            _sf_explorer = sensorfly.SensorFly(str(i), sf_xy, 0, 100,
                                               case.noise_velocity, case.noise_turn, 
                                               case.noise_radio, case.noise_mag, case.fail_prob, _cnt, case)
            
            '''
            _sf_explorer = sensorfly.SensorFly( (i), sf_xy, 0, 100,
                                               case.noise_velocity, case.noise_turn, 
                                               case.noise_radio, case.noise_mag, case.fail_prob, _cnt, case )
            
            
            #Initialize map direction
            _sf_explorer.map_init_dir = 151
            _sf_explorer.dir = 151
            
            _sf_explorer.rssi_cnt_stop = 10
            
            _cnt.addExplorer(_sf_explorer)
        
        
        # Create SensorFly Anchors
        for i in range(case.num_anchors): #@UnusedVariable
            '''
            _sf_anchor = sensorfly.SensorFly(str(100 + i), 
                                             [1 + random.random() * (case.al-2), 1 + random.random() * (case.aw-2)], 0, 100, 
                                             case.noise_velocity, case.noise_turn, 
                                             case.noise_radio, case.noise_mag, case.fail_prob, _cnt, case)  
            '''
            _sf_anchor = sensorfly.SensorFly( (100 + i), 
                                             [1 + random.random() * (case.al-2), 1 + random.random() * (case.aw-2)], 0, 100, 
                                             case.noise_velocity, case.noise_turn, 
                                             case.noise_radio, case.noise_mag, case.fail_prob, _cnt, case) 
            
                  
            _cnt.addAnchor(_sf_anchor)            
        
        
        
        
        # Run the simulation
        
        folder_str = "./Data/" + case.name + "/"
        if not os.path.exists(folder_str):
            os.makedirs(folder_str)
        file_str = folder_str +"/expdata_m"  + mapsize + '_e' + str(case.num_explorers) + "_a" + str(case.num_anchors) \
                                        + "_p" + str(case.num_particles) + "_i" + str(case.max_iterations) \
                                        + "_nr" + str(case.noise_radio) \
                                        + "_nv" + str(int(case.noise_velocity * 100)) \
                                        + "_nt" + str(int(case.noise_turn * 100))+'.txt'
#                                         + "_" + timestr
        try:
            record = _cnt.run(num_ticks, case, pbar, it,clients, data,systemRunning,file_str)
            record_list.append(np.array(record))
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
    
    
    mdict = {}
    mdict['record_list'] = record_list
    mdict['caseInfo'] = [case.name, case.num_explorers, case.num_anchors, case.num_particles, case.max_iterations, \
                         case.noise_radio, case.noise_velocity, case.noise_turn, case.noise_mag]

    #saveMatFile(mdict, case)
    pbar.finish()


def saveMatFile(mdict, case):
#     timestr = time.strftime("%Y%m%d-%H%M%S")
    folder_str = "./Data/" + case.name + "/"
    # Delete old data in folder
    if not os.path.exists(folder_str):
        os.makedirs(folder_str)
    file_str = folder_str + "/data_m"  + mapsize + '_e' + str(case.num_explorers) + "_a" + str(case.num_anchors) \
                                        + "_p" + str(case.num_particles) + "_i" + str(case.max_iterations) \
                                        + "_nr" + str(case.noise_radio) \
                                        + "_nv" + str(int(case.noise_velocity * 100)) \
                                        + "_nt" + str(int(case.noise_turn * 100))
#                                         + "_" + timestr
    scipy.io.savemat(file_str, mdict, oned_as='row')
    
    
#if __name__ == '__main__':
#    main()
    
