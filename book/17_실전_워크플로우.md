# 챕터 17: 실전 개발 워크플로우

> **학습 목표**
> - TDD 사이클을 Claude Code로 수행한다
> - 에러 로그 기반 디버깅 루프를 익힌다
> - Plan 모드로 안전하게 리팩토링한다
> - 비대화형 모드로 작업을 자동화한다
> - IDE 확장에서 Claude Code를 활용한다
> - Worktree로 병렬 개발을 진행한다

---

지금까지 개별 기능을 배웠습니다.
이번 챕터에서는 실전에서 쓰는 워크플로우를 다룹니다.
하나의 기능이 아니라, 여러 기능을 조합합니다.
현업 개발자의 일과를 따라가며 익혀봅시다.

---

## 17.1 TDD with Claude Code

테스트 주도 개발(TDD)은 세 단계입니다.
Red, Green, Refactor.
Claude Code는 이 사이클을 가속합니다.

### Red: 실패하는 테스트 작성

먼저 테스트부터 작성합니다.
구현은 아직 없으니 당연히 실패합니다.

```bash
> validateEmail 함수의 테스트를 먼저 작성해줘.
> 유효한 이메일, 빈 문자열, @없는 경우를 포함해.
> 구현은 하지 마.
```

Claude Code가 테스트 파일을 생성합니다.
`npm test`를 실행하면 빨간 불이 켜집니다.
이것이 Red 단계입니다.

```typescript
// src/__tests__/validateEmail.test.ts
import { validateEmail } from '../validateEmail';

describe('validateEmail', () => {
  it('유효한 이메일을 통과시킨다', () => {
    expect(validateEmail('user@example.com')).toBe(true);
  });

  it('빈 문자열을 거부한다', () => {
    expect(validateEmail('')).toBe(false);
  });

  it('@가 없으면 거부한다', () => {
    expect(validateEmail('userexample.com')).toBe(false);
  });

  it('도메인이 없으면 거부한다', () => {
    expect(validateEmail('user@')).toBe(false);
  });
});
```

### Green: 테스트를 통과시키는 구현

이제 구현을 요청합니다.

```bash
> 모든 테스트가 통과하도록 validateEmail을 구현해줘.
> 테스트를 실행해서 확인까지 해줘.
```

Claude Code가 함수를 구현합니다.
그리고 `npm test`를 실행해 초록 불을 확인합니다.
테스트가 모두 통과하면 Green 단계 완료입니다.

### Refactor: 테스트를 유지하며 개선

구현이 동작하지만, 코드가 지저분할 수 있습니다.

```bash
> validateEmail을 리팩토링해줘.
> 정규식을 사용하고, 테스트는 계속 통과해야 해.
```

Claude Code가 코드를 개선합니다.
매번 테스트를 돌려 깨지지 않는지 확인합니다.
이것이 Refactor 단계입니다.

> **팁**: `CLAUDE.md`에 "테스트를 먼저 작성하고, 구현 후 반드시 테스트를 실행하라"고 적어두면 Claude Code가 TDD 사이클을 자연스럽게 따릅니다.

---

## 17.2 디버깅 시나리오

버그가 발생했습니다.
에러 로그가 있습니다.
Claude Code에게 맡겨봅시다.

### 1단계: 에러 로그 전달

터미널의 에러 메시지를 복사합니다.
그대로 Claude Code에 붙여넣으세요.

```bash
> 이 에러를 분석해줘:
> TypeError: Cannot read properties of undefined
>   (reading 'userId')
>   at AuthService.verify (src/auth/service.ts:42)
>   at Router.handle (src/routes/api.ts:18)
```

Claude Code는 스택 트레이스를 추적합니다.
관련 파일을 자동으로 읽고 분석합니다.

### 2단계: 근본 원인 파악

Claude Code가 코드를 탐색합니다.
`src/auth/service.ts:42`를 열고,
호출 경로를 역추적합니다.
어디서 `undefined`가 전달되는지 찾습니다.

### 3단계: 수정과 검증

원인을 찾으면 수정을 제안합니다.

```bash
> 이 버그를 재현하는 테스트를 먼저 작성해줘.
> 그다음 수정하고, 테스트가 통과하는지 확인해줘.
```

이 흐름이 디버깅 루프입니다.
에러 로그 -> 추적 -> 테스트 -> 수정 -> 검증.
한 번의 프롬프트로 전체 과정이 진행됩니다.

> **팁**: 에러 메시지뿐 아니라 재현 조건도 함께 전달하세요. "로그인 후 3분 뒤 토큰 만료 시 발생"처럼 구체적일수록 정확한 수정이 나옵니다.

---

## 17.3 안전한 리팩토링

