# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

Context for every number below: about 240 comments, so the 15% test split is
about 36 comments and one comment moves accuracy by about 3 points. Four labels
means a random guess gets 25%. I expect `chatter` to be the biggest label at
roughly 35–40%, so always guessing `chatter` scores about that. Every target
has to hold on all three seeds (42, 7, 2024).

## 1. Overall accuracy

Overall accuracy on the held-out test split is **at least 0.55** on all three
seeds.

**Why this target:** 0.55 is 15–20 points above always guessing `chatter` and
more than twice chance. That's what I'd call useful for short, slangy Reddit
comments. With about 36 test comments, it leaves roughly two comments of slack
for seed noise before a miss.

---

## 2. The three bigger labels

`experience`, `hot_take` and `chatter` each have a test-split F1 of **at least
0.50** on all three seeds.

**Why this target:** each of these should have 8 or more test examples, so
their F1 is steadier than `argued`'s. `experience` has strong surface signals
(numbers, "I got", "OA", company names) and `chatter` has question marks and
emoji, so 0.50 should be reachable. `hot_take` is the one at risk, because it's
defined partly by what's *missing* (no checkable reason). If it misses, that's
where I'd look first.

---

## 3. `argued`

`argued` has a test-split F1 of **at least 0.30** on all three seeds.

**Why this target:** `argued` is my smallest label and sits on my hardest
boundary (`argued` vs `hot_take`, decided by whether the reason is checkable).
At about 12% of the data, only 4–5 `argued` comments land in the test split, so
its F1 swings the most of any label, which is why it's looser than criterion 2.
It still fails the most likely bad outcome: a model that never predicts
`argued` scores 0. Getting 2 of 5 right with a couple of false alarms would
already pass.

---

## 4. Confidence means something

The most-confident third of test predictions is **at least 15 points more
accurate** than the least-confident third, on all three seeds
(`accuracy_most_confident_third − accuracy_least_confident_third` in
`results.json`).

**Why this target:** each third is about 12 comments, so 15 points is roughly
two more correct answers in the confident third. Anything smaller is within
noise at this size. If the model is as often wrong when it's sure as when it's
guessing, its confidence can't be used to decide which predictions to trust,
and that should fail.

---

## 5. Labelling consistency

I agree with the staff labels on **at least 21 of the 30** staff posts (70%),
labelling under the staff taxonomy in `data/staff_taxonomy.md`.

**Why this target:** the staff set's `analysis` vs `hot_take` rule tests the
same skill as my `argued` vs `hot_take` rule: does the reason given count as
support? Several of the 30 are deliberately ambiguous, so 100% isn't realistic.
Below 70% would mean I apply written rules loosely, and that would be a
labelling explanation, not a model one, for a miss on criterion 2 or 3.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
