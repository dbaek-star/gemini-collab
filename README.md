<div align="center">

# Claude Collab

### Claude × Claude Subagent — AI-to-AI Collaborative Intelligence

[![Claude Code Skill](https://img.shields.io/badge/Claude_Code-Skill-7C3AED?style=for-the-badge&logo=anthropic&logoColor=white)](https://docs.anthropic.com/en/docs/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-F59E0B?style=for-the-badge)](LICENSE)

<br/>

**Two Claude instances. One unified output.**
Claude Collab orchestrates structured, round-based collaboration between the main Claude and a Claude subagent — producing higher-quality results through independent research, cross-verification, and iterative refinement.

<br/>

[한국어 README](README.ko.md)

---

<img src="https://img.shields.io/badge/Draft-Main_Claude-7C3AED?style=flat-square" alt="Main"> →
<img src="https://img.shields.io/badge/Review-Subagent-E0926C?style=flat-square" alt="Reviewer"> →
<img src="https://img.shields.io/badge/Decision-Main_Claude-7C3AED?style=flat-square" alt="Main"> →
<img src="https://img.shields.io/badge/Final-Consensus-10B981?style=flat-square" alt="Final">

</div>

<br/>

## Table of Contents

- [Why Claude Collab?](#-why-claude-collab)
- [How It Works](#-how-it-works)
- [Collaboration Modes](#-collaboration-modes)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Model Support](#-model-support)
- [Output Structure](#-output-structure)
- [Architecture](#-architecture)
- [Examples](#-examples)
- [Contributing](#-contributing)

---

## Why Claude Collab?

> A single AI can draft. Two AI instances can **verify, challenge, and refine**.

| Problem | Solution |
|:--------|:---------|
| Single-instance blind spots | Two independent instances cross-verify outputs |
| Unchallenged assumptions | Structured review rounds force critical evaluation |
| Hallucination risk | Web search integration + dual verification |
| Confirmation bias | Independent research before cross-review |

**Claude Collab** brings the power of **adversarial collaboration** to your CLI workflow — the same principle that drives peer review in academia and red-teaming in security. By using a subagent, the reviewing Claude operates independently from the main Claude, ensuring genuine critical evaluation.

---

## How It Works

```
┌─────────────────────────────────────────────────────────┐
│                    CLAUDE COLLAB                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐         │
│   │   MAIN   │───▶│ REVIEWER │───▶│   MAIN   │         │
│   │  CLAUDE   │    │(Subagent)│    │  CLAUDE   │        │
│   │  Draft    │    │  Review  │    │ Decision  │        │
│   │ +WebSearch│    │ +WebSearch│    │ Accept/   │        │
│   └──────────┘    └──────────┘    │ Reject    │        │
│                                    └─────┬────┘         │
│                                          │              │
│                              ┌───────────▼───────────┐  │
│                              │   FINAL OUTPUT        │  │
│                              │  collab_final.md      │  │
│                              │  collab_summary.md    │  │
│                              └───────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

1. **Main Claude researches** the topic via web search, then creates an initial draft
2. **Reviewer (subagent) reviews** the draft independently (with its own web search)
3. **Main Claude evaluates** the reviewer's feedback — accepting, rejecting, or partially adopting suggestions
4. **(Optional)** Additional rounds continue until consensus or termination
5. **Final output** is generated along with a comprehensive collaboration summary

---

## Collaboration Modes

<table>
<tr>
<td width="25%" align="center">

### 1 Round
**Fast & Light**

</td>
<td width="25%" align="center">

### 2 Round
**Recommended**

</td>
<td width="25%" align="center">

### Adaptive
**Until Consensus**

</td>
<td width="25%" align="center">

### Devil's Advocate
**Unlimited Debate**

</td>
</tr>
<tr>
<td>

```
Main Draft
    ↓
Reviewer Review
    ↓
Main Decision
    ↓
  Final
```

</td>
<td>

```
Main Draft
    ↓
Reviewer Review
    ↓
Main Revision
    ↓
Reviewer Re-review
    ↓
Main Final Call
    ↓
  Final
```

</td>
<td>

```
Main Draft
    ↓
┌─── Loop ───┐
│ Reviewer Rev│
│     ↓       │
│ Main Dec    │
└─── × N ────┘
    ↓
  Final
```

</td>
<td>

```
Main Argument
    ↓
Reviewer Counter
    ↓
Main Rebuttal
    ↓
    ...
    ↓
 Surrender!
```

</td>
</tr>
<tr>
<td>

Subagent calls: **1**
Best for: Quick reviews

</td>
<td>

Subagent calls: **2**
Best for: Most tasks

</td>
<td>

Subagent calls: **1-5**
Best for: Complex topics

</td>
<td>

Subagent calls: **unlimited**
Best for: Controversial topics

</td>
</tr>
</table>

### Mode Details

| Mode | Flow | Termination | Prompt Tone |
|:-----|:-----|:------------|:------------|
| **1 Round** | Draft → Review → Decision → Final | After 1 review cycle | Constructive feedback |
| **2 Round** | Draft → Review → Revision → Re-review → Final | After 2 review cycles | Constructive feedback |
| **Adaptive** | Repeats 2-Round pattern | Consensus or max 5 rounds | Constructive + consensus judgment |
| **Devil's Advocate** | Argument → Counter → Rebuttal → ... | Explicit surrender declaration | Critical argumentation |

> **Devil's Advocate** mode uses a debater-vs-debater structure. Each side attacks logical weaknesses and unsupported claims. The debate continues until one side explicitly declares: *"I concede defeat."* No random winner determination is allowed.

---

## Prerequisites

| Requirement | Details |
|:------------|:--------|
| **Claude Code** | [Anthropic's official CLI](https://docs.anthropic.com/en/docs/claude-code) |

That's it! No additional CLI tools, no Python, no npm packages. Claude Collab uses Claude Code's built-in `Agent` tool to spawn subagents directly.

---

## Installation

### 1. Clone & Install the Skill

```
git clone https://github.com/dbaek-star/gemini-collab.git
```

#### Windows — Git Bash (Recommended)

> Claude Code on Windows uses Git Bash as the default shell. This is the recommended method.

```bash
mkdir -p ~/.claude/skills/claude-collab
cp -r gemini-collab/SKILL.md gemini-collab/references ~/.claude/skills/claude-collab/
```

#### Windows — CMD

```cmd
mkdir "%USERPROFILE%\.claude\skills\claude-collab"
xcopy /E /I /Y "gemini-collab\SKILL.md" "%USERPROFILE%\.claude\skills\claude-collab\"
xcopy /E /I /Y "gemini-collab\references" "%USERPROFILE%\.claude\skills\claude-collab\references"
```

#### Windows — PowerShell

```powershell
$dest = "$env:USERPROFILE\.claude\skills\claude-collab"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item -Path ".\gemini-collab\SKILL.md" -Destination $dest
Copy-Item -Path ".\gemini-collab\references" -Destination $dest -Recurse -Force
```

#### macOS / Linux

```bash
mkdir -p ~/.claude/skills/claude-collab
cp -r gemini-collab/SKILL.md gemini-collab/references ~/.claude/skills/claude-collab/
```

### 2. Verify

Open Claude Code and type any trigger phrase:

```
> collaborate with subagent on a project plan
```

If the skill loads, you're all set!

---

## Usage

### Trigger Phrases

You can invoke the skill using any of these phrases (English or Korean):

| Language | Trigger Examples |
|:---------|:-----------------|
| English | `"collaborate with subagent"`, `"discuss with another Claude"`, `"second opinion"` |
| Korean | `"AI 협업"`, `"Claude 협업"`, `"서브에이전트와 협업"`, `"AI끼리 토론"`, `"두 AI 의견 비교"`, `"세컨드 오피니언"`, `"PRD 작성"`, `"워크플로우 설계"` |

### Interactive Setup

When triggered, the skill presents two simultaneous selection prompts:

```
┌─ Collaboration Mode ───────────────────────────┐
│  ● 2 Round (Recommended)                       │
│  ○ 1 Round                                     │
│  ○ Adaptive Round                              │
│  ○ Devil's Advocate                             │
└────────────────────────────────────────────────┘

┌─ Reviewer Model ──────────────────────────────┐
│  ● Claude Sonnet (Recommended)                 │
│  ○ Claude Opus                                 │
│  ○ Claude Haiku                                │
└────────────────────────────────────────────────┘
```

### Example Session

```bash
# In Claude Code
> Collaborate with subagent to design a microservices architecture for an e-commerce platform

# Claude will:
# 1. Ask you to select mode and reviewer model
# 2. Research the topic via web search
# 3. Create an initial draft
# 4. Spawn a subagent for review
# 5. Evaluate feedback and produce final output
```

---

## Model Support

### Available Reviewer Models

| Model | Agent `model` value | Best For |
|:------|:-------------------|:---------|
| **Claude Sonnet** | `sonnet` | Balanced performance & speed (recommended) |
| **Claude Opus** | `opus` | Highest reasoning capability, complex analysis |
| **Claude Haiku** | `haiku` | Fast & lightweight, simple reviews |

> No fallback chain needed — Claude Code's Agent tool handles model availability internally.

---

## Output Structure

All outputs are saved under your current working directory:

```
{CWD}/.collab/{YYYYMMDD_HHMMSS}_{topic}/
├── round1_1_main_draft.md          # Main Claude's initial draft
├── round1_2_reviewer_review.md     # Reviewer's review
├── round1_3_main_decision.md       # Main Claude's decision on feedback
├── round2_1_reviewer_review.md     # (2-Round+) Reviewer's re-review
├── round2_2_main_decision.md       # (2-Round+) Main Claude's final decision
├── collab_final.md                 # Final collaborative output
└── collab_summary.md               # Collaboration summary & metadata
```

### Summary Report (`collab_summary.md`)

The summary includes:
- Reviewer model used
- Collaboration mode & total rounds
- Original request summary
- Per-round key decisions (accepted/rejected items with rationale)
- Final output summary
- Output file locations

---

## Architecture

```
claude-collab/
├── SKILL.md                     # Skill definition & orchestration rules
└── references/
    ├── subagent-common.md       # Agent tool usage rules & parameters
    └── modes.md                 # Detailed mode specifications
```

### Key Design Decisions

| Decision | Rationale |
|:---------|:----------|
| **Subagent via Agent tool** | Direct in-process invocation — no external CLI, no Python wrapper, zero dependencies |
| **No fixed prompts** | Each subagent call gets a dynamically generated prompt based on topic, round, mode, and prior feedback |
| **Independent reviewer** | Subagent operates independently from main Claude, ensuring genuine critical evaluation |
| **Context injection per round** | Each round spawns a fresh subagent with prior context injected into the prompt — no experimental flags needed |
| **Zero dependencies** | Only requires Claude Code — no npm, Python, or external tools |

### Subagent Call Pattern

```
Agent({
  description: "Round 1 - Review draft",
  model: "sonnet",
  prompt: "You are an independent reviewer. Review the following draft critically..."
})
```

**Response:** The Agent tool returns the subagent's response text directly — no JSON parsing needed.

---

## Examples

### Planning a System Architecture

```
> Collaborate with subagent to plan a real-time notification system
> Mode: 2 Round | Model: Claude Sonnet

Result: Main Claude drafts architecture → Reviewer identifies scaling concerns
→ Main Claude revises with event-driven approach → Reviewer validates → Final output
```

### Writing a Technical Document

```
> AI 협업해서 API 설계 문서 작성해줘
> Mode: Adaptive | Model: Claude Opus

Result: Iterates until both Claude instances agree on endpoint design,
error handling patterns, and authentication flow
```

### Debating a Technical Decision

```
> Devil's Advocate: Should we use microservices or monolith for our startup?
> Mode: Devil's Advocate | Model: Claude Sonnet

Result: Main Claude argues for monolith (simplicity, speed)
↔ Reviewer argues for microservices (scalability, team independence)
→ One side concedes when unable to counter the other's argument
```

---

## Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** this repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Areas for Contribution

- New collaboration modes
- Additional language support for trigger phrases
- Enhanced summary report formatting
- Advanced subagent prompt strategies
- Test coverage

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built for the era of multi-instance AI collaboration**

<br/>

<img src="https://img.shields.io/badge/Main_Claude-×-7C3AED?style=for-the-badge" alt="Main">
<img src="https://img.shields.io/badge/Reviewer_Claude-E0926C?style=for-the-badge" alt="Reviewer">

<br/><br/>

*Two minds are better than one — even when they share the same model.*

</div>
