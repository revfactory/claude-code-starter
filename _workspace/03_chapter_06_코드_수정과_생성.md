# 챕터 6: 코드 수정과 생성

코드를 직접 타이핑하지 않아도 됩니다. 자연어로 말하면 Claude Code가 수정합니다. 이번 챕터에서는 코드 수정과 생성의 핵심 기술을 익혀보겠습니다.

**학습 목표**
- 자연어로 코드 수정을 요청할 수 있다
- Write(새 파일 생성)와 Edit(기존 파일 편집)의 차이를 안다
- 여러 파일에 걸친 수정을 한 번에 요청할 수 있다
- 권한 모드를 상황에 맞게 전환할 수 있다

---

## 6.1 수정 요청의 기술

좋은 프롬프트는 Claude Code의 정확도를 극적으로 높입니다. 핵심은 **구체성**입니다.

### 나쁜 요청 vs 좋은 요청

```
❌ 나쁜 요청:
"이 코드 좀 고쳐줘"
"로그인 기능을 개선해줘"
"이 함수를 최적화해줘"
```

```
✅ 좋은 요청:
"src/auth/login.ts의 validateToken 함수에서
 만료된 토큰을 갱신하지 않는 버그를 수정해줘.
 실패 테스트를 먼저 작성하고, 그다음 수정해줘."
```

차이가 보이시나요? 좋은 요청에는 세 가지가 있습니다.

1. **위치**: 어떤 파일, 어떤 함수인지
2. **문제**: 무엇이 잘못되었는지
3. **방법**: 어떤 순서로 해결할지

실제 CLI에서 사용해봅시다.

```bash
$ claude "src/utils/format.ts의 formatDate 함수가
  UTC 시간대를 무시하고 있어.
  KST(+09:00) 기본값을 추가해줘."
```

```
[Claude이 src/utils/format.ts를 읽고 분석한 뒤,
 formatDate 함수에 timezone 매개변수를 추가하고
 기본값을 'Asia/Seoul'로 설정합니다.]
```

> **팁**: 파일 경로를 정확히 알려주면 Claude Code가 탐색 시간을 줄이고 바로 수정에 집중합니다.

---

## 6.2 단일 파일 수정

Claude Code는 두 가지 도구(Tool)로 파일을 다룹니다.

| 도구 | 용도 | 특징 |
|------|------|------|
| **Write** | 새 파일 생성, 전체 재작성 | 파일 전체를 한 번에 씀 |
| **Edit** | 기존 파일 일부 수정 | 변경 부분만 교체, 컨텍스트 효율적 |

### 예제 1: 새 파일 생성 (Write)

```bash
$ claude "src/utils/validators.ts에
  이메일 유효성 검사 함수를 만들어줘.
  정규식 기반으로, 빈 문자열도 처리해야 해."
```

```typescript
// src/utils/validators.ts (새로 생성됨)
export function validateEmail(email: string): boolean {
  if (!email || email.trim() === '') {
    return false;
  }
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}
```

Write 도구가 파일을 생성할 때 **체크포인트가 자동으로 만들어집니다**. 실수해도 복원할 수 있으니 걱정하지 마세요.

### 예제 2: 함수 추가 (Edit)

이미 존재하는 파일에 함수를 추가합니다.

```bash
$ claude "src/utils/validators.ts에
  전화번호 유효성 검사 함수도 추가해줘.
  한국 형식(010-XXXX-XXXX)을 지원해야 해."
```

```typescript
// Edit 도구가 기존 파일 끝에 추가
export function validatePhone(phone: string): boolean {
  const regex = /^01[016789]-\d{3,4}-\d{4}$/;
  return regex.test(phone);
}
```

> **팁**: 기존 파일을 수정할 때 Claude Code는 자동으로 Edit 도구를 선택합니다. 파일 전체를 다시 쓰지 않으므로 토큰을 절약합니다.

### 예제 3: 버그 수정

```bash
$ claude "src/cart/calculator.ts의 calculateTotal에서
  할인율이 100%를 초과할 때 음수 금액이 되는 버그가 있어.
  할인율을 0~100% 범위로 제한해줘."
```

```typescript
// Before (버그)
const discounted = price * (1 - discount / 100);

// After (수정됨)
const clampedDiscount = Math.min(Math.max(discount, 0), 100);
const discounted = price * (1 - clampedDiscount / 100);
```

Claude Code가 정확히 해당 줄만 찾아 교체합니다. 나머지 코드는 그대로 유지됩니다.

---

## 6.3 다중 파일 수정

실제 기능 구현은 여러 파일을 동시에 건드립니다. Claude Code는 이를 한 번의 요청으로 처리합니다.

### 예제 4: API 엔드포인트 추가

