# 챕터 15: 훅과 에이전트

> **학습 목표**
> - 훅 시스템의 이벤트 기반 구조를 이해한다
> - 실전 훅을 직접 설정할 수 있다
> - 내장 에이전트 3종의 역할을 구분한다
> - 커스텀 에이전트를 만들 수 있다
> - Worktree로 병렬 작업을 수행한다

---

## 15.1 훅 시스템 개요

Claude Code는 이벤트 기반 훅을 지원합니다. 특정 시점에 여러분의 스크립트가 자동 실행됩니다. 파일 저장 후 포맷팅, 위험한 명령 차단, 알림 전송 등을 자동화할 수 있습니다.

### 훅이란

훅은 "갈고리"입니다. Claude Code의 동작 흐름에 여러분의 코드를 걸어 놓는 것입니다. 도구가 실행되기 직전, 직후 등 정확한 시점에 개입합니다.

### 주요 이벤트 표

| 이벤트 | 시점 | 대표 용도 |
|--------|------|-----------|
| **SessionStart** | 세션 시작 | 환경 초기화 |
| **UserPromptSubmit** | 프롬프트 제출 | 입력 검증 |
| **PreToolUse** | 도구 실행 전 | 명령 차단, 권한 확인 |
| **PostToolUse** | 도구 실행 후 | 자동 포맷팅, 로깅 |
| **PostToolUseFailure** | 도구 실패 시 | 에러 처리 |
| **Notification** | 알림 발생 | 데스크톱 알림 |
| **SubagentStart** | 서브에이전트 시작 | 리소스 관리 |
| **SubagentStop** | 서브에이전트 종료 | 정리 작업 |
| **PreCompact** | 컨텍스트 압축 전 | 컨텍스트 재주입 |
| **Stop** | 응답 완료 | 최종 검증 |
| **SessionEnd** | 세션 종료 | 정리 |

### 훅의 동작 원리

훅은 stdin으로 JSON을 받습니다. `session_id`, `tool_name`, `tool_input` 등이 포함됩니다. 종료 코드로 결과를 전달합니다.

- **exit 0**: 정상 통과, 계속 진행합니다
- **exit 2**: 차단, 해당 동작을 중단합니다

> **팁**: 훅은 4가지 타입을 지원합니다. `command`(셸 명령), `prompt`(AI 판단), `agent`(에이전트 검증), `http`(원격 전송). 가장 많이 쓰는 것은 `command`입니다.

---

## 15.2 실전 훅 설정

훅은 settings.json에 정의합니다. 설정 위치에 따라 적용 범위가 달라집니다.

| 설정 파일 | 범위 |
|-----------|------|
| `~/.claude/settings.json` | 모든 프로젝트 |
| `.claude/settings.json` | 현재 프로젝트 (팀 공유) |
| `.claude/settings.local.json` | 현재 프로젝트 (개인) |

### 예제 1: 파일 편집 후 자동 포맷팅

Prettier로 저장 직후 코드를 정리합니다. `PostToolUse` 이벤트에 `Edit|Write` 매처를 걸어줍니다.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write \"$TOOL_INPUT_FILE_PATH\""
          }
        ]
      }
    ]
  }
}
```

파일이 편집될 때마다 Prettier가 실행됩니다. 여러분이 직접 실행할 필요가 없습니다.

### 예제 2: 보호 파일 수정 차단

`.env`, `credentials.json` 같은 민감 파일을 보호합니다. `PreToolUse`에서 차단합니다.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$TOOL_INPUT_FILE_PATH\" | grep -qE '(\\.env|credentials)' && exit 2 || exit 0"
          }
        ]
      }
    ]
  }
}
```

> **주의**: exit 2는 "차단"을 의미합니다. 보호 파일 경로가 매칭되면 Claude Code가 해당 편집을 중단합니다. 실수로 민감 정보가 노출되는 것을 방지합니다.

### 예제 3: 데스크톱 알림

긴 작업이 끝났을 때 알림을 받습니다. `Notification` 이벤트를 활용합니다.

