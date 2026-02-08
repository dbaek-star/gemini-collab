---
name: gemini-collab
description: |
  Collaborative planning, discussion, and analysis between Claude and Gemini.
  For coding: creates PRD, workflow, and task plans instead of writing code directly.
  For discussion: both AIs independently research and then cross-verify.
  Triggers: "collaborate with Gemini", "Gemini과 협업", "AI 협업",
  "Gemini와 함께 계획", "PRD 작성", "워크플로우 설계",
  "discuss with Gemini", "Gemini와 논의", "Gemini한테 물어봐",
  "AI끼리 토론", "두 AI 의견 비교".
---

# Gemini Collaboration (Round-based)

Gemini 호출은 `scripts/gemini_call.py`로 수행. 사용법은 [references/gemini-cli-common.md](references/gemini-cli-common.md) 참조.

**경로 규칙:**
- `{CWD}` = Claude의 현재 작업 디렉토리 (Primary working directory). 스킬 호출 시점의 CWD를 기준으로 한다.
- 모든 산출물은 반드시 `{CWD}/.gemini/collab/` 하위에 저장할 것. **절대로 스킬 정의 디렉토리(`~/.claude/skills/`)나 다른 경로에 저장하지 말 것.**

**스킬 고유 규칙:**
- 고정 프롬프트 사용 금지. 매 Gemini 호출 시 주제·라운드·모드·이전 피드백을 고려하여 상세 지시사항(-p 인자)을 자율 생성할 것
- 상세 지시사항은 stdin 입력 자료 앞에 자동 추가됨. gemini CLI의 -p 옵션에는 고정 프롬프트가 적용됨
- 첫 라운드에서 WebSearch로 최신 정보를 조사한 뒤 초안 작성할 것
- Fallback 발생 시 `collab_summary.md` 상단에 명시할 것

## Gemini 호출 방법

```bash
python {스킬경로}/scripts/gemini_call.py INPUT_FILE -p "상세 지시사항" -o OUTPUT_FILE [-m MODEL] [--resume [SESSION_ID]]
```

**중요:** `-p` 인자의 "상세 지시사항"은 stdin 입력 자료 앞에 자동으로 추가됩니다.

**stdin 구조:**
```
# 지시사항
{-p 인자의 내용}

---

# 입력 자료
{INPUT_FILE의 내용}
```

**실제 gemini CLI에 전달되는 고정 프롬프트:**
```
입력된 자료에 대한 답변요청. 필요한 경우 웹 검색을 통해 최신 정보를 조사하여 활용하고, 출처를 함께 제시. ultrathink
```

스크립트가 자동 처리하는 항목: 모델 fallback, JSON 파싱, 고정 프롬프트 적용, 에러/타임아웃 처리, 세션 관리.

stdout JSON의 `success`, `model`, `fallback`, `web_searched` 필드를 확인할 것.
- `success=false` → Claude 단독으로 대체 처리할 것
- `web_searched=false` → `collab_summary.md`에 기록할 것

## 실행 방식

스킬 호출 시 반드시 다음 순서로 실행할 것:

```
1. AskUserQuestion으로 협업 모드 + Gemini 모델 선택 (동시)
2. 출력 폴더 생성
3. 모드별 협업 수행 (아래 수행 절차 참조)
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
      - label: "Dog Fight"
        description: "비판적 토론, 한쪽 패배 시까지 (무제한)"
  - question: "Gemini 모델을 선택해주세요."
    header: "Gemini 모델"
    options:
      - label: "gemini-3-pro (Recommended)"
        description: "최고 성능. 복잡한 추론·코딩에 적합"
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
| gemini-3-pro | `gemini-3-pro-preview` |
| gemini-3-flash | `gemini-3-flash-preview` |
| gemini-2.5-pro | `gemini-2.5-pro` |
| gemini-2.5-flash | `gemini-2.5-flash` |
| (Other 입력) | 입력값 그대로 |

Fallback 우선순위: 선택한 모델부터 하위 모델로 자동 전환.
```
gemini-3-pro-preview → gemini-3-flash-preview → gemini-2.5-pro → gemini-2.5-flash → gemini-2.5-flash-lite
```

## 협업 모드

### [1] 1 Round

```
Claude 초안 → Gemini 검토 → Claude 판단 → 최종본
```

| 순서 | 파일명 | 주체 | 내용 |
|------|--------|------|------|
| 1 | `round1_1_claude_draft.md` | Claude | 초안 (WebSearch 포함) |
| 2 | `round1_2_gemini_review.md` | Gemini | 검토 |
| 3 | `round1_3_claude_decision.md` | Claude | 판단 |
| 4 | `collab_final.md` | Claude | 최종본 |
| 5 | `collab_summary.md` | Claude | 요약 |

Gemini 호출: 1회

### [2] 2 Round (기본값)

```
Claude 초안 → Gemini 검토 → Claude 판단·수정
  → Gemini 재검토 → Claude 최종 판단 → 최종본
