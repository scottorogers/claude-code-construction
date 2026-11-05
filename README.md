# Construction Skills for Claude Code — UK Edition

Open-source skills that give Claude Code the working knowledge of a site/project engineer on **UK** jobs. Split drawings, parse specs, tabulate tenders, generate subcontracts, draft RFIs/TQs, and more — directly from your terminal or IDE.

This is a UK fork of [dleerdefi/claude-code-construction](https://github.com/dleerdefi/claude-code-construction). It replaces the US framework with:

| Area | UK baseline |
|---|---|
| Spec classification | Uniclass 2015 (NBS Chorus) — `Ss_70_30_45`; NBS CAWS and US CSI still recognised and flagged |
| Regulations | Building Regulations 2010 + Approved Documents (England); Wales/Scotland/NI regimes flagged, never assumed |
| Electrical | BS 7671:2018+A4:2026 |
| Fire / access figures | AD B Vol 2 and AD M Vol 2 tables, each with table/paragraph refs |
| Health & safety | CDM 2015 duty holders |
| Contracts | JCT 2024 (DBSub / SBCSub) and NEC4 (ECS / ECSS) — standard conditions incorporated by reference, never reproduced |
| Drawings | BS EN ISO 19650-2 UK National Annex naming, status (S0–S7, A, B, CR) and revision (P/C) codes; metric scales; A-series sheets |
| Money / units | GBP, ex-VAT; metric |

**Citation rule:** a regulation, Approved Document paragraph or standard clause is cited only if it is held in `reference/` with its source, or appears in the project documents. BS / BS EN clause text is paywalled, so clause-level content is marked `[VERIFY]` for you to check against a licensed copy.

## Prerequisites

- [Claude Code](https://claude.ai/code) (CLI, VS Code extension, or JetBrains)
- Python 3.10+
- Your construction project documents (drawings, specs, bids, etc.)

## Setup

**1. Install the skills:**

```bash
# Global install (available in all projects)
git clone https://github.com/scottorogers/claude-code-construction ~/.claude/skills/construction

# Or per-project install
git clone https://github.com/scottorogers/claude-code-construction .claude/skills/construction
```

**2. Run setup** (installs Python dependencies into an isolated venv):

```bash
cd ~/.claude/skills/construction    # or .claude/skills/construction
./setup
```

**3. Connect to your project.** Add this line to your project's `CLAUDE.md`:

```
@~/.claude/skills/construction/.claude/skills/CLAUDE.md
```

If your project doesn't have a `CLAUDE.md` yet, run `/init` in Claude Code first.

**4. Start using skills.** Open Claude Code in your project folder and type:

```
/project-setup
```

This inventories your project files, classifies document types, and establishes context for the other skills.

### Uploading to claude.ai / Claude desktop

Uploaded skills must be single folders, so build self-contained packages:

```bash
bin/package-skills          # writes dist/<skill>.zip for all 13 skills + dist/uk-construction-skills-all.zip
```

Each zip bundles its skill with the shared `reference/` data (US legacy tables excluded), the shared `scripts/` as `shared_scripts/`, and the UK baseline rules as `CONSTRUCTION_CONTEXT.md`. Upload each zip under Settings → Capabilities → Skills.

## Skills

| Command | What it does |
|---------|-------------|
| `/project-setup` | Inventory project files, classify documents, establish context |
| `/sheet-splitter` | Split a bound drawing set PDF into individual sheet PDFs |
| `/spec-splitter` | Split a bound project manual into individual spec section PDFs + text |
| `/schedule-extractor` | Extract door, finish, window, luminaire or DB schedules to Excel |
| `/submittal-log-generator` | Read every NBS section and generate a submittal register in Excel |
| `/bid-tabulator` | Tabulate multiple subcontractor tenders into a comparison spreadsheet (GBP) |
| `/bid-evaluator` | Evaluate tabulated tenders — scope gaps, risk scoring, award recommendation |
| `/code-researcher` | Gap research against Building Regulations / Approved Documents, BS 7671 and BS/BS EN standards |
| `/subcontract-writer` | Generate a JCT 2024 or NEC4 subcontract / order from your firm's template |
| `/pe-review` | Document review — red flags, coordination matrix, scope gaps by Uniclass group |
| `/rfi-drafter` | Turn logged issues into RFIs / TQs with contract position (early warning / notice) |
| `/tag-audit-and-takeoff` | Count-based takeoff and tag completeness audit (doors, luminaires, data outlets…) |
| `/viewport-highlighter` | Detect and highlight viewports on sheets (needs AgentCM) |

## AgentCM (Optional)

If your project uses [AgentCM](https://github.com/dleerdefi/AgentCM), skills automatically read from pre-indexed structured data in the `.construction/` directory for faster results. Skills work without AgentCM using Claude's built-in vision and PDF tools.

## Output

Skills save structured results to a `.construction/` directory in your project root. Excel files, split PDFs, and extracted text are written to your project folder. Each skill reports its output location when complete.

## Architecture & Technical Details

See [CM Skills SOP](docs/CM_SKILLS_SOP.md) for the full technical breakdown — skill architecture, design philosophy, YAML front matter spec, and the evaluation framework.

## Documentation

- [Quickstart Guide](docs/QUICKSTART.md) — try your first skill in 5 minutes
- [CM Skills SOP](docs/CM_SKILLS_SOP.md) — skill architecture and design standard
- [Troubleshooting](docs/TROUBLESHOOTING.md) — common issues and fixes
- [Evaluation Spec](evals/EVAL_SPEC.md) — test framework for validating skills (current cases use a US test project — see below)
- [Running Evals](docs/RUNNING_EVALS.md) — how to run eval test cases

## Requirements

Python dependencies are installed automatically by `./setup` into an isolated venv at `~/.construction-skills/venv/`. No manual activation needed — all scripts run through `bin/construction-python`.

Packages: `pdfplumber`, `pymupdf`, `openpyxl`, `Pillow`, `PyYAML`

## Evals — known gap

The eval cases in `evals/` were written against a US test project (Holabird Academy) and score against US answers (`reference/legacy_us/`). They still exercise the extraction and tabulation mechanics, but the code-researcher and subcontract-writer cases no longer match the UK skills. UK eval cases need a real UK test project and are not yet written.

## License

MIT

---

Original skills by [dleerdefi](https://github.com/dleerdefi). UK edition maintained by [scottorogers](https://github.com/scottorogers).