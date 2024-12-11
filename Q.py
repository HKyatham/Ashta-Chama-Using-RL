from stable_baselines3 import PPO
from stable_baselines3 import DQN
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import CheckpointCallback
from ashtachamma_env import AshtachammaEnv

# Create and check the environment
env = AshtachammaEnv()
check_env(env)

# Wrap the environment
env = DummyVecEnv([lambda: env])

# Create the model with custom hyperparameters
#model = PPO("MlpPolicy", env, verbose=1, learning_rate=1e-4, n_steps=2048, batch_size=64)
model = DQN("MlpPolicy", env, verbose=1, learning_rate=1e-4, batch_size=64, tensorboard_log="./ppo_tensorboard/", target_update_interval = 500 )

# Define checkpoint callback
checkpoint_callback = CheckpointCallback(save_freq=10000, save_path="./checkpoints/", name_prefix="ashtachamma_model")

# Train the agent
print("Training the model...")
model.learn(total_timesteps=1000000, callback=checkpoint_callback)
print("Training completed!")

# Save and load the model
model.save("ashtachamma_dqn_agent")


model = DQN.load("ashtachamma_dqn_agent")

# Evaluate the policy
print("Evaluating the policy...")
mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=100)
print(f"Mean Reward: {mean_reward}, Std Reward: {std_reward}")

num_games = 100
for i in range(num_games):

    # Play a single game
    # print("Playing a single game...")
    obs = env.reset()
    done = False
    while not done:
        action, _ = model.predict(obs)
        obs, reward, done, _ = env.step(action)
        env.render()

env.close()
print("Game finished, resources cleaned up!")