---
name: gemini-collab
description: |
  Collaborative planning, discussion, and analysis between Claude and Gemini.
  Both AIs independently research and then cross-verify through structured rounds.
  Triggers: "collaborate with Gemini", "Gemini와 협업", "AI 협업",
  "Gemini와 함께 계획", "PRD 작성", "워크플로우 설계",
  "discuss with Gemini", "Gemini와 논의", "Gemini한테 물어봐",
  "AI끼리 토론", "두 AI 의견 비교".
---

# Gemini Collaboration (Round-based)

Gemini 호출은 `scripts/gemini_call.py`로 수행. 인자·출력·fallback 등 상세는 [references/gemini-cli-common.md](references/gemini-cli-common.md) 참조.

**경로 규칙:**
- `{CWD}` = Claude의 현재 작업 디렉토리. 스킬 호출 시점의 CWD를 기준으로 한다.
- 모든 산출물은 반드시 `{CWD}/.gemini/collab/` 하위에 저장할 것. **절대로 스킬 정의 디렉토리(`~/.claude/skills/`)나 다른 경로에 저장하지 말 것.**

**스킬 고유 규칙:**
- 고정 프롬프트 사용 금지. 매 Gemini 호출 시 주제·라운드·모드·이전 피드백을 고려하여 상세 지시사항(-p 인자)을 자율 생성할 것
- 상세 지시사항은 stdin 입력 자료 앞에 자동 추가됨. gemini CLI의 -p 옵션에는 고정 프롬프트가 적용됨
- 첫 라운드에서 WebSearch로 최신 정보를 조사한 뒤 초안 작성할 것
- Fallback 발생 시 `collab_summary.md` 상단에 명시할 것

## 실행 방식

스킬 호출 시 반드시 다음 순서로 실행할 것:

```
1. AskUserQuestion으로 협업 모드 + Gemini 모델 선택 (동시)
2. 출력 폴더 생성: {CWD}/.gemini/collab/{YYYYMMDD_HHMMSS}_{주제요약}/
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
  - question: "Gemini 모델을 선택해주세요."
    header: "Gemini 모델"
    options:
      - label: "gemini-3.1-pro (Recommended)"
        description: "최신 최고 성능. 복잡한 추론·코딩에 적합"
      - label: "gemini-3-flash"
        description: "빠르고 저렴. 일반 작업에 적합"
      - label: "gemini-2.5-pro"
        description: "안정적 성능. 검증된 모델"
      - label: "gemini-2.5-flash"
        description: "경량 고속. 단순 작업에 적합"
```

모델 선택값과 `-m` 인자 매핑:

| 사용자 선택 | `-m` 값 |
|------------|---------|
| gemini-3.1-pro | `gemini-3.1-pro-preview` |
| gemini-3-flash | `gemini-3-flash-preview` |
| gemini-2.5-pro | `gemini-2.5-pro` |
| gemini-2.5-flash | `gemini-2.5-flash` |
| (Other 입력) | 입력값 그대로 |

Fallback 우선순위: 선택한 모델부터 하위 모델로 자동 전환. 상세는 [references/gemini-cli-common.md](references/gemini-cli-common.md) 참조.

## 협업 모드 개요

4가지 모드를 지원. 각 모드의 상세 흐름, 파일명 규칙, 종료 조건, 수행 절차는 [references/modes.md](references/modes.md) 참조.

| 모드 | 흐름 | Gemini 호출 |
|------|------|-------------|
| [1] 1 Round | 초안→검토→판단→최종 | 1회 |
| [2] 2 Round (기본) | 초안→검토→수정→재검토→최종판단→최종 | 2회 |
| [3] Adaptive | [2] 반복, 합의 시 종료 | 1~5회 |
| [4] Devil's Advocate | 주장→반박 무한 반복, 패배 선언 시 종료 | 무제한 |

## 프롬프트 생성 규칙

매 Gemini 호출 시 Claude가 `-p` 인자의 상세 지시사항을 자율 생성할 것.

**고려 요소**: 주제, 현재 라운드 번호, 선택된 모드, 이전 피드백 내용

**웹검색 지시 규칙** (상세 지시사항 생성 시 주제에 따라 적용):

| 주제 유형 | 강도 | 상세 지시사항에 추가할 문구 |
|-----------|------|---------------------------|
| 팩트체크/최신정보 필요 | 강제 | "반드시 웹 검색을 수행하여 정보의 정확성을 교차 검증하라. 검색 결과가 불충분할 경우, 그 사실을 명시하고 내부 지식 기반으로 답변하되 불확실성을 표시하라" |
| 코드리뷰/로직분석/번역 | 생략 | 별도 지시 불필요 (FIXED_PROMPT의 선택적 지시로 충분) |
| 판단 불확실 | 권장 | "가능하면 웹 검색으로 핵심 주장의 사실 여부를 확인하라" |

주제 유형 판별:
- **강제**: 최신 기술 트렌드, 버전 정보, 통계/날짜/인용 검증, 시장 분석, API 문서 확인
- **생략**: 코드 리뷰, 버그 분석, 아키텍처 토론, 번역/교정, 이전 라운드 피드백 검토
- **권장**: 위 두 카테고리에 명확히 속하지 않거나 사실 정보와 주관적 분석이 혼재된 경우

**자동 적용됨** (고정 프롬프트에 포함): 웹 검색 활용 및 출처 제시 요청, ultrathink 모드

**모드별 톤**: [references/modes.md](references/modes.md)의 "프롬프트 톤" 섹션 참조.

## 산출물

`{CWD}/.gemini/collab/{YYYYMMDD_HHMMSS}_{주제요약}/`에 저장.

**파일명 규칙**: `roundN_M_주체_유형.md` (N=라운드, M=순번, 주체=claude/gemini, 유형=draft/review/decision 등)

**고정 파일**: `collab_final.md` (최종본), `collab_summary.md` (요약)

## 요약 생성 (collab_summary.md)

포함 항목: 사용 모델, Fallback 여부, web_searched 상태, 모드, 총 라운드 수, 원래 요청 요약, 라운드별 주요 결정 (반영/미반영 항목과 이유), 작업 결과물 요약, 산출물 위치.
- [3] Adaptive: 합의/강제종료 여부 추가
- [4] Devil's Advocate: 승패 결과, 핵심 논점 추가

## context.md 업데이트

`.gemini/context.md`에 추가:
```
## 최근 협업 (collab)
- {날짜}: {주제} ({모드}, {라운드}R) → 결과: {요약}
```

## 사용자에게 결과 전달

- `collab_summary.md` 핵심 내용 전달
- Fallback 알림이 있으면 명확히 전달
- 상세 내용은 `.gemini/collab/` 폴더 참조 안내

## 주의사항

- 모델 Fallback 발생 시 반드시 사용자에게 알림
- Gemini CLI 인증 정보를 산출물 파일에 포함하지 않을 것
- [4] Devil's Advocate: 종료 조건·금지사항은 [references/modes.md](references/modes.md) 참조
