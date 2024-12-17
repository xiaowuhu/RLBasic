
import matplotlib.pyplot as plt
import gymnasium as gym
import numpy as np


def test():
    env = gym.make("Taxi-v3")
    env.reset(seed=5)
    behavior_policy = np.ones((env.observation_space.n, env.action_space.n)) / env.action_space.n
    episodes = 1000
    alpha = 0.1
    gamma = 1
    epsilon = 0.1
    n = 5

    ctrl = SARSA_n(env, episodes, behavior_policy, alpha=alpha, gamma=gamma, n=n, epsilon=epsilon)
    Q = ctrl.run()
    print(Q)

    env = gym.make("Taxi-v3", render_mode="human")
    s, _ = env.reset()
    step = 0
    done = False
    R = 0
    for step in range(100):
        env.render()
        action = np.argmax(Q[s])
        next_s, r, done, _, _ = env.step(action)
        R += r
        s = next_s
        if done:
            print(R)
            break
    env.close()

if __name__ == "__main__":
    env = gym.make("LunarLander-v2", render_mode="human")
    observation, info = env.reset()

    for _ in range(100):
        action = env.action_space.sample()  # agent policy that uses the observation and info
        observation, reward, terminated, truncated, info = env.step(action)
        print(observation)
        if terminated or truncated:
            observation, info = env.reset()

    env.close()