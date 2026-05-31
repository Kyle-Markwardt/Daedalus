# Daedalus

**Python reference implementation and RL training backend for [Hawara](https://github.com/Kyle-Markwardt) — an Egyptian labyrinth tile-pushing game.**

Hawara is a digital board game inspired by the shifting-tile labyrinth mechanic, themed around the sunken Egyptian labyrinth near Lake Moeris — the structure described by Herodotus as surpassing even the pyramids. This repository contains the authoritative Python game engine, which serves two purposes:

1. **Reference implementation** — the source of truth for game rules, ported to GDScript for the Godot 4 game
2. **RL training environment** — a Gymnasium-compatible environment for training AI agents (in progress)

The shipped game lives in a separate Godot 4 repository. This repo is the logic layer.

---

## Game Overview

Hawara is a 4-player tile-pushing board game played on a 7×7 grid. On each turn a player:

1. Rotates the spare tile and slides it into any movable row or column (rows/columns 1, 3, 5), pushing one tile off the opposite edge
2. Moves their piece along any connected path reachable from their new position

The goal: collect your 6 assigned artifacts in order, then return to your starting corner to win.

**24 Egyptian artifacts** are hidden across the board — 12 on fixed tiles, 12 shuffled into movable tiles each game. Tokens include the Alabaster Canopic Vessel, Cartouche of Amenemhat, Tekenu Shroud, Mehen Game Board, and others. The Greek mythology token set is preserved as an alternate skin (`token_names_greek` in `board.py`).

---

## Repository Structure

```
Daedalus/
├── Notebooks/
│   ├── board.py          # Board, Tile classes — grid, tile pushing, BFS pathfinding
│   ├── game_logic.py     # Player, LabyrinthEnv — game orchestration, turn logic
│   └── main.py           # CLI game loop (human-playable, matplotlib visualization)
├── tests/
│   ├── conftest.py
│   ├── test_board.py     # Excess tile pool, push mechanics
│   └── test_game_logic.py # Player-tile sync, anti-pushback, end-game
└── requirements.txt
```

---

## Current Status

### Phase 0 — Python Logic (Complete)

All critical game bugs resolved:

| Bug | Status |
|---|---|
| Player pieces not moving with pushed tiles | Fixed — players wrap to opposite edge if pushed off |
| Anti-pushback check silently failing (tuple vs int comparison) | Fixed |
| No end-game condition | Fixed — collect all tokens + return home to win |
| Excess tile always spawning as `straight` type | Fixed — drawn from shuffled movable pool |

**30 unit tests passing** (`pytest tests/`).

### Phase 1 — Godot 4 Port (Up next)

Porting the game engine to Godot 4 (GDScript). The Python implementation here is the spec — every rule, edge case, and BFS algorithm gets replicated exactly before visuals are added.

### Phase 2 — Rule-Based AI

Heuristic opponent evaluating all legal push candidates (up to 44: 11 pushes × 4 orientations) via board state simulation.

### Phase 3 — Web / itch.io Demo

HTML5 export of the Godot build, hosted on itch.io as a free demo.

### Phase 4 — Steam Release

Full visual polish, GodotSteam integration, achievements, Steam Deck support.

### Phase 5+ — RL Training Pipeline

Gymnasium wrapper around this Python environment, trained with `sb3-contrib.MaskablePPO`. Trained policy exported to ONNX and embedded in Godot via GDScript matrix inference — no runtime Python dependency in the shipped game.

---

## Getting Started

### Prerequisites

- Python 3.11
- `numpy`, `matplotlib` (game), `pytest` (tests)

### Installation

```bash
git clone https://github.com/Kyle-Markwardt/Daedalus.git
cd Daedalus
pip install -r requirements.txt
```

### Run the game (CLI)

```bash
cd Notebooks
python main.py
```

### Run tests

```bash
MPLBACKEND=Agg pytest tests/ -v
```

On Windows:

```powershell
$env:MPLBACKEND="Agg"; python -m pytest tests/ -v
```

---

## Architecture

### `Board` (`board.py`)
- 7×7 grid of `Tile` objects
- 16 fixed tiles (corners + interior T-junctions with tokens A–L)
- 33 movable tiles shuffled each game; 1 spare tile held as the excess
- `push_tile(direction, lane)` — shifts row/col 1, 3, or 5; returns exit position
- `get_open_paths()` per tile — drives all BFS pathfinding

### `LabyrinthEnv` (`game_logic.py`)
- Owns the board and 4 `Player` objects
- `step(player_id, action)` — dispatches push or move actions
- `get_valid_moves(pos)` — flood-fill BFS returning all reachable cells
- `is_done()` — returns `(True, winner_id)` when a player collects all tokens and reaches their home corner
- `last_push` — tracks `(direction, lane)` to enforce the anti-pushback rule

### `Player` (`game_logic.py`)
- `home` — starting corner; must be reached after all tokens collected
- `current_card` — the artifact to find next; becomes `'HOME'` when all collected
- `collect_token(token)` — collects if token matches current card; advances to next

---

## License

MIT
