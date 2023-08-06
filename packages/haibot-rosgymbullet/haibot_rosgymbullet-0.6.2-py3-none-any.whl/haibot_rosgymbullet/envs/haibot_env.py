#!usr/bin/env python3

import rospy
from geometry_msgs.msg import *
from sensor_msgs.msg import *
import gym
from gym import spaces
import importlib
from gym.utils import seeding
import numpy as np
import math
from math import *
import time
import matplotlib.pyplot as plt
from std_srvs.srv import Empty
from haibot_rosgymbullet.resources.function_exec_manager import FuncExecManager
import os
import pybullet_data
from typing import Optional, Union

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
#---Directory Path---#
dirPath = os.path.dirname(os.path.realpath(__file__))
robot_path = dirPath + "/robot/diffbot.urdf.xacro"
target_path = dirPath + "/robot/cylinder.urdf"


        

class DiffBotDrivingEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, render_mode: Optional[str] = None):
        self.pb = importlib.import_module('pybullet')
        rospy.init_node('ros_gym_bullet', anonymous=False)
        self.plugins = []
        self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=20)
        #----------Action | Observation Space------------------
        self.prev_dist = 0.0
        self.action_size = rospy.get_param('~action_size', 5)
        self.prev_action = np.array([0.,0.])
        obs_high = np.concatenate((np.array([50.] * 10) ,np.array([10.0, 10.0]), np.array([6.]), np.array([4]) ))
        obs_low = np.concatenate((np.array([0.] * 10) ,np.array([0.0, -10.0]), np.array([-6.]), np.array([-4]) ))
        self.action_space = spaces.Box(low=np.array([0.0, -0.5]) ,high=np.array([0.3, 0.5]), dtype=np.float32)
        self.observation_space = spaces.Box(low=obs_low , high=obs_high, dtype=np.float32)
        # self.count_collision, self.count_overtime, self.count_goal  = 0,0,0

        # self.reward_range = (-np.inf, np.inf)

        # self.client =self.pb.connect(self.pb.DIRECT)
        # Reduce length of episodes for RL algorithms
        # self.pb.setTimeStep(1/30, self.client)
        # self.max_episode_steps = 

        self.loop_rate = rospy.get_param('~loop_rate', 80.0)
        self.pause_simulation = False
        rospy.Service('reset_simulation', Empty, self.handle_reset_simulation)
        # setup services for pausing/unpausing simulation
        rospy.Service('pause_physics', Empty, self.handle_pause_physics)
        rospy.Service('unpause_physics', Empty, self.handle_unpause_physics)
        self.vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=5)
        is_gui_needed = True
        physicsClient = self.start_gui(gui=is_gui_needed)
        self.render_mode = render_mode
        self.goal = None
        self.done = False
 
        # self.reset()
        # self.render()
        #------------------------------------------------------------------------------------

        # get pybullet path in your system and store it internally for future use, e.g. to set floor
        self.pb.setAdditionalSearchPath(pybullet_data.getDataPath())
        # create object of environment class for later use
        env_plugin = rospy.get_param('~environment', 'my_environment') # default : plugins/my_environment.py
        plugin_import_prefix = rospy.get_param('~plugin_import_prefix', 'haibot_rosgymbullet.resources.plugins')
        self.environment = getattr(importlib.import_module(f'{plugin_import_prefix}.{env_plugin}'), 'Environment')(self.pb)
        # load robot URDF model, set gravity, and ground plane
        self.urdf_path = rospy.get_param('~robot_urdf_path', robot_path)
        self.target_urdf = rospy.get_param('~target_urdf', target_path)
        # self.target_urdf = target_path
        self.x_goal_pos = 1.7
        self.y_goal_pos = 1.8
        self.robot , self.target_point = self.init_pybullet_robot()
        self.connected_to_physics_server = None
        if not self.robot:
            self.connected_to_physics_server = False
            return # Error while loading urdf file
        else:
            self.connected_to_physics_server = True
        self.rev_joint_index_name_dic, self.prismatic_joint_index_name_dic, self.fixed_joint_index_name_dic, self.link_names_to_ids_dic = self.get_properties()
        # import plugins dynamically
        plugins = rospy.get_param('~plugins', [ {'module': 'haibot_rosgymbullet.resources.plugins.body_vel_control', 'class': 'cmdVelCtrl'},\
                                                {'module': 'haibot_rosgymbullet.resources.plugins.odometry', 'class': 'simpleOdometry'},\
                                                {'module': 'haibot_rosgymbullet.resources.plugins.control', 'class': 'Control'},\
                                                {'module': 'haibot_rosgymbullet.resources.plugins.joint_state_pub', 'class': 'joinStatePub'},\
                                                {'module': 'haibot_rosgymbullet.resources.plugins.laser_scanner', 'class': 'laserScanner'},\
                                                {'module': 'haibot_rosgymbullet.resources.plugins.rgbd_camera', 'class': 'RGBDCamera'},\
                                                {'module': 'haibot_rosgymbullet.resources.plugins.diff_drive', 'class': 'DiffDrive', 'name': 'diff_drive_controller'} ])
                                        
        ##############################################################################################################################################
        # params = {'plugins': [{'module': 'haibot_rosgymbullet.resources.plugins.body_vel_control', 'class': 'cmdVelCtrl'},\                        #
        #             {'module': 'haibot_rosgymbullet.resources.plugins.odometry', 'class': 'simpleOdometry'},\                                      #
        #             {'module': 'haibot_rosgymbullet.resources.plugins.control', 'class': 'Control'},\                                              #
        #             {'module': 'haibot_rosgymbullet.resources.plugins.joint_state_pub', 'class': 'joinStatePub'},\                                 #
        #             {'module': 'haibot_rosgymbullet.resources.plugins.laser_scanner', 'class': 'laserScanner'},\                                   #
        #             {'module': 'haibot_rosgymbullet.resources.plugins.rgbd_camera', 'class': 'RGBDCamera'},\                                       #
        #             {'module': 'haibot_rosgymbullet.resources.plugins.diff_drive', 'class': 'DiffDrive', 'name': 'diff_drive_controller'}],\       #
        #         'loop_rate': 80.0, 'gravity': -9.81, 'max_effort': 10.0, 'use_intertia_from_file': False,\                                         #
        #         'laser': {'frame_id': 'base_scan', 'angle_min': -2.26889, 'angle_max': 2.26889, 'num_beams': 75,\                                  #
        #         'range_min': 0.05, 'range_max': 5.6, 'beam_visualisation': True},\                                                                 #
        #         'rgbd_camera': {'frame_id': 'kinect_link', 'resolution': {'width': 640, 'height': 480}},\                                          #
        #         'diff_drive_controller': {'left_joints': ['joint_left_wheel'],\                                                                    #
        #         'right_joints': ['joint_right_wheel'], 'wheel_separation': 1.0, 'wheel_radius': 0.05, 'cmd_vel': '/cmd_vel'}}                      #
        ##############################################################################################################################################
        # self.Recall_plugins(rev_joint_index_name_dic, prismatic_joint_index_name_dic, fixed_joint_index_name_dic, link_names_to_ids_dic)
        # import plugins dynamically
        if not plugins:
            rospy.logwarn('No plugins found, forgot to set param ~plugins?')
        # return to normal shell color
        print('\033[0m')
        # load plugins
        for plugin in plugins:
            module_ = plugin.pop("module")
            class_ = plugin.pop("class")
            params_ = plugin.copy()
            rospy.loginfo('loading plugin: {} class from {}'.format(class_, module_))
            # create object of the imported file class
            obj = getattr(importlib.import_module(module_), class_)(self.pb, self.robot,
                        rev_joints=self.rev_joint_index_name_dic,
                        prism_joints=self.prismatic_joint_index_name_dic,
                        fixed_joints=self.fixed_joint_index_name_dic,
                        link_ids=self.link_names_to_ids_dic,
                        **params_)
            # store objects in member variable for future use
            self.plugins.append(obj)