리팩토링은 위험합니다.
동작하는 코드를 건드리니까요.
Claude Code의 Plan 모드가 도움됩니다.

### 1단계: Plan 모드로 계획 수립

먼저 계획만 세웁니다.
코드를 수정하지 않습니다.

```bash
> /plan CommonJS를 ESM으로 마이그레이션하려고 해.
> 어떤 파일을 어떤 순서로 변경해야 하는지 알려줘.
```

Plan 모드에서는 읽기만 가능합니다.
Claude Code가 코드베이스를 분석합니다.
변경 계획을 상세하게 제시합니다.

```
## 마이그레이션 계획

1. package.json에 "type": "module" 추가
2. tsconfig.json의 module을 "ESNext"로 변경
3. src/utils/*.ts의 require → import 변환 (8개 파일)
4. src/routes/*.ts의 module.exports → export 변환 (5개 파일)
5. 테스트 설정 파일 업데이트 (jest.config)
6. 전체 테스트 실행으로 검증
```

### 2단계: 계획 검토 후 실행

계획을 검토합니다.
빠진 부분이 없는지 확인합니다.
그다음 일반 모드에서 실행을 요청합니다.

```bash
> 위 계획대로 마이그레이션을 진행해줘.
> 각 단계마다 테스트를 실행해서 확인해줘.
```

### 3단계: 단계별 검증

Claude Code가 파일을 하나씩 수정합니다.
매 단계마다 테스트를 실행합니다.
실패하면 즉시 멈추고 원인을 분석합니다.

> **주의**: 대규모 리팩토링은 반드시 Plan 모드로 시작하세요. 계획 없이 바로 수정하면, 중간에 의존성 문제가 발생할 수 있습니다. 되돌리기 어렵습니다.

---

## 17.4 자동화: 비대화형 모드

Claude Code를 스크립트에서 호출할 수 있습니다.
`-p` 플래그가 핵심입니다.

### 기본 사용법

```bash
# 한 줄 질문, 즉시 응답
claude -p "src/api/ 디렉터리의 모든 엔드포인트를 나열해줘"

# JSON 형식으로 출력
claude -p "이 프로젝트의 의존성을 분석해줘" \
  --output-format json

# 스트리밍 JSON 출력
claude -p "코드를 분석해줘" \
  --output-format stream-json
```

### 배치 처리 스크립트

여러 파일을 한 번에 처리할 수 있습니다.

```bash
#!/bin/bash
# migrate_to_esm.sh
# CommonJS 파일을 ESM으로 일괄 변환

while IFS= read -r file; do
  echo "변환 중: $file"
  claude -p "Convert $file from CommonJS to ESM" \
    --allowedTools "Read,Edit" \
    --max-turns 3
done < cjs_files.txt
```

### CI/CD 파이프라인 통합

GitHub Actions에서 자동 리뷰를 실행합니다.

```yaml
# .github/workflows/ai-review.yml
name: AI Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: AI 코드 리뷰
        run: |
          gh pr diff ${{ github.event.pull_request.number }} | \
          claude -p "이 diff를 리뷰해줘. 버그, 보안, 성능 이슈를 찾아줘" \
            --output-format json \
            --max-budget-usd 1.00 > review.json
```

### 유용한 옵션 정리

| 옵션 | 설명 |
|------|------|
| `--output-format json` | JSON으로 출력 |
| `--output-format stream-json` | 스트리밍 JSON |
| `--max-budget-usd 5.00` | 비용 상한 설정 |
| `--max-turns 3` | 최대 턴 수 제한 |
| `--allowedTools "Read,Edit"` | 허용 도구 제한 |
| `--append-system-prompt "..."` | 시스템 프롬프트 추가 |

> **팁**: `--max-budget-usd`로 비용을 제한하세요. CI에서 예상치 못한 비용이 발생하는 것을 방지합니다. 코드 리뷰라면 $1 정도면 충분합니다.

---

## 17.5 IDE에서 사용하기

터미널을 벗어나 IDE에서도 사용할 수 있습니다.

### VS Code 확장

VS Code에서 Claude Code를 사용하는 방법입니다.

**설치**:
1. 마켓플레이스에서 "Claude Code"를 검색합니다
2. 설치를 클릭합니다
3. 사이드바에 Spark 아이콘이 나타납니다

**사용법**:
- Spark 아이콘을 클릭합니다
- 또는 `Cmd+Shift+P` > "Claude Code: Open"
- 터미널과 동일한 대화형 인터페이스입니다

```
주요 기능:
- @파일명으로 파일 참조
- 에디터에서 코드 선택 후 질문
- 권한 모드, 슬래시 커맨드 모두 지원
- 통합 diff 뷰어로 변경사항 확인
```