```bash
$ claude "사용자 프로필 조회 API를 만들어줘.
  - src/routes/user.ts에 GET /users/:id 라우트 추가
  - src/services/userService.ts에 getUserById 함수 추가
  - src/types/user.ts에 UserProfile 타입 정의
  - tests/user.test.ts에 테스트 작성"
```

Claude Code는 다음 순서로 작업합니다.

1. 타입 정의를 먼저 생성합니다
2. 서비스 로직을 구현합니다
3. 라우트를 연결합니다
4. 테스트를 작성합니다

**의존성 순서를 자동으로 파악합니다.** 여러분이 순서를 지정할 필요 없습니다.

각 파일 수정마다 승인을 요청합니다. 전체를 검토한 뒤 하나씩 승인하세요.

> **주의**: 한 번에 너무 많은 파일을 수정하면 컨텍스트 윈도우를 빠르게 소모합니다. 관련 파일 5~6개 이내로 유지하는 것이 좋습니다.

---

## 6.4 권한 모드 전환

파일을 수정할 때마다 매번 승인하는 것이 번거로울 수 있습니다. 상황에 따라 권한 모드를 전환하세요.

### 권한 모드 비교

| 모드 | 파일 수정 | 명령 실행 | 용도 |
|------|---------|---------|------|
| **default** | 매번 확인 | 매번 확인 | 처음 사용, 중요한 코드 |
| **acceptEdits** | 자동 승인 | 확인 | 반복 수정 작업 |
| **plan** | 불가 | 불가 | 계획 검토만 |
| **bypassPermissions** | 모두 자동 | 모두 자동 | 신뢰할 수 있는 작업 |

### Shift+Tab으로 모드 전환

대화 중 언제든 `Shift+Tab`을 누르면 권한 모드를 전환할 수 있습니다. 가장 자주 쓰는 패턴은 이렇습니다.

**추천 워크플로우**:
1. `plan` 모드로 수정 계획을 검토합니다
2. 계획이 만족스러우면 `acceptEdits`로 전환합니다
3. Claude Code가 파일 수정을 자동으로 진행합니다
4. 완료 후 `default`로 돌아옵니다

```bash
# Plan 모드에서 시작
$ claude
> [Shift+Tab → plan 선택]
> "src/auth 모듈을 리팩토링하려고 해. 계획을 세워줘."

[Claude이 수정 계획만 제시하고, 실제 수정은 하지 않음]

> [Shift+Tab → acceptEdits 선택]
> "좋아, 실행해줘."

[파일 수정이 승인 없이 자동으로 진행됨]
```

> **주의**: `bypassPermissions` 모드는 셸 명령도 자동 실행합니다. 프로덕션 코드에서는 사용을 자제하세요. `acceptEdits`가 대부분의 경우 충분합니다.

---

## 6.5 안전망: 체크포인트와 되돌리기

수정이 잘못되었을 때 당황하지 마세요. Claude Code는 안전망을 제공합니다.

### 자동 체크포인트

Claude Code가 파일을 수정할 때마다 Git 체크포인트가 자동 생성됩니다. 이는 일반 커밋과 별개로, Claude Code 전용 복원 지점입니다.

### /rewind로 되돌리기

```bash
$ claude
> "src/auth/login.ts를 리팩토링해줘"

[Claude이 수정 완료]

> "아, 이전이 더 나았어."
> /rewind

[체크포인트 목록이 표시됨]
[원하는 시점을 선택하면 코드가 복원됨]
```

### 예제 5: 수정 후 복원

```bash
$ claude
> "calculatePrice 함수를 화살표 함수로 바꿔줘"

[수정 완료 - 그런데 테스트가 깨짐]

> /rewind
[수정 전 상태로 복원]

> "calculatePrice 함수를 화살표 함수로 바꾸되,
   기존 테스트가 통과하는지 확인하면서 진행해줘."

[이번에는 테스트를 실행하며 안전하게 수정]
```

> **팁**: `/rewind`는 파일 상태만 되돌립니다. 대화 컨텍스트는 유지되므로, 이전 시도에서 배운 것을 활용할 수 있습니다.

---

## 정리

이번 챕터에서 배운 핵심을 정리합니다.

| 주제 | 핵심 포인트 |
|------|------------|
| 수정 요청 | 위치 + 문제 + 방법을 구체적으로 |
| Write vs Edit | 새 파일은 Write, 부분 수정은 Edit |
| 다중 파일 | 한 번의 요청으로, 5~6개 이내 권장 |
| 권한 모드 | plan → acceptEdits 워크플로우 추천 |
| 안전망 | /rewind로 언제든 복원 가능 |

다음 챕터에서는 테스트 작성과 디버깅을 다룹니다. Claude Code와 함께 TDD 워크플로우를 실전에서 활용하는 방법을 알아보겠습니다.
