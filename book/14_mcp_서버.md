# 챕터 14: MCP 서버 연동

> **학습 목표**
> - MCP가 무엇인지 이해한다
> - 세 가지 전송 방식으로 서버를 추가할 수 있다
> - `.mcp.json` 설정 파일을 직접 작성할 수 있다
> - 범위(Scope)를 구분하여 팀과 공유할 수 있다
> - GitHub MCP 서버를 실습으로 연동할 수 있다
> - MCP 서버를 관리하고 디버깅할 수 있다

---

여러분, Claude Code는 강력합니다.
하지만 혼자서 모든 일을 할 수는 없습니다.
GitHub 이슈를 조회하고 싶다면?
Slack에 메시지를 보내고 싶다면?
데이터베이스를 직접 쿼리하고 싶다면?

이때 필요한 것이 바로 **MCP 서버**입니다.
이번 챕터에서는 외부 도구(Tool)를
Claude Code에 연결하는 방법을 배웁니다.

---

## 14.1 MCP 이해하기

MCP는 **Model Context Protocol**의 약자입니다.
외부 도구를 AI에 연결하는 오픈 소스 표준입니다.

쉽게 비유하면 USB 포트와 같습니다.
USB가 키보드, 마우스, 저장장치를 연결하듯,
MCP는 GitHub, Slack, DB 등을 연결합니다.

MCP의 핵심 구조는 간단합니다.

```text
Claude Code (클라이언트)
    ↕  MCP 프로토콜
MCP 서버 (GitHub, Slack, DB 등)
    ↕  API 호출
외부 서비스
```

MCP 서버가 하나 연결되면,
그 서버가 제공하는 도구(Tool)를 사용할 수 있습니다.
예를 들어 GitHub MCP 서버는
이슈 생성, PR 조회, 코드 검색 등의 도구를 제공합니다.

> **팁**: MCP는 Anthropic이 주도하는 오픈 표준입니다. 다양한 커뮤니티 서버가 이미 존재합니다. [modelcontextprotocol.io](https://modelcontextprotocol.io)에서 목록을 확인하세요.

---

## 14.2 서버 추가

MCP 서버를 추가하는 명령어는 하나입니다.

```bash
claude mcp add <이름> <서버 주소 또는 명령>
```

전송 방식은 세 가지입니다.

### HTTP 원격 서버 (권장)

가장 간단한 방식입니다.
URL만 지정하면 됩니다.

```bash
claude mcp add \
  --transport http \
  github \
  https://api.githubcopilot.com/mcp/
```

Streamable HTTP 프로토콜을 사용합니다.
대부분의 공식 MCP 서버가 이 방식을 지원합니다.

### SSE 원격 서버

Server-Sent Events 방식입니다.
일부 서비스가 이 방식을 사용합니다.

```bash
claude mcp add \
  --transport sse \
  asana \
  https://mcp.asana.com/sse
```

### Stdio 로컬 서버

로컬에서 프로세스를 실행하는 방식입니다.
`npx`로 패키지를 바로 실행할 수 있습니다.

```bash
claude mcp add \
  --transport stdio \
  airtable \
  -- npx -y airtable-mcp-server
```

`--` 뒤에 실행할 명령을 적습니다.
Claude Code가 이 프로세스를 관리합니다.

> **주의**: Stdio 방식은 로컬에 Node.js가 필요합니다. `npx`가 설치되어 있는지 먼저 확인하세요.

---

## 14.3 설정 파일

CLI 명령 대신 설정 파일로도 구성할 수 있습니다.
프로젝트 루트에 `.mcp.json`을 만듭니다.

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${GITHUB_TOKEN}"
      }
    },
    "airtable": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "airtable-mcp-server"],
      "env": {
        "AIRTABLE_API_KEY": "${AIRTABLE_KEY}"
      }
    }
  }
}
```

### 환경 변수 확장

설정 파일 안에서 환경 변수를 쓸 수 있습니다.
두 가지 문법을 지원합니다.

| 문법 | 의미 |
|------|------|
| `${VAR}` | 환경 변수 값을 그대로 삽입 |
| `${VAR:-default}` | 값이 없으면 기본값 사용 |

예를 들어 다음과 같이 쓸 수 있습니다.

```json
{
  "env": {
    "API_KEY": "${MY_API_KEY}",
    "PORT": "${MCP_PORT:-3000}"
  }
}
```

`MY_API_KEY`가 설정되어 있지 않으면 에러가 납니다.
`MCP_PORT`가 없으면 `3000`이 사용됩니다.

> **팁**: 토큰이나 API 키를 `.mcp.json`에 직접 적지 마세요. 반드시 환경 변수로 참조하세요. `.mcp.json`은 소스 컨트롤에 커밋됩니다.

---

## 14.4 범위와 공유

MCP 서버 설정에는 세 가지 범위가 있습니다.

| 범위 | 저장 위치 | 용도 |
|------|----------|------|
| **Local** (기본) | `~/.claude.json` | 개인, 현재 프로젝트 |
| **Project** | `.mcp.json` | 팀 전체 공유 |
| **User** | `~/.claude.json` | 모든 프로젝트에서 사용 |

### --scope 옵션

`claude mcp add` 명령에 `--scope`를 붙입니다.

```bash
# 팀 공유: .mcp.json에 저장
claude mcp add --scope project \
  --transport http github \
  https://api.githubcopilot.com/mcp/

