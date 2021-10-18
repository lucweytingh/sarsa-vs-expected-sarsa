from plot import plot_results
from src.experimentresults import ExperimentResults
from src.sarsa import NAME2ALG

import fire
import optimize_params
import gym
import random

import numpy as np
import matplotlib.pyplot as plt


def run(env_name):
    optimize_params.run(env_name)
    exp2results = ExperimentResults.from_storage()
    env = gym.envs.make(env_name)
    alg2results = {}
    for name, alg in NAME2ALG.items():
        alpha = exp2results[env_name][name]["opt_alpha"]
        alg2results[name] = get_results(alg, env, n_runs=3, n_episodes=1000)
    plt.close("all")
    plot_results(
        alg2results,
        env_name,
    )


def get_results(sarsa_fn, env, n_runs=3, n_episodes=1000):
    seeds = range(2, 10)
    returns = np.zeros((n_episodes, n_runs))
    lengths = np.zeros((n_episodes, n_runs))
    times = np.zeros((n_episodes, n_runs))
    for r in range(n_runs):
        seed = seeds[r]
        np.random.seed(seed)
        random.seed(seed)
        env.seed(seed)

        (
            _,
            (episode_lengths, episode_returns, episode_times),
            _,
        ) = sarsa_fn(env, n_episodes)
        returns[:, r] = episode_returns
        lengths[:, r] = episode_lengths
        times[:, r] = episode_times
    return {
        "episode_returns": returns,
        "xvar2results": {"episode lengths": lengths, "time": times},
    }


if __name__ == "__main__":
    fire.Fire(run)
