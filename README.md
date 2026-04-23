# AI 201 — Week 6: Advanced Git & Collaboration

## Instructor Demo Guide

This repo powers the Week 6 live demo: rebasing two feature branches, hitting a real merge conflict, and resolving it by intent — live, in VS Code, while narrating the decision-making out loud.

There is no AI or LLM in this demo. The focus is entirely on the Git workflow.

---

## The Scenario

Two contributors have been working on the game night scheduler in parallel:

- **`feature/dedup-games`** — added a duplicate check to `add_game()` so the same game can't appear twice in the rotation
- **`feature/random-picker`** — added a `pick_random()` method and also modified `add_game()` to shuffle the list on every insert

Both changes touch the same method. When you rebase `feature/random-picker` onto `feature/dedup-games`, git stops and asks you to decide what `add_game()` should look like.

The resolution preserves both intents: keep the dedup check, keep `pick_random()`, and drop the shuffle (because shuffling on every `add_game()` call is the wrong place for that randomness — `pick_random()` already handles it).

---

## Setup (Do This Before Class)

### 1. Clone the repo

```bash
git clone <github-url>
cd ai201-week6-game-night
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Confirm both branches exist

```bash
git branch -a
```

You should see `main`, `feature/dedup-games`, and `feature/random-picker`.

### 4. Run tests on main to confirm the baseline

```bash
pytest tests/ -v
```

Expected output — 3 pass, 2 skip-worthy (the dedup and pick_random tests will fail on main, which is expected and intentional):

```bash
PASSED tests/test_scheduler.py::test_add_game
PASSED tests/test_scheduler.py::test_build_schedule_cycles_through_games
PASSED tests/test_scheduler.py::test_build_schedule_raises_with_no_games
FAILED tests/test_scheduler.py::test_add_game_skips_duplicates
FAILED tests/test_scheduler.py::test_pick_random_returns_a_game_from_rotation
FAILED tests/test_scheduler.py::test_pick_random_returns_none_when_rotation_is_empty
```

The 3 failing tests are the spec for what the resolved code needs to satisfy. After conflict resolution, all 6 should pass.

### 5. Open the repo in VS Code

```bash
code .
```

Make sure the **GitLens** or built-in **Source Control** panel is visible. During the demo, VS Code will show the conflict markers inline with Accept/Ignore buttons — that's the UI you'll resolve in.

### 6. Keep `conflict_resolution.py` open as a reference tab

This file shows the correct resolved version with annotations. Do not share your screen while this tab is open — it's for your reference only. You can open it on a second monitor or a separate window.

---

## Demo Script (~10 minutes)

### Before opening the terminal (1 min)

Show students the two feature branches in the Source Control panel or by running:

```bash
git log --oneline --all --graph
```

Walk through the history out loud:

> "Here's what we've got. `main` has three commits — the base scheduler, a summary method, and the test suite. Then two contributors branched off and went in different directions. One was fixing a data quality issue — duplicate games in the rotation. The other was adding a feature — random game selection. Neither one knew what the other was doing."

---

### Start the rebase (2 min)

```bash
git checkout feature/random-picker
git log --oneline
```

> "This branch has one commit: adding `pick_random()` and a shuffle to `add_game()`. We want to bring in the dedup work before we merge this to main. So we're going to rebase onto `feature/dedup-games`."

```bash
git rebase feature/dedup-games
```

Git stops with a conflict message. The terminal output will look something like:

```bash
CONFLICT (content): Merge conflict in scheduler.py
error: could not apply abc1234... feat: add pick_random method and shuffle rotation on add
hint: Resolve all conflicts manually, mark them as resolved with
hint: "git add/rm <conflicted_files>", then run "git rebase --continue".
```

> "Git is telling us it can't automatically combine these two changes. Both branches touched the same method. Let's go see what it looks like."

---

### Read the conflict markers (2 min)

Open `scheduler.py` in VS Code. The conflict section will look like this:

```python
    def add_game(self, game: str) -> None:
<<<<<<< HEAD
        """Add a game to the rotation. Skips duplicates."""
        if game not in self.games:
            self.games.append(game)
