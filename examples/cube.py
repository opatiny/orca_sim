"""In-hand cube reorientation, with a viewer that stays open and a simulation in real time.
Goal: rotate cube so red face point up.

On MacOS, run with:  mjpython cube.py        (mjpython is required for the viewer on macOS)
"""

import time

import numpy as np

from orca_sim import OrcaHandRightCubeOrientation

# --- parameters ---------------------------------------------------------------
SPEED = 1  # 1.0 = real time, 0.25 = slow motion, 4.0 = fast, 0 = uncapped
EPISODES = None  # None = run until you close the window
SMOOTHING = 0.05  # 0..1, how fast the random target is chased
POSE_REFRESH = 40  # how many steps to keep the same target pose for
# -------------------------------------------------------------------------

env = OrcaHandRightCubeOrientation(
    version="v2",  # version of the hand
    render_mode="human",  # render the environment to the screen in MuJoCo viewer
    max_episode_steps=200,  # maximum number of steps per episode
    frame_skip=5,  # number of simulation steps to run before each action
)

# default timestep is 2ms and frame_skip is 5
# Duration of one env step
dt = env.model.opt.timestep * env.frame_skip


def new_episode():
    options = env.sample_randomized_reset_options(
        seed=None,  # None = a different cube pose every episode
        initial_red_face="random",
        cube_pos_xy_jitter=0.01,  # randomize where cube appears in XY plane in meters
    )
    return env.reset(options=options)


obs, info = new_episode()

# reset() already rendered once, so the viewer handle exists by now.
viewer = env._viewer

action = np.zeros(env.action_space.shape, dtype=np.float32)
episode = 0

while viewer is None or viewer.is_running():  # keep running until the viewer is closed
    frame_start = time.perf_counter()
    stepCount = info.get("elapsed_steps", 0)

    # Placeholder policy: chase a random target slowly, so the motion stays
    if stepCount % POSE_REFRESH == 0:  # new pose every N steps
        # draw random value in rad for each of the 17 joints (defines a new pose to reach)
        target = env.action_space.sample()
    action += SMOOTHING * (target - action)
    obs, reward, terminated, truncated, info = env.step(
        np.clip(action, env.action_low, env.action_high)
    )

    # terminated: goal reached or cube dropped, truncated: max steps reached
    if terminated or truncated:
        episode += 1
        print(
            f"episode {episode:3d} | steps {info['elapsed_steps']:3d} "
            f"| success {info['is_success']} | dropped {info['dropped']} "
            f"| reward {reward:+.3f}"
        )
        if EPISODES is not None and episode >= EPISODES:
            break
        obs, info = new_episode()

    # Pace the loop against the wall clock. Without this the sim runs as fast
    # as Python can iterate, which is much faster than real time.
    if SPEED > 0:
        time.sleep(max(0.0, dt / SPEED - (time.perf_counter() - frame_start)))

env.close()
