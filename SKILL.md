---
name: claude-collab
description: |
  Collaborative planning, discussion, and analysis between the main Claude and a Claude subagent.
  Both instances independently research and then cross-verify through structured rounds.
  Triggers: "AI 협업", "Claude 협업", "서브에이전트와 협업",
  "PRD 작성", "워크플로우 설계", "collaborate with subagent",
  "discuss with another Claude", "AI끼리 토론", "두 AI 의견 비교",
  "second opinion", "세컨드 오피니언".
---

# Claude Collaboration (Round-based)

서브에이전트 호출은 Claude Code의 `Agent` 도구로 수행. 인자·출력 등 상세는 [references/subagent-common.md](references/subagent-common.md) 참조.

**경로 규칙:**
- `{CWD}` = Claude의 현재 작업 디렉토리. 스킬 호출 시점의 CWD를 기준으로 한다.
- 모든 산출물은 반드시 `{CWD}/.collab/` 하위에 저장할 것. **절대로 스킬 정의 디렉토리(`~/.claude/skills/`)나 다른 경로에 저장하지 말 것.**

**스킬 고유 규칙:**
- 고정 프롬프트 사용 금지. 매 서브에이전트 호출 시 주제·라운드·모드·이전 피드백을 고려하여 상세 지시사항(Agent prompt)을 자율 생성할 것
- 첫 라운드에서 WebSearch로 최신 정보를 조사한 뒤 초안 작성할 것
- Fallback 발생 시 `collab_summary.md` 상단에 명시할 것

## 실행 방식

스킬 호출 시 반드시 다음 순서로 실행할 것:

```
1. AskUserQuestion으로 협업 모드 + Reviewer 모델 선택 (동시)
2. 출력 폴더 생성: {CWD}/.collab/{YYYYMMDD_HHMMSS}_{주제요약}/
3. 모드별 협업 수행 (references/modes.md 참조)
4. collab_summary.md 생성
5. context.md 업데이트
6. 사용자에게 결과 전달
```

### 초기 설정 (AskUserQuestion - 2개 질문 동시)

```
questions:
  - question: "협업 모드를 선택해주세요."
    header: "협업 모드"
    options:
      - label: "2 Round (Recommended)"
        description: "초안→검토→수정→재검토→최종. 균형 잡힌 기본 모드"
      - label: "1 Round"
        description: "초안→검토→최종. 빠른 협업"
      - label: "Adaptive Round"
        description: "양쪽 합의 시까지 반복 (최대 5라운드)"
      - label: "Devil's Advocate"
        description: "비판적 토론, 한쪽 패배 시까지 (무제한)"
  - question: "Reviewer(서브에이전트) 모델을 선택해주세요."
    header: "Reviewer 모델"
    options:
      - label: "Claude Sonnet (Recommended)"
        description: "균형 잡힌 성능과 속도. 대부분의 작업에 적합"
      - label: "Claude Opus"
        description: "최고 수준의 추론 능력. 복잡한 분석에 적합"
      - label: "Claude Haiku"
        description: "빠르고 경량. 단순 검토에 적합"
```

모델 선택값과 Agent `model` 인자 매핑:

| 사용자 선택 | `model` 값 |
|------------|-----------|
| Claude Sonnet | `sonnet` |
| Claude Opus | `opus` |
| Claude Haiku | `haiku` |

## 협업 모드 개요

4가지 모드를 지원. 각 모드의 상세 흐름, 파일명 규칙, 종료 조건, 수행 절차는 [references/modes.md](references/modes.md) 참조.

| 모드 | 흐름 | 서브에이전트 호출 |
|------|------|-----------------|
| [1] 1 Round | 초안→검토→판단→최종 | 1회 |
| [2] 2 Round (기본) | 초안→검토→수정→재검토→최종판단→최종 | 2회 |
| [3] Adaptive | [2] 반복, 합의 시 종료 | 1~5회 |
| [4] Devil's Advocate | 주장→반박 무한 반복, 패배 선언 시 종료 | 무제한 |

## 프롬프트 생성 규칙

매 서브에이전트 호출 시 메인 Claude가 Agent 도구의 `prompt` 인자를 자율 생성할 것.

**고려 요소**: 주제, 현재 라운드 번호, 선택된 모드, 이전 피드백 내용

### 맥락 주입 규칙

매 라운드 새 Agent를 호출하며, 이전 라운드 내용을 프롬프트에 구조화하여 포함한다. 상세 구조는 [references/subagent-common.md](references/subagent-common.md)의 "세션 관리" 참조.

- **Round 1~2**: 이전 라운드 전문 포함 가능
- **Round 3+**: 이전 라운드는 핵심 요약만, 직전 라운드만 전문 포함
- **요약 시 포함 항목**: 주요 쟁점, 합의된 사항, 미해결 사항

**웹검색 지시 규칙** (프롬프트 생성 시 주제에 따라 적용):

| 주제 유형 | 강도 | 프롬프트에 추가할 문구 |
|-----------|------|----------------------|
| 팩트체크/최신정보 필요 | 강제 | "반드시 웹 검색을 수행하여 정보의 정확성을 교차 검증하라. 검색 결과가 불충분할 경우, 그 사실을 명시하고 내부 지식 기반으로 답변하되 불확실성을 표시하라" |
| 코드리뷰/로직분석/번역 | 생략 | 별도 지시 불필요 |
| 판단 불확실 | 권장 | "가능하면 웹 검색으로 핵심 주장의 사실 여부를 확인하라" |

주제 유형 판별:
- **강제**: 최신 기술 트렌드, 버전 정보, 통계/날짜/인용 검증, 시장 분석, API 문서 확인
- **생략**: 코드 리뷰, 버그 분석, 아키텍처 토론, 번역/교정, 이전 라운드 피드백 검토
- **권장**: 위 두 카테고리에 명확히 속하지 않거나 사실 정보와 주관적 분석이 혼재된 경우

**모드별 톤**: [references/modes.md](references/modes.md)의 "프롬프트 톤" 섹션 참조.

## 산출물

`{CWD}/.collab/{YYYYMMDD_HHMMSS}_{주제요약}/`에 저장.

**파일명 규칙**: `roundN_M_주체_유형.md` (N=라운드, M=순번, 주체=main/reviewer, 유형=draft/review/decision 등)

**고정 파일**: `collab_final.md` (최종본), `collab_summary.md` (요약)

## 요약 생성 (collab_summary.md)

포함 항목: 사용 모델, 모드, 총 라운드 수, 원래 요청 요약, 라운드별 주요 결정 (반영/미반영 항목과 이유), 작업 결과물 요약, 산출물 위치.
- [3] Adaptive: 합의/강제종료 여부 추가
- [4] Devil's Advocate: 승패 결과, 핵심 논점 추가

## context.md 업데이트

`.collab/context.md`에 추가:
```
## 최근 협업 (collab)
- {날짜}: {주제} ({모드}, {라운드}R) → 결과: {요약}
```

## 사용자에게 결과 전달

- `collab_summary.md` 핵심 내용 전달
- 상세 내용은 `.collab/` 폴더 참조 안내

## 주의사항

- 서브에이전트(Reviewer)는 독립적 시각에서 검토해야 함. 메인 Claude의 결론을 그대로 추종하지 않도록 프롬프트에 명시할 것
- [4] Devil's Advocate: 종료 조건·금지사항은 [references/modes.md](references/modes.md) 참조
