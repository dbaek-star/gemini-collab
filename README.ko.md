<div align="center">

# Claude Collab

### Claude × Claude 서브에이전트 — AI 간 협업 지능 시스템

[![Claude Code Skill](https://img.shields.io/badge/Claude_Code-Skill-7C3AED?style=for-the-badge&logo=anthropic&logoColor=white)](https://docs.anthropic.com/en/docs/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-F59E0B?style=for-the-badge)](LICENSE)

<br/>

**두 개의 Claude 인스턴스. 하나의 통합된 결과물.**
Claude Collab은 메인 Claude와 Claude 서브에이전트 사이의 구조화된 라운드 기반 협업을 오케스트레이션합니다. 독립적인 조사, 교차 검증, 반복적 개선을 통해 더 높은 품질의 결과물을 만들어냅니다.

<br/>

[English README](README.md)

---

<img src="https://img.shields.io/badge/초안-Main_Claude-7C3AED?style=flat-square" alt="Main"> →
<img src="https://img.shields.io/badge/검토-Reviewer-E0926C?style=flat-square" alt="Reviewer"> →
<img src="https://img.shields.io/badge/판단-Main_Claude-7C3AED?style=flat-square" alt="Main"> →
<img src="https://img.shields.io/badge/최종-합의-10B981?style=flat-square" alt="Final">

</div>

<br/>

## 목차

- [왜 Claude Collab인가?](#-왜-claude-collab인가)
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

## 왜 Claude Collab인가?

> 하나의 AI가 초안을 작성할 수 있다. 두 개의 AI 인스턴스는 **검증하고, 도전하고, 개선**할 수 있다.

| 문제점 | 해결책 |
|:-------|:-------|
| 단일 인스턴스의 맹점 | 두 독립 인스턴스가 서로의 출력을 교차 검증 |
| 검증 없는 가정 | 구조화된 검토 라운드로 비판적 평가 강제 |
| 환각(Hallucination) 위험 | 웹 검색 통합 + 이중 검증 |
| 확증 편향 | 교차 검토 전 독립적 조사 수행 |

**Claude Collab**은 **적대적 협업(Adversarial Collaboration)** 의 힘을 CLI 워크플로우에 가져옵니다 — 학계의 동료 심사(peer review)와 보안 분야의 레드팀(red-teaming)을 이끄는 동일한 원리입니다. 서브에이전트를 활용하여 검토하는 Claude가 메인 Claude와 독립적으로 작동하므로, 진정한 비판적 평가가 보장됩니다.

---

## 작동 방식

```
┌─────────────────────────────────────────────────────────┐
│                    CLAUDE COLLAB                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐         │
│   │   MAIN   │───▶│ REVIEWER │───▶│   MAIN   │         │
│   │  CLAUDE   │    │(서브에이전트)│   │  CLAUDE   │        │
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

1. **메인 Claude가 조사** — 웹 검색으로 주제를 조사한 후 초안을 작성합니다
2. **Reviewer(서브에이전트)가 검토** — 초안을 독립적으로 검토합니다 (자체 웹 검색 포함)
3. **메인 Claude가 평가** — Reviewer의 피드백을 수용, 반박, 또는 부분 채택합니다
4. **(선택)** 합의 또는 종료 조건까지 추가 라운드를 진행합니다
5. **최종 산출물** — 종합적인 협업 요약과 함께 최종본이 생성됩니다

---

## 협업 모드

<table>
<tr>
<td width="25%" align="center">

### 1 Round
**빠른 협업**

</td>
<td width="25%" align="center">

### 2 Round
**추천 (기본값)**

</td>
<td width="25%" align="center">

### Adaptive
**합의까지 반복**

</td>
<td width="25%" align="center">

### Devil's Advocate
**무제한 토론**

</td>
</tr>
<tr>
<td>

```
Main 초안
    ↓
Reviewer 검토
    ↓
Main 판단
    ↓
  최종본
```

</td>
<td>

```
Main 초안
    ↓
Reviewer 검토
    ↓
Main 수정
    ↓
Reviewer 재검토
    ↓
Main 최종 판단
    ↓
  최종본
```

</td>
<td>

```
Main 초안
    ↓
┌─── 반복 ───┐
│ Reviewer 검토│
│     ↓       │
│ Main 판단   │
└─── × N ────┘
    ↓
  최종본
```

</td>
<td>

```
Main 주장
    ↓
Reviewer 반박
    ↓
Main 재반박
    ↓
    ...
    ↓
 패배 선언!
```

</td>
</tr>
<tr>
<td>

서브에이전트 호출: **1회**
적합: 빠른 검토

</td>
<td>

서브에이전트 호출: **2회**
적합: 대부분의 작업

</td>
<td>

서브에이전트 호출: **1~5회**
적합: 복잡한 주제

</td>
<td>

서브에이전트 호출: **무제한**
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

## 사전 요구사항

| 요구사항 | 상세 |
|:---------|:-----|
| **Claude Code** | [Anthropic 공식 CLI](https://docs.anthropic.com/en/docs/claude-code) |

그게 전부입니다! 추가 CLI 도구, Python, npm 패키지가 필요 없습니다. Claude Collab은 Claude Code의 내장 `Agent` 도구를 사용하여 서브에이전트를 직접 호출합니다.

---

## 설치 방법

### 1. 스킬 클론 & 설치

```
git clone https://github.com/dbaek-star/gemini-collab.git
```

#### Windows — Git Bash (권장)

> Windows에서 Claude Code는 Git Bash를 기본 셸로 사용합니다. 이 방법을 권장합니다.

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

### 2. 설치 확인

Claude Code를 열고 트리거 문구를 입력합니다:

```
> AI 협업해서 프로젝트 계획 세워줘
```

스킬이 로드되면 설치 완료입니다!

---

## 사용 방법

### 트리거 문구

다음 문구로 스킬을 실행할 수 있습니다 (한국어 및 영어):

| 언어 | 트리거 예시 |
|:-----|:------------|
| 한국어 | `"AI 협업"`, `"Claude 협업"`, `"서브에이전트와 협업"`, `"AI끼리 토론"`, `"두 AI 의견 비교"`, `"세컨드 오피니언"`, `"PRD 작성"`, `"워크플로우 설계"` |
| 영어 | `"collaborate with subagent"`, `"discuss with another Claude"`, `"second opinion"` |

### 인터랙티브 설정

스킬이 실행되면 두 개의 선택 프롬프트가 동시에 표시됩니다:

```
┌─ 협업 모드 ────────────────────────────────────┐
│  ● 2 Round (추천)                              │
│  ○ 1 Round                                     │
│  ○ Adaptive Round                              │
│  ○ Devil's Advocate                             │
└────────────────────────────────────────────────┘

┌─ Reviewer 모델 ───────────────────────────────┐
│  ● Claude Sonnet (추천)                        │
│  ○ Claude Opus                                 │
│  ○ Claude Haiku                                │
└────────────────────────────────────────────────┘
```

### 세션 예시

```bash
# Claude Code에서
> AI 협업해서 이커머스 플랫폼의 마이크로서비스 아키텍처 설계해줘

# Claude가 다음을 수행합니다:
# 1. 모드와 Reviewer 모델 선택 요청
# 2. 웹 검색으로 주제 조사
# 3. 초안 작성
# 4. 서브에이전트를 생성하여 검토 요청
# 5. 피드백 평가 후 최종 산출물 생성
```

---

## 모델 지원

### 사용 가능한 Reviewer 모델

| 모델 | Agent `model` 값 | 적합한 용도 |
|:------|:----------------|:------------|
| **Claude Sonnet** | `sonnet` | 균형 잡힌 성능·속도 (추천) |
| **Claude Opus** | `opus` | 최고 수준 추론 능력, 복잡한 분석 |
| **Claude Haiku** | `haiku` | 빠르고 경량, 단순 검토 |

> Fallback 체인 불필요 — Claude Code의 Agent 도구가 모델 가용성을 내부적으로 관리합니다.

---

## 산출물 구조

모든 산출물은 현재 작업 디렉토리 하위에 저장됩니다:

```
{CWD}/.collab/{YYYYMMDD_HHMMSS}_{주제}/
├── round1_1_main_draft.md          # 메인 Claude의 초안
├── round1_2_reviewer_review.md     # Reviewer의 검토
├── round1_3_main_decision.md       # 메인 Claude의 피드백 판단
├── round2_1_reviewer_review.md     # (2 Round+) Reviewer의 재검토
├── round2_2_main_decision.md       # (2 Round+) 메인 Claude의 최종 판단
├── collab_final.md                 # 최종 협업 산출물
└── collab_summary.md               # 협업 요약 & 메타데이터
```

### 요약 보고서 (`collab_summary.md`)

요약에 포함되는 항목:
- 사용된 Reviewer 모델
- 협업 모드 & 총 라운드 수
- 원래 요청 요약
- 라운드별 주요 결정 사항 (수용/반박 항목과 사유)
- 최종 산출물 요약
- 산출물 파일 위치

---

## 아키텍처

```
claude-collab/
├── SKILL.md                     # 스킬 정의 & 오케스트레이션 규칙
└── references/
    ├── subagent-common.md       # Agent 도구 사용 규칙 & 파라미터
    └── modes.md                 # 협업 모드 상세 명세
```

### 핵심 설계 결정

| 결정 | 이유 |
|:-----|:-----|
| **Agent 도구로 서브에이전트 호출** | 외부 CLI 없이 직접 호출 — Python 래퍼 불필요, 의존성 제로 |
| **고정 프롬프트 미사용** | 매 서브에이전트 호출마다 주제, 라운드, 모드, 이전 피드백에 기반한 동적 프롬프트 생성 |
| **독립적 Reviewer** | 서브에이전트는 메인 Claude와 독립적으로 작동하여 진정한 비판적 평가 보장 |
| **라운드별 맥락 주입** | 매 라운드 새 서브에이전트 호출 시 이전 맥락을 프롬프트에 포함 — 실험적 플래그 불필요 |
| **의존성 제로** | Claude Code만 있으면 됨 — npm, Python, 외부 도구 불필요 |

### 서브에이전트 호출 패턴

```
Agent({
  description: "Round 1 - 초안 검토",
  model: "sonnet",
  prompt: "당신은 독립적인 Reviewer입니다. 다음 초안을 비판적으로 검토하세요..."
})
```

**응답:** Agent 도구가 서브에이전트의 응답 텍스트를 직접 반환 — JSON 파싱 불필요.

---

## 사용 예시

### 시스템 아키텍처 설계

```
> AI 협업해서 실시간 알림 시스템 설계해줘
> 모드: 2 Round | 모델: Claude Sonnet

결과: 메인 Claude 아키텍처 초안 → Reviewer 확장성 문제 지적
→ 메인 Claude 이벤트 기반 설계로 수정 → Reviewer 검증 → 최종 산출물
```

### 기술 문서 작성

```
> 서브에이전트와 협업해서 API 설계 문서 작성해줘
> 모드: Adaptive | 모델: Claude Opus

결과: 엔드포인트 설계, 에러 처리 패턴, 인증 흐름에 대해
양쪽 Claude 인스턴스가 합의할 때까지 반복 개선
```

### 기술적 의사결정 토론

```
> AI끼리 토론해봐: 우리 스타트업에 마이크로서비스 vs 모놀리스 중 뭐가 좋을까?
> 모드: Devil's Advocate | 모델: Claude Sonnet

결과: 메인 Claude가 모놀리스 주장 (단순성, 속도)
↔ Reviewer가 마이크로서비스 주장 (확장성, 팀 독립성)
→ 한쪽이 상대의 논거를 반박할 수 없을 때 패배 인정
```

---

## 기여하기

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
- 고급 서브에이전트 프롬프트 전략
- 테스트 커버리지 확대

---

## 라이선스

이 프로젝트는 MIT 라이선스에 따라 배포됩니다 — 자세한 내용은 [LICENSE](LICENSE) 파일을 확인하세요.

---

<div align="center">

**멀티 인스턴스 AI 협업 시대를 위해 만들어졌습니다**

<br/>

<img src="https://img.shields.io/badge/Main_Claude-×-7C3AED?style=for-the-badge" alt="Main">
<img src="https://img.shields.io/badge/Reviewer_Claude-E0926C?style=for-the-badge" alt="Reviewer">

<br/><br/>

*두 개의 머리가 하나보다 낫다 — 같은 모델이라 해도.*

</div>
