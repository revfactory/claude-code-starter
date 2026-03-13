# 챕터 2. 설치와 첫 실행

---

## 학습 목표

이 챕터를 마치면 여러분은 다음을 할 수 있습니다.

- 자신의 OS에 맞게 Claude Code를 설치할 수 있다
- 인증(로그인)을 완료할 수 있다
- 첫 실행과 대화 시작이 가능하다
- `claude doctor`로 설치 상태를 진단할 수 있다

---

## 2.1 시스템 요구사항

설치 전에 환경부터 확인합시다. Claude Code는 대부분의 최신 OS를 지원합니다.

| 항목 | 요구사항 |
|------|----------|
| **OS** | macOS 13.0 이상, Windows 10 1809 이상, Ubuntu 20.04 이상 |
| **RAM** | 최소 4GB |
| **네트워크** | 인터넷 연결 필수 |
| **Shell** | Bash, Zsh, PowerShell, CMD |

> **주의**: Windows에서는 **Git for Windows**가 반드시 필요합니다. 아직 설치하지 않았다면 [git-scm.com](https://git-scm.com)에서 먼저 설치하세요.

Claude Code는 클라우드 기반 도구입니다. 로컬에서 AI 모델을 돌리지 않습니다. 그래서 고사양 GPU가 필요 없습니다. 안정적인 인터넷 연결만 있으면 충분합니다.

---

## 2.2 설치하기

OS별로 설치 방법이 다릅니다. 자신의 환경에 맞는 방법을 따라 하세요.

### macOS / Linux

가장 간단한 방법은 공식 설치 스크립트입니다.

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

이 한 줄이면 끝입니다. 별도 의존성이 필요 없습니다. 자동 업데이트도 포함되어 있습니다.

macOS 사용자라면 Homebrew도 가능합니다.

```bash
brew install --cask claude-code
```

> **주의**: Homebrew 설치는 자동 업데이트를 지원하지 않습니다. 새 버전이 나오면 `brew upgrade claude-code`를 직접 실행해야 합니다.

### Windows

PowerShell을 관리자 권한으로 열고 실행하세요.

```powershell
irm https://claude.ai/install.ps1 | iex
```

WinGet을 선호한다면 이 방법도 됩니다.

```powershell
winget install Anthropic.ClaudeCode
```

> **팁**: Windows에서는 PowerShell 설치 스크립트를 권장합니다. 가장 안정적이고 자동 업데이트도 지원합니다.

---

## 2.3 인증 설정

Claude Code를 사용하려면 인증이 필요합니다. 세 가지 방법이 있습니다.

### 방법 1: Claude Pro/Max 구독 (개인 사용자)

가장 간단한 방법입니다. [claude.ai/pricing](https://claude.ai/pricing)에서 Pro 또는 Max 플랜을 구독하세요. 구독 후 Claude Code를 실행하면 브라우저에서 로그인할 수 있습니다.

### 방법 2: Console API (개발자)

API 기반으로 사용하고 싶다면 [console.anthropic.com](https://console.anthropic.com)에서 계정을 만드세요. Claude Code를 처음 실행하면 "Claude Code" 워크스페이스가 자동 생성됩니다. 사용량에 따라 비용이 청구됩니다.

### 방법 3: 클라우드 제공자 (엔터프라이즈)

기업 환경이라면 클라우드 제공자를 통해 연결할 수 있습니다.

- Amazon Bedrock
- Google Vertex AI
- Microsoft Foundry

각 제공자의 환경 변수를 설정한 뒤 사용합니다. 이 방법은 보안 정책이 엄격한 조직에 적합합니다.

> **팁**: 처음 시작한다면 **방법 1(Claude Pro/Max)**을 추천합니다. 설정이 가장 간단하고, 월정액이라 비용 예측이 쉽습니다.

---

## 2.4 첫 실행

설치와 인증 준비가 끝났습니다. 이제 실행해 봅시다.

### 실행하기

터미널을 열고 프로젝트 폴더로 이동합니다. 그리고 `claude`를 입력하세요.

```bash
cd /path/to/your/project
claude
```

처음 실행하면 브라우저가 자동으로 열립니다. Claude.ai 계정으로 로그인하세요. 인증이 완료되면 터미널로 돌아옵니다.

### 첫 실행 화면

인증이 끝나면 아래와 같은 화면이 나타납니다.

```
╭─────────────────────────────────────╮
│ ✻ Claude Code                       │
│                                     │
│   /help for commands                │
│   /model to change model            │
│                                     │
╰─────────────────────────────────────╯

 >
```

축하합니다! Claude Code가 준비되었습니다. `>` 뒤에 자연어로 질문하면 됩니다.

### 첫 대화 시도

간단한 질문으로 시작해 봅시다.

```
> 이 프로젝트가 무엇을 하는 건지 설명해줘
```

Claude Code는 프로젝트의 파일 구조를 분석합니다. 그리고 전체적인 설명을 제공합니다. 여러분이 방금 코드베이스를 처음 열었을 때 특히 유용합니다.

> **팁**: 프로젝트 폴더 안에서 실행해야 합니다. Claude Code는 현재 디렉터리의 파일을 컨텍스트로 활용합니다. 빈 폴더에서 실행하면 분석할 코드가 없습니다.

### 자격증명은 어디에 저장되나요?

로그인 정보는 안전하게 관리됩니다.

- **macOS**: 암호화된 Keychain에 저장
- **Windows/Linux**: 로컬 암호화 저장소에 저장

계정을 전환하고 싶다면 `/logout` 슬래시 커맨드를 사용하세요.

---

## 2.5 설치 확인과 진단

설치가 제대로 되었는지 확인해 봅시다.

### 버전 확인

```bash
claude --version
```

```
1.0.x (claude-code)
```

버전 번호가 출력되면 설치가 정상입니다.

### 상세 진단: claude doctor

뭔가 이상하다면 `claude doctor`를 실행하세요. 설치 상태를 종합적으로 진단해 줍니다.

```bash
claude doctor
```

```
Claude Code Doctor

  ✓ Environment    All checks passed
  ✓ Authentication Logged in
  ✓ Network        API reachable
  ✓ Permissions    Config valid

All checks passed!
```

모든 항목에 체크 표시가 나오면 준비 완료입니다.

> **팁**: `claude doctor`는 네트워크 연결, 인증 상태, 설정 파일까지 한 번에 확인합니다. 문제가 생겼을 때 가장 먼저 실행할 명령어로 기억해 두세요.

### 자주 만나는 문제

| 증상 | 원인 | 해결 |
|------|------|------|
| `command not found` | PATH에 등록 안 됨 | 터미널을 재시작하거나 셸 설정 파일을 다시 로드하세요 |
| 브라우저가 안 열림 | 기본 브라우저 미설정 | 터미널에 출력된 URL을 직접 복사해서 열어 보세요 |
| 인증 실패 | 구독 미완료 | [claude.ai/pricing](https://claude.ai/pricing)에서 플랜을 확인하세요 |
| 네트워크 오류 | 방화벽/프록시 | 회사 네트워크라면 IT 팀에 문의하세요 |

---

## 정리

이번 챕터에서 배운 내용을 정리합니다.

| 단계 | 내용 | 핵심 명령어 |
|------|------|-------------|
| 요구사항 확인 | OS, RAM 4GB, 인터넷 연결 | — |
| 설치 | OS별 설치 스크립트 실행 | `curl -fsSL https://claude.ai/install.sh \| bash` |
| 인증 | Pro/Max 구독 또는 Console API | 브라우저 로그인 |
| 첫 실행 | 프로젝트 폴더에서 `claude` 입력 | `claude` |
| 진단 | 설치 상태 확인 | `claude --version`, `claude doctor` |

여러분의 컴퓨터에 Claude Code가 설치되었습니다. 인증도 마쳤고, 첫 대화도 시작해 봤습니다. 다음 챕터에서는 Claude Code의 인터페이스를 본격적으로 살펴보겠습니다. 대화를 이어가는 법, 슬래시 커맨드, 단축키 등 실전에서 바로 쓸 수 있는 기술을 익힐 예정입니다.
