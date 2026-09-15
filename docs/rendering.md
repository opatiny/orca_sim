# Rendering the simulation

This document describes how to render the simulation and how to control the display from Python.

## Rendering modes

The environment class defines the following rendering modes:

```python
metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 30}
```

The main modes are:

- `"human"`: opens an interactive MuJoCo viewer for visualization;
- `"rgb_array"`: renders offscreen and returns a NumPy array of pixels.

## Displaying the simulation in mujoco viewer

```python
from orca_sim import OrcaHandRight

env = OrcaHandRight(render_mode="human")
obs, info = env.reset(seed=0)

for _ in range(1000): # number of steps
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)

env.close()
```

With this script, the viewer will close after the 1000 steps are computed.

## macOS note: use `mjpython`

On macOS, interactive MuJoCo rendering may fail when launched from a plain Python process. The environment raises a clear error in that case and recommends using `mjpython`.

```bash
mjpython my_script.py
```

## Keeping the viewer open

The MuJoCo passive viewer is non-blocking: it closes when the end of the script is reached. To keep the viewer open, you can use:

```python
env = OrcaHandRight(render_mode="human")
obs, info = env.reset()

while env._viewer is not None and env._viewer.is_running():
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)

env.close()
```

With `env._viewer.is_running()`, the viewer with the simulaiton will run until the user closes it.

This tip is used in [../examples/cube.py](../examples/cube.py).

## See also

- [getting-started.md](./getting-started.md)
- [cube-reward.md](./cube-reward.md)
- [README.md](../README.md)

> Note: this documentation was assisted by GitHub Copilot, version MAI-Code-1.1-Flash.
> ß
