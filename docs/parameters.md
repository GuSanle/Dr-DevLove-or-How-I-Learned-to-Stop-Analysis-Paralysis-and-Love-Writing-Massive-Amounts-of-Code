# gh-stats Parameter Specifications

Based on the [CLI Declarative Argument Architecture Protocol](./myrules.md).

---

## Entity Hierarchy

```
gh-stats
├── E_USER          # User Identity
├── E_DISCOVERY     # Repository Discovery
├── E_DATE          # Date Range
├── E_EXPORT        # Export Control
├── E_ORG_SUMMARY   # Organization Summary Mode
│   └── E_ARENA     # Arena Rankings (Depends on E_ORG_SUMMARY)
└── E_DISPLAY       # Display Control
```

---

## Parameter Detailed Specifications

### E_USER - User Identity

| Parameter | Type | Default | Value Range | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--user` | string | (Current Auth User) | GitHub Username | Target user for analysis. |

---

### E_DISCOVERY - Repository Discovery

| Parameter | Type | Default | Value Range | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--personal` / `--no-personal` | bool | `true` | `true` \| `false` | Include personal repositories. |
| `--orgs` | string | `""` | Comma-separated org names | List of organizations to analyze. |
| `--personal-limit` | int | `null` | ≥0 (0=unlimited) | Max personal repos to scan. |
| `--org-limit` | int | `null` | ≥0 (0=unlimited) | Max repos per organization to scan. |
| `--all-branches` | flag | `false` | - | Scan all active branches (via Events API). |

---

### E_DATE - Date Range

| Parameter | Type | Default | Value Range | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--since` | string | `today` | Date Format (see below) | Start date. |
| `--until` | string | `today` | Date Format (see below) | End date. |
| `--range` | string | `null` | Presets (see below) | Date range preset. |

**Date Formats**:
- Absolute: `YYYY-MM-DD`, `YYYYMMDD`
- Relative: `today`, `today-1week`, `today-3days`

**Range Presets**:
- `today` — Today
- `week` — This week
- `month` — This month
- `3days`, `7days`, `30days` — Last N days

---

### E_EXPORT - Export Control

| Parameter | Type | Default | Value Range | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--export-commits` | flag | `false` | - | Export commit messages to Markdown. |
| `--full-message` | flag | `false` | - | Include full commit body in export. |
| `--output`, `-o` | string | `null` | File path | Custom output filename. |

---

### E_ORG_SUMMARY - Organization Summary Mode

| Parameter | Type | Default | Value Range | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--org-summary` | string | `null` | Organization Name | Enable Org Summary Mode (Analyze single org). |

---

### E_ARENA - Arena Rankings

| Parameter | Type | Default | Value Range | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--arena` | flag | `false` | - | Show competition rankings. |
| `--arena-top` | int | `5` | ≥0 (0=all) | Number of top contributors to show. |

**Dependencies**: `--arena` requires `--org-summary`.

**Derivation Rules (D)**: Valid `--arena-top` (non-default) automatically activates `--arena`.

---

### E_DISPLAY - Display Control

| Parameter | Type | Default | Value Range | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--highlights` | flag | `false` | - | Show insights (longest streak, etc.). |
| `--exclude-noise` | flag | `false` | - | Exclude noisy files like lockfiles and generated artifacts. |
| `--dry-run` | flag | `false` | - | Diagnostic mode (show params only). |
| `--dev` | flag | `false` | - | Developer mode (print command & parsing details). |

---

## Mutually Exclusive Constraints (X - Exclusions)

| Constraint ID | Mutually Exclusive Group | Description |
| :--- | :--- | :--- |
| X001 | `--org-summary` ⟷ `--orgs` | Org Summary Mode is mutually exclusive with Multi-Org Mode. |

---

## Derivation Rules (D - Derivations)

| Rule ID | Trigger Condition | Derived Result |
| :--- | :--- | :--- |
| D001 | `--arena-top` ≠ 5 | Automatically sets `--arena = true` |

---

## Dependencies

```
--arena ──requires──> --org-summary
```

---

## Type definitions

| Type | Format | Example |
| :--- | :--- | :--- |
| `flag` | Boolean Switch | `--arena` |
| `string` | String | `--user=octocat` |
| `int` | Integer | `--arena-top=10` |
