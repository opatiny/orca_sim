# Rendering the simulation

This document describes how to render the simulation and how to control the display from Python.

## Rendering modes

The environment class defines the following rendering modes:

- `"human"`: opens an interactive MuJoCo viewer for visualization;
- `"rgb_array"`: renders offscreen and returns a NumPy array of pixels.

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
