# Claude Code 고급 기능 조사 보고서

## 1. CLAUDE.md 시스템

### 위치 계층
| 범위 | 위치 | 공유 |
|------|------|------|
| 조직 정책 | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) | 모든 사용자 |
| 프로젝트 | `./CLAUDE.md` 또는 `./.claude/CLAUDE.md` | 소스 컨트롤 |
| 사용자 | `~/.claude/CLAUDE.md` | 개인 전체 |

### 작성 원칙
- 200줄 이하 권장
- 구체적 지시 (추상적 X)
- `@파일경로`로 외부 파일 임포트 (최대 5단계 깊이)

### `.claude/rules/` 경로별 규칙
```yaml
---
paths:
  - "src/api/**/*.ts"
---
# 이 경로에서만 적용되는 규칙
```

### Auto Memory 시스템
- 저장 위치: `~/.claude/projects/<project>/memory/`
- MEMORY.md (처음 200줄 매 세션 로드)
- 주제별 자동 분산 저장

---

## 2. MCP 서버 연동

### MCP란
외부 도구/서비스를 AI 모델에 연결하는 오픈 소스 표준 (Model Context Protocol)

### 설치 방법

#### HTTP 원격 서버 (권장)
```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

#### SSE 원격 서버
```bash
claude mcp add --transport sse asana https://mcp.asana.com/sse
```

#### 로컬 Stdio 서버
```bash
claude mcp add --transport stdio airtable -- npx -y airtable-mcp-server
```

### 설치 범위
| 범위 | 저장 위치 | 용도 |
|------|---------|------|
| Local (기본) | `~/.claude.json` | 개인/현재 프로젝트 |
| Project | `.mcp.json` | 팀 공유 |
| User | `~/.claude.json` | 모든 프로젝트 |

### `.mcp.json` 구조
```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": { "Authorization": "Bearer ${GITHUB_TOKEN}" }
    }
  }
}
```

### 환경 변수 확장
- `${VAR}` → 환경변수 값
- `${VAR:-default}` → 기본값 지원

### OAuth 인증
- 동적 클라이언트 등록 (브라우저 흐름)
- 사전 구성된 client-id/secret

### Tool Search
- MCP 도구가 컨텍스트 10% 이상 차지 시 자동 활성화
- `ENABLE_TOOL_SEARCH` 환경변수로 제어

---

## 3. 훅(Hooks) 시스템

### 훅 이벤트
| 이벤트 | 시점 | 용도 |
|-------|------|------|
| SessionStart | 세션 시작 | 환경 설정, 초기화 |
| UserPromptSubmit | 프롬프트 제출 | 입력 검증 |
| PreToolUse | 도구 실행 전 | 명령 차단, 권한 확인 |
| PostToolUse | 도구 실행 후 | 포맷팅, 로깅 |
| PostToolUseFailure | 도구 실패 | 에러 처리 |
| PermissionRequest | 권한 요청 | 자동 승인/거부 |
| Notification | 알림 발생 | 데스크톱 알림 |
| SubagentStart/Stop | 서브에이전트 시작/종료 | 리소스 관리 |
| Stop | 응답 완료 | 최종 검증 |
| ConfigChange | 설정 변경 | 감시 |
| PreCompact | 압축 전 | 컨텍스트 재주입 |
| SessionEnd | 세션 종료 | 정리 |

### 설정 위치
- `~/.claude/settings.json` (사용자)
- `.claude/settings.json` (프로젝트 공유)
- `.claude/settings.local.json` (프로젝트 개인)

### 매처 (정규식)
```json
{ "matcher": "Edit|Write", "hooks": [...] }
{ "matcher": "Bash", "hooks": [...] }
{ "matcher": "mcp__github__.*", "hooks": [...] }
```

### 훅 타입
1. **command**: 셸 명령 실행
2. **prompt**: AI 의사결정 (JSON 반환)
3. **agent**: 에이전트가 파일 접근하며 검증
4. **http**: 원격 서버로 전송

### 입출력
- 입력: stdin으로 JSON (session_id, tool_name, tool_input 등)
- 출력: exit 0 = 계속, exit 2 = 차단

### 실전 예시
1. 파일 편집 후 자동 포맷팅 (Prettier)
2. 보호 파일 수정 방지 (.env 등)
3. macOS/Linux 데스크톱 알림
4. Bash 명령 로깅
5. 압축 후 컨텍스트 재주입

---

## 4. 에이전트 시스템

### 내장 에이전트
| 에이전트 | 모델 | 도구 | 용도 |
|---------|------|------|------|
| Explore | Haiku | Read-only | 빠른 코드 탐색 |
| Plan | 상속 | Read-only | 계획 수립 |
| general-purpose | 상속 | 모두 | 복잡한 작업 |

### 에이전트 정의 파일
`.claude/agents/code-reviewer.md`:
```yaml
---
name: code-reviewer
description: 코드 리뷰 전문가
tools: Read, Grep, Glob, Bash
model: sonnet
permissionMode: acceptEdits
maxTurns: 20
memory: user
isolation: worktree
---
시스템 프롬프트 내용...
```

### 설정 옵션
- name, description, tools, disallowedTools
- model (sonnet/opus/haiku/inherit)
- permissionMode (default/acceptEdits/plan/dontAsk/bypassPermissions)
- maxTurns, memory (user/project/local)
- background, isolation (worktree)
- mcpServers, hooks

### 에이전트 범위 (우선순위)
1. CLI `--agents` (최고)
2. `.claude/agents/` (프로젝트)
3. `~/.claude/agents/` (사용자)
4. 플러그인 (최저)

---

## 5. 스킬 시스템

### 에이전트 vs 스킬
| | 에이전트 | 스킬 |
|--|---------|------|
| 실행 | 독립 컨텍스트 | 메인 대화 내 |
| 호출 | 자동/명시적 | `/skill-name` 또는 자동 |
| 컨텍스트 | 격리 | 공유 |
| 토큰 비용 | 높음 | 낮음 |

### 스킬 정의
`.claude/skills/deploy/SKILL.md`:
```yaml
---
name: deploy
description: 배포 실행
disable-model-invocation: true
argument-hint: [environment]
allowed-tools: Read, Bash
model: sonnet
context: fork
agent: Explore
---
워크플로우 내용...
```

### 동적 컨텍스트 주입
```yaml
PR diff: !`gh pr diff`
```

---

## 6. IDE 통합

### VS Code
- 마켓플레이스에서 "Claude Code" 설치
- Spark 아이콘 또는 `Cmd+Shift+P` > "Claude Code: Open"
- @파일참조, 권한 모드, 슬래시 커맨드 지원

### JetBrains (IntelliJ, PyCharm, WebStorm 등)
- 마켓플레이스에서 "Claude Code" 설치
- `Cmd+Esc` (Mac) / `Ctrl+Esc` (Win/Linux)
- 통합 diff 뷰어, 파일 참조

### 설정 계층 (우선순위)
1. CLI 플래그
2. `.claude/settings.local.json`
3. `.claude/settings.json`
4. `~/.claude/settings.json`
5. 조직 정책 (managed-settings.json)
