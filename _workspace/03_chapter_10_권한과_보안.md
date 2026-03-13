# 챕터 10: 권한과 보안

> **학습 목표**
> - 5가지 권한 모드의 차이를 이해한다
> - 상황에 맞는 권한 모드를 선택할 수 있다
> - Allow/Deny 규칙을 설정할 수 있다
> - 민감 파일을 보호할 수 있다

---

## 10.1 왜 권한이 중요한가

Claude Code는 강력한 에이전트입니다. 파일을 읽고, 수정하고, 터미널 명령을 실행합니다. 이 능력은 양날의 검입니다.

여러분이 "이 프로젝트를 정리해줘"라고 말했을 때, AI가 `.env` 파일을 삭제한다면 어떨까요? 프로덕션 데이터베이스에 접속하는 명령을 실행한다면요? 권한 시스템은 이런 사고를 방지합니다.

**AI 도구 보안의 3대 원칙**을 기억하세요.

1. **최소 권한**: 필요한 만큼만 허용합니다
2. **명시적 승인**: 위험한 작업은 반드시 확인합니다
3. **방어적 차단**: 민감 파일은 사전에 차단합니다

> **팁**: 처음에는 `default` 모드로 시작하세요. Claude Code가 어떤 권한을 요청하는지 파악한 뒤, 점진적으로 규칙을 추가하는 것이 안전합니다.

---

## 10.2 5가지 모드 비교

Claude Code는 5가지 권한 모드를 제공합니다. 각 모드는 파일 편집과 명령 실행에 대해 서로 다른 수준의 통제를 적용합니다.

| 모드 | 파일 편집 | 명령 실행 | 추천 상황 |
|------|---------|---------|----------|
| **default** | 매번 확인 | 매번 확인 | 보안이 중요한 환경 |
| **acceptEdits** | 자동 승인 | 매번 확인 | 빠른 코드 작성 |
| **plan** | 불가 | 불가 | 계획 검토, 코드 리뷰 |
| **dontAsk** | 사전 허용만 | 사전 허용만 | CI/CD 자동화 |
| **bypassPermissions** | 전부 자동 | 전부 자동 | 격리된 컨테이너 전용 |

### 모드 전환 방법

세션 중에는 **Shift+Tab**으로 순환 전환합니다. 시작할 때 지정할 수도 있습니다.

```bash
# 시작 시 모드 지정
claude --permission-mode plan
```

settings.json에서 기본값을 설정할 수도 있습니다.

```json
{
  "permissions": {
    "defaultMode": "acceptEdits"
  }
}
```

> **주의**: `bypassPermissions` 모드는 모든 보안 장치를 해제합니다. 반드시 Docker 컨테이너 등 격리된 환경에서만 사용하세요. 로컬 머신에서는 절대 사용하지 마세요.

### 모드 선택 가이드

- **혼자 개발할 때**: `acceptEdits`가 편리합니다. 파일 편집은 자동으로, 쉘 명령만 확인합니다.
- **코드 리뷰할 때**: `plan` 모드로 시작하세요. 실수로 코드가 변경될 걱정이 없습니다.
- **CI/CD 파이프라인**: `dontAsk` 모드에 Allow 규칙을 조합합니다.
- **처음 쓰는 프로젝트**: `default`로 시작해서 패턴을 파악하세요.

---

## 10.3 Allow/Deny 규칙

권한 모드만으로는 세밀한 제어가 어렵습니다. Allow/Deny 규칙으로 도구별, 경로별 권한을 정밀하게 설정할 수 있습니다.

### 규칙 작성법

