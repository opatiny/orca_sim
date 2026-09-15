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

With `env._viewer.is_running()`, the viewer with the simulation will run until the user closes the MuJoCo viewer.

For a more complete example, check [../examples/cube.py](../examples/cube.py).

> Note: this documentation was written with the help of Claude Code, model Claude Opus 5.
