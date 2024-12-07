import gym
from gym_env import StrategicGameEnv
from stable_baselines3 import DQN

# Register your custom environment
env = StrategicGameEnv()

# Train an RL agent
model = DQN("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=100000)

# Save the trained model
model.save("strategic_game_agent")

# Test the agent
obs = env.reset()
done = False
while not done:
    action, _states = model.predict(obs)
    obs, reward, done, info = env.step(action)
    env.render()