```bash
# macOS
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude Code 작업 완료\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

> **팁**: Linux에서는 `notify-send "Claude Code 작업 완료"`를 사용하세요. OS별로 명령이 다르므로 `.claude/settings.local.json`에 개인 설정으로 저장하는 것을 권장합니다.

---

## 15.3 에이전트 이해하기

Claude Code에는 3가지 내장 에이전트가 있습니다. 각각 역할과 권한이 다릅니다.

### 내장 에이전트 비교

| 에이전트 | 모델 | 사용 가능 도구 | 주요 역할 |
|---------|------|--------------|-----------|
| **Explore** | Haiku | 읽기 전용 | 빠른 코드 탐색, 구조 파악 |
| **Plan** | 상속 | 읽기 전용 | 작업 계획 수립, 분석 |
| **general-purpose** | 상속 | 모든 도구 | 복잡한 서브태스크 처리 |

**Explore**는 가벼운 모델을 씁니다. 코드베이스를 빠르게 탐색할 때 적합합니다. 비용이 낮고 속도가 빠릅니다.

**Plan**은 현재 세션의 모델을 상속합니다. 코드를 읽고 분석하지만, 수정은 하지 않습니다. 계획을 세울 때 안전합니다.

**general-purpose**는 모든 도구에 접근합니다. 메인 에이전트가 복잡한 작업을 위임할 때 사용합니다. 파일 편집, 명령 실행이 모두 가능합니다.

> **팁**: Claude Code는 작업의 복잡도에 따라 자동으로 적절한 에이전트를 선택합니다. 여러분이 명시적으로 지정할 수도 있습니다.

---

## 15.4 커스텀 에이전트 만들기

내장 에이전트로 부족할 때, 직접 만들 수 있습니다. `.claude/agents/` 디렉터리에 마크다운 파일을 생성합니다.

### 에이전트 정의 파일 구조

```markdown
---
name: my-agent
description: 에이전트에 대한 간단한 설명
tools: Read, Grep, Glob, Bash
model: sonnet
permissionMode: acceptEdits
maxTurns: 20
memory: user
---

여기에 시스템 프롬프트를 작성합니다.
에이전트의 행동 규칙을 정의합니다.
```

### frontmatter 주요 옵션

| 옵션 | 설명 | 예시 |
|------|------|------|
| **name** | 에이전트 이름 | `code-reviewer` |
| **description** | 간단한 설명 | `코드 리뷰 전문가` |
| **tools** | 허용할 도구 목록 | `Read, Grep, Glob` |
| **disallowedTools** | 차단할 도구 목록 | `Bash, Write` |
| **model** | 사용 모델 | `sonnet`, `opus`, `haiku` |
| **permissionMode** | 권한 모드 | `default`, `acceptEdits`, `plan` |
| **maxTurns** | 최대 실행 턴 수 | `20` |
| **memory** | 메모리 범위 | `user`, `project`, `local` |
| **isolation** | 격리 방식 | `worktree` |

### 에이전트 검색 우선순위

1. CLI `--agents` 플래그 (최고)
2. `.claude/agents/` (프로젝트)
3. `~/.claude/agents/` (사용자 전역)
4. 플러그인 (최저)

> **주의**: `permissionMode: bypassPermissions`는 격리된 환경에서만 사용하세요. 로컬 머신에서는 `acceptEdits` 이하를 권장합니다.

---

## 15.5 Worktree로 병렬 작업

Git Worktree를 활용하면 여러 작업을 동시에 진행할 수 있습니다. 메인 브랜치를 건드리지 않고 독립된 작업 공간을 만듭니다.

### --worktree 플래그

```bash
# 새 워크트리에서 에이전트 실행
claude --worktree "버그 수정해줘"
```

별도의 디렉터리에 소스를 체크아웃합니다. 원본과 완전히 격리됩니다. 작업이 끝나면 결과를 머지합니다.

### 에이전트에서 isolation 설정

커스텀 에이전트 정의에서 `isolation: worktree`를 지정할 수 있습니다.

```yaml
---
name: feature-builder
description: 기능 개발 전문 에이전트
tools: Read, Write, Edit, Bash, Glob, Grep
model: sonnet
permissionMode: acceptEdits
isolation: worktree
---

