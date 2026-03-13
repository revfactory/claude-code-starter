---
name: book-writing
description: "Claude Code 입문서 집필 오케스트레이터. '책 쓰기', '도서 집필', '챕터 작성', '원고 작업' 요청 시 트리거. 5명의 전문 에이전트를 조율하여 체계적으로 도서를 집필한다."
---

# Claude Code 입문서 집필 오케스트레이터

Claude Code를 처음 시작하는 사람들을 위한 도서를 체계적으로 집필하는 오케스트레이터 스킬.

## 에이전트 구성

| 에이전트 | 파일 | 역할 | Phase |
|---------|------|------|-------|
| book-researcher | `.claude/agents/book-researcher.md` | Claude Code 기능/생태계 조사 | 1 |
| book-architect | `.claude/agents/book-architect.md` | 도서 구조/목차 설계 | 2 |
| chapter-writer | `.claude/agents/chapter-writer.md` | 챕터 본문 집필 | 3 |
| code-example-creator | `.claude/agents/code-example-creator.md` | 실습 예제 코드 작성 | 3 |
| book-editor | `.claude/agents/book-editor.md` | 교정/교열/일관성 검토 | 4 |

## 레퍼런스

- `references/claude-code-topics.md` — 도서 주제 영역 및 독자 페르소나
- `references/style-guide.md` — 문체, 용어, 포맷 규칙

## 워크플로우

### Phase 1: 리서치 (순차)

book-researcher 에이전트를 실행하여 Claude Code 전반을 조사한다.

**실행:**
```
Agent(book-researcher): 다음 주제를 조사하세요:
1. Claude Code의 핵심 기능 전체 목록과 각 기능 설명
2. 설치/설정 방법 (OS별)
3. 초보자가 자주 겪는 문제와 FAQ
4. CLAUDE.md, 훅, MCP 서버, 슬래시 커맨드 등 고급 기능
5. 실제 사용 워크플로우 (Git, TDD, 디버깅 등)
references/claude-code-topics.md를 참고하여 누락 없이 조사하세요.
결과는 _workspace/01_research_*.md에 저장하세요.
```

**산출물:** `_workspace/01_research_*.md` (주제별 조사 보고서)

### Phase 2: 구조 설계 (순차)

book-architect 에이전트로 도서 구조를 설계한다.

**실행:**
```
Agent(book-architect): _workspace/01_research_*.md 조사 결과를 바탕으로:
1. 전체 목차를 설계하세요 (15~20챕터)
2. 각 챕터의 명세를 작성하세요 (목표, 범위, 핵심 내용, 예상 분량)
3. 챕터 간 의존성 맵을 만드세요
4. 각 챕터에 필요한 코드 예제 목록을 정리하세요
references/claude-code-topics.md와 references/style-guide.md를 참고하세요.
결과는 _workspace/02_architect_outline.md와 _workspace/02_architect_dependency.md에 저장하세요.
```

**산출물:**
- `_workspace/02_architect_outline.md` — 전체 목차 및 챕터 명세
- `_workspace/02_architect_dependency.md` — 챕터 의존성 맵

**체크포인트:** 사용자에게 목차를 보여주고 승인을 받는다. 수정 요청이 있으면 반영 후 다음 Phase로.

### Phase 3: 집필 + 예제 작성 (병렬)

chapter-writer와 code-example-creator를 **병렬로** 실행한다.
의존성이 없는 챕터들은 동시에 집필할 수 있다.

**실행 (병렬):**
```
# 챕터 집필 — chapter-writer 에이전트
Agent(chapter-writer): _workspace/02_architect_outline.md의 챕터 {N} 명세에 따라 본문을 집필하세요.
- _workspace/01_research_*.md에서 관련 자료를 참고하세요
- references/style-guide.md의 문체와 포맷 규칙을 준수하세요
- 결과는 _workspace/03_chapter_{NN}_{title}.md에 저장하세요

# 예제 작성 — code-example-creator 에이전트
Agent(code-example-creator): _workspace/02_architect_outline.md의 챕터 {N} 예제 요구사항에 따라 코드 예제를 작성하세요.
- 모든 예제는 실행 가능해야 합니다
- CLI 대화 예시 포맷을 포함하세요
- 결과는 _workspace/03_example_{NN}_{topic}.md에 저장하세요
```

**병렬 실행 전략:**
- 의존성 없는 챕터 2~3개를 동시에 진행
- 예제 작성은 챕터 집필과 동시에 진행
- 의존성 맵(`02_architect_dependency.md`)을 참조하여 순서 결정

**산출물:**
- `_workspace/03_chapter_{NN}_{title}.md` — 챕터 원고
- `_workspace/03_example_{NN}_{topic}.md` — 코드 예제

### Phase 4: 편집 검토 (순차)

book-editor 에이전트로 원고를 검토한다.

