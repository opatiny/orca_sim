# The cube task: reward, success and termination

How `OrcaHandRightCubeOrientation` scores what the hand is doing.

All numbers below were measured on `version="v2"`

## The task

The cube has a red face — a thin, non-colliding plate glued to its local **+Z**
side (`task_cube_red_face` in the scene XML). The cube body is declared with
`quat="0 1 0 0"` (a 180° rotation), so the red face starts pointing **straight
down**.

The goal is to flip it so the red face points **up**, within 15°. Rotation about
the vertical axis is free — only the direction the red face points matters, which
makes this much easier than matching a full target orientation.

## Success condition

Three steps, all in `task_envs.py`.

**1. Where is the red face pointing?** Rotate the cube's local +Z axis into world
coordinates:

```python
def _cube_red_face_world_normal(self):
    w, x, y, z = self._normalize_quat(self._cube_quat())
    return np.array([2*(x*z + y*w), 2*(y*z - x*w), 1 - 2*(x*x + y*y)])
```

That is the third column of the rotation matrix built from the cube's quaternion.
It matches MuJoCo's own `data.xmat[cube_body].reshape(3, 3)[:, 2]` to 1e-6.

**2. How well does that line up with "up"?** A dot product with world up
`[0, 0, 1]`, which just extracts the z-component:

```python
alignment = np.dot(normal, WORLD_UP)      # in [-1, 1]
```

| alignment | meaning                                          |
| --------- | ------------------------------------------------ |
| `+1.0`    | red face straight up                             |
| `0.0`     | red face horizontal                              |
| `-1.0`    | red face straight down (this is the start state) |

**3. Threshold it:**

```python
def _goal_reached(self):
    return self._red_face_up_alignment() >= np.cos(self.success_tolerance_rad)
```

`success_tolerance_rad` defaults to 15°, so the bar is `cos(15°) = 0.9659`.

## The reward formula

```python
def _get_reward(self) -> float:
    alignment_reward = 0.5 * (self._red_face_up_alignment() + 1.0)
    lift_bonus = np.clip(self.data.xpos[self._cube_body_id, 2] - 0.12, 0.0, 0.12) / 0.12
    drop_penalty = 1.0 if self._cube_dropped() else 0.0
    return float(alignment_reward + 0.10 * lift_bonus - drop_penalty)
```

Three terms:

### Alignment — range [0, 1]

`0.5 * (alignment + 1.0)` rescales alignment from [-1, +1] to [0, 1]. Red face
down scores 0, horizontal scores 0.5, up scores 1.0. Paid **every step**, so
partial progress counts.

### Lift bonus — range [0, 0.1]

A linear ramp on the cube's height, rewarding _keeping the cube up in the fingers_
rather than letting it sag into the palm or dribble toward being dropped:

| cube z       | `lift_bonus` | contributes |
| ------------ | ------------ | ----------- |
| ≤ 0.12       | 0.000        | +0.000      |
| 0.15         | 0.250        | +0.025      |
| 0.19 (start) | 0.583        | +0.058      |
| ≥ 0.24       | 1.000        | +0.100      |

The `0.10` weight caps it at a tenth of what alignment is worth — hence "small".
Two wrinkles: the ramp bottoms out at z = 0.12 while `drop_height` is 0.05, so
there is a **dead zone** between them where the cube is slipping but the score says
nothing; and the ceiling at 0.24 is never reached in practice (the cube starts at
0.19 and was measured between 0.143 and 0.190), so it acts as a plain linear term.

### Drop penalty — 0 or -1

`-1.0` the moment the cube body falls below z = 0.05.

## Current rewards function makes perfect alignment suboptimal

Reaching the goal sets `terminated = True`, which stops the episode. Stopping the
episode stops the per-step income.

| strategy                 | outcome                                           | return    |
| ------------------------ | ------------------------------------------------- | --------- |
| flip properly at step 50 | success → episode ends at step 50                 | **≈ 27**  |
| hover just short of 15°  | never triggers → runs all 200 steps at ~1.04 each | **≈ 208** |

Per-step reward is 1.058 at perfect alignment and 1.038 just below the threshold —
almost identical. But finishing forfeits the remaining ~150 steps of income, so
**deliberately not finishing scores about 8× better.**

## Some environment options

All on the constructor:

```python
env = OrcaHandRightCubeOrientation(
    version="v2",
    success_tolerance_rad=np.deg2rad(15.0),   # how close counts as success
    drop_height=0.05,                          # below this z, cube counts as dropped
    max_episode_steps=200,                     # 200 steps = 2 s of simulated time
    initial_red_face="down",                   # or "up", "random"
    cube_pos_xy_jitter=0.0,                    # start-position randomization
)
```
