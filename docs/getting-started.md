# Getting started with ORCA Hand and `orca_sim`

This project provides a simulation interface for the ORCA hand in the Gymnasium API, which in turn uses MuJoCo as a physical engine and for rendering. The hand classes inherit from the `gymnasium.Env` class. Most method of these classes are therefore directly coming from Gymnasium, and you should check their documentation for more information about each function.

## Reference documentation

- [Gymnasium documentation](https://gymnasium.farama.org/)
- [MuJoCo documentation](https://mujoco.readthedocs.io/en/stable/overview.html)

## Rendered simulation

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

This will open the MuJoCo renderer for a very short time, because the simulation only has 200 steps. Increase number of steps to have longer simulation.

> On macOS, interactive MuJoCo rendering is usually launched with `mjpython`.

## Cube reorientation example

The cube task is the recommended beginner example because it exercises the full environment loop: reset, action application, reward computation, termination, and viewer interaction.

```python
from orca_sim import OrcaHandRightCubeOrientation

env = OrcaHandRightCubeOrientation(version="v2", render_mode="human")
obs, info = env.reset(seed=0)

for _ in range(200):
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        obs, info = env.reset()

env.close()
```

This task places a cube on the hand and defines a red face as the objective. The implementation and reward logic are described in [./cube-reward.md](./cube-reward.md).

## See also

- [rendering.md](./rendering.md)
- [cube-reward.md](./cube-reward.md)
- [README.md](../README.md)

> Note: this documentation was assisted by GitHub Copilot, version MAI-Code-1.1-Flash.
