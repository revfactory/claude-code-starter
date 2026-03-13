# 챕터 7: 터미널 명령 실행과 테스트

Claude Code는 코드만 작성하지 않습니다.
빌드, 테스트, 린트까지 터미널에서 직접 실행합니다.
이번 챕터에서는 셸 명령 실행부터
테스트 자동화까지 함께 익혀보겠습니다.

---

## 7.1 Bash 도구 이해하기

Claude Code에는 **Bash 도구**가 내장되어 있습니다.
여러분이 터미널에서 하는 일을 대신 수행합니다.

### 기본 사용법

프롬프트에 자연어로 요청하면 됩니다.

```text
> 현재 디렉토리의 파일 목록을 보여줘
```

Claude Code가 내부적으로 `ls -la`를 실행합니다.
결과를 읽고 다음 작업에 활용합니다.

### 타임아웃 설정

Bash 도구의 기본 타임아웃은 **2분**입니다.
최대 **10분**(600,000ms)까지 늘릴 수 있습니다.
오래 걸리는 빌드나 테스트에 유용합니다.

### 배경 실행

시간이 오래 걸리는 명령은 배경에서 실행됩니다.
완료되면 Claude Code가 알림을 보냅니다.
결과를 기다리는 동안 다른 대화를 이어갈 수 있습니다.

```text
> npm run build를 백그라운드에서 실행해줘
```

### 작업 디렉토리

Bash 도구는 워크스페이스 디렉토리를 기준으로 동작합니다.
별도 지정 없이도 프로젝트 루트에서 명령이 실행됩니다.

> **팁**: Claude Code는 명령 실행 전에 승인을 요청합니다. 신뢰하는 명령 패턴은 권한 설정에서 허용해두면 편리합니다.

---

## 7.2 `!` 빠른 명령

프롬프트 앞에 `!`를 붙이면 셸 명령을 직접 실행합니다.
Claude Code를 거치지 않는 **즉시 실행** 방식입니다.

```bash
! git status
```

```bash
! npm test
```

```bash
! cat package.json | head -20
```

AI 분석 없이 터미널 명령만 필요할 때 사용합니다.
결과는 컨텍스트에 포함됩니다.
이후 대화에서 결과를 참조할 수 있습니다.

```text
! npm test
> 방금 실패한 테스트를 수정해줘
```

이렇게 하면 테스트 결과가 컨텍스트에 남아 있어
Claude Code가 실패 원인을 정확히 파악합니다.

> **팁**: `!` 명령은 권한 확인 없이 즉시 실행됩니다. 위험한 명령에는 사용을 주의하세요.

---

## 7.3 테스트 작성

테스트 작성은 Claude Code가 가장 잘하는 일 중 하나입니다.
함수나 모듈을 지정하면 적절한 테스트를 생성합니다.

### 단일 함수 테스트

```text
> src/utils/validate.ts의 validateEmail 함수에 대한
  단위 테스트를 작성해줘
```

Claude Code는 해당 함수를 분석합니다.
정상 케이스, 엣지 케이스, 에러 케이스를 포함합니다.

```typescript
// src/utils/__tests__/validate.test.ts
import { validateEmail } from '../validate';

describe('validateEmail', () => {
  it('유효한 이메일을 통과시킨다', () => {
    expect(validateEmail('user@example.com')).toBe(true);
  });

  it('@ 없는 이메일을 거부한다', () => {
    expect(validateEmail('invalid-email')).toBe(false);
  });

  it('빈 문자열을 거부한다', () => {
    expect(validateEmail('')).toBe(false);
  });

  it('공백 포함 이메일을 거부한다', () => {
    expect(validateEmail('user @test.com')).toBe(false);
  });
});
```

### TDD 워크플로우

테스트 주도 개발도 자연스럽게 진행됩니다.

```text
> validatePhone 함수의 실패하는 테스트를 먼저 작성해줘
```