#---------------------------------------------------------------------------------------
    def init_pybullet_robot(self):
        """load robot URDF model, set gravity, ground plane and environment"""
        # get from param server the path to the URDF robot model to load at startup
        # urdf_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources/urdf", "diff_robot.urdf")
        urdf_path = self.urdf_path
        if urdf_path == None:
            rospy.signal_shutdown('mandatory param robot_urdf_path not set, will exit now')
        # test urdf file existance
        if not os.path.isfile(urdf_path):
            rospy.logerr('param robot_urdf_path is set, but file does not exist : ' + urdf_path)
            rospy.signal_shutdown('required robot urdf file not found')
            return None

        if 'xacro' in urdf_path:
            robot_description = rospy.get_param('robot_description', None)
            if not robot_description:
                rospy.logerr('required robot_description param not set')
                return None
            # remove xacro from name
            urdf_path_without_xacro = urdf_path[0:urdf_path.find('.xacro')]+urdf_path[urdf_path.find('.xacro')+len('.xacro'):]
            # rospy.loginfo('generating urdf model from xacro from robot_description param server under: {0}'.format(urdf_path_without_xacro))
            try:
                urdf_file = open(urdf_path_without_xacro,'w')
            except:
                rospy.logerr('Failed to create urdf file from xacro, cannot write into destination: {0}'.format(urdf_path_without_xacro))
                return None
            urdf_file.write(robot_description)
            urdf_file.close()
            urdf_path = urdf_path_without_xacro
        # get robot spawn pose from parameter server
        robot_pose_x = rospy.get_param('~robot_pose_x', -2.3)
        robot_pose_y = rospy.get_param('~robot_pose_y', -1.0)
        robot_pose_z = rospy.get_param('~robot_pose_z', 0.0)
        robot_pose_yaw = rospy.get_param('~robot_pose_yaw', 0.0)
        robot_spawn_orientation = self.pb.getQuaternionFromEuler([0.0, 0.0, robot_pose_yaw])
        fixed_base = rospy.get_param('~fixed_base', False)
        # load robot from URDF model
        # user decides if inertia is computed automatically by pybullet or custom
        if rospy.get_param('~use_intertia_from_file', False):
            # combining several boolean flags using "or" according to pybullet documentation
            urdf_flags = self.pb.URDF_USE_INERTIA_FROM_FILE | self.pb.URDF_USE_SELF_COLLISION
        else:
            urdf_flags = self.pb.URDF_USE_SELF_COLLISION
        # load environment
        rospy.loginfo('loading environment')
        self.environment.load_environment()
        # set no realtime simulation, NOTE: no need to stepSimulation if setRealTimeSimulation is set to 1
        self.pb.setRealTimeSimulation(0) # NOTE: does not currently work with effort controller, thats why is left as 0
        # rospy.loginfo('loading urdf model: ' + urdf_path)
        # NOTE: self collision enabled by default
        
        
        return self.pb.loadURDF(urdf_path, basePosition=[robot_pose_x, robot_pose_y, robot_pose_z],
                                           baseOrientation=robot_spawn_orientation,
                                           useFixedBase=fixed_base, flags=urdf_flags), self.load_target()

    def get_properties(self):
        rev_joint_index_name_dic = {}
        fixed_joint_index_name_dic = {}
        prismatic_joint_index_name_dic = {}
        link_names_to_ids_dic = {}
        for joint_index in range(0, self.pb.getNumJoints(self.robot)):
            info = self.pb.getJointInfo(self.robot, joint_index)
            # build a dictionary of link names to ids
            link_names_to_ids_dic[info[12].decode('utf-8')] = joint_index
            # ensure we are dealing with a revolute joint
            if info[2] == self.pb.JOINT_REVOLUTE:
                # insert key, value in dictionary (joint index, joint name)
                rev_joint_index_name_dic[joint_index] = info[1].decode('utf-8') # info[1] refers to joint name
            elif info[2] == self.pb.JOINT_FIXED:
                # insert key, value in dictionary (joint index, joint name)
                fixed_joint_index_name_dic[joint_index] = info[1].decode('utf-8') # info[1] refers to joint name
            elif info[2] == self.pb.JOINT_PRISMATIC:
                prismatic_joint_index_name_dic[joint_index] = info[1].decode('utf-8') # info[1] refers to joint name
        return rev_joint_index_name_dic, prismatic_joint_index_name_dic, fixed_joint_index_name_dic, link_names_to_ids_dic

    def start_gui(self, gui=True):
        """start physics engine (client) with or without gui"""
        if(gui):
            # start simulation with gui
            rospy.loginfo('Landing RosGymBullet Environment with GUI')
            rospy.loginfo('*****************************************')
            gui_options = rospy.get_param('~gui_options', '') # e.g. to maximize screen: options="--width=2560 --height=1440"
            return self.pb.connect(self.pb.GUI, options=gui_options)
        else:
            # start simulation without gui (non-graphical version)
            rospy.loginfo('Landing RosGymBullet Environment with GUI')
            # hide console output from pybullet
            rospy.loginfo('*****************************************')
            return self.pb.connect(self.pb.DIRECT)

    def handle_reset_simulation(self, req):
        rospy.loginfo('reseting simulation now')
        # pause simulation to prevent reading joint values with an empty world
        self.pause_simulation = True
        # remove all objects from the world and reset the world to initial conditions
        self.pb.resetSimulation()
        # load URDF model again, set gravity, floor and target point
        self.init_pybullet_robot()
        # resume simulation control cycle now that a new robot is in place
        self.pause_simulation = False
        return []

    def handle_pause_physics(self, req):
        rospy.loginfo('pausing simulation')
        self.pause_simulation = False
        return []

    def handle_unpause_physics(self, req):
        rospy.loginfo('unpausing simulation')
        self.pause_simulation = True
        return []

    def pause_simulation_function(self):
        return self.pause_simulation

    def start_RosGymBullet_wrapper_sequential(self):
        """
        This function is deprecated, we recommend the use of parallel plugin execution
        """
        rate = rospy.Rate(self.loop_rate)
        while not rospy.is_shutdown():
            if not self.pause_simulation:
                # run x plugins
                for task in self.plugins:
                    task.execute()
                # perform all the actions in a single forward dynamics simulation step such
                # as collision detection, constraint solving and integration
                self.pb.stepSimulation()
            rate.sleep()
        rospy.logwarn('killing node now...')
        # if node is killed, disconnect
        if self.connected_to_physics_server:
            self.pb.disconnect()

    def start_RosGymBullet_wrapper_parallel(self):
        """
        Execute plugins in parallel, however watch their execution time and warn if exceeds the deadline (loop rate)
        """
        # create object of our parallel execution manager
        exec_manager_obj = FuncExecManager(self.plugins, rospy.is_shutdown, self.pb.stepSimulation, self.pause_simulation_function,
                                    log_info=rospy.loginfo, log_debug=rospy.logdebug, function_name='plugin')
        # start parallel execution of all "execute" class methods in a synchronous way
        exec_manager_obj.start_synchronous_execution(loop_rate=self.loop_rate)
        # ctrl + c was pressed, exit
        rospy.logwarn('killing node now...')
        # if node is killed, disconnect
        if self.connected_to_physics_server:
            self.pb.disconnect()

    def start_RosGymBullet_wrapper(self):
        if rospy.get_param('~parallel_plugin_execution', True):
            self.start_RosGymBullet_wrapper_parallel()
        else:
            self.start_RosGymBullet_wrapper_sequential()