```

| 순서 | 파일명 | 주체 | 내용 |
|------|--------|------|------|
| 1 | `round1_1_claude_draft.md` | Claude | 초안 |
| 2 | `round1_2_gemini_review.md` | Gemini | 1차 검토 |
| 3 | `round1_3_claude_decision.md` | Claude | 판단 + 수정 내용 포함 |
| 4 | `round2_1_gemini_review.md` | Gemini | 2차 검토 |
| 5 | `round2_2_claude_decision.md` | Claude | 최종 판단 |
| 6 | `collab_final.md` | Claude | 최종본 |
| 7 | `collab_summary.md` | Claude | 요약 |

Gemini 호출: 2회

### [3] Adaptive Round (최대 5라운드)

```
Claude 초안 → [Gemini 검토 → Claude 판단·수정] × N → 최종본
```

[2]와 동일 패턴을 반복. 파일명: `roundN_M_주체_유형.md`

**종료 조건**:
- Gemini 응답에 추가 지적사항 없음 → 합의
- Claude가 모든 피드백에 동의 완료 → 합의
- 5라운드 도달 → 강제 종료, 그 시점 합의사항 기반 최종본

Gemini 호출: 1~5회. `collab_summary.md`에 총 라운드 수, 합의/강제종료 여부 기록.

### [4] Dog Fight (무제한 - 명시적 패배 선언까지)

```
Claude 주장 → Gemini 반박 → Claude 재반박 → Gemini 재반박 → ... → 한쪽 명시적 패배 선언 시까지 무한 지속
```

**debater-debater 구조** (creator-reviewer 아님). **라운드 제한 없음 - 한쪽이 명시적 패배를 선언할 때까지 무한 지속**.

| 순서 | 파일명 패턴 | 주체 | 내용 |
|------|------------|------|------|
| 1 | `round1_1_claude_argument.md` | Claude | 초기 주장 |
| 2 | `round1_2_gemini_counter.md` | Gemini | 반박 |
| 3 | `round2_1_claude_rebuttal.md` | Claude | 재반박 |
| 4 | `round2_2_gemini_rebuttal.md` | Gemini | 재반박 |
| 5 | `round3_1_claude_rebuttal.md` | Claude | 재반박 (계속) |
| 6 | `round3_2_gemini_rebuttal.md` | Gemini | 재반박 (계속) |
| ... | `roundN_M_주체_action.md` | 교대 | 패배 선언 시까지 무한 반복 |
| 최종 | `roundN_surrender_loser.md` | 패배자 | **"패배를 인정합니다" 명시적 선언** |

**패배 선언 형식** (반드시 포함해야 함):
```
## 패배를 인정합니다.