```text
> 테스트가 통과하도록 구현해줘
```

```text
> 테스트를 유지하면서 리팩토링해줘
```

Red → Green → Refactor 사이클을 대화로 수행합니다.

> **팁**: CLAUDE.md에 테스트 프레임워크와 규칙을 명시해두면 프로젝트 컨벤션에 맞는 테스트를 생성합니다.

---

## 7.4 테스트 실행과 수정 루프

Claude Code의 진짜 강점은 여기에 있습니다.
테스트 실행, 실패 분석, 코드 수정을 **자동으로 반복**합니다.

### 자동 수정 루프

```text
> 테스트를 실행하고 실패하면 수정해줘
```

Claude Code는 다음 과정을 자동으로 수행합니다.

1. `npm test` 실행
2. 실패한 테스트 확인
3. 실패 원인 분석
4. 소스 코드 또는 테스트 수정
5. 다시 테스트 실행
6. 모두 통과할 때까지 반복

```text
> npm test를 실행해줘

  FAIL src/utils/__tests__/validate.test.ts
  ● validateEmail › 공백 포함 이메일을 거부한다
    Expected: false
    Received: true

> 실패한 테스트에 맞게 validateEmail을 수정해줘
```

이 과정이 한 번의 요청으로 일어납니다.
여러분은 결과만 확인하면 됩니다.

### 특정 테스트만 실행

```text
> validate.test.ts만 실행해줘
```

```text
> "validateEmail" 관련 테스트만 실행해줘
```

범위를 좁히면 수정 루프가 더 빠르게 동작합니다.

> **주의**: 수정 루프가 3회 이상 반복되면 접근 방식을 바꿔야 할 수 있습니다. 구체적인 힌트를 추가로 제공해보세요.

---

## 7.5 빌드와 린트

### 빌드 에러 자동 수정

```text
> 프로젝트를 빌드하고 에러가 있으면 수정해줘
```

Claude Code는 빌드 로그를 분석합니다.
타입 에러, 임포트 누락, 구문 오류를 자동으로 수정합니다.

```text
> npm run build

  ERROR in src/api/handler.ts(42,5)
  TS2345: Argument of type 'string' is not
  assignable to parameter of type 'number'.
```

이런 에러를 발견하면 해당 파일을 열어 수정합니다.
그리고 다시 빌드를 실행해 확인합니다.

### 린트 적용

```text
> ESLint를 실행하고 자동 수정해줘
```

Claude Code는 `eslint --fix`로 해결되지 않는 문제도 처리합니다.
규칙 위반을 분석하고 코드를 직접 수정합니다.

```text
> lint 경고를 모두 해결해줘. any 타입은 구체적 타입으로 바꿔줘
```

### 빌드 + 린트 + 테스트 한 번에

```text
> 빌드, 린트, 테스트를 순서대로 실행하고
  문제가 있으면 모두 수정해줘
```

전체 검증 파이프라인을 한 문장으로 실행합니다.
CI에 푸시하기 전에 로컬에서 확인할 때 유용합니다.

> **팁**: CLAUDE.md에 `npm run build`, `npm run lint`, `npm test` 같은 프로젝트 명령을 기록해두세요. Claude Code가 정확한 명령을 사용합니다.

---

## 정리

이번 챕터에서 배운 내용을 정리합니다.

| 기능 | 사용법 |
|------|--------|
| Bash 도구 | 자연어로 셸 명령 요청 |
| `!` 빠른 명령 | `! git status`로 즉시 실행 |
| 테스트 작성 | 함수 지정하여 테스트 생성 요청 |
| 수정 루프 | 실행 → 실패 → 수정 자동 반복 |
| 빌드/린트 | 에러 분석 후 자동 수정 |

다음 챕터에서는 Git 연동과 PR 워크플로우를 다룹니다.
Claude Code로 커밋, 리뷰, PR 생성까지 자동화해보겠습니다.