#---------------------------------------------------------------------------------------
    def differential_drive(self,action ,D=0.418,R=0.05,speed=10):
        # D=distance between wheels, R=wheel radius
        # action[0]=linear vel , action[1] = angular vel
        rightWheelVelocity = 0.
        leftWheelVelocity = 0.
        # rightWheelVelocity += (2*action[0] + action[1]*L) / 2*R
        # leftWheelVelocity += (2*action[0] - action[1]*L) / 2*R
        rightWheelVelocity+= (action[0]+action[1])*speed
        leftWheelVelocity += (action[0]-action[1])*speed
        return np.array([rightWheelVelocity,leftWheelVelocity])
    
    def load_target(self):
        # trans,rot = self.pb.getBasePositionAndOrientation(self.urdf_path)
        # margin = 0.1 * self.max_x
        # x_pos = np.random.uniform(self.min_x + margin, self.max_x - margin)
        # y_pos = np.random.uniform(self.min_y + margin, self.max_y - margin)

        # print("----------->> Target point loaded !!!")
        self.target_cylinder = self.pb.loadURDF(self.target_urdf, [self.x_goal_pos , self.y_goal_pos , 0], useFixedBase=True)
        
        return np.array([self.x_goal_pos , self.y_goal_pos ])

    def reset_target(self):
        self.pb.removeBody(self.target_cylinder)
        self.target = self.target_point
        print("Deleted old target")