[패배 사유 설명]
```

**페르소나 주입 규칙**:
- **Claude**: 상대 의견의 약점을 논리적으로 공격할 것. 근거 없는 주장 즉시 지적할 것. 반박 불가능 시만 패배 인정할 것. 반박 가능한 한 무한 진행할 것.
- **Gemini 프롬프트**: "상대 주장에 매우 비판적으로 반응하라. 논리적 허점·근거 부족·대안적 해석을 적극 제시하라. 반박 불가능 시 반드시 '패배를 인정합니다'라고 명시 선언하라. (필수)"

**종료 조건** (이 중 하나만 발생):
- ✅ **Gemini 응답**에 명시적으로 "패배를 인정합니다" 포함 → Gemini 패배, 즉시 종료
- ✅ **Claude가 명시적으로 "패배를 인정합니다" 선언** → Claude 패배, 즉시 종료
- ❌ **패배 선언 없음**: 계속 진행 (무한 반복 가능)

**중요: 임의의 제3자 판정 금지**
- 양쪽 모두 패배 선언을 하지 않으면, 절대 임의로 승패를 결정하지 말 것
- 대신 다음 라운드를 계속 진행할 것

**최종본 생성 조건**:
- **패배 선언이 있어야만** `collab_final.md` 생성
- 패배 선언 없으면 `collab_final.md` 생성 금지 (대신 협업 계속)

**최종본**: 승자 논리 중심. Claude 패배 시 Gemini 논리 중심으로 작성.
`collab_summary.md`에 총 라운드 수, 승패, 핵심 논점, 패배 선언 라운드 기록.

## 프롬프트 생성 규칙

매 Gemini 호출 시 Claude가 `-p` 인자의 상세 지시사항을 자율 생성할 것.

**고려 요소**: 주제, 현재 라운드 번호, 선택된 모드, 이전 피드백 내용

**자동 적용됨** (고정 프롬프트에 포함되어 있음):
- 웹 검색 활용 및 출처 제시 요청
- ultrathink 모드

**상세 지시사항(-p 인자)에 포함할 내용**:
- 구체적인 검토/분석/반박 요청 사항
- 모드별 특화된 지시 (아래 모드별 톤 참조)
- 이전 라운드 맥락 (필요시)

**모드별 톤**:

| 모드 | 톤 | 예시 |
|------|-----|------|
| [1] 1 Round | 건설적 피드백 요청 | "다음 초안을 검토하고 개선점을 제안해주세요." |
| [2] 2 Round | 건설적 피드백 요청 | "수정된 내용을 재검토하고 추가 개선사항이 있는지 확인해주세요." |
| [3] Adaptive | 건설적 + 합의 도달 여부 판단 요청 | "다음 내용을 검토하고, 합의에 도달했는지 판단해주세요." |
| [4] Dog Fight | 비판적 반론 + 패배 선언 조건 포함 | "상대 주장에 매우 비판적으로 반응하라. 논리적 허점을 적극 제시하라. 반박 불가능 시 '패배를 인정합니다'라고 선언하라." |

## 산출물

`{CWD}/.gemini/collab/{YYYYMMDD_HHMMSS}_{주제요약}/`에 저장. (`{CWD}` = 현재 작업 디렉토리)

**파일명 규칙**: `roundN_M_주체_유형.md`
- `N`: 라운드 번호 (1, 2, 3...)
- `M`: 라운드 내 순번 (1, 2, 3...)
- `주체`: `claude` 또는 `gemini`
- `유형`: `draft`, `review`, `decision`, `argument`, `counter`, `rebuttal` 등

**고정 파일** (모든 모드 공통):
- `collab_final.md` — 최종 결과물
- `collab_summary.md` — 요약

## 수행 절차

### 1. 출력 폴더 생성
`{CWD}/.gemini/collab/{YYYYMMDD_HHMMSS}_{주제요약}/` 생성 (`{CWD}` = 현재 작업 디렉토리)

### 2. 모드별 협업 수행

#### [1] 1 Round
1. Claude WebSearch 조사 후 초안 → `round1_1_claude_draft.md`
2. Gemini 호출 (자율 프롬프트) → `round1_2_gemini_review.md`
   - session_id 기록. fallback, web_searched 확인.
3. Claude 판단 (동의/반박/부분동의) → `round1_3_claude_decision.md`
4. 최종본 → `collab_final.md`

#### [2] 2 Round (기본값)
1. Claude WebSearch 조사 후 초안 → `round1_1_claude_draft.md`
2. Gemini 호출 → `round1_2_gemini_review.md`
   - session_id 기록.
3. Claude 판단 + 수정 내용 포함 → `round1_3_claude_decision.md`
4. Gemini 재검토 (--resume session_id, --context round1_1, round1_2) → `round2_1_gemini_review.md`
5. Claude 최종 판단 → `round2_2_claude_decision.md`
6. 최종본 → `collab_final.md`

#### [3] Adaptive Round (최대 5라운드)
1. [2]와 동일 패턴으로 시작.
2. 매 라운드 종료 시 합의 판정:
   - Gemini 추가 지적 없음 또는 Claude 전체 동의 → 합의 → 최종본
   - 미합의 → 다음 라운드 (--resume으로 세션 유지)
3. 5라운드 도달 시 강제 종료 → 그 시점 합의사항 기반 최종본.

#### [4] Dog Fight

위 [4] 모드 정의의 종료 조건·루프·프롬프트 규칙을 따른다.

1. Claude 초기 주장 작성 → `round1_1_claude_argument.md`
2. 루프 실행: Gemini 반박 → 패배 감지 → Claude 재반박 → 패배 감지 → 반복
   - 각 Gemini 호출에 `--resume SESSION_ID` 사용
3. 패배 선언 감지 시 → `collab_final.md` 생성 (승자 논리 중심)

### 3. 요약 생성
`collab_summary.md` 생성:
- 사용 모델, Fallback 여부, web_searched 상태
- 선택된 모드, 총 라운드 수
- 원래 요청 요약
- 라운드별 주요 결정 (반영/미반영 항목과 이유)
- 작업 결과물 요약
- [3]: 합의/강제종료 여부
- [4]: 승패 결과, 핵심 논점
- 산출물 위치

### 4. context.md 업데이트
`.gemini/context.md`에 추가:
```
## 최근 협업 (collab)
- {날짜}: {주제} ({모드}, {라운드}R) → 결과: {요약}
```

### 5. 사용자에게 결과 전달
- `collab_summary.md` 핵심 내용 전달
- Fallback 알림이 있으면 명확히 전달
- 상세 내용은 `.gemini/collab/` 폴더 참조 안내

## 주의사항

- 모델 Fallback 발생 시 반드시 사용자에게 알림
- Gemini CLI 인증 정보를 산출물 파일에 포함하지 않을 것
- [4] Dog Fight: 위 모드 정의의 종료 조건·금지사항을 반드시 준수할 것
