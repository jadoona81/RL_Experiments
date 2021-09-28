# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 21:15:19 2020


@author: ebaccourepbesaid
"""


from stable_baselines.common.policies import MlpPolicy #,LnMlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common.vec_env import SubprocVecEnv
#from stable_baselines.deepq.policies import DQNPolicy
#from stable_baselines import PPO2
from stable_baselines import DQN

from stable_baselines.deepq.policies import FeedForwardPolicy


#from Env import NetworkEnv
import pandas as pd
import numpy as np
import gym


# Same as before we instantiate the agent along with the environment
from stable_baselines import DQN




def main():

# 	env = SubprocVecEnv([lambda:  NetworkEnv() for i in range(1)])
# 	model = DQN(DQNPolicy, env, verbose=0) #PPO2(MlpPolicy, env, verbose=0)#,cliprange_vf=-1)
# 	model.learn(total_timesteps=3000000) #2261475
# 	model.save("DQN_optimization_sigma_-10.pkl")


    env = gym.make('CartPole-v1')
    
    # Deactivate all the DQN extensions to have the original version
# In practice, it is recommend to have them activated
    kwargs = {'double_q': False, 'prioritized_replay': False, 'policy_kwargs': dict(dueling=False)}

# Note that the MlpPolicy of DQN is different from the one of PPO
# but stable-baselines handles that automatically if you pass a string
    model = DQN('MlpPolicy', 'CartPole-v1', verbose=1, **kwargs)

    
    #model = DQN(MlpPolicy, env, verbose=1)
    model.learn(total_timesteps=25000)
    model.save("deepq_cartpole")
    
    del model # remove to demonstrate saving and loading
    
    model = DQN.load("deepq_cartpole")
    
    obs = env.reset()
    while True:
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        env.render()



if __name__ == "__main__":
	main()