새 기능을 독립된 워크트리에서 개발합니다.
메인 브랜치에 영향을 주지 않습니다.
```

이렇게 하면 에이전트가 실행될 때마다 자동으로 워크트리가 생성됩니다. 병렬로 여러 에이전트를 돌릴 수 있습니다.

> **팁**: 워크트리는 Git 저장소에서만 작동합니다. 프로젝트가 Git으로 관리되지 않으면 `isolation` 옵션을 사용할 수 없습니다.

---

## 15.6 실습: 코드 리뷰 에이전트 만들기

지금까지 배운 내용을 종합합니다. 코드 리뷰 전문 에이전트를 직접 만들어 봅시다.

### 1단계: 에이전트 정의 파일 생성

`.claude/agents/code-reviewer.md` 파일을 만듭니다.

```markdown
---
name: code-reviewer
description: PR 코드 리뷰 전문 에이전트
tools: Read, Grep, Glob, Bash
model: sonnet
permissionMode: plan
maxTurns: 30
---

당신은 시니어 개발자입니다.
코드 리뷰를 수행합니다.

## 리뷰 절차

1. 변경된 파일 목록을 확인합니다
2. 각 파일의 diff를 분석합니다
3. 다음 관점에서 검토합니다:
   - 버그 가능성
   - 보안 취약점
   - 성능 문제
   - 코드 스타일 일관성
   - 테스트 누락

## 출력 형식

각 이슈를 다음 형식으로 보고합니다:
- **파일**: 경로
- **라인**: 번호
- **심각도**: 높음/중간/낮음
- **설명**: 문제와 개선 제안
```

### 2단계: 리뷰 훅 추가 (선택)

리뷰 결과를 자동으로 기록하는 훅을 추가합니다. `.claude/settings.json`에 다음을 추가합니다.

```json
{
  "hooks": {
    "SubagentStop": [
      {
        "matcher": "code-reviewer",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"[$(date)] 코드 리뷰 완료\" >> .claude/review-log.txt"
          }
        ]
      }
    ]
  }
}
```

### 3단계: 에이전트 실행

슬래시 커맨드로 에이전트를 호출합니다.

```bash
# Claude Code 세션에서
/code-reviewer 최근 PR의 변경 사항을 리뷰해줘
```

또는 CLI에서 직접 실행할 수 있습니다.

```bash
claude --agent code-reviewer "main 브랜치 대비 변경 사항을 리뷰해줘"
```

### 실행 결과 예시

에이전트가 코드베이스를 탐색하고, diff를 분석한 뒤 다음과 같은 리뷰를 생성합니다.

```
## 코드 리뷰 결과

### 이슈 1
- **파일**: src/api/auth.ts
- **라인**: 42
- **심각도**: 높음
- **설명**: JWT 토큰 검증 없이 사용자 정보를
  신뢰합니다. `verifyToken()` 호출을 추가하세요.

### 이슈 2
- **파일**: src/utils/format.ts
- **라인**: 15
- **심각도**: 낮음
- **설명**: 미사용 import가 있습니다. 정리하세요.
```

> **팁**: `permissionMode: plan`으로 설정했기 때문에 리뷰 에이전트는 코드를 읽기만 합니다. 실수로 파일을 수정할 걱정이 없습니다. 안전한 리뷰가 가능합니다.

---

## 정리

이번 챕터에서 다룬 핵심 내용입니다.

| 개념 | 핵심 포인트 |
|------|------------|
| 훅 시스템 | 이벤트 기반 자동 실행, exit 코드로 제어 |
| 매처 | 정규식으로 특정 도구만 필터링 |
| 내장 에이전트 | Explore(탐색), Plan(계획), general-purpose(범용) |
| 커스텀 에이전트 | `.claude/agents/`에 마크다운으로 정의 |
| Worktree | `--worktree` 또는 `isolation: worktree`로 격리 |

> **다음 챕터 미리보기**: 챕터 16에서는 CI/CD 파이프라인에서 Claude Code를 활용하는 방법을 다룹니다. GitHub Actions, 자동 PR 리뷰 등 팀 워크플로우를 자동화합니다.