#---------------------------------------------------------------------------------------
    def calculate_observation(self, data):
        min_range = 0.45
        done = False
        for i, item in enumerate(data.ranges):
            if (min_range > data.ranges[i] > 0.3):
                done = True
        return data.ranges, done


    # def setReward(self, state, done, action):
    #     yaw_reward = []
    #     current_distance = state[-1]
    #     heading = state[-2]

    #     for i in range(5):
    #         angle = -pi / 4 + heading + (pi / 8 * i) + pi / 2
    #         tr = 1 - 4 * fabs(0.5 - modf(0.25 + 0.5 * angle % (2 * pi) / pi)[0])
    #         yaw_reward.append(tr)

    #     distance_rate = 2 ** (current_distance / self.goal_distance)
    #     reward = ((round(yaw_reward[action] * 5, 2)) * distance_rate)

    #     if done:
    #         rospy.loginfo("Collision!!")
    #         reward = -200
    #         self.pub_cmd_vel.publish(Twist())

    #     return reward
    

    def step(self, action):
        # rospy.wait_for_service('/unpause_physics')
        # try:
        #     unpause = rospy.ServiceProxy("/unpause_physics", Empty)
        #     unpause()
        # except (rospy.ServiceException) as e:
        #     print ("/unpause_physics service call failed")

        # self.render()
        max_angular_vel = 1.5
        ang_vel = ((self.action_size - 1)/2 - action) * max_angular_vel * 0.5

        vel_cmd = Twist()
        vel_cmd.linear.x = 1.0
        vel_cmd.angular.z = ang_vel
        self.vel_pub.publish(vel_cmd)


        data = None
        while data is None:
            try:
                data = rospy.wait_for_message('/scan', LaserScan, timeout=5)
            except:
                pass
            
        data = rospy.wait_for_message('/scan', LaserScan, timeout=5)
        # rospy.wait_for_service('/pause_physics')
        # try:
        #     pause = rospy.ServiceProxy("/pause_physics", Empty)
        #     pause()
        # except (rospy.ServiceException) as e:
        #     print ("/pause_physics service call failed")

        obs, done = self.calculate_observation(data)
        
        trans,rot = self.pb.getBasePositionAndOrientation(self.robot)
        _,_,yaw = self.pb.getEulerFromQuaternion(rot)
        goal_angle = np.arctan2(self.target[1] - trans[1], self.target[0] - trans[0])
        # heading = np.array([goal_angle - yaw])

        dist = np.linalg.norm(np.array([trans[0],trans[1]]) - self.target)
        # nowLidarTime = time.time()
        dist_rate = dist - self.prev_dist
        # print('prev_dist:',self.prev_dist,'dist:',dist)
        self.prev_dist = dist

        if done: # done if collided with obstacles
            reward = -550
            print("..................")
            print(' => COLLISION !!! ')
            print("..................")
            # self.reset()
            rospy.wait_for_service('/pause_physics')
            try:
                pause = rospy.ServiceProxy("/pause_physics", Empty)
                pause()
                print("Respawning environment ...")
            except (rospy.ServiceException) as e:
                print ("/pause_physics service call failed")
                
            vel_cmd = Twist()
            vel_cmd.linear.x = 0
            vel_cmd.angular.z = 0
            self.vel_pub.publish(vel_cmd)
            pass


        elif dist_rate > 0:
            reward = 200.*dist_rate

        elif dist_rate <= 0:
            reward = -8.
            # print('reward:',reward)

        if dist <= 0.4:   # reached target
            reward = 500
            # Reset target
            print("*********************")
            print(' => GOAL REACHED !!! ')
            print("*********************")
            self.reset_target() 

        
        return np.asarray(obs), reward, done, {}


    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]
            

    def reset(self):
        # Resets the state of the environment and returns an initial observation.
        rospy.wait_for_service('/reset_simulation')
        try:
            reset_proxy = rospy.ServiceProxy('/reset_simulation', Empty)
            reset_proxy()
            pass
        except (rospy.ServiceException) as e:
            print ("/reset_simulation service call failed")
        self.target = self.target_point
        # Unpause simulation to make observation
        # rospy.wait_for_service('/unpause_physics')
        # try:
        #     unpause = rospy.ServiceProxy("/unpause_physics", Empty)
        #     unpause()
        # except (rospy.ServiceException) as e:
        #     print ("/unpause_physics service call failed")
        
        # self.rev_joint_index_name_dic=self.rev_joint_index_name_dic.copy()
        # self.prismatic_joint_index_name_dic=self.prismatic_joint_index_name_dic.copy()
        # self.fixed_joint_index_name_dic=self.fixed_joint_index_name_dic.copy()
        # self.link_names_to_ids_dic=self.link_names_to_ids_dic.copy()
        # self.plugins = self.plugins.copy()
        
        #read laser data
        data = None
        while data is None:
            try:
                data = rospy.wait_for_message('/scan', LaserScan, timeout=5)
            except:
                pass

        # rospy.wait_for_service('/pause_physics')
        # try:
        #     pause = rospy.ServiceProxy("/pause_physics", Empty)
        #     pause()
        # except (rospy.ServiceException) as e:
        #     print ("/pause_physics service call failed")
            
        # trans,rot = self.pb.getBasePositionAndOrientation(self.urdf_path)
        # self.target = self.target_point() #  TODO: 

        # dist = np.linalg.norm(np.array([trans[0],trans[1]]) - self.target)
        # self.render()
        
        state, _ = self.calculate_observation(data)
        return np.asarray(state)

    def render(self, mode='human'):
        self.start_RosGymBullet_wrapper()

    def close(self):
       self.pb.disconnect()
