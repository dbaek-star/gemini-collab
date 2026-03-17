<div align="center">

# 🤖 Gemini Collab

### Claude × Gemini — AI-to-AI Collaborative Intelligence

[![Claude Code Skill](https://img.shields.io/badge/Claude_Code-Skill-7C3AED?style=for-the-badge&logo=anthropic&logoColor=white)](https://docs.anthropic.com/en/docs/claude-code)
[![Gemini CLI](https://img.shields.io/badge/Gemini_CLI-Required-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://github.com/google-gemini/gemini-cli)
[![Python 3](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-F59E0B?style=for-the-badge)](LICENSE)

<br/>

**Two frontier AI models. One unified output.**
Gemini Collab orchestrates structured, round-based collaboration between Claude and Google's Gemini — producing higher-quality results through independent research, cross-verification, and iterative refinement.

<br/>

[한국어 README](README.ko.md)

---

<img src="https://img.shields.io/badge/Draft-Claude-7C3AED?style=flat-square" alt="Claude"> →
<img src="https://img.shields.io/badge/Review-Gemini-4285F4?style=flat-square" alt="Gemini"> →
<img src="https://img.shields.io/badge/Decision-Claude-7C3AED?style=flat-square" alt="Claude"> →
<img src="https://img.shields.io/badge/Final-Consensus-10B981?style=flat-square" alt="Final">

</div>

<br/>

## 📋 Table of Contents

- [Why Gemini Collab?](#-why-gemini-collab)
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

## 💡 Why Gemini Collab?

> A single AI can draft. Two AIs can **verify, challenge, and refine**.

| Problem | Solution |
|:--------|:---------|
| Single-model blind spots | Two models cross-verify each other's outputs |
| Unchallenged assumptions | Structured review rounds force critical evaluation |
| Hallucination risk | Web search integration + dual verification |
| Confirmation bias | Independent research before cross-review |

**Gemini Collab** brings the power of **adversarial collaboration** to your CLI workflow — the same principle that drives peer review in academia and red-teaming in security.

---

## 🔄 How It Works

```
┌─────────────────────────────────────────────────────────┐
│                    GEMINI COLLAB                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐         │
│   │  CLAUDE   │───▶│  GEMINI  │───▶│  CLAUDE   │        │
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

1. **Claude researches** the topic via web search, then creates an initial draft
2. **Gemini reviews** the draft independently (with its own web search)
3. **Claude evaluates** Gemini's feedback — accepting, rejecting, or partially adopting suggestions
4. **(Optional)** Additional rounds continue until consensus or termination
5. **Final output** is generated along with a comprehensive collaboration summary

---

## 🎮 Collaboration Modes

<table>
<tr>
<td width="25%" align="center">

### ⚡ 1 Round
**Fast & Light**

</td>
<td width="25%" align="center">

### ⭐ 2 Round
**Recommended**

</td>
<td width="25%" align="center">

### 🔄 Adaptive
**Until Consensus**

</td>
<td width="25%" align="center">

### 😈 Devil's Advocate
**Unlimited Debate**

</td>
</tr>
<tr>
<td>

```
Claude Draft
    ↓
Gemini Review
    ↓
Claude Decision
    ↓
  Final
```

</td>
<td>

```
Claude Draft
    ↓
Gemini Review
    ↓
Claude Revision
    ↓
Gemini Re-review
    ↓
Claude Final Call
    ↓
  Final
```

</td>
<td>

```
Claude Draft
    ↓
┌─── Loop ───┐
│ Gemini Rev  │
│     ↓       │
│ Claude Dec  │
└─── × N ────┘
    ↓
  Final
```

</td>
<td>

```
Claude Argument
    ↓
Gemini Counter
    ↓
Claude Rebuttal
    ↓
    ...
    ↓
 Surrender!
```

</td>
</tr>
<tr>
<td>

Gemini calls: **1**
Best for: Quick reviews

</td>
<td>

Gemini calls: **2**
Best for: Most tasks

</td>
<td>

Gemini calls: **1–5**
Best for: Complex topics

</td>
<td>

Gemini calls: **∞**
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

## 📦 Prerequisites

| Requirement | Details |
|:------------|:--------|
| **Claude Code** | [Anthropic's official CLI](https://docs.anthropic.com/en/docs/claude-code) |
| **Node.js** | 20.0.0 or later ([download](https://nodejs.org)) — required for npm and Gemini CLI |
| **Gemini CLI** | `npm install -g @google/gemini-cli` |
| **Python** | 3.x (standard library only — no pip packages required) |
| **Gemini Auth** | Gemini CLI must be authenticated (`gemini` command should work) |

---

## 🚀 Installation

### 1. Install Gemini CLI

```bash
npm install -g @google/gemini-cli
```

Verify the installation:
```bash
gemini --version
```

### 2. Clone & Install the Skill

```
git clone https://github.com/dbaek-star/gemini-collab.git
```

#### Windows — Git Bash (Recommended)

> Claude Code on Windows uses Git Bash as the default shell. This is the recommended method.

```bash
mkdir -p ~/.claude/skills/gemini-collab
cp -r gemini-collab/SKILL.md gemini-collab/scripts gemini-collab/references ~/.claude/skills/gemini-collab/
```

#### Windows — CMD

```cmd
mkdir "%USERPROFILE%\.claude\skills\gemini-collab"
xcopy /E /I /Y "gemini-collab\SKILL.md" "%USERPROFILE%\.claude\skills\gemini-collab\"
xcopy /E /I /Y "gemini-collab\scripts" "%USERPROFILE%\.claude\skills\gemini-collab\scripts"
xcopy /E /I /Y "gemini-collab\references" "%USERPROFILE%\.claude\skills\gemini-collab\references"
```

#### Windows — PowerShell

```powershell
$dest = "$env:USERPROFILE\.claude\skills\gemini-collab"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item -Path ".\gemini-collab\SKILL.md" -Destination $dest
Copy-Item -Path ".\gemini-collab\scripts" -Destination $dest -Recurse -Force
Copy-Item -Path ".\gemini-collab\references" -Destination $dest -Recurse -Force
```

#### macOS / Linux

```bash
mkdir -p ~/.claude/skills/gemini-collab
cp -r gemini-collab/SKILL.md gemini-collab/scripts gemini-collab/references ~/.claude/skills/gemini-collab/
```

### 3. Verify

Open Claude Code and type any trigger phrase:

```
> collaborate with Gemini on a project plan
```

If the skill loads, you're all set!

---

## 💬 Usage

### Trigger Phrases

You can invoke the skill using any of these phrases (English or Korean):

| Language | Trigger Examples |
|:---------|:-----------------|
| English | `"collaborate with Gemini"`, `"discuss with Gemini"` |
| Korean | `"Gemini와 협업"`, `"AI 협업"`, `"Gemini와 논의"`, `"Gemini한테 물어봐"`, `"AI끼리 토론"`, `"두 AI 의견 비교"` |

### Interactive Setup

When triggered, the skill presents two simultaneous selection prompts:

```
┌─ Collaboration Mode ───────────────────────────┐
│  ● 2 Round (Recommended)                       │
│  ○ 1 Round                                     │
│  ○ Adaptive Round                              │
│  ○ Devil's Advocate                             │
└────────────────────────────────────────────────┘

┌─ Gemini Model ─────────────────────────────────┐
│  ● gemini-3-pro (Recommended)                  │
│  ○ gemini-2.5-pro                              │
│  ○ gemini-3-flash                              │
│  ○ gemini-2.5-flash                            │
└────────────────────────────────────────────────┘
```

### Example Session

```bash
# In Claude Code
> Collaborate with Gemini to design a microservices architecture for an e-commerce platform

# Claude will:
# 1. Ask you to select mode and model
# 2. Research the topic via web search
# 3. Create an initial draft
# 4. Send to Gemini for review
# 5. Evaluate feedback and produce final output
```

---

## 🧠 Model Support

### Available Models

| Model | API ID | Best For |
|:------|:-------|:---------|
| **Gemini 3 Pro** | `gemini-3-pro-preview` | Complex reasoning & coding |
| **Gemini 2.5 Pro** | `gemini-2.5-pro` | Stable, proven performance |
| **Gemini 3 Flash** | `gemini-3-flash-preview` | Fast, cost-effective general tasks |
| **Gemini 2.5 Flash** | `gemini-2.5-flash` | Lightweight, simple tasks |

### Automatic Fallback Chain

If the selected model is unavailable, the system automatically falls back to the next available model:

```
gemini-3-pro-preview
        ↓ (fail)
gemini-2.5-pro
        ↓ (fail)
gemini-3-flash-preview
        ↓ (fail)
gemini-2.5-flash
```

> Fallback events are always reported in `collab_summary.md` and communicated to the user.

---

## 📁 Output Structure

All outputs are saved under your current working directory:

```
{CWD}/.gemini/collab/{YYYYMMDD_HHMMSS}_{topic}/
├── round1_1_claude_draft.md        # Claude's initial draft
├── round1_2_gemini_review.md       # Gemini's review
├── round1_3_claude_decision.md     # Claude's decision on feedback
├── round2_1_gemini_review.md       # (2-Round+) Gemini's re-review
├── round2_2_claude_decision.md     # (2-Round+) Claude's final decision
├── collab_final.md                 # ✅ Final collaborative output
└── collab_summary.md               # 📊 Collaboration summary & metadata
```

### Summary Report (`collab_summary.md`)

The summary includes:
- Model used (with fallback status)
- Web search usage
- Collaboration mode & total rounds
- Original request summary
- Per-round key decisions (accepted/rejected items with rationale)
- Final output summary
- Output file locations

---

## 🏗 Architecture

```
gemini-collab/
├── SKILL.md                     # Skill definition & orchestration rules
├── scripts/
│   └── gemini_call.py           # Gemini CLI wrapper with fallback
└── references/
    ├── gemini-cli-common.md     # Common Gemini CLI rules & parameters
    └── modes.md                 # Detailed mode specifications
```

### Key Design Decisions

| Decision | Rationale |
|:---------|:----------|
| **No fixed prompts** | Each Gemini call gets a dynamically generated prompt based on topic, round, mode, and prior feedback |
| **JSON output** | Structured results with metadata (model, fallback, search stats, session ID) |
| **Session management** | `--resume` enables multi-round conversations; auto-fallback to context injection on failure |
| **Zero dependencies** | Python script uses only standard library modules |
| **Windows support** | Handles npm global `.cmd` wrappers via `shutil.which()` |

### Gemini Call Wrapper (`gemini_call.py`)

```bash
python gemini_call.py INPUT_FILE \
  -p "Detailed instructions" \
  [-o OUTPUT_FILE] \
  [-m MODEL] \
  [--resume SESSION_ID] \
  [--context FILE ...] \
  [--timeout 120]
```

**Output (JSON):**
```json
{
  "success": true,
  "model": "gemini-3-pro-preview",
  "fallback": false,
  "session_id": "abc123",
  "resume_failed": false,
  "web_searched": true,
  "search_count": 3,
  "stats": {},
  "response": "Gemini's response text..."
}
```

---

## 📌 Examples

### Planning a System Architecture

```
> Collaborate with Gemini to plan a real-time notification system
> Mode: 2 Round | Model: gemini-3-pro

Result: Claude drafts architecture → Gemini identifies scaling concerns
→ Claude revises with event-driven approach → Gemini validates → Final output
```

### Writing a Technical Document

```
> Gemini와 협업해서 API 설계 문서 작성해줘
> Mode: Adaptive | Model: gemini-2.5-pro

Result: Iterates until both AIs agree on endpoint design,
error handling patterns, and authentication flow
```

### Debating a Technical Decision

```
> Devil's Advocate: Should we use microservices or monolith for our startup?
> Mode: Devil's Advocate | Model: gemini-3-pro

Result: Claude argues for monolith (simplicity, speed)
↔ Gemini argues for microservices (scalability, team independence)
→ One side concedes when unable to counter the other's argument
```

---

## 🤝 Contributing

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
- Integration with other AI providers
- Test coverage

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built for the era of multi-model AI collaboration**

<br/>

<img src="https://img.shields.io/badge/Claude-×-7C3AED?style=for-the-badge" alt="Claude">
<img src="https://img.shields.io/badge/Gemini-4285F4?style=for-the-badge" alt="Gemini">

<br/><br/>

*Two minds are better than one — even when they're artificial.*

</div>
