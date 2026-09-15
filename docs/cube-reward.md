# The cube task: reward, success and termination

In this file, you will find more information about the `OrcaHandRightCubeOrientation` reward function.

All values below were measured on `version="v2"`

## The task

The cube has a red face — a thin, non-colliding plate glued to its local **+Z**
side (`task_cube_red_face` in the scene XML). The cube body is declared with
`quat="0 1 0 0"` (a 180° rotation), so the red face starts pointing **straight
down**.

The goal is to flip it so the red face points **up**, within 15°. Rotation about
the vertical axis is free — only the direction the red face points matters, which
makes this much easier than matching a full target orientation.

## Success condition

They are three main steps to compute the reward for a given cube pose.

**1. Compute cube coordinates in world frame** Rotate the cube's local +Z axis into world
coordinates

**2. Extract z coordinate** A dot product with world up
`[0, 0, 1]`, which just extracts the z-component:

```python
alignment = np.dot(normal, WORLD_UP)      # in [-1, 1]
```

| alignment | meaning                                          |
| --------- | ------------------------------------------------ |
| `+1.0`    | red face straight up                             |
| `0.0`     | red face horizontal                              |
| `-1.0`    | red face straight down (this is the start state) |

**3. Set success threshold**: define an angle tolerance

```python
def _goal_reached(self):
    return self._red_face_up_alignment() >= np.cos(self.success_tolerance_rad)
```

`success_tolerance_rad` defaults to 15°, so the bar is `cos(15°) = 0.9659`.

## Reward computation

The following function is used to compute the final reward:

```python
def _get_reward(self) -> float:
    alignment_reward = 0.5 * (self._red_face_up_alignment() + 1.0)
    lift_bonus = np.clip(self.data.xpos[self._cube_body_id, 2] - 0.12, 0.0, 0.12) / 0.12
    drop_penalty = 1.0 if self._cube_dropped() else 0.0
    return float(alignment_reward + 0.10 * lift_bonus - drop_penalty)
```

### Alignment — range [0, 1]

`0.5 * (alignment + 1.0)` rescales alignment from [-1, +1] to [0, 1]. Red face
down scores 0, horizontal scores 0.5, up scores 1.0. Paid **every step**, so
partial progress counts.

### Lift bonus — range [0, 0.1]

A linear ramp on the cube's height, rewarding _keeping the cube up in the fingers_.

| cube height (in m) | `lift_bonus` | contributes |
| ------------------ | ------------ | ----------- |
| ≤ 0.12             | 0.000        | +0.000      |
| 0.15               | 0.250        | +0.025      |
| 0.19 (start)       | 0.583        | +0.058      |
| ≥ 0.24             | 1.000        | +0.100      |

The `0.10` weight caps it at a tenth of what alignment is worth — hence "small".

### Drop penalty — 0 or -1

`-1.0` the moment the cube body falls below z = 0.05.

## Caution: current reward function makes perfect alignment suboptimal

Reaching the goal sets `terminated = True`, which stops the episode. Stopping the
episode stops the per-step income.

| strategy                   | outcome                                           | return    |
| -------------------------- | ------------------------------------------------- | --------- |
| orient properly at step 50 | success → episode ends at step 50                 | **≈ 27**  |
| hover just short of 15°    | never triggers → runs all 200 steps at ~1.04 each | **≈ 208** |

Per-step reward is 1.058 at perfect alignment and 1.038 just below the threshold —
almost identical. But finishing forfeits the remaining ~150 steps of income, so
**deliberately not finishing scores about 8× better.**

## Useful environment options

```python
env = OrcaHandRightCubeOrientation(
    version="v2",
    success_tolerance_rad=np.deg2rad(15.0),    # angle tolerance to consider orientation of the cube successful
    drop_height=0.05,                          # below this height, cube counts as dropped
    max_episode_steps=200,                     # max number of simulation steps per episode
    initial_red_face="down",                   # can also be: "up", "random"
    cube_pos_xy_jitter=0.01,                   # randomize where the cube appears, in meters
)
```

> Note: this documentation was written with the help of Claude Code, model Claude Opus 5.
