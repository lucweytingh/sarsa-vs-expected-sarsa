import time
from tqdm import tqdm as _tqdm

from src.utils import init_Q, EpsilonGreedyPolicy


def sarsa(
    env,
    num_episodes,
    discount_factor=1.0,
    alpha=0.5,
):
    """
    SARSA algorithm: On-policy TD control. Finds the optimal epsilon-greedy
    policy.

    Args:
        env: OpenAI environment.
        policy: A policy which allows us to sample actions with its
        sample_action method.
        Q: Q value function, numpy array Q[s,a] -> state-action value.
        num_episodes: Number of episodes to run for.
        discount_factor: Gamma discount factor.
        alpha: TD learning rate.

    Returns:
        A tuple (Q, stats).
        Q is a numpy array Q[s,a] -> state-action value.
        stats is a list of tuples giving the episode lengths and returns.
    """

    Q = init_Q(env)
    policy = EpsilonGreedyPolicy(Q, 0.1)
    # Keeps track of useful statistics
    stats = []
    diffs = []
    R = 0
    for i_episode in _tqdm(range(num_episodes)):
        start_time = time.time()
        policy.Q = Q
        state = env.reset()
        i = 0
        old_R = R
        R = 0
        action = policy.sample_action(state)
        while True:

            (new_state, reward, done, _) = env.step(action)
            policy.Q = Q
            new_action = policy.sample_action(new_state)
            R += reward * (discount_factor ** i)
            update = Q.get(state, action) + alpha * (
                reward
                + discount_factor * Q.get(new_state, new_action)
                - Q.get(state, action)
            )
            Q.set(state, action, update)
            state = new_state
            action = new_action
            i += 1
            if done:
                break
        T = time.time() - start_time
        stats.append((i, R, T))

    episode_lengths, episode_returns, episode_times = zip(*stats)
    return Q, (episode_lengths, episode_returns, episode_times), diffs


def expected_sarsa(
    env,
    num_episodes,
    discount_factor=1.0,
    alpha=0.5,
):
    """
    expected SARSA algorithm: On-policy TD control. Finds the optimal
    epsilon-greedy policy.

    Args:
        env: OpenAI environment.
        policy: A policy which allows us to sample actions with its
        sample_action method.
        Q: Q value function, numpy array Q[s,a] -> state-action value.
           True if converged
        num_episodes: Number of episodes to run for.
        discount_factor: Gamma discount factor.
        alpha: TD learning rate.

    Returns:
        A tuple (Q, stats).
        Q is a numpy array Q[s,a] -> state-action value.
        stats is a list of tuples giving the episode lengths and returns.
    """

    Q = init_Q(env)
    policy = EpsilonGreedyPolicy(Q, 0.1)
    # Keeps track of useful statistics

    stats = []
    diffs = []
    R = 0
    for i_episode in _tqdm(range(num_episodes)):
        s = env.reset()
        i = 0
        old_R = R
        R = 0
        a = policy.sample_action(s)
        start_time = time.time()
        while True:
            s_, r, done, _ = env.step(a)
            a_ = policy.sample_action(s_)
            ba = Q.get_best_action(s_)
            q_max = Q.get(s_, ba)
            non_greedy_action_probability = policy.epsilon / env.action_space.n
            greedy_action_probability = (
                (1 - policy.epsilon)
            ) + non_greedy_action_probability
            expected_q = sum(
                Q.get(s_, i) * greedy_action_probability
                if Q.get(s_, i) == q_max
                else Q.get(s_, i) * non_greedy_action_probability
                for i in range(env.action_space.n)
            )
            update = Q.get(s, a) + alpha * (
                r + discount_factor * expected_q - Q.get(s, a)
            )
            Q.set(s, a, update)
            s = s_
            a = a_
            R += r
            i += 1
            if done:
                break

        T = time.time() - start_time
        stats.append((i, R, T))
    episode_lengths, episode_returns, episode_times = zip(*stats)
    return Q, (episode_lengths, episode_returns, episode_times), diffs


NAME2ALG = {"expected_sarsa": expected_sarsa, "sarsa": sarsa}


# from windy_gridworld import WindyGridworldEnv
# import matplotlib.pyplot as plt
# import numpy as np

# env = WindyGridworldEnv()


# def running_mean(vals, n=1):
#     cumvals = np.array(vals).cumsum()
#     return (cumvals[n:] - cumvals[:-n]) / n


# (
#     Q_sarsa,
#     (episode_lengths_sarsa, episode_returns_sarsa, episode_times_sarsa),
#     diffs,
# ) = sarsa(env, 1000)

# (
#     Q_sarsa,
#     (episode_lengths_e_sarsa, episode_returns_e_sarsa, episode_times_e_sarsa),
#     diffs,
# ) = expected_sarsa(env, 1000)

# print(len(episode_lengths_sarsa))
# n = 50
# # We will help you with plotting this time
# plt.clf()
# plt.plot(
#     np.cumsum(episode_times_sarsa[:-n]),
#     running_mean(episode_returns_sarsa, n),
#     label="sarsa",
# )
# plt.plot(
#     np.cumsum(episode_times_e_sarsa[:-n]),
#     running_mean(episode_returns_e_sarsa, n),
#     label="expected_sarsa",
# )
# plt.title("Return attained during training ")
# plt.xlabel("Time")
# plt.ylabel("Return")
# plt.legend()
# plt.show()