### JetBrains 플러그인

IntelliJ, PyCharm, WebStorm 등을 지원합니다.

**설치**:
1. Settings > Plugins에서 "Claude Code" 검색
2. Install을 클릭합니다
3. IDE를 재시작합니다

**사용법**:
- `Cmd+Esc` (macOS) / `Ctrl+Esc` (Windows/Linux)
- 하단 도구 창에서 대화합니다
- 에디터의 코드를 직접 참조할 수 있습니다

### 터미널 vs IDE 비교

| 항목 | 터미널 | IDE 확장 |
|------|--------|----------|
| 속도 | 빠름 | 동일 |
| 파일 참조 | `@경로` 입력 | 클릭으로 선택 |
| diff 확인 | 터미널 출력 | 시각적 diff 뷰어 |
| 자동화 | `-p` 플래그 | 불가 |
| 멀티태스킹 | 탭/창 분리 | 사이드바 고정 |

> **팁**: 터미널과 IDE를 함께 사용하세요. 코드 탐색은 IDE에서, 자동화와 배치 작업은 터미널에서 수행하면 효율적입니다.

---

## 17.6 병렬 개발: Worktree

하나의 작업이 끝나기를 기다리지 마세요.
Git Worktree로 여러 작업을 동시에 진행합니다.

### Worktree란

Git Worktree는 하나의 저장소에서
여러 작업 디렉터리를 만드는 기능입니다.
각 디렉터리는 독립된 브랜치를 가집니다.
서로 간섭하지 않습니다.

### --worktree 플래그 사용

```bash
# 터미널 1: 인증 기능 개발
claude --worktree feature-auth \
  "OAuth2 로그인을 구현해줘"

# 터미널 2: 버그 수정
claude --worktree bugfix-session \
  "세션 만료 버그를 수정해줘"

# 터미널 3: 코드 리뷰
claude --worktree review-pr-42 \
  "PR #42를 리뷰해줘"
```

세 작업이 동시에 진행됩니다.
각각 별도의 브랜치에서 작업합니다.
메인 브랜치는 안전합니다.

### 에이전트와 Worktree 조합

커스텀 에이전트에 `isolation: worktree`를 설정하면
에이전트 실행 시 자동으로 워크트리가 생성됩니다.

```markdown
---
name: feature-builder
description: 기능 개발 전문 에이전트
tools: Read, Write, Edit, Bash, Glob, Grep
model: sonnet
permissionMode: acceptEdits
isolation: worktree
---

새 기능을 독립된 워크트리에서 개발합니다.
테스트 작성과 구현을 함께 진행합니다.
```

이 에이전트를 호출하면 격리된 환경에서 작업합니다.

```bash
/feature-builder 사용자 프로필 페이지를 만들어줘
```

### Writer-Reviewer 패턴

병렬 워크트리의 고급 활용법입니다.
한쪽에서 코드를 쓰고, 다른 쪽에서 리뷰합니다.

```bash
# 터미널 1: 코드 작성 (Writer)
claude --worktree writer-auth \
  "JWT 인증 미들웨어를 구현해줘"

# 터미널 2: 코드 리뷰 (Reviewer)
claude --worktree reviewer-auth \
  "writer-auth 브랜치의 변경사항을 리뷰해줘"
```

Writer가 코드를 작성합니다.
Reviewer가 독립적으로 검토합니다.
두 관점이 교차하면 품질이 올라갑니다.

> **주의**: Worktree는 Git 저장소에서만 작동합니다. 프로젝트가 Git으로 관리되지 않으면 사용할 수 없습니다. `git init`으로 먼저 초기화하세요.

---

## 정리

이번 챕터에서 다룬 실전 워크플로우입니다.

| 워크플로우 | 핵심 포인트 |
|-----------|------------|
| TDD | 테스트 먼저, 구현, 리팩토링 순서 |
| 디버깅 | 에러 로그 전달 -> 자동 추적 -> 수정 |
| 리팩토링 | Plan 모드로 계획, 단계별 검증 |
| 자동화 | `-p` 플래그, `--output-format json` |
| IDE 통합 | VS Code 확장, JetBrains 플러그인 |
| 병렬 개발 | `--worktree`로 동시 작업 |

여러분의 개발 워크플로우에 맞게 조합하세요.
TDD로 기능을 만들고, 디버깅으로 버그를 잡고,
리팩토링으로 코드를 개선합니다.
이 모든 과정을 Claude Code가 함께합니다.

> **다음 챕터 미리보기**: 챕터 18에서는 팀 협업과 조직 운영 방법을 다룹니다. 여러 개발자가 Claude Code를 함께 사용하는 전략, CLAUDE.md 공유, 조직 정책 설정 등을 알아봅니다.
