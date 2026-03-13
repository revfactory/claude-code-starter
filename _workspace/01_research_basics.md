# Claude Code 기초 및 설치/설정 조사 보고서

## 1. Claude Code란 무엇인가

### 정의
Claude Code는 AI 기반 코딩 어시스턴트로, 터미널에서 실행되는 **에이전트(Agentic) 코딩 도구**. 단순한 자동완성이 아니라 전체 프로젝트를 이해하고, 파일을 수정하고, 명령어를 실행하며, 개발 도구들과 통합되는 '에이전트'로 작동.

### 핵심 특징
1. **전체 코드베이스 이해**: 프로젝트의 모든 파일을 읽고 분석, 맥락 파악
2. **자율적 작업 수행**: 여러 파일 수정, 명령어 실행, 테스트, 결과 검증
3. **다중 환경 지원**: 터미널, VS Code, JetBrains IDE, 데스크톱 앱, 웹, Slack
4. **대화형 상호작용**: 언제든 작업 중단/방향 조정 가능

### 다른 AI 코딩 도구와의 차별점

| 특징 | Claude Code | 일반 자동완성 AI |
|------|-----------|----------|
| 범위 | 전체 프로젝트 이해 및 다중 파일 수정 | 현재 파일만 제안 |
| 자율성 | 사용자 지시에 따라 자동으로 여러 단계 실행 | 각 제안에 대해 개별 승인 필요 |
| 도구 접근 | 파일 편집, 명령 실행, Git 작업, 검색 등 | 코드 제안만 가능 |
| 검증 | 테스트 실행, 결과 확인, 자동 오류 수정 | 검증 불가 |
| 확장성 | MCP, Skills, Hooks, Subagents 등 | 제한적 |

### Claude Code로 할 수 있는 일들
- 버그 수정: 에러 메시지 붙여넣으면 자동 추적/수정
- 기능 구현: 자연어 설명으로 여러 파일에 걸쳐 개발
- 코드 리팩토링: 전체 프로젝트 아키텍처 개선
- 테스트 작성/실행: 테스트 코드 생성 및 자동 검증
- Git 작업: 커밋, 브랜치, PR 작성
- 문서화: README, API 문서 작성
- 반복 작업 자동화: 린트 에러 수정, 의존성 업데이트

---

## 2. 설치 방법

### 시스템 요구사항

| 항목 | 요구사항 |
|------|--------|
| OS | macOS 13.0+, Windows 10 1809+, Ubuntu 20.04+, Debian 10+, Alpine Linux 3.19+ |
| RAM | 최소 4GB |
| 네트워크 | 인터넷 연결 필수 |
| Shell | Bash, Zsh, PowerShell, CMD |
| Windows 추가 | Git for Windows 필수 |

### OS별 설치

#### macOS & Linux (권장)
```bash
curl -fsSL https://claude.ai/install.sh | bash
```
자동 업데이트 포함, 의존성 없음

#### macOS - Homebrew
```bash
brew install --cask claude-code
```
주의: 자동 업데이트 미지원, 수동 `brew upgrade claude-code` 필요

#### Windows PowerShell (권장)
```powershell
irm https://claude.ai/install.ps1 | iex
```

