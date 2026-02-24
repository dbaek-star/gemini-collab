<div align="center">

# 🤖 Gemini Collab

### Claude × Gemini — AI 간 협업 지능 시스템

[![Claude Code Skill](https://img.shields.io/badge/Claude_Code-Skill-7C3AED?style=for-the-badge&logo=anthropic&logoColor=white)](https://docs.anthropic.com/en/docs/claude-code)
[![Gemini CLI](https://img.shields.io/badge/Gemini_CLI-필수-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://github.com/google-gemini/gemini-cli)
[![Python 3](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-F59E0B?style=for-the-badge)](LICENSE)

<br/>

**두 개의 최정상 AI 모델. 하나의 통합된 결과물.**
Gemini Collab은 Claude와 Google Gemini 사이의 구조화된 라운드 기반 협업을 오케스트레이션합니다. 독립적인 조사, 교차 검증, 반복적 개선을 통해 더 높은 품질의 결과물을 만들어냅니다.

<br/>

[English README](README.md)

---

<img src="https://img.shields.io/badge/초안-Claude-7C3AED?style=flat-square" alt="Claude"> →
<img src="https://img.shields.io/badge/검토-Gemini-4285F4?style=flat-square" alt="Gemini"> →
<img src="https://img.shields.io/badge/판단-Claude-7C3AED?style=flat-square" alt="Claude"> →
<img src="https://img.shields.io/badge/최종-합의-10B981?style=flat-square" alt="Final">

</div>

<br/>

## 📋 목차

- [왜 Gemini Collab인가?](#-왜-gemini-collab인가)
- [작동 방식](#-작동-방식)
- [협업 모드](#-협업-모드)
- [사전 요구사항](#-사전-요구사항)
- [설치 방법](#-설치-방법)
- [사용 방법](#-사용-방법)
- [모델 지원](#-모델-지원)
- [산출물 구조](#-산출물-구조)
- [아키텍처](#-아키텍처)
- [사용 예시](#-사용-예시)
- [기여하기](#-기여하기)

---

## 💡 왜 Gemini Collab인가?

> 하나의 AI가 초안을 작성할 수 있다. 두 개의 AI는 **검증하고, 도전하고, 개선**할 수 있다.

| 문제점 | 해결책 |
|:-------|:-------|
| 단일 모델의 맹점 | 두 모델이 서로의 출력을 교차 검증 |
| 검증 없는 가정 | 구조화된 검토 라운드로 비판적 평가 강제 |
| 환각(Hallucination) 위험 | 웹 검색 통합 + 이중 검증 |
| 확증 편향 | 교차 검토 전 독립적 조사 수행 |

**Gemini Collab**은 **적대적 협업(Adversarial Collaboration)** 의 힘을 CLI 워크플로우에 가져옵니다 — 학계의 동료 심사(peer review)와 보안 분야의 레드팀(red-teaming)을 이끄는 동일한 원리입니다.

---

## 🔄 작동 방식

```
┌─────────────────────────────────────────────────────────┐
│                    GEMINI COLLAB                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐         │
│   │  CLAUDE   │───▶│  GEMINI  │───▶│  CLAUDE   │        │
│   │   초안    │    │   검토   │    │   판단    │        │
│   │ +웹검색   │    │ +웹검색  │    │ 수용/     │        │
│   └──────────┘    └──────────┘    │ 반박      │        │
│                                    └─────┬────┘         │
│                                          │              │
│                              ┌───────────▼───────────┐  │
│                              │     최종 산출물       │  │
│                              │  collab_final.md      │  │
│                              │  collab_summary.md    │  │
│                              └───────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

1. **Claude가 조사** — 웹 검색으로 주제를 조사한 후 초안을 작성합니다
2. **Gemini가 검토** — 초안을 독립적으로 검토합니다 (자체 웹 검색 포함)
3. **Claude가 평가** — Gemini의 피드백을 수용, 반박, 또는 부분 채택합니다
4. **(선택)** 합의 또는 종료 조건까지 추가 라운드를 진행합니다
5. **최종 산출물** — 종합적인 협업 요약과 함께 최종본이 생성됩니다

---

## 🎮 협업 모드

<table>
<tr>
<td width="25%" align="center">

### ⚡ 1 Round
**빠른 협업**

</td>
<td width="25%" align="center">

### ⭐ 2 Round
**추천 (기본값)**

</td>
<td width="25%" align="center">

### 🔄 Adaptive
**합의까지 반복**

</td>
<td width="25%" align="center">

### 😈 Devil's Advocate
**무제한 토론**

</td>
</tr>
<tr>
<td>

```
Claude 초안
    ↓
Gemini 검토
    ↓
Claude 판단
    ↓
  최종본
```

</td>
<td>

```
Claude 초안
    ↓
Gemini 검토
    ↓
Claude 수정
    ↓
Gemini 재검토
    ↓
Claude 최종 판단
    ↓
  최종본
```

</td>
<td>

```
Claude 초안
    ↓
┌─── 반복 ───┐
│ Gemini 검토 │
│     ↓       │
│ Claude 판단 │
└─── × N ────┘
    ↓
  최종본
```

</td>
<td>

```
Claude 주장
    ↓
Gemini 반박
    ↓
Claude 재반박
    ↓
    ...
    ↓
 패배 선언!
```

</td>
</tr>
<tr>
<td>

Gemini 호출: **1회**
적합: 빠른 검토

</td>
<td>

Gemini 호출: **2회**
적합: 대부분의 작업

</td>
<td>

Gemini 호출: **1~5회**
적합: 복잡한 주제

</td>
<td>

Gemini 호출: **무제한**
적합: 논쟁적 주제

</td>
</tr>
</table>

### 모드 상세

| 모드 | 흐름 | 종료 조건 | 프롬프트 톤 |
|:-----|:-----|:----------|:------------|
| **1 Round** | 초안 → 검토 → 판단 → 최종 | 1회 검토 후 | 건설적 피드백 |
| **2 Round** | 초안 → 검토 → 수정 → 재검토 → 최종 | 2회 검토 후 | 건설적 피드백 |
| **Adaptive** | 2 Round 패턴 반복 | 합의 도달 또는 최대 5라운드 | 건설적 + 합의 판단 |
| **Devil's Advocate** | 주장 → 반박 → 재반박 → ... | 명시적 패배 선언 | 비판적 반론 |

> **Devil's Advocate** 모드는 토론자 대 토론자 구조입니다. 각 측은 상대의 논리적 약점과 근거 없는 주장을 공격합니다. 한쪽이 *"패배를 인정합니다"* 라고 명시적으로 선언할 때까지 토론이 계속됩니다. 임의 승패 결정은 금지됩니다.

---

## 📦 사전 요구사항

| 요구사항 | 상세 |
|:---------|:-----|
| **Claude Code** | [Anthropic 공식 CLI](https://docs.anthropic.com/en/docs/claude-code) |
| **Gemini CLI** | `npm install -g @google/gemini-cli` |
| **Python** | 3.x (표준 라이브러리만 사용 — pip 패키지 불필요) |
| **Gemini 인증** | Gemini CLI 인증 완료 (`gemini` 명령어 실행 가능해야 함) |

---

## 🚀 설치 방법

### 1. Gemini CLI 설치

```bash
npm install -g @google/gemini-cli
```

설치 확인:
```bash
gemini --version
```

### 2. 스킬 클론 & 설치

```
git clone https://github.com/dbaek-star/gemini-collab.git
```

#### Windows — Git Bash (권장)

> Windows에서 Claude Code는 Git Bash를 기본 셸로 사용합니다. 이 방법을 권장합니다.

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

### 3. 설치 확인

Claude Code를 열고 트리거 문구를 입력합니다:

```
> Gemini와 협업해서 프로젝트 계획 세워줘
```

스킬이 로드되면 설치 완료입니다!

---

## 💬 사용 방법

### 트리거 문구

다음 문구로 스킬을 실행할 수 있습니다 (한국어 및 영어):

| 언어 | 트리거 예시 |
|:-----|:------------|
| 한국어 | `"Gemini와 협업"`, `"AI 협업"`, `"Gemini와 논의"`, `"Gemini한테 물어봐"`, `"AI끼리 토론"`, `"두 AI 의견 비교"`, `"PRD 작성"`, `"워크플로우 설계"` |
| 영어 | `"collaborate with Gemini"`, `"discuss with Gemini"` |

### 인터랙티브 설정

스킬이 실행되면 두 개의 선택 프롬프트가 동시에 표시됩니다:

```
┌─ 협업 모드 ────────────────────────────────────┐
│  ● 2 Round (추천)                              │
│  ○ 1 Round                                     │
│  ○ Adaptive Round                              │
│  ○ Devil's Advocate                             │
└────────────────────────────────────────────────┘

┌─ Gemini 모델 ──────────────────────────────────┐
│  ● gemini-3.1-pro (추천)                         │
│  ○ gemini-3-flash                              │
│  ○ gemini-2.5-pro                              │
│  ○ gemini-2.5-flash                            │
└────────────────────────────────────────────────┘
```

### 세션 예시

```bash
# Claude Code에서
> Gemini와 협업해서 이커머스 플랫폼의 마이크로서비스 아키텍처 설계해줘

# Claude가 다음을 수행합니다:
# 1. 모드와 모델 선택 요청
# 2. 웹 검색으로 주제 조사
# 3. 초안 작성
# 4. Gemini에 검토 요청
# 5. 피드백 평가 후 최종 산출물 생성
```

---

## 🧠 모델 지원

### 사용 가능한 모델

| 모델 | API ID | 적합한 용도 |
|:------|:-------|:------------|
| **Gemini 3.1 Pro** | `gemini-3.1-pro-preview` | 복잡한 추론 & 코딩 |
| **Gemini 3 Flash** | `gemini-3-flash-preview` | 빠르고 경제적인 일반 작업 |
| **Gemini 2.5 Pro** | `gemini-2.5-pro` | 안정적이고 검증된 성능 |
| **Gemini 2.5 Flash** | `gemini-2.5-flash` | 경량, 단순 작업 |

### 자동 모델 Fallback 체인

선택한 모델이 사용 불가능한 경우, 다음 모델로 자동 전환됩니다:

```
gemini-3.1-pro-preview
        ↓ (실패)
gemini-3-flash-preview
        ↓ (실패)
gemini-2.5-pro
        ↓ (실패)
gemini-2.5-flash
        ↓ (실패)
gemini-2.5-flash-lite
```

> Fallback 발생 시 항상 `collab_summary.md`에 기록되며, 사용자에게 알림이 전달됩니다.

---

## 📁 산출물 구조

모든 산출물은 현재 작업 디렉토리 하위에 저장됩니다:

```
{CWD}/.gemini/collab/{YYYYMMDD_HHMMSS}_{주제}/
├── round1_1_claude_draft.md        # Claude의 초안
├── round1_2_gemini_review.md       # Gemini의 검토
├── round1_3_claude_decision.md     # Claude의 피드백 판단
├── round2_1_gemini_review.md       # (2 Round+) Gemini의 재검토
├── round2_2_claude_decision.md     # (2 Round+) Claude의 최종 판단
├── collab_final.md                 # ✅ 최종 협업 산출물
└── collab_summary.md               # 📊 협업 요약 & 메타데이터
```

### 요약 보고서 (`collab_summary.md`)

요약에 포함되는 항목:
- 사용된 모델 (Fallback 여부 포함)
- 웹 검색 사용 여부
- 협업 모드 & 총 라운드 수
- 원래 요청 요약
- 라운드별 주요 결정 사항 (수용/반박 항목과 사유)
- 최종 산출물 요약
- 산출물 파일 위치

---

## 🏗 아키텍처

```
gemini-collab/
├── SKILL.md                     # 스킬 정의 & 오케스트레이션 규칙
├── scripts/
│   └── gemini_call.py           # Gemini CLI 래퍼 (자동 Fallback 포함)
└── references/
    ├── gemini-cli-common.md     # Gemini CLI 공통 규칙 & 파라미터
    └── modes.md                 # 협업 모드 상세 명세
```

### 핵심 설계 결정

| 결정 | 이유 |
|:-----|:-----|
| **고정 프롬프트 미사용** | 매 Gemini 호출마다 주제, 라운드, 모드, 이전 피드백에 기반한 동적 프롬프트 생성 |
| **JSON 출력** | 메타데이터(모델, fallback, 검색 통계, 세션 ID)를 포함한 구조화된 결과 |
| **세션 관리** | `--resume`으로 다중 라운드 대화 지원; 실패 시 컨텍스트 주입으로 자동 전환 |
| **의존성 제로** | Python 스크립트는 표준 라이브러리만 사용 |
| **Windows 지원** | `shutil.which()`로 npm 글로벌 `.cmd` 래퍼 처리 |

### Gemini 호출 래퍼 (`gemini_call.py`)

```bash
python gemini_call.py INPUT_FILE \
  -p "상세 지시사항" \
  [-o OUTPUT_FILE] \
  [-m MODEL] \
  [--resume SESSION_ID] \
  [--context FILE ...] \
  [--timeout 120]
```

**출력 (JSON):**
```json
{
  "success": true,
  "model": "gemini-3.1-pro-preview",
  "fallback": false,
  "session_id": "abc123",
  "resume_failed": false,
  "web_searched": true,
  "search_count": 3,
  "stats": {},
  "response": "Gemini의 응답 텍스트..."
}
```

---

## 📌 사용 예시

### 시스템 아키텍처 설계

```
> Gemini와 협업해서 실시간 알림 시스템 설계해줘
> 모드: 2 Round | 모델: gemini-3.1-pro

결과: Claude 아키텍처 초안 → Gemini 확장성 문제 지적
→ Claude 이벤트 기반 설계로 수정 → Gemini 검증 → 최종 산출물
```

### 기술 문서 작성

```
> Gemini와 함께 API 설계 문서 작성해줘
> 모드: Adaptive | 모델: gemini-2.5-pro

결과: 엔드포인트 설계, 에러 처리 패턴, 인증 흐름에 대해
양쪽 AI가 합의할 때까지 반복 개선
```

### 기술적 의사결정 토론

```
> AI끼리 토론해봐: 우리 스타트업에 마이크로서비스 vs 모놀리스 중 뭐가 좋을까?
> 모드: Devil's Advocate | 모델: gemini-3.1-pro

결과: Claude가 모놀리스 주장 (단순성, 속도)
↔ Gemini가 마이크로서비스 주장 (확장성, 팀 독립성)
→ 한쪽이 상대의 논거를 반박할 수 없을 때 패배 인정
```

---

## 🤝 기여하기

기여를 환영합니다! 다음 절차를 따라주세요:

1. 이 저장소를 **Fork**합니다
2. 기능 브랜치를 **생성**합니다 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 **커밋**합니다 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 **Push**합니다 (`git push origin feature/amazing-feature`)
5. **Pull Request**를 생성합니다

### 기여 가능한 영역

- 새로운 협업 모드 추가
- 트리거 문구의 다국어 지원 확대
- 요약 보고서 포맷 개선
- 다른 AI 프로바이더 연동
- 테스트 커버리지 확대

---

## 📄 라이선스

이 프로젝트는 MIT 라이선스에 따라 배포됩니다 — 자세한 내용은 [LICENSE](LICENSE) 파일을 확인하세요.

---

<div align="center">

**멀티 모델 AI 협업 시대를 위해 만들어졌습니다**

<br/>

<img src="https://img.shields.io/badge/Claude-×-7C3AED?style=for-the-badge" alt="Claude">
<img src="https://img.shields.io/badge/Gemini-4285F4?style=for-the-badge" alt="Gemini">

<br/><br/>

*두 개의 머리가 하나보다 낫다 — 인공지능이라 해도.*

</div>