**실행:**
```
Agent(book-editor): _workspace/03_chapter_{NN}_{title}.md 원고를 검토하세요.
- references/style-guide.md의 기준에 따라 검토
- 용어 통일, 문체 일관성, 기술 정확성 확인
- 검토 결과는 _workspace/04_review_{NN}_{title}.md에 저장
- 편집된 원고는 _workspace/04_edited_{NN}_{title}.md에 저장
- 판정: PASS / MINOR / MAJOR / REWRITE
```

**판정별 후속 조치:**
- **PASS/MINOR**: Phase 5로 진행
- **MAJOR**: chapter-writer에게 수정 요청 후 재검토 (최대 1회)
- **REWRITE**: 사용자에게 보고 후 지시 대기

**산출물:**
- `_workspace/04_review_{NN}_{title}.md` — 검토 보고서
- `_workspace/04_edited_{NN}_{title}.md` — 편집 완료 원고

### Phase 5: 최종 조립 (순차)

편집 완료된 원고를 통합한다.

**실행:**
1. 모든 `_workspace/04_edited_*.md` 파일을 목차 순서대로 통합
2. 상호 참조(챕터 간 링크) 유효성 확인
3. 최종 원고를 `book/` 디렉토리에 챕터별 파일로 저장
4. `book/00_목차.md` 생성 (전체 목차 + 각 챕터 링크)

**산출물:**
- `book/00_목차.md` — 전체 목차
- `book/01_챕터제목.md` ~ `book/NN_챕터제목.md` — 최종 챕터 파일

### Phase 6: 정리

중간 산출물을 정리한다.

**실행:**
1. 사용자에게 `_workspace/` 삭제 여부 확인
2. 승인 시 `_workspace/` 디렉토리 삭제
3. 최종 요약 보고서 출력

## 데이터 전달 프로토콜

**파일 기반 전달** 사용 (대용량 원고 데이터에 적합):

| Phase | 생성 에이전트 | 파일 패턴 | 소비 에이전트 |
|-------|-------------|----------|-------------|
| 1 | book-researcher | `01_research_*.md` | book-architect |
| 2 | book-architect | `02_architect_*.md` | chapter-writer, code-example-creator |
| 3 | chapter-writer | `03_chapter_*.md` | book-editor |
| 3 | code-example-creator | `03_example_*.md` | chapter-writer, book-editor |
| 4 | book-editor | `04_edited_*.md` | 최종 조립 |

모든 중간 파일은 `_workspace/` 하위에 저장.

## 에러 핸들링

| 에러 유형 | 전략 | 구현 |
|----------|------|------|
| 에이전트 실패 | 재시도 1회 → 부분 진행 | 실패한 챕터만 스킵, 나머지 진행. 보고서에 누락 명시 |
| 편집 검토 REWRITE | 사용자 판단 | 자동 재집필하지 않고 사용자에게 보고 |
| 리서치 부족 | 추가 조사 | 부족한 주제만 추가 리서치 실행 |
| 예제 실행 불가 | 검증 후 수정 | code-example-creator에게 재작성 요청 (1회) |
| 분량 초과 | 챕터 분리 | book-architect에게 챕터 분리안 요청 |

## 사용법

### 전체 도서 집필
```
/book-writing
```
→ Phase 1부터 6까지 순차 실행

### 특정 챕터만 집필
```
사용자: 3장만 다시 써줘
```
→ Phase 3(해당 챕터) → Phase 4(해당 챕터) → Phase 5(재조립) 실행

### 목차만 설계
```
사용자: 목차만 먼저 잡아줘
```
→ Phase 1 → Phase 2만 실행, 체크포인트에서 멈춤

### 편집만 요청
```
사용자: 기존 원고 검토해줘
```
→ Phase 4만 실행 (기존 `_workspace/03_chapter_*.md` 대상)

## 테스트 시나리오

### 정상 흐름: 3챕터 미니북 집필
1. Phase 1: Claude Code 기초 3개 주제 리서치 → `01_research_*.md` 3개 생성 확인
2. Phase 2: 3챕터 목차 설계 → `02_architect_outline.md` 생성, 사용자 승인
3. Phase 3: 3챕터 병렬 집필 + 예제 작성 → `03_chapter_*.md` 3개 + `03_example_*.md` 3개
4. Phase 4: 3챕터 편집 검토 → 전부 PASS/MINOR 판정
5. Phase 5: `book/` 디렉토리에 4개 파일 (목차 + 3챕터)
6. Phase 6: `_workspace/` 정리

### 에러 흐름: 편집 검토에서 MAJOR 판정
1. Phase 1~3: 정상 완료
2. Phase 4: 2장이 MAJOR 판정
3. chapter-writer에게 2장 수정 요청 (피드백 포함)
4. 수정된 2장 재검토 → PASS
5. Phase 5~6: 정상 완료
