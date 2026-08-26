# Defect report

> **Status: not yet completed.**
>
> This file is filled in from an actual run, not written in advance. Until the
> suite has been run against the broken accounts and the output recorded here,
> the entries below are empty on purpose. A defect report that describes
> failures nobody observed is worth less than no report at all.

## How to produce it

```bash
pip install -r requirements.txt
pytest -m broken_user --headed
```

Run it headed the first time. Watching the browser is how you find out what
actually happened, rather than only that an assertion returned False.

For each failure, record what follows. Keep it short. The value is in the
reproduction steps and the reasoning, not the length.

## Template

### D1. <short title>

**Account:** problem_user / performance_glitch_user / other

**Test:** the test function that caught it

**Expected:** what the requirement in docs/test_plan.md says should happen

**Observed:** what actually happened, including the assertion output

**Reproduction:**
1. 
2. 
3. 

**Where it sits:** front end rendering, form handling, back end, network, or
unknown. Say unknown if it is unknown. Guessing a layer and being wrong is
worse than saying you did not determine it.

**Severity and why:** not just high or low, but what it costs the user or the
business if it ships.

---

### D2. <short title>

---

### D3. <short title>

---

## Notes on scope

SauceDemo seeds these defects on purpose, so nothing here is a real bug in a
real product. The exercise is not bug hunting. It is checking whether the
assertions in this suite are load bearing, which is a question a passing suite
cannot answer.
