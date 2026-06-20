# Branch Strategy Reference

## Visual Map

```
TIME ──────────────────────────────────────────────────────────────────────────────►

PRODUCTION
  main         ●─────────────────────────────────────────────────────●  (v0.2.0 tag)
               │                                                      │
               │  [cut release/v0.2.0 when v0.2 features complete]   │
               │                                                      │
RELEASES       │   release/v0.2.0  ●──────────────────────●  [frozen: bug fixes only]
               │                   │                       │
HOTFIXES       │                   │  hotfix/v0.2.1-       │
               │                   │  null-pointer-fix  ●──●  [fast-track → v0.2.1]
               │                   │                       │    QA + eng lead sign-off
               │                   │                       │    required
               │                                           │
INTEGRATION    │   develop         ●──────────────────────────────────────────────►
               │                   │
               │                   │  [cut release/v0.3.0 when v0.3 features done]
NEXT RELEASE   │                   │   release/v0.3.0  ●──────────────────────────►
               │                   │                   [frozen; open to fixes only]
               │                   │
FEATURES       │                   ├── feature/INV-42-search-endpoint   ●──●  ✓ merged
               │                   │
               │                   ├── feature/PAYMENTS-101-stripe-integration  ●──●──►
               │                   │       2 commits ahead of develop
               │                   │       integration window: Sprint 14
               │                   │
               │                   ├── feature/AUTH-55-oauth-refresh    ●──●──●──►
               │                   │       3 commits ahead of develop
               │                   │       integration window: Sprint 14
               │                   │
               │                   └── feature/DASH-77-analytics-dashboard  ●──●──●──●──●──●──►
               │                           6 commits ahead of develop  ⚠️  DRIFT WARNING
               │                           Flag for conversation with team lead
```

---

## Branch Rules

### Feature Branches
| Rule | Detail |
|------|--------|
| **Naming** | `feature/<TICKET-ID>-<short-description>` |
| **Branches from** | `develop` |
| **Merges into** | `develop` |
| **Lifetime** | One sprint / one ticket — no long-lived branches |
| **Drift KPI** | Flag at > 5 commits behind `develop` |
| **Gate to merge** | Automated regression suite must pass — no exceptions without eng lead sign-off |

### Release Branches
| Rule | Detail |
|------|--------|
| **Naming** | `release/v<MAJOR>.<MINOR>.0` |
| **Branches from** | `develop` (when features are code-complete) |
| **Merges into** | `main` + back-merged to `develop` |
| **Allowed changes** | Bug fixes and release-gating issues only — no new features |
| **Purpose** | Stable QA target; decouples QA from ongoing feature work |

### Hotfix Branches
| Rule | Detail |
|------|--------|
| **Naming** | `hotfix/v<MAJOR>.<MINOR>.<PATCH>-<description>` |
| **Branches from** | `release/v*` or production tag — **NOT main** |
| **Merges into** | The release branch it was cut from + `main` + `develop` |
| **Why not from main** | main may contain in-flight develop work; hotfix must be surgical |
| **Gate** | Explicit QA sign-off + engineering lead approval required |

### Drift Health KPI
```
for each feature branch:
    distance = git rev-list --count develop...<branch>
    if distance > DRIFT_THRESHOLD (e.g. 5):
        alert: "⚠️ <branch> is <distance> commits behind develop — flag for team lead"
```

Current state of this repo:
- `feature/INV-42-search-endpoint`         — ✅ merged
- `feature/PAYMENTS-101-stripe-integration` — 2 commits ahead — ✅ healthy
- `feature/AUTH-55-oauth-refresh`           — 3 commits ahead — ✅ healthy  
- `feature/DASH-77-analytics-dashboard`     — 6 commits ahead — ⚠️ needs conversation

---

## Merge Gate Checklist

```
[ ] Automated regression suite passes (CI required — no bypass)
[ ] PR reviewed by ≥ 1 peer
[ ] Hotfix / release only: QA sign-off documented in PR
[ ] Hotfix only: engineering lead approval in PR
[ ] Branch is within drift threshold (or exception recorded)
```

---

## Why These Rules Exist

| Pain point | Rule that prevents it |
|---|---|
| Merge nightmares from long-lived branches | Feature branches die at sprint boundary |
| QA chasing a moving target | Release branch is frozen for new features |
| Hotfix pulls in in-flight dev work | Hotfix cuts from release tag, not main |
| Silent regressions at merge | Automated regression gate on every merge |
| Unnoticed drift until it's critical | Commit-distance KPI + team lead review |