#### Windows CMD
```batch
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

#### Windows - WinGet
```powershell
winget install Anthropic.ClaudeCode
```

### 설치 확인
```bash
claude --version
claude doctor  # 상세 진단
```

---

## 3. 초기 설정 및 인증

### 인증 방법

#### 1. Claude Pro/Max 구독 (개인)
- claude.com/pricing에서 구독 → Claude.ai 계정 로그인

#### 2. Claude for Teams/Enterprise (팀)
- Teams: 자가 서비스, 소규모 팀
- Enterprise: SSO, 역할 기반 권한, 정책 관리

#### 3. Claude Console (API 기반)
- console.anthropic.com 계정 필요
- 자동으로 "Claude Code" 워크스페이스 생성

#### 4. 클라우드 제공자 (엔터프라이즈)
- Amazon Bedrock, Google Vertex AI, Microsoft Foundry
- 환경 변수 설정 후 사용

### 첫 실행
```bash
cd /path/to/your/project
claude
# 브라우저 자동 열림 → 로그인 → 세션 시작
```

### 자격증명 관리
- macOS: 암호화된 Keychain 저장
- 다른 OS: 로컬 암호화 저장소
- 계정 전환: `/logout`

---

## 4. 기본 사용법

### 시작 방법
```bash
claude                          # 대화형 모드
claude "what does this do?"     # 초기 프롬프트와 함께
claude -c                       # 이전 세션 재개
claude -r "session-name"        # 이름으로 재개
claude --model opus             # 특정 모델
claude --permission-mode plan   # 특정 권한 모드
cat logs.txt | claude -p "find errors"  # 파이프 입력
```

### 기본 워크플로우
1. 코드베이스 이해: `what does this project do?`
2. 코드 변경: `add input validation to the login function`
3. 결과 검증: `run the tests`
4. Git 커밋: `commit my changes with a descriptive message`

---

## 5. 권한 모드

### 5가지 모드

| 모드 | 동작 | 용도 |
|------|------|------|
| **default** | 매번 권한 요청 | 보안 중시 |
| **acceptEdits** | 파일 편집 자동 승인, bash는 확인 | 빠른 코드 변경 |
| **plan** | 읽기 전용, 수정 불가 | 계획 검토 |
| **dontAsk** | 사전 허용된 것만 실행 | 자동화 환경 |
| **bypassPermissions** | 모든 권한 스킵 | 격리 환경 전용 |

### 모드 전환
- **Shift+Tab**: 세션 중 순환 전환
- `claude --permission-mode plan`: 시작 시 지정
- settings.json: `{"permissions": {"defaultMode": "plan"}}`

### 권한 규칙
```json
{
  "permissions": {
    "allow": ["Bash(npm run *)", "Read", "Edit(/src/**/*.ts)"],
    "deny": ["Bash(rm -rf *)", "Edit(/.env)"]
  }
}
```
평가 순서: Deny → Ask → Allow

---

## 6. 터미널 인터페이스

### 주요 단축키

| 단축키 | 기능 |
|--------|------|
| Ctrl+C | 입력/생성 취소 |
| Ctrl+D | 종료 |
| Ctrl+L | 화면 지우기 |
| Ctrl+O | 상세 출력 전환 |
| Ctrl+V / Cmd+V | 이미지 붙여넣기 |
| Shift+Tab | 권한 모드 전환 |
| `!` 접두사 | bash 명령 직접 실행 |
| `@` | 파일 경로 자동완성 |

### 멀티라인 입력
- `\ + Enter`: 모든 터미널
- `Option+Enter`: macOS
- `Shift+Enter`: iTerm2, WezTerm, Ghostty, Kitty
- `Ctrl+J`: 라인 피드

### Vim 모드
```bash
/vim  # 토글 활성화
```

---

## 7. 비용 구조

### 평균 비용
- 일일 ~$6/개발자 (변동성 큼)
- 월 $100-200 (Sonnet 4.6 기준)
- `/cost` 명령으로 토큰 사용량 확인

### 모델별 비용

| 모델 | 용도 | 비용 |
|------|------|------|
| Sonnet 4.6 | 일일 코딩 작업 | 낮음 |
| Opus 4.6 | 복잡한 아키텍처 결정 | 높음 |
| Haiku | 단순/배경 작업 | 아주 낮음 |

### 비용 최적화
1. 모델 선택: 대부분 Sonnet, 필요시만 Opus
2. 컨텍스트 관리: `/compact`, `/clear`
3. MCP 서버: 미사용 서버 비활성화
4. Extended Thinking 조절: MAX_THINKING_TOKENS 환경변수
5. Skill로 CLAUDE.md 축소
6. Subagent 위임

---

## 8. 모델 선택

### 모델 별칭

| 별칭 | 설명 |
|------|------|
| `default` | 계정 맞춤 추천 |
| `sonnet` | 최신 Sonnet (4.6) |
| `opus` | 최신 Opus (4.6) |
| `haiku` | 빠른 Haiku |
| `sonnet[1m]` | 1M 토큰 컨텍스트 |
| `opusplan` | Opus 계획 → Sonnet 실행 |

### 모델 변경
```bash
/model opus          # 세션 중
claude --model opus  # 시작 시
```

### Effort Level
- Low / Medium(기본) / High
- `/model` → 화살표 키로 조절
- `CLAUDE_CODE_EFFORT_LEVEL` 환경변수

---

## 9. 에이전틱 루프

Claude Code 핵심 동작 방식: 3단계 루프

1. **Context 수집**: 파일 읽기, 검색, 상태 파악
2. **Action 수행**: 파일 편집, 명령 실행, Git 작업
3. **검증**: 테스트 실행, 결과 확인, 필요시 수정

---

## 10. 주요 개념 요약

- **Session**: 하나의 대화 단위, `/resume`으로 재개 가능
- **CLAUDE.md**: 프로젝트 규칙 파일, 세션마다 자동 로드
- **Skills**: 재사용 가능한 도메인 특화 명령어
- **MCP**: 외부 도구/데이터 연결 프로토콜
- **Subagents**: 독립적 AI 에이전트, 병렬 작업 가능
- **Hooks**: 이벤트 기반 자동 실행 스크립트
- **Checkpoints**: 파일 변경 전 자동 스냅샷, Esc 2번으로 복원
