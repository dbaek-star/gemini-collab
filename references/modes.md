# 협업 모드 상세

## 목차

- [1] 1 Round
- [2] 2 Round (기본값)
- [3] Adaptive Round
- [4] Devil's Advocate
- 프롬프트 톤

---

## [1] 1 Round

```
Main 초안 → Reviewer 검토 → Main 판단 → 최종본
```

| 순서 | 파일명 | 주체 | 내용 |
|------|--------|------|------|
| 1 | `round1_1_main_draft.md` | Main | 초안 (WebSearch 포함) |
| 2 | `round1_2_reviewer_review.md` | Reviewer | 검토 |
| 3 | `round1_3_main_decision.md` | Main | 판단 |
| 4 | `collab_final.md` | Main | 최종본 |
| 5 | `collab_summary.md` | Main | 요약 |

서브에이전트 호출: 1회

### 수행 절차

1. Main WebSearch 조사 후 초안 → `round1_1_main_draft.md`
2. Agent 도구로 Reviewer 호출 (자율 프롬프트) → `round1_2_reviewer_review.md`
3. Main 판단 (동의/반박/부분동의) → `round1_3_main_decision.md`
4. 최종본 → `collab_final.md`

---

## [2] 2 Round (기본값)

```
Main 초안 → Reviewer 검토 → Main 판단·수정 → Reviewer 재검토 → Main 최종 판단 → 최종본
```

| 순서 | 파일명 | 주체 | 내용 |
|------|--------|------|------|
| 1 | `round1_1_main_draft.md` | Main | 초안 |
| 2 | `round1_2_reviewer_review.md` | Reviewer | 1차 검토 |
| 3 | `round1_3_main_decision.md` | Main | 판단 + 수정 내용 포함 |
| 4 | `round2_1_reviewer_review.md` | Reviewer | 2차 검토 |
| 5 | `round2_2_main_decision.md` | Main | 최종 판단 |
| 6 | `collab_final.md` | Main | 최종본 |
| 7 | `collab_summary.md` | Main | 요약 |

서브에이전트 호출: 2회

### 수행 절차

1. Main WebSearch 조사 후 초안 → `round1_1_main_draft.md`
2. Agent 도구로 Reviewer 호출 → `round1_2_reviewer_review.md`
3. Main 판단 + 수정 내용 포함 → `round1_3_main_decision.md`
4. 새 Agent 호출로 Reviewer 재검토 (이전 초안·검토·판단 내용을 프롬프트에 포함) → `round2_1_reviewer_review.md`
5. Main 최종 판단 → `round2_2_main_decision.md`
6. 최종본 → `collab_final.md`

---

## [3] Adaptive Round (최대 5라운드)

```
Main 초안 → [Reviewer 검토 → Main 판단·수정] × N → 최종본
```

[2]와 동일 패턴을 반복. 파일명: `roundN_M_주체_유형.md`

서브에이전트 호출: 1~5회

**종료 조건**:
- Reviewer 추가 지적 없음 → 합의
- Main이 모든 피드백에 동의 완료 → 합의
- 5라운드 도달 → 강제 종료, 그 시점 합의사항 기반 최종본

### 수행 절차

1. [2]와 동일 패턴으로 시작.
2. 매 라운드 종료 시 합의 판정:
   - Reviewer 추가 지적 없음 또는 Main 전체 동의 → 합의 → 최종본
   - 미합의 → 다음 라운드 (새 Agent 호출에 이전 맥락을 요약하여 포함. 3라운드 이상 시 이전 라운드는 핵심 요약만 포함)
3. 5라운드 도달 시 강제 종료 → 그 시점 합의사항 기반 최종본.

`collab_summary.md`에 총 라운드 수, 합의/강제종료 여부 기록.

---

## [4] Devil's Advocate (무제한)

debater-debater 구조. 한쪽이 명시적 패배를 선언할 때까지 무한 지속.

```
Main 주장 → Reviewer 반박 → Main 재반박 → ... → 패배 선언
```

| 순서 | 파일명 패턴 | 주체 | 내용 |
|------|------------|------|------|
| 1 | `round1_1_main_argument.md` | Main | 초기 주장 |
| 2 | `round1_2_reviewer_counter.md` | Reviewer | 반박 |
| 3+ | `roundN_M_주체_rebuttal.md` | 교대 | 패배 선언 시까지 반복 |
| 최종 | `roundN_surrender_loser.md` | 패배자 | 패배 선언 |

**페르소나 규칙**:
- **Main**: 상대 약점을 논리적으로 공격. 근거 없는 주장 즉시 지적. 반박 불가능 시만 패배 인정.
- **Reviewer 프롬프트에 포함**: "상대 주장에 매우 비판적으로 반응하라. 논리적 허점·근거 부족·대안적 해석을 적극 제시하라. 반박 불가능 시 반드시 '패배를 인정합니다'라고 명시 선언하라."

**종료 조건** (하나만 발생):
- Reviewer 응답에 "패배를 인정합니다" 포함 → Reviewer 패배, 즉시 종료
- Main이 "패배를 인정합니다" 선언 → Main 패배, 즉시 종료
- 패배 선언 없으면 다음 라운드 계속 (임의 승패 결정 금지)

**패배 선언 형식**:
```
## 패배를 인정합니다.

[패배 사유 설명]
```

**최종본**: 패배 선언이 있어야만 `collab_final.md` 생성. 승자 논리 중심으로 작성.

### 수행 절차

1. Main 초기 주장 → `round1_1_main_argument.md`
2. 루프: Reviewer 반박 → 패배 감지 → Main 재반박 → 패배 감지 → 반복
   - 각 Reviewer 호출은 새 Agent로 수행하되, 이전 논쟁 맥락을 요약하여 프롬프트에 포함 (3라운드 이상 시 핵심 논점만 포함)
3. 패배 선언 감지 시 → `collab_final.md` 생성 (승자 논리 중심)

`collab_summary.md`에 총 라운드 수, 승패, 핵심 논점, 패배 선언 라운드 기록.

---

## 프롬프트 톤

| 모드 | 톤 | 예시 |
|------|-----|------|
| [1] 1 Round | 건설적 피드백 | "다음 초안을 검토하고 개선점을 제안해주세요." |
| [2] 2 Round | 건설적 피드백 | "수정된 내용을 재검토하고 추가 개선사항이 있는지 확인해주세요." |
| [3] Adaptive | 건설적 + 합의 판단 | "다음 내용을 검토하고, 합의에 도달했는지 판단해주세요." |
| [4] Devil's Advocate | 비판적 반론 | "상대 주장에 비판적으로 반응하라. 반박 불가능 시 '패배를 인정합니다' 선언." |
