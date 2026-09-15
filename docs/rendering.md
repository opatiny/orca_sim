# Rendering the simulation

This document describes how simulation windows are created and how to control the display from Python.

## Rendering modes

The environment class defines the following rendering modes:

```python
metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 30}
```

The main modes are:

- `"human"`: opens an interactive MuJoCo viewer for visualization;
- `"rgb_array"`: renders offscreen and returns a NumPy array of pixels.

The base implementation is in `src/orca_sim/envs.py`.

## Minimal interactive render

```python
from orca_sim import OrcaHandRight

env = OrcaHandRight(render_mode="human")
obs, info = env.reset(seed=0)

for _ in range(50):
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)

env.close()
```

This keeps the simulator running and calls the viewer synchronizer through the environment render method.

## Offscreen rendering

For image processing or automated evaluation, `rgb_array` is more suitable.

```python
from orca_sim import OrcaHandRight

env = OrcaHandRight(render_mode="rgb_array")
obs, info = env.reset(seed=0)

frame = env.render()
print(frame.shape)

env.close()
```

This produces a rendered image as a NumPy array, which can be passed to downstream processing or saved to disk.

## macOS note: use `mjpython`

On macOS, interactive MuJoCo rendering may fail when launched from a plain Python process. The project explicitly raises a clear error in that case and recommends `mjpython`.

```bash
mjpython my_script.py
```

This is the appropriate way to launch an interactive viewer on macOS, because MuJoCo requires the Python executable used by the viewer to be compatible with the underlying native integration.

## Viewer lifetime and playback speed

The passive viewer is non-blocking. It returns immediately and then expects later calls to `sync()`. A script that resets and terminates immediately may show the viewer for only a brief instant before the process exits.

A common pattern is to keep stepping until the window is closed by the user:

```python
env = OrcaHandRight(render_mode="human")
obs, info = env.reset()

while env._viewer is not None and env._viewer.is_running():
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)

env.close()
```

## Simulation frequency and control rate

### 2. `frame_skip` — defines observation rate

The number of **physics substeps run per `env.step()`**. It decouples the rate your
policy acts at from the rate MuJoCo integrates at:

```python
self.data.ctrl[:] = np.clip(action, self.action_low, self.action_high)
mujoco.mj_step(self.model, self.data, nstep=self.frame_skip)
```

With the defaults (`timestep = 0.002`, `frame_skip = 5`):

|                       | rate   | interval |
| --------------------- | ------ | -------- |
| physics integration   | 500 Hz | 2 ms     |
| control / observation | 100 Hz | 10 ms    |

One `env.step()` runs the simulator forward five times **holding your action
constant** across all five (a zero-order hold). The state is observed only after
the last substep.

## See also

- [getting-started.md](./getting-started.md)
- [gymnasium-mujoco.md](./gymnasium-mujoco.md)
- [README.md](../README.md)

> Note: this documentation was assisted by GitHub Copilot, version MAI-Code-1.1-Flash.
