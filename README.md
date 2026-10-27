# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

TakeMeter sorts comments from **r/csmajors**, the public subreddit for computer
science students, into four kinds: `experience` (the writer reports what
happened to them, with an outcome or a number), `argued` (a claim or advice
backed by something the reader could check), `hot_take` (a confident claim with
no checkable support) and `chatter` (questions, check-ins, support, venting and
jokes). It's a fine-tuned DistilBERT trained on 266 comments I collected and
labelled. The point is to separate the comments worth reading in a recruiting
thread, a real data point or a checkable argument, from the confident noise
around them.

---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

Four labels for r/csmajors comments. Every comment gets exactly one. They come
from four distinctions I saw while reading 69 comments (`notes/milestone1.md`)
and were tightened by a stress test (`notes/stress_test.md`).

### `experience`

**Definition:** Reports something that happened to the writer, with an outcome
or a measured detail: an offer, a rejection, an invite, pay, a timeline or a
count.

**Example 1:**
> i finished the OA at 10:30 PM on the 23rd of September, recruiter emailed me asking for some info and scheduling on the 25th of September. got the times/date for the two interviews a day later.

**Example 2:**
> 160 base, 320 that vests across 4 years + a relocation bonus (can't say and not included because you could lowkey try and doxx me with it). This is at an established firm, not a startup.

### `argued`

**Definition:** Makes a claim about the field or gives advice, and backs it
with a reason the reader could check: a company practice, a recruiting step, a
number, or something the writer or others saw happen.

**Example 1:**
> I am also under review. According to sources online for JPMC, under review means it passed ATS and is sitting in queue. Under consideration means a recruiter reviewed your resume, verified basic qualifications, and shortlisted your app to the hiring manager. So im ngl its pretty unlikely we get anything because we haven't even been seen by the normal recruiter yet obv dont lose hope.

**Example 2:**
> Try changing up your resume or getting it professionally reviewed. If you're not getting interviews it usually is something with your resume not passing the ATS auto scan. This market is awful though so you also have to pump out tons of applications to be getting them.

### `hot_take`

**Definition:** Makes a confident claim or gives advice with no checkable reason
offered, or with a "reason" that is only another claim.

**Example 1:**
> this is a classic case of Computer Science majors thinking if they dont get into FAANG, then they've failed at life. And that is tied into the Computer Science Superiority Complex

**Example 2:**
> AI is here to stay and it will only get better. But ya, reality is depressing in some ways.

### `chatter`

**Definition:** Adds no claim and no outcome: questions, status check-ins,
support, venting and jokes.

**Example 1:**
> did you get the offer,or currently under screening process?

**Example 2:**
> Same but i got a bf but no job(my bf on other hand has maang job and a gf 😭)

### The hardest boundary

**Which two labels:** `argued` and `hot_take`. r/csmajors is full of claims
with a "because" attached, and whether the "because" counts decides the label.

**The decision rule I used every time:** It's `argued` only if the reason
points to something the reader could check: a specific company practice, a
recruiting step, a number, or something the writer or others saw happen. If the
reason is a guess about motives or a sweeping claim about "everyone" or "the
market," it's `hot_take`, however sensible it sounds.

**The post that made me write it:**
> A lot of times those big companies have a resume screen after the initial OA since they wanna cast a bigger net to get everyone good enough.
> Trading firms give out OAs all the time but interviews sre much rare.

The "since they wanna cast a bigger net" part is a guess about motive and on its
own would make this `hot_take`. The trading-firm pattern (lots of OAs, few
interviews) is a company practice anyone recruiting this cycle can check, so
under the rule it's `argued`.

**Two smaller rules the stress test forced:**

- **A first-hand outcome wins.** If a comment reports the writer's own outcome
  or measured detail, it's `experience` even if it also draws a conclusion
  ("I did 400 leetcode and still bombed the OA, so grinding doesn't work").
- **Waiting isn't an outcome.** "Had my powerday Monday, still nothing, anyone
  else?" is `chatter`. "Finished the OA 3 weeks ago and haven't heard back"
  gives a measured wait, so it's `experience`.


---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** public r/csmajors comments collected on
2026-10-14, from two sources: the PullPush archive (100 recent comments) and
Reddit's public RSS feeds (the 100 most recent comments, plus the comment feeds
of 10 of the month's top threads). That gave 1,012 comments. `collect.py`
dropped 280 of them: under 40 characters ("lol", "same"), deleted, bot notices,
non-English, link-only, the threads' own posts, and duplicates. That left 732.
I sampled 20 from each of the 12 sources (240) so no single thread sets the
tone, then added 26 more from the leftover pool to top up the two thin labels
(see below). The Reddit link for every row is in `notes/sources.csv`; the
unsampled comments are in `notes/pool.csv`.

**How I labelled them:** every row was pre-labelled, then I read each one and
checked it against the definitions above (see the disclosure in How I Used AI).
16 rows are flagged in the note as hard cases, with the other label they could
be.

The first draft of 240 came out at 27 `experience` and 29 `argued`, about 4 each
in a 15% test split. So I added 15 `experience` and 11 `argued` comments from
the pool. Those 26 are marked `added from pool to top up <label>`. That means
the thin labels were partly chosen *for* their label, not sampled at random,
which I'll keep in mind if their scores look too good.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `chatter` | 102 | 38.3% |
| `hot_take` | 82 | 30.8% |
| `experience` | 42 | 15.8% |
| `argued` | 40 | 15.0% |
| **Total** | 266 | 100% |

No label is above 70%. `chatter` is the biggest at 38%, so always guessing it
scores about 0.38.

**Three hard cases**

**1.**
> *The post:* "This is cope. People from prestigious schools have a network of connections built-in to their school that can get them work based solely on that. Their 'intelligence' in abstract is more or less irrelevant. The only thing that really matters to employers is perceived competence… Actual competence is difficult to determine for people without long and well documented work histories…"
>
> *Could have been:* `argued` or `hot_take`.
>
> *I chose, because:* `hot_take`. It's a long, careful-sounding mechanism, but every step (networks get people jobs, employers only see perceived competence) is asserted, not checkable. Under the decision rule, a reason that's only another claim doesn't count, however sensible it sounds.

**2.**
> *The post:* "This frankly sounds like a mental health issue not a CS issue… My kid recently graduated from a regular public university in flyover country and landed a competitive 6 figure job working with elite grads… My spouse and I both have CS degrees and have worked and hired in tech…"
>
> *Could have been:* `experience` or `argued`.
>
> *I chose, because:* `argued`. There's a real outcome (a six-figure job), but it's the writer's kid's, not the writer's. `experience` is defined as what happened *to the writer*. The kid's outcome is something the writer saw happen, which is exactly what makes a reason count for `argued`.

**3.**
> *The post:* "I did 250 leetcode and can't find a gf :("
>
> *Could have been:* `chatter` or `experience`.
>
> *I chose, because:* `chatter`. "250 leetcode" is a measured first-hand detail, so the letter of the `experience` definition fits. But it's a joke in a joke thread, not a report anyone could use. This one shows a gap in the definitions: nothing says what to do with a number used as a punchline.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`, the notebook default.

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, 128 tokens per
comment, seed 42.

**Trained on:** `mps` (Apple Silicon GPU), torch 2.14.1, as recorded in
`results.json`. Training took about 30 seconds.

**Anything I changed from the defaults, and why:** nothing except `LABELS`
(set to `experience`, `argued`, `hot_take`, `chatter`) and my name and email.
128 tokens covers almost every comment: the median comment is 124 characters,
and `collect.py` dropped anything over 1,500.

One thing about *how* it ran rather than what it ran: the Jupyter kernel
wouldn't start in my environment (it timed out on its local connection), so
sections 1–5 were executed cell by cell in one Python process with the
notebook's own code, and each cell's printed output was saved back into
`takemeter.ipynb`. In unit 6, sections 6 and 7 were run the same way: section
1 in full, the earlier sections only far enough to define the functions
section 6 calls (so `results.json` and `test_split.csv` weren't rewritten),
then sections 6 and 7 in full.

**Split sizes:** 186 train / 40 val / 40 test, stratified.

| Label | Train | Val | Test |
|---|---|---|---|
| `experience` | 30 | 6 | 6 |
| `argued` | 28 | 6 | 6 |
| `hot_take` | 57 | 13 | 12 |
| `chatter` | 71 | 15 | 16 |

**`experience` and `argued` have only 6 examples each in the test split**,
below the ~8 the notebook flags. One comment is worth about 17 points of recall
for those two labels, so their F1 will move a lot between seeds next unit, and
criteria 2 and 3 will be read with that in mind.

---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1: stress-testing the labels**

- *What I asked for:* eight comments written to sit on the boundaries of my
  four draft labels, without being told which label Claude would pick.
- *What came back:* eight r/csmajors-style comments (`notes/stress_test.md`).
  I labelled all eight, and two of my answers contradicted my own written
  definitions. I called a "had my powerday Monday, still nothing, anyone else?"
  comment `chatter` though it named a company and a round, and I called a
  comment with a stated mechanism `hot_take` though the definition said a
  mechanism was enough for `argued`.
- *What I changed:* I asked Claude to recommend fixes. It proposed the
  `argued` vs `hot_take` decision rule (the reason has to be checkable), the
  "waiting isn't an outcome" rule, and tighter `experience` and `chatter`
  definitions, each checked against my stress-test answers. I adopted them as
  written.

**Moment 2: the acceptance criteria**

- *What I asked for:* recommended acceptance criteria, with reasons tied to
  this dataset.
- *What came back:* five criteria (accuracy ≥ 0.55; F1 ≥ 0.50 for the three
  bigger labels; `argued` F1 ≥ 0.30; a 15-point confidence gap; ≥ 21/30
  agreement with staff), with reasons based on a ~36-comment test split and
  `argued` being the thinnest label. It also pointed out that a balance
  criterion would be close to impossible to miss, since I control it while
  labelling.
- *What I changed:* nothing. I adopted all five as written, before any
  training.

**Moment 3: the baseline prediction (unit 6)**

- *What I asked for:* a one-sentence prediction of where the trained model
  would beat the zero-shot baseline and where it wouldn't.
- *What came back:* the prediction under Baseline vs. Trained, reasoned from
  the per-label training counts and the unit 5 zeros.
- *What I changed:* nothing. I used it as written.

**Pre-labelling disclosure:** Claude pre-labelled all 266 rows from my
definitions and flagged 16 as hard cases. I read and checked every row and kept
all of Claude's labels. No rows were labelled cold. Claude also collected the
comments (`collect.py` and the RSS fetch) and chose the 26 top-up rows from the
pool.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.300 | 0.525 | +0.225 |
| Macro F1 | 0.289 | 0.302 | +0.013 |
| F1 — `argued` | 0.500 | 0.000 | -0.500 |
| F1 — `chatter` | 0.000 | 0.638 | +0.638 |
| F1 — `experience` | 0.357 | 0.000 | -0.357 |
| F1 — `hot_take` | 0.300 | 0.571 | +0.271 |

Both columns are scored on the same 40 posts in `test_split.csv` (seed 42).
The baseline is `facebook/bart-large-mnli`, zero-shot, prompted with the four
definitions in `label_definitions.txt`. It took about 23 seconds for the 40
posts on `mps`.

**What my definitions were worth:** run again with bare label names only, the
baseline scored 0.200 accuracy and 0.180 macro F1
(`baseline_results_bare.json`). The definitions added 10 points of accuracy.

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

My trained model will beat the baseline overall and on `chatter` and
`hot_take`, the two labels it had 57–71 training examples of. It will lose to
the baseline on `argued` and `experience`, the two thin labels (28–30 examples
each), where reading the definitions does better than a model that never
learned to predict them.

Not a blind prediction: I wrote it after seeing the baseline's own numbers and
my unit 5 `results.json`, which already showed 0.00 F1 for `experience` and
`argued`. It was committed before the comparison table was generated.

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->

The prediction held on every label. The 22-point accuracy gap mostly measures
`chatter`: it's 16 of the 40 test posts, the trained model calls almost
everything `chatter` (15 of 16 right, and 16 other posts pulled into it), and
the baseline got none of them, calling 12 of the 16 `experience`. On macro F1,
which weights the four labels equally, fine-tuning added only 0.013. The two
models failed in opposite places. The trained model learned the two big labels
and never predicted `experience` or `argued`. The baseline, reading only the
definitions, found 5 of 6 `experience` and 4 of 6 `argued` posts but couldn't
recognise `chatter` from its definition. So fine-tuning didn't make a better
classifier overall. It traded the thin labels for the big ones.



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.55 | 0.525 | 0.525 | 0.425 | Miss |
| 2. F1 of `experience` / `hot_take` / `chatter` | each ≥ 0.50 | 0.000 / 0.571 / 0.638 | 0.000 / 0.522 / 0.667 | 0.000 / 0.133 / 0.604 | Miss |
| 3. F1 of `argued` | ≥ 0.30 | 0.000 | 0.000 | 0.000 | Miss |
| 4. Confidence gap (most-sure third − least-sure third) | ≥ 0.15 | 0.538 | 0.308 | 0.538 | Pass |
| 5. Agreement with staff | ≥ 21/30 | | | | Milestone 3 |

All three seeds trained on `mps` (Apple Silicon GPU), torch 2.14.1, recorded in
`results_three_seeds_before.json`. Seed 42 reproduced the unit 5 run exactly
(0.525 accuracy, 0.302 macro F1). Each seed took well under a minute.

The notebook's spread table:

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.525 | 0.525 | 0.425 | 0.100 |
| Macro F1 | 0.302 | 0.297 | 0.184 | 0.118 |
| F1 — `experience` | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 — `argued` | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 — `hot_take` | 0.571 | 0.522 | 0.133 | 0.438 |
| F1 — `chatter` | 0.638 | 0.667 | 0.604 | 0.063 |

**The spread:** accuracy moved 10 points (0.525 to 0.425), right at the line
the notebook draws for "too small or too lopsided for a stable measure", and
the notebook flagged it. One test post is 2.5 points here, so the drop is 4
posts. Almost all of it is `hot_take`: seed 2024 found 1 of 12 where the other
two seeds found 6, while `chatter` barely moved. The two zeros don't move at
all, because no seed ever predicts `experience` or `argued`. That's a stable
result, not a stable model: with 28–30 training examples each, those labels
lose to always saying `chatter` (71 examples), which is the lopsidedness the
note is pointing at.

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

Seed 42, the same 40 posts as `test_split.csv` and the Baseline vs. Trained
table. Rows are true labels, columns are the model's guesses.

| true \ predicted | experience | argued | hot_take | chatter |
|---|---|---|---|---|
| **experience** | 0 | 0 | 1 | 5 |
| **argued** | 0 | 0 | 1 | 5 |
| **hot_take** | 0 | 0 | 6 | 6 |
| **chatter** | 0 | 0 | 1 | 15 |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->

6 real `hot_take` posts were called `chatter` and only 1 `chatter` post went
the other way, so the model hasn't learned the `hot_take`/`chatter` boundary
and falls back on `chatter` whenever a short opinion doesn't look strongly
opinionated. It's the same direction on every seed (6, 6 and 11 `hot_take`
posts called `chatter`, against 1, 1 and 0 the other way), and the `experience`
and `argued` rows show the same pull: 10 of their 12 posts went to `chatter`.


---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
