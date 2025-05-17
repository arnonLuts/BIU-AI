import zuma
import ex2
from typing import List, Dict
from tabulate import tabulate
import random
import time

example = {
    'chosen_action_prob': {1: 0.6, 2: 0.7, 3: 0.5, 4: 0.9},
    # 'chosen_action_prob': {1: 1, 2: 1, 3: 1, 4: 1},
    'next_color_dist': {1: 0.1, 2: 0.6, 3: 0.15, 4: 0.15},
    'color_pop_prob': {1: 0.6, 2: 0.7, 3: 0.4, 4: 0.9},
    'color_pop_reward': {'3_pop': {1: 3, 2: 1, 3: 2, 4: 2},
                         'extra_pop': {1: 1, 2: 2, 3: 3, 4: 1}},
    'color_not_finished_punishment': {1: 2, 2: 3, 3: 5, 4: 1},
    'finished_reward': 150,
    'seed': 42}

def solve(game: zuma.Game) -> float:
    policy = ex2.Controller(game)
    num_moves = game.get_current_state()[3]  # Get the number of moves from the state
    for i in range(num_moves):
        game.submit_next_action(chosen_action=policy.choose_next_action())
    reward = game.get_current_reward()
    return reward

def run_game_configuration(moves: int, initial_state: List[int], config: Dict, debug_mode: bool,
                           num_runs: int = 80, rand: bool = False) -> float:
    total_reward = 0
    config_copy = config.copy()  # Create a copy of the config to avoid modifying the original
    random.seed(time.time())
    for i in range(num_runs):
        config_copy['seed'] = random.randint(1, 100) if rand else i
        game = zuma.create_zuma_game((moves, initial_state.copy(), config_copy, debug_mode))
        total_reward += solve(game)
    return total_reward / num_runs

def main():
    debug_mode = False
    target_rewards = {
        "test1": 10.93, "test2": -12.36, "test3": 104.74, "test4": 118.55, "test5": 124.85,
        "test6": 107.71, "test7": 138.21, "test8": 108.69, "test9": 3.14, "test10": -5.38,
        "test11": 3.24, "test12": 3.79, "test13": -6.19, "test14": 8.79, "test15": 10.69,
        "test16": 13.48, "test17": 12.45, "test18": 13.1, "test19": 13.74, "test20": 19.5,
        "test21": 18.74, "test22": 15.67, "test23": 9.82
    }
    game_configurations = [
        # Format: (moves, initial_state, description)
        (20, [1, 1], "test1"),
        (20, [1, 2, 3, 3, 3, 4, 2, 1, 2, 3, 4, 4], "test2"),
        (200, [1, 2, 3, 3, 3, 4, 2, 1, 2, 3, 4, 4], "test3"),
        (200, [1, 2, 1, 2, 1, 2, 1, 2], "test4"),
        (200, [3, 3, 3, 3, 3, 4, 4, 4, 4, 4], "test5"),
        (200, [1, 4, 2, 3, 4, 1, 3, 2, 4, 1], "test6"),
        (200, [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3], "test7"),
        (200, [1, 4, 4, 2, 2, 3, 3, 1, 1, 4, 4, 2, 2, 3, 3], "test8"),
        (30, [1, 2, 1, 2, 3], "test9"),
        (30, [4, 3, 4, 3, 4], "test10"),
        (30, [2, 2, 3, 3, 4], "test11"),
        (30, [1, 1, 1, 2, 2], "test12"),
        (30, [4, 1, 4, 1, 3], "test13"),
        (54, [1, 4, 1, 4, 2], "test14"),
        (54, [2, 3, 2, 3, 4], "test15"),
        (54, [3, 3, 2, 2, 1], "test16"),
        (54, [1, 2, 3, 1, 2], "test17"),
        (54, [4, 4, 4, 3, 2], "test18"),
        (54, [3, 4, 2, 4, 3], "test19"),
        (54, [1, 2, 4, 1, 3], "test20"),
        (54, [2, 2, 1, 3, 1], "test21"),
        (54, [3, 1, 3, 4, 2], "test22"),
        (54, [4, 1, 2, 4, 3], "test23")
    ]

    # Run all configurations and collect results
    results = []
    total_difference = 0
    rand = True
    for moves, initial_state, description in game_configurations:
        initial_state_copy = initial_state.copy()  # Create a copy of the initial state
        avg_reward = run_game_configuration(moves, initial_state_copy, example, debug_mode, rand = rand)
        goal_reward = target_rewards[description]
        difference = avg_reward - goal_reward
        total_difference += difference
        results.append([description, moves, str(initial_state), f"{avg_reward:.2f}", f"{goal_reward:.2f}", f"{difference:.2f}"])

    # Calculate overall average difference
    overall_avg_difference = total_difference / len(game_configurations)

    # Print results table
    headers = ["Game Description", "Moves", "Initial State", "Average Reward", "Goal Reward", "Difference"]
    print("\nZuma Games Results Summary:")
    print(tabulate(results, headers=headers, tablefmt="grid"))

    # Print overall statistics
    print(f"\nOverall Average Difference from Goal Rewards: {overall_avg_difference:.2f}")

if __name__ == "__main__":
    main()
