# Getting started with ORCA Hand and `orca_sim`

This project provides a simulation interface for the ORCA hand in the Gymnasium API. The environment is built on MuJoCo, and the simulation assets are provided as MJCF and XML scene files. The intended entry point is a beginner-friendly environment with a minimal API surface and clear task examples.

## Scope

The repository contains:

- the environment factory for left, right, and combined hand configurations;
- a task example for in-hand cube reorientation;
- MJCF and scene XML files defining the hand geometry and kinematics;
- a Python interface compatible with Gymnasium.

This is enough to start from a simple environment and progressively build more complex control policies or manipulation tasks.

## Installation

We recommend Python 3.11 in a virtual environment.

### Using `uv`

```bash
uv venv orca --python 3.11
source orca/bin/activate
uv pip install orca_sim
```

### Using `conda`

```bash
conda create -n orca python=3.11 -y
conda activate orca
python -m pip install orca_sim
```

### Working from source

```bash
git clone https://github.com/orcahand/orca_sim
cd orca_sim
uv pip install -e .
```

This is the recommended approach for development, because it exposes the repository source code and task definitions directly.

## Minimal example

```python
from orca_sim import OrcaHandRight

env = OrcaHandRight(render_mode="rgb_array")
obs, info = env.reset(seed=0)

action = env.action_space.sample()
obs, reward, terminated, truncated, info = env.step(action)

env.close()
```

This script performs the minimal interaction loop:

1. instantiate an environment;
2. reset the simulator state;
3. sample an action from the action space;
4. step the environment;
5. close the renderer or viewer when finished.

## Rendered simulation

To display an interactive viewer, use `render_mode="human"`.

```python
from orca_sim import OrcaHandRight

env = OrcaHandRight(render_mode="human")
obs, info = env.reset(seed=0)

for _ in range(200):
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        obs, info = env.reset()

env.close()
```

On macOS, MuJoCo human rendering may require the `mjpython` launcher. See [rendering.md](./rendering.md) for details.

## Task example: cube reorientation

The repository includes a task-level environment for right-hand cube reorientation.

```python
from orca_sim import OrcaHandRightCubeOrientation

env = OrcaHandRightCubeOrientation(version="v2", render_mode="human")
obs, info = env.reset(seed=0)
```

This task places a cube on the palm and defines a target orientation. A useful starting point is to inspect the nominal reset and the randomized reset options.

```python
nominal = env.nominal_reset_options()
obs, info = env.reset(options=nominal)

randomized = env.sample_randomized_reset_options(
    seed=0,
    initial_red_face="random",
    cube_pos_xy_jitter=0.01,
)
obs, info = env.reset(options=randomized)
```

## Repository structure

The important directories are:

- `src/orca_sim/envs.py`: base environment and hand-specific wrappers;
- `src/orca_sim/task_envs.py`: task logic and reset logic;
- `src/orca_sim/scenes/`: MuJoCo scene XML files;
- `src/orca_sim/models/`: MJCF model files for each embodied version.

The environment follows the Gymnasium API, with `reset()` and `step()` as the main interaction methods.

## See also

- [gymnasium-mujoco.md](./gymnasium-mujoco.md)
- [rendering.md](./rendering.md)
- [README.md](../README.md)

> Note: this documentation was assisted by GitHub Copilot, version MAI-Code-1.1-Flash.
