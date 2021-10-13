import numpy as np
import gym
from collections import defaultdict


def init_Q(env):
    "initialize empty Q table given the environment"
    # breakpoint()
    if (
        len(env.observation_space.shape) > 1
        or len(env.action_space.spaces) > 1
    ):
        return dictQ(env)
    else:
        return matrixQ(env)


def float_ddict():
    return defaultdict(float)


class dictQ:
    def __init__(self, env):
        self.state2action2Q = defaultdict(float_ddict)
        self.env = env
        self.action_space = env.action_space

    def get_best_action(self, state):
        action2Q = self.state2action2Q[state]
        if len(action2Q.keys()) == 0:
            return self.action_space.sample()
        else:
            return max(action2Q, key=action2Q.get)

    def get(self, state, action):
        return self.state2action2Q[state][action]

    def set(self, state, action, value):
        self.state2action2Q[state][action] = value


class matrixQ:
    def __init__(self, env):
        self.Q = np.zeros((env.observation_space.n, env.action_space.n))
        self.env = env

    def get_best_action(self, state):
        return self.Q[state].argmax()

    def get(self, state, action):
        return self.Q[state, action]

    def set(self, state, action, value):
        self.Q[state, action] = value


class EpsilonGreedyPolicy(object):
    """
    A simple epsilon greedy policy.
    """

    def __init__(self, Q, epsilon):
        self.Q = Q
        self.epsilon = epsilon

    def sample_action(self, obs):
        """
        This method takes a state as input and returns an action sampled from
        this policy.

        Args:
            obs: current state

        Returns:
            An action (int).
        """
        if np.random.random() < self.epsilon:
            action = self.Q.env.action_space.sample()
        else:
            action = self.Q.get_best_action(obs)
        return action


def get_samples_used(episode_lenghts):
    "given the outputted episode_lengths list, returns the number of samples used"
    return sum(episode_lenghts)


def get_noXgf_actions(env):
    if type(env.action_space) == gym.spaces.tuple_space.Tuple:
        return np.prod([act_space.n for act_space in env.action_space.spaces])
    return env.action_space.n


def running_mean(vals, n=1):
    cumvals = np.array(vals).cumsum()
    return (cumvals[n:] - cumvals[:-n]) / n
