# Additional documentation for newcomers

This directory collects technical notes for people who are new to Gymnasium and MuJoCO. It also shows you how to render the simulation so you can see what is happening, instead of it just running in the background.

## Generalities

This project provides a simulation interface for the ORCA hand in the Gymnasium API, which in turn uses MuJoCo as a physical engine and for rendering. The hand classes inherit from the `gymnasium.Env` class. Most method of these classes are therefore directly coming from Gymnasium, and you should check their documentation for more information about each function.

- [Gymnasium documentation](https://gymnasium.farama.org/)
- [MuJoCo documentation](https://mujoco.readthedocs.io/en/stable/overview.html)

## Render simulation

To display an interactive viewer, use `render_mode="human"`. This will make a MuJoCo window appear, which allows you to visualise the hand movements.

```python
from orca_sim import OrcaHandRight

env = OrcaHandRight(render_mode="human")
obs, info = env.reset(seed=0)

for _ in range(200): # number of steps
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        obs, info = env.reset()

env.close()
```

This will open the MuJoCo renderer for a very short time, because the simulation only has 200 steps. Increase number of steps to have longer simulation. More tips on rendering can be found in [rendering.md](./rendering.md).

> On macOS, interactive MuJoCo rendering is usually launched with `mjpython`.

## Cube orientation example

An example script is provided in [examples/cube.py](../examples/cube.py). This script simulates random movements of each joint and shows you how the hand interacts with a cube. The simulation runs until you close the MuJoCo viewer. What is more, you can define the simulation speed. By default, it is real-time.

The objective is to rotate the cube so thatß the red face points up. The reward logic is described in [./cube-reward.md](./cube-reward.md).

## See also

- For more information on mujoco rendering: [rendering.md](./rendering.md)
- Explanations about the reward function of the `OrcaHandRightCubeOrientation` environment: [cube-reward.md](./cube-reward.md)

> Note: this documentation was written with the help of Claude Code, model Claude Opus 5.