=======
        """Add a game to the rotation and shuffle for varied order."""
        self.games.append(game)
        random.shuffle(self.games)
>>>>>>> feat: add pick_random method and shuffle rotation on add
```

Read both sides out loud:

> "HEAD is `feature/dedup-games` — it added a duplicate check before the append. The incoming change — `feature/random-picker` — changed the docstring and added a shuffle after the append. Git marked both versions and stopped. It doesn't know which one is right. That's our job."

> "Before I touch anything — what was each change *trying to do*? The dedup branch was preventing data quality issues: the same game appearing twice in the rotation. The random-picker branch was trying to vary the order. Those are different goals. A resolution that only picks one side loses something."

---

### Resolve the conflict in VS Code (3 min)

Click **"Accept Both Changes"** in VS Code's conflict UI as a starting point. This gives you both versions stacked. Now manually edit the method to look like this:

```python
    def add_game(self, game: str) -> None:
        """Add a game to the rotation. Skips duplicates."""
        if game not in self.games:
            self.games.append(game)
```

Narrate as you edit:

> "I'm keeping the dedup check — that's the whole point of `feature/dedup-games`. I'm dropping the shuffle. Here's why: `pick_random()` is already on this branch, and it uses `random.choice()` to pick unpredictably at call time. Shuffling on every `add_game()` call is a side effect that callers don't expect — every time someone adds a game, the order of the list silently changes. That's a bug waiting to happen. The randomness belongs in `pick_random()`, not here."

Also verify that `pick_random()` is present in the file — it should be, since it came from the `feature/random-picker` commit but isn't part of the conflict. Point it out:

> "And `pick_random()` is still here — unaffected by the conflict. That feature is fully preserved."

Make sure `import random` is at the top of the file (it was added by `feature/random-picker`).

---

### Complete the rebase (1 min)

```bash
git add scheduler.py
git rebase --continue
```

Git will prompt for a commit message — keep the existing one or press `:wq` / save and close.

Then show the clean history:

```bash
git log --oneline
```

Output:

```bash
def4567 feat: add pick_random method and shuffle rotation on add
abc1234 fix: prevent duplicate games in rotation when add_game is called
789abcd chore: add pytest test suite and requirements
456def0 feat: add schedule summary and host display to scheduler
123abc9 feat: initialize game night scheduler with add and schedule methods
```

> "Linear history. No merge commit. If you squinted at this log, you'd never know two people worked on this in parallel. That's the whole point of rebasing before you open a PR — you give the reviewer a clean story."

---

### Run the tests (1 min)

```bash
pytest tests/ -v
```

All 6 tests pass:

```bash
PASSED tests/test_scheduler.py::test_add_game
PASSED tests/test_scheduler.py::test_build_schedule_cycles_through_games
PASSED tests/test_scheduler.py::test_build_schedule_raises_with_no_games
PASSED tests/test_scheduler.py::test_add_game_skips_duplicates
PASSED tests/test_scheduler.py::test_pick_random_returns_a_game_from_rotation
PASSED tests/test_scheduler.py::test_pick_random_returns_none_when_rotation_is_empty

6 passed in 0.12s
```

> "Both intents are preserved. The dedup test passes. The random picker tests pass. And the original baseline tests still pass — we didn't break anything."

---

## Troubleshooting

**`git rebase` doesn't produce a conflict** — Check that you're on `feature/random-picker` before rebasing. If you accidentally ran the rebase from a different branch, `git rebase --abort` to reset and try again.

**VS Code doesn't show the inline conflict UI** — Make sure you're using VS Code 1.70 or later. The conflict markers are always in the file even if the UI doesn't render — you can resolve manually by deleting the `<<<<<<<`, `=======`, and `>>>>>>>` lines.

**Tests fail after resolution** — Open `conflict_resolution.py` and compare your resolved `add_game()` against it. The most common mistake is keeping the `random.shuffle()` line or accidentally deleting `pick_random()`.

**`import random` is missing from the top of the file** — Add it manually below the existing imports. It was introduced by `feature/random-picker` but may have been dropped during an imperfect resolution.

**Accidentally committed during rebase** — Run `git rebase --abort` to return to the pre-rebase state and start over.