# 모든 프로젝트: ~/.claude.json에 저장
claude mcp add --scope user \
  --transport http github \
  https://api.githubcopilot.com/mcp/
```

범위를 생략하면 **Local**이 기본값입니다.

언제 어떤 범위를 쓸까요?

- **Local**: 실험적으로 테스트할 때
- **Project**: 팀원 모두가 같은 도구를 쓸 때
- **User**: 개인 도구를 모든 프로젝트에서 쓸 때

> **팁**: 팀 프로젝트라면 Project 범위를 사용하세요. `.mcp.json`을 커밋하면 모든 팀원이 같은 MCP 서버를 자동으로 사용합니다.

---

## 14.5 실습: GitHub MCP 서버 연동

실제로 GitHub MCP 서버를 연동해봅시다.
단계별로 따라해보세요.

### 1단계: 서버 추가

터미널에서 다음 명령을 실행합니다.

```bash
claude mcp add \
  --transport http \
  github \
  https://api.githubcopilot.com/mcp/
```

### 2단계: 인증

명령을 실행하면 브라우저가 열립니다.
GitHub OAuth 인증 화면이 나타납니다.
**Authorize** 버튼을 클릭하세요.

인증이 완료되면 터미널에 성공 메시지가 뜹니다.

### 3단계: 도구 확인

Claude Code를 실행하고 `/mcp`를 입력합니다.

```text
> /mcp

MCP Servers:
  github (http) ✅ Connected
    Tools: 22 available
```

`✅ Connected`가 보이면 성공입니다.

### 4단계: 사용해보기

이제 Claude Code에게 GitHub 작업을 요청합니다.

```text
> 이 저장소의 열린 이슈 목록을 보여줘

Claude가 github MCP 서버의
list_issues 도구를 사용하여 조회합니다.
```

처음 사용할 때 도구 실행 권한을 묻습니다.
**Allow**를 선택하세요.

> **주의**: MCP 도구는 외부 서비스에 접근합니다. 처음 실행할 때 반드시 어떤 동작을 하는지 확인하세요. 신뢰할 수 없는 MCP 서버는 추가하지 마세요.

---

## 14.6 관리와 디버깅

### /mcp 슬래시 커맨드

연결된 MCP 서버 상태를 확인합니다.

```text
> /mcp
```

서버 이름, 전송 방식, 연결 상태, 도구 개수가 표시됩니다.
문제가 있으면 `❌` 표시와 에러 메시지가 나옵니다.

### 서버 비활성화

특정 서버를 끄고 싶을 때 사용합니다.

```bash
# 서버 비활성화
claude mcp disable github

# 다시 활성화
claude mcp enable github

# 완전 삭제
claude mcp remove github
```

비활성화는 설정을 유지한 채 끄는 것입니다.
삭제하면 설정 자체가 사라집니다.

### Tool Search

MCP 서버가 많아지면 도구(Tool)도 많아집니다.
도구가 컨텍스트의 10% 이상을 차지하면,
**Tool Search**가 자동으로 활성화됩니다.

Tool Search가 켜지면 Claude Code는
모든 도구를 한 번에 로드하지 않습니다.
필요한 도구만 검색해서 가져옵니다.
이렇게 컨텍스트 공간을 절약합니다.

수동으로 제어하려면 환경 변수를 설정합니다.

```bash
# 항상 활성화
export ENABLE_TOOL_SEARCH=true

# 항상 비활성화
export ENABLE_TOOL_SEARCH=false
```

### 디버깅 체크리스트

MCP 서버가 연결되지 않을 때,
다음 순서로 확인하세요.

1. `/mcp`로 서버 상태를 확인합니다
2. 환경 변수가 올바르게 설정되었는지 확인합니다
3. Stdio 서버라면 `npx` 명령이 작동하는지 확인합니다
4. HTTP/SSE 서버라면 URL에 접근 가능한지 확인합니다
5. OAuth 인증이 만료되지 않았는지 확인합니다

> **팁**: `claude mcp list`로 등록된 서버 목록과 설정을 빠르게 확인할 수 있습니다. 범위별로 어디에 저장되었는지도 표시됩니다.

---

## 정리

이번 챕터에서 배운 내용을 정리합니다.

| 주제 | 핵심 내용 |
|------|----------|
| MCP | 외부 도구를 AI에 연결하는 오픈 표준 |
| 전송 방식 | HTTP(권장), SSE, Stdio 세 가지 |
| 설정 파일 | `.mcp.json`에 서버 정의, 환경 변수 확장 지원 |
| 범위 | Local/Project/User, `--scope`로 지정 |
| 관리 | `/mcp`로 상태 확인, disable/enable로 제어 |
| Tool Search | 도구가 많으면 자동 활성화, 컨텍스트 절약 |

다음 챕터에서는 훅(Hook)을 사용하여
Claude Code의 동작을 자동화하는 방법을 배웁니다.
