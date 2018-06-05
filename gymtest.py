import gym
env = gym.make('LunarLander-v2')   # 选择环境
for i_episode in range(20):
    observation = env.reset()      # 环境初始化，返回当前环境状态
    for t in range(100):
        env.render()               # 环境显示
        print(observation)
        # 从动作空间中随机采样选择动作
        action = env.action_space.sample() 
        # 执行动作获得反馈,从左至右分别是状态，奖励，结束标识符，debug信息
        observation, reward, done, info = env.step(action)  
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break