# Gymnasium and MuJoCo in this repository

This repository uses the Gymnasium API for environment interaction and MuJoCo for rigid-body simulation and rendering.
--- explain that the OrcaHand class is a wrapper (what is correct word) which uses the Gymnasium env class, so a lot of methods come directly from gymnasium and can be found in their doc

--- add section here with links to gymnasium and mujoco docs

## Gymnasium interface

The environment class inherits from `gymnasium.Env`:

```python
class BaseOrcaHandEnv(gym.Env[np.ndarray, np.ndarray]):
```

The essential methods are:

- `reset()`: initialize the simulator state and return an observation and metadata;
- `step(action)`: apply an action, integrate the physics, and return observation, reward, termination, truncation, and information;
- `render()`: open a viewer or return an image array depending on `render_mode`.
  --- render automatically called in step?

The action space is a bounded continuous box corresponding to the MuJoCo actuator limits:
--- what is bounded continuous box -Y rephrase, specify dimensions of variables and units

```python
self.action_space = spaces.Box(
    low=self.action_low,
    high=self.action_high,
    dtype=np.float32,
)
```

The observation is built from the raw MuJoCo state which consists of the joint positions and velocities.

```python
return np.concatenate([self.data.qpos.copy(), self.data.qvel.copy()])
```

## Action and state flow

The control flow is simple and explicit:

```python
action = np.asarray(action, dtype=np.float32)
self.data.ctrl[:] = np.clip(action, self.action_low, self.action_high)
mujoco.mj_step(self.model, self.data, nstep=self.frame_skip)
```

This means:

1. the policy produces an action;
2. the action is clipped to actuator limits;
3. the control signal is written into MuJoCo data;
4. MuJoCo integrates the dynamics for `frame_skip` substeps;
5. the environment returns the updated observation and metadata.

The `frame_skip` value is part of the simulation policy design: it allows the environment to run the simulator at a higher internal integration rate than the policy acts.

## Reset semantics

The base environment reset path is also simple:

```python
mujoco.mj_resetData(self.model, self.data)
```

This initializes the model state to its default configuration. Additional reset options can override the joint configuration or object pose when needed. This is especially relevant in the cube task environment, where the cube pose and hand pose are set explicitly as part of a task reset.

## Why this combination is useful

Gymnasium provides a clean RL interface and MuJoCo provides physically plausible rigid-body dynamics and a viewer. Together they allow a compact environment API while retaining the underlying simulator expressiveness.

For a new user, the most important practical idea is that the environment is not a black box: the model, scene, and data objects are directly available. For many tasks, a user can inspect the MJCF, understand the joint topology, and then modify the task logic or environment reset behavior without rewriting the entire simulation stack.

## See also

- [getting-started.md](./getting-started.md)
- [rendering.md](./rendering.md)
- [README.md](../README.md)

> Note: this documentation was assisted by GitHub Copilot, version MAI-Code-1.1-Flash.
