# AIG course materials

The public site of the Autonomous Intelligence Group courses — lecture slides, recordings,
registration: **https://olehsamoilenko.github.io/aig-materials/**

| URL | Page |
|---|---|
| `/` | **Temporary** redirect to `course/engineering/` (`HOME` in `build.py`; set it to `courses/` to make the all-courses page the front door) |
| `/courses/` | All courses |
| `/course/engineering/` | Autonomous Robotic Systems Engineering |
| `/course/intro/` | Introduction to Autonomous Systems |
| `/logo.png`, `/logo-text.png` | The AIG mark and wordmark — other repos hot-link them, keep the names |

**Deploying is pushing.** Every push to `main` runs [`build.py`](build.py) in GitHub Actions
and publishes the result ([`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)) —
about a minute; progress in the **Actions** tab. Nothing to install, nothing to build by hand.

## Adding a lecture

1. **Slides.** Put the PDF in `slides/<course>/`, e.g. `slides/intro/ias-lec06-state-estimation-2.pdf`.
2. **Info.** Add it to that course's `"lectures"` in [`courses.json`](courses.json), copied from
   the PDF's cover. `pdf` is the file name in `slides/<course>/`; `sub` and `topics` are optional.
   ```json
   {
     "num": 6,
     "title": "State Estimation (II)",
     "sub": "Module III",
     "topics": "Kalman filter · …",
     "pdf": "ias-lec06-state-estimation-2.pdf"
   }
   ```
3. **Video**, when it is up. Upload it to the course's playlist, at the end. On YouTube:
   **Share** → `https://youtu.be/<id>?si=…` — copy the `<id>`. Add to the course's `"videos"`:
   ```json
   "6": "https://www.youtube.com/watch?v=<id>&list=<playlist id>&index=<position in the playlist>"
   ```
   `intro` starts at Lecture 1, so `index` = N; `engineering` starts at Lecture 0, so `index` =
   N + 1. A link with only `list` and `index` (no `v=`) does not work — YouTube then starts at
   the first video.
4. **Commit and push** (or open a pull request — it deploys when merged).

A lecture without a video shows its PDF alone. If `courses.json` lists a PDF that is not in
`slides/`, the build fails and nothing is deployed — the live site stays as it was.

**`engineering` is synced from its deck repo** (Marp slides, kept separately and not public):
its PDFs and its `"lectures"` are written from the decks' covers, so a hand edit to them would be
overwritten on the next sync. Its `"videos"` and everything else are edited here as usual.

```bash
python3 tools/sync_engineering.py               # deck repo cloned next to this one, ../ros2-course
python3 tools/sync_engineering.py PATH/TO/DECKS # or anywhere else
```

The sync lists a deck once its PDF has been exported next to it, copies that PDF into
`slides/engineering/`, and takes the title, subtitle and topics from the cover. It deletes
nothing. Then add the video (above) and commit.

## Checking before pushing

```bash
python3 build.py                          # prints the lectures per course
python3 -m http.server 8000 -d _site      # http://localhost:8000/ — Ctrl+C to stop
```

`_site/` is output only — deleted and rebuilt on every build, not committed.

## Other changes

| What | Where |
|---|---|
| A new course | one more object in `courses.json` — `slug` (its URL), `status` (the heading it goes under; `Ongoing` gets the green dot), `title`, `eyebrow`, `tagline`, `register`, `playlist`, `lectures`, `videos` — and a `slides/<slug>/` folder |
| Form and playlist links | `courses.json` |
| LinkedIn | `templates/courses.html` |
| Footer (same on every page) | `FOOTER` in `build.py` |
| Where `/` goes | `HOME` in `build.py` |
| Look | `assets/style.css` — monochrome, square corners, hard shadows, like the lecture decks |

| Path | What it is |
|---|---|
| `courses.json` | Everything the site shows |
| `slides/<course>/` | The lecture PDFs |
| `templates/` | `courses.html` (all courses) and `course.html` (one course) |
| `assets/` | `style.css` and the logos, copied to the site root |
| `build.py` | Fills the templates → `_site/`. Python 3, standard library only |
| `tools/sync_engineering.py` | Pulls the engineering lectures in from the deck repo |
| `CLAUDE.md` | Conventions for an AI agent working in this repo |
| `.github/workflows/deploy.yml` | Builds and publishes on every push to `main` |

## Access and setup

- **To contribute:** the owner adds you under **Settings → Collaborators** (then you push to
  `main`), or fork and open a pull request.
- **One-time:** **Settings → Pages → Build and deployment → Source: GitHub Actions**.
