# Gemini CLI 공통 규칙

## 호출 스크립트

모든 Gemini 호출은 `scripts/gemini_call.py`로 수행한다.

### 사용법

```bash
python {스킬경로}/scripts/gemini_call.py INPUT_FILE -p "상세 지시사항" [-o OUTPUT_FILE] [-m MODEL] [--resume [SESSION_ID]] [--context FILE ...] [--timeout N]
```

**중요:** `-p` 인자의 "상세 지시사항"은 stdin 입력 자료 앞에 자동으로 추가됩니다. 실제 gemini CLI에 전달되는 `-p` 옵션은 고정 프롬프트입니다.

### 인자

| 인자 | 필수 | 설명 |
|------|------|------|
| `INPUT_FILE` | O | Gemini에 전달할 입력 파일 경로 (stdin의 "입력 자료" 섹션에 포함) |
| `-p PROMPT` | O | 상세 지시사항 (stdin의 "지시사항" 섹션에 포함. 고정 프롬프트는 별도 자동 적용) |
| `-o OUTPUT` | X | 응답 텍스트를 저장할 파일 경로 |
| `-m MODEL` | X | 사용할 모델명 (기본: `gemini-3.1-pro-preview`). 실패 시 하위 모델로 자동 fallback |
| `--resume [SESSION_ID]` | X | 이전 세션 이어서 대화. session_id 지정 시 해당 세션, 생략 시 `latest` |
| `--context FILE ...` | X | resume 실패 시 맥락 복원용 파일 목록 (이전 입력, 이전 응답 등) |
| `--timeout N` | X | 타임아웃 초 (기본: 120) |

### 모델 및 Fallback 체인

선택한 모델부터 시작하여 하위 모델로 자동 전환:

```
gemini-3.1-pro-preview → gemini-3-flash-preview → gemini-2.5-pro → gemini-2.5-flash → gemini-2.5-flash-lite
```

예: `-m gemini-2.5-pro` 지정 시 → `gemini-2.5-pro` → `gemini-2.5-flash` → `gemini-2.5-flash-lite` 순서로 시도.

### 출력 (stdout JSON)

```json
{
  "success": true,
  "model": "gemini-3.1-pro-preview",
  "fallback": false,
  "session_id": "...",
  "resume_failed": false,
  "web_searched": true,
  "search_count": 2,
  "stats": { "models": {...}, "tools": {...}, "files": {...} },
  "response": "Gemini 응답 텍스트"
}
```

| 필드 | 타입 | 설명 |
|------|------|------|
| `success` | bool | 호출 성공 여부 |
| `model` | string/null | 실제 사용된 모델명 |
| `fallback` | bool | 선택 모델이 아닌 하위 모델로 대체되었는지 여부 |
| `session_id` | string | 세션 ID (--resume에 사용) |
| `resume_failed` | bool | 세션 복구 실패 → 새 세션으로 재시도 여부 |
| `web_searched` | bool | Gemini가 google_web_search를 사용했는지 여부 |
| `search_count` | int | 웹 검색 호출 횟수 |
| `stats` | object | Gemini CLI 원본 통계 (모델별 토큰, 도구 호출, 파일 변경) |
| `response` | string | Gemini 응답 본문 (성공 시) |
| `error` | string | 에러 메시지 (실패 시) |

### stdin 구조

스크립트는 다음 구조로 stdin을 자동 구성합니다:

```
# 지시사항

{-p 인자의 상세 지시사항}

---

# 입력 자료

{INPUT_FILE의 내용}
```

resume 실패 시 context 파일 포함:

```
# 지시사항

{-p 인자의 상세 지시사항}

---

# 이전 맥락

## context_file_1.md
{내용}

## context_file_2.md
{내용}

---

# 후속 질문

{INPUT_FILE의 내용}
```

### 자동 처리 항목

- **모델 Fallback**: 선택 모델부터 하위 모델로 5단계 자동 전환 (3.1-pro → 3-flash → 2.5-pro → 2.5-flash → 2.5-flash-lite)
- **고정 프롬프트**: gemini CLI의 `-p` 옵션에는 항상 고정 프롬프트 적용 (`"입력된 자료에 대한 답변요청. 필요한 경우 웹 검색을 통해 최신 정보를 조사하여 활용하고, 출처를 함께 제시. ultrathink"`)
- **stdin 구조화**: `-p` 인자의 상세 지시사항과 INPUT_FILE을 구조화하여 stdin에 결합
- **JSON 파싱**: `-o json` 자동 적용, `response` 필드 자동 추출
- **에러 감지**: exit code, JSON 파싱 실패, 빈 응답, 타임아웃 자동 판단
- **세션 관리**: `--resume` 시 session_id 또는 `latest` 지정 가능
- **세션 복구**: `--resume` 실패 시 `--context` 파일을 stdin에 합쳐 새 세션으로 자동 재시도

### Claude의 후처리

스크립트 실행 후:

1. `success` 확인 — `false`이면 Claude 단독 수행
2. `fallback` 확인 — `true`이면 사용자에게 모델 변경 알림
3. `resume_failed` 확인 — `true`이면 세션 복구가 발생했음을 사용자에게 알림
4. `web_searched` 확인 — `false`이면 웹 검색 없이 응답한 것이므로 `collab_summary.md`에 기록
5. `response` 또는 `-o`로 저장된 파일 내용을 분석