settings.json의 `permissions` 항목에 규칙을 작성합니다.

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(npm run *)",
      "Bash(git diff *)",
      "Edit(/src/**/*.ts)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(curl *)",
      "Edit(/.env)",
      "Read(**/.env.*)"
    ]
  }
}
```

규칙의 형식은 `도구명(패턴)`입니다. 와일드카드 `*`과 글롭 패턴 `**`을 사용할 수 있습니다.

### 평가 순서: Deny → Ask → Allow

규칙 평가는 세 단계로 진행됩니다.

1. **Deny 확인**: deny 목록에 매칭되면 즉시 차단합니다
2. **Allow 확인**: allow 목록에 매칭되면 자동 승인합니다
3. **Ask (기본)**: 어디에도 매칭되지 않으면 사용자에게 묻습니다

이 순서가 핵심입니다. **Deny가 항상 우선**합니다. allow에 `Edit`을 넣더라도, deny에 `Edit(/.env)`가 있으면 `.env` 편집은 차단됩니다.

> **팁**: deny 규칙을 먼저 작성하세요. "절대 하면 안 되는 것"부터 정의하는 것이 안전합니다.

---

## 10.4 민감 파일 보호

실무에서 반드시 보호해야 할 파일 유형이 있습니다. 환경 변수, 자격증명, SSH 키가 대표적입니다.

### 보호 패턴 템플릿

다음은 실무에서 바로 사용할 수 있는 보호 규칙입니다.

```json
{
  "permissions": {
    "deny": [
      "Read(**/.env)",
      "Read(**/.env.*)",
      "Read(**/.env.local)",
      "Edit(**/.env)",
      "Edit(**/.env.*)",
      "Read(~/.ssh/**)",
      "Read(~/.aws/**)",
      "Read(~/.config/gcloud/**)",
      "Read(**/*credential*)",
      "Read(**/*secret*)",
      "Read(**/*.pem)",
      "Read(**/*.key)",
      "Bash(cat */.env*)",
      "Bash(echo $*_KEY*)",
      "Bash(echo $*_SECRET*)",
      "Bash(echo $*_TOKEN*)"
    ]
  }
}
```

### 보호 대상 체크리스트

| 파일/경로 | 위험 | 보호 규칙 |
|----------|------|---------|
| `.env`, `.env.*` | API 키, DB 비밀번호 노출 | Read/Edit 차단 |
| `~/.ssh/` | 서버 접근 키 유출 | Read 차단 |
| `~/.aws/` | 클라우드 자격증명 유출 | Read 차단 |
| `*.pem`, `*.key` | 인증서/개인키 유출 | Read 차단 |
| `*credential*`, `*secret*` | 기타 민감 정보 | Read 차단 |

> **주의**: `.env.example`처럼 템플릿 파일은 보호 대상에서 제외해도 됩니다. 하지만 실수를 방지하려면 일단 차단하고, 필요할 때 Allow에 예외를 추가하는 것이 좋습니다.

### API 키 관리 원칙

1. **파일에 직접 저장하지 마세요**. 환경 변수를 사용합니다.
2. **macOS라면 Keychain을 활용하세요**. Claude Code는 자격증명을 Keychain에 저장합니다.
3. **`--allowedTools`로 도구를 제한하세요**. CI/CD에서는 필요한 도구만 허용합니다.

```bash
# 필요한 도구만 허용하여 실행
claude -p "코드를 분석해줘" \
  --allowedTools "Read,Grep,Glob"
```

---

## 10.5 팀을 위한 보안

개인 설정만으로는 팀 전체를 보호할 수 없습니다. 프로젝트 수준의 settings.json을 공유하면 팀원 모두에게 동일한 보안 규칙이 적용됩니다.

### 설정 파일 계층 구조

Claude Code는 설정을 세 단계에서 읽습니다.

1. **프로젝트 설정**: `.claude/settings.json` (Git에 커밋)
2. **사용자 설정**: `~/.claude/settings.json` (개인 환경)
3. **시스템 설정**: `/etc/claude/settings.json` (관리자)

Deny 규칙은 모든 단계에서 합산됩니다. 프로젝트에서 차단한 것은 개인 설정으로 해제할 수 없습니다.

### 팀 보안 설정 예시

프로젝트 루트의 `.claude/settings.json`에 다음을 작성하고 Git에 커밋합니다.

```json
{
  "permissions": {
    "defaultMode": "default",
    "deny": [
      "Read(**/.env)",
      "Read(**/.env.*)",
      "Edit(**/.env)",
      "Read(~/.ssh/**)",
      "Read(**/*secret*)",
      "Read(**/*.key)",
      "Bash(rm -rf *)",
      "Bash(curl *)",
      "Bash(wget *)"
    ],
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(npm run *)",
      "Bash(npm test *)",
      "Bash(git diff *)",
      "Bash(git log *)",
      "Bash(git status *)"
    ]
  }
}
```

### 팀 보안 체크리스트

- [ ] `.claude/settings.json`을 Git에 커밋했는가
- [ ] Deny 규칙에 민감 파일 패턴이 포함되었는가
- [ ] 위험한 쉘 명령(`rm -rf`, `curl`)이 차단되었는가
- [ ] CI/CD에서 `--allowedTools`를 사용하고 있는가
- [ ] 신규 팀원 온보딩 문서에 권한 설정이 포함되었는가

> **팁**: 프로젝트 settings.json은 코드 리뷰 대상입니다. 보안 규칙을 변경하는 PR은 팀 리드가 반드시 검토하세요.

---

## 정리

| 개념 | 핵심 요약 |
|------|---------|
| 권한 모드 | 5가지 모드로 전체 수준 조절 |
| Allow/Deny | 도구별·경로별 세밀한 제어 |
| 평가 순서 | Deny → Ask → Allow |
| 민감 파일 | `.env`, SSH 키, 자격증명 사전 차단 |
| 팀 보안 | 프로젝트 settings.json 공유 |

보안은 불편함이 아니라 **신뢰의 기반**입니다. 적절한 권한 설정은 여러분이 Claude Code를 더 자유롭게, 더 과감하게 활용할 수 있게 해줍니다. 다음 챕터에서는 훅(Hook)과 자동화를 다루겠습니다.
