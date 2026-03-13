# Claude Code 핵심 기능 및 도구 조사 보고서

## 1. 내장 도구(Built-in Tools) 전체 목록

### 1.1 파일 작업 도구

#### Read Tool
- 파일 내용 읽기 (바이너리, 이미지, PDF 포함)
- 라인 범위 지정 가능 (offset, limit)
- 2000줄까지 기본 읽기

#### Write Tool
- 새 파일 생성 또는 전체 재작성
- 체크포인트 자동 생성 (원본 백업)

#### Edit Tool
- 파일 일부분만 수정 (exact string replacement)
- Write보다 컨텍스트 효율적
- replace_all 옵션으로 전체 치환

### 1.2 검색 도구

#### Glob Tool
- 파일 패턴 매칭 (`**/*.ts`, `src/**/*.tsx`)
- 수정 시간순 정렬
- 디렉토리 탐색

#### Grep Tool
- ripgrep 기반 정규식 검색
- 출력 모드: content, files_with_matches, count
- 멀티라인 매칭 지원
- 파일 타입/glob 필터링

### 1.3 실행 도구

#### Bash Tool
- 셸 명령 실행
- 배경 실행 (run_in_background)
- 타임아웃 설정 (최대 10분)
- 작업 디렉토리 유지

### 1.4 웹 접근 도구

#### WebFetch
- URL에서 콘텐츠 가져오기
- HTML → Markdown 변환

#### WebSearch
- 웹 검색 수행
- 최신 정보 접근

### 1.5 에이전트/태스크 도구

#### Agent Tool
- 서브에이전트 스폰 (general-purpose, Explore, Plan)
- 커스텀 에이전트 정의 호출
- 격리된 컨텍스트, 병렬 실행
- worktree 격리 옵션

#### TaskCreate / TaskUpdate / TaskList / TaskGet
- 작업 항목 생성/추적
- 상태 관리: pending → in_progress → completed
- 의존성 관리 (blockedBy, blocks)

#### AskUserQuestion
- 사용자에게 질문/입력 요청

#### NotebookEdit
- Jupyter 노트북 편집

### 1.6 코드 인텔리전스
- 타입 에러/경고 시각화
- 정의로 이동, 참조 찾기

---

## 2. 슬래시 커맨드

### 2.1 빌트인 커맨드

#### 컨텍스트/메모리
| 커맨드 | 기능 |
|--------|------|
| `/context` | 컨텍스트 사용량 확인 |
| `/compact` | 대화 요약으로 컨텍스트 압축 |
| `/memory` | CLAUDE.md 및 자동 메모리 보기/편집 |
| `/rewind` | 이전 체크포인트로 되돌리기 |

#### 세션/워크플로우
| 커맨드 | 기능 |
|--------|------|
| `/help` | 도움말 |
| `/clear` | 세션 초기화 |
| `/cost` | 토큰 사용량/비용 |
| `/doctor` | 설치/구성 진단 |
| `/debug` | 디버그 로그 |

#### 에이전트/자동화
| 커맨드 | 기능 |
|--------|------|
| `/agents` | 서브에이전트 관리 |
| `/hooks` | 훅 구성 |
| `/loop` | 프롬프트 주기적 실행 |

#### 커스터마이제이션
| 커맨드 | 기능 |
|--------|------|
| `/config` | 설정 변경 |
| `/theme` | 테마 선택 |
| `/model` | 모델 변경 |
| `/vim` | Vim 모드 전환 |
| `/init` | CLAUDE.md 생성 마법사 |
| `/terminal-setup` | 터미널 설정 |
| `/mcp` | MCP 서버 관리 |

### 2.2 커스텀 슬래시 커맨드

#### 스킬 방식 (권장)
`~/.claude/skills/deploy/SKILL.md` 또는 `.claude/skills/deploy/SKILL.md`

```yaml
---
name: deploy
description: Deploy the application
---
Deploy steps here...
```

#### 커맨드 방식 (레거시)
`.claude/commands/review.md`

#### 동적 컨텍스트 주입
`!` backtick으로 명령 선행 실행:
```yaml
PR diff: !`gh pr diff`
```

#### 인자 처리
`$ARGUMENTS`, `$0`, `$1` 등으로 인자 접근

---

## 3. 컨텍스트 관리

### 3.1 컨텍스트 윈도우 구조
1. 시스템 프롬프트 (고정)
2. CLAUDE.md + 자동 메모리 (매 요청)
3. 스킬 설명 + MCP 도구 (매 요청)
4. 대화 이력 (동적, 오래된 것부터 제거)
5. 파일 컨텍스트 (도구 사용 결과)

### 3.2 자동 압축
- 95% 도달 시 자동 실행 (CLAUDE_AUTOCOMPACT_PCT_OVERRIDE로 조정)
- 오래된 도구 출력 먼저 제거
- 핵심 정보 보존

### 3.3 `/compact` 사용법
```
/compact                              # 전체 요약
/compact focus on API changes         # 특정 주제 집중
```

### 3.4 `/context` 확인
토큰 분포 확인: 시스템, CLAUDE.md, 스킬, MCP, 대화

### 3.5 최적화 전략
1. CLAUDE.md 200줄 이하 유지
2. 미사용 스킬에 `disable-model-invocation: true`
3. 미사용 MCP 서버 disconnect
4. Subagent로 대용량 출력 격리
5. `/clear`로 새 세션 시작
