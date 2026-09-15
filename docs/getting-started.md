# Getting started with ORCA Hand and `orca_sim`

This project provides a simulation interface for the ORCA hand in the Gymnasium API, which in turn uses MuJoCo as a physical engine and for rendering.

## Rendered simulation

To display an interactive viewer, use `render_mode="human"`.

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

> On macOS, MuJoCo human rendering may require the `mjpython` launcher.

## Cube reorientation complete example with human rendering

A good example code for beginner based on the cube reorientation task can be found in: --- add link here

In this script, the simulation is rendered, so you see what happens. It is also slowed down to real time instead of running as fast as Python can handle. Moreover, the MuJoCo window does not close by itself, so you can watch the hand move for as long as you want.

## See also

- [gymnasium-mujoco.md](./gymnasium-mujoco.md)
- [rendering.md](./rendering.md)
- [README.md](../README.md)

> Note: this documentation was assisted by GitHub Copilot, version MAI-Code-1.1-Flash.
