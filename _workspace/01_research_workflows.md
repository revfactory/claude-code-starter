# Claude Code 실전 워크플로우 및 베스트 프랙티스 조사 보고서

## 1. Git 워크플로우

### 1.1 커밋 생성
```bash
# 대화형
> 커밋 메시지와 함께 변경사항을 커밋해줘

# 비대화형
claude -p "Look at my staged changes and create a commit" \
  --allowedTools "Bash(git diff *),Bash(git commit *)"
```
- staged 변경사항 자동 분석
- 적절한 커밋 메시지 자동 생성

### 1.2 PR 생성/관리
```bash
# 대화형
> create a pr

# PR에서 세션 시작
claude --from-pr 123
```
- gh CLI 통합
- 자동 PR 설명 생성

### 1.3 코드 리뷰
- Writer/Reviewer 패턴 (별도 worktree)
- CI/CD 자동 리뷰 통합

### 1.4 브랜치 관리
```bash
claude --worktree feature-auth     # 격리된 worktree
claude --worktree bugfix-123       # 병렬 작업
```

---

## 2. 개발 워크플로우

### 2.1 TDD 워크플로우
1. 테스트 작성 (Red): "Write failing tests for validateEmail"
2. 구현 (Green): "Implement to make all tests pass"
3. 리팩토링 (Refactor): "Refactor while keeping tests green"

### 2.2 디버깅 워크플로우
1. 버그 재현: 에러 메시지/로그 제공
2. 근본 원인 파악: 코드 추적
3. 수정: 테스트 작성 → 수정 → 검증

### 2.3 리팩토링 워크플로우
- Plan Mode로 시작 (안전한 계획 수립)
- 계획 검토 후 Normal Mode로 구현
- 테스트로 검증

### 2.4 새 프로젝트 시작
```bash
claude
> /init          # CLAUDE.md 자동 생성
> give me an overview of this codebase
```

---

## 3. 효과적인 프롬프트 작성법

### 3.1 좋은 프롬프트 원칙

#### 나쁜 프롬프트 (추상적)
```
로그인 기능을 개선해줘
이 함수를 최적화해줘
```

#### 좋은 프롬프트 (구체적)
```
The checkout flow is broken for users with expired cards.
Check src/payments/ for the issue.
Write a failing test first, then fix it.
```

### 3.2 구체적 지시의 중요성
- 파일 위치 지정
- 검증 방법 정의
- 기대 결과 명시
- 비교 예시: 스크린샷, before/after

### 3.3 컨텍스트 제공
- `@파일경로`로 파일 참조
- 이미지/스크린샷 붙여넣기 (Ctrl+V)
- MCP 리소스 참조

### 3.4 반복 대화
1. 탐색: "What would you improve?"
2. 계획: "Create a plan for improvements"
3. 정제: "Prioritize: 1. session timeout 2. token refresh"
4. 구현: "Implement the first priority with tests"

---

## 4. 헤드리스/비대화형 모드

### 4.1 `-p` 플래그
```bash
claude -p "Explain what this project does"              # 한 번 실행
claude -p "List API endpoints" --output-format json      # JSON 출력
claude -p "Analyze" --output-format stream-json          # 스트리밍
```

### 4.2 CI/CD 통합
```yaml
# GitHub Actions
- name: Review PR
  run: |
    gh pr diff ${{ github.event.pull_request.number }} | \
    claude -p "Review this code" --output-format json > review.json
```

### 4.3 스크립트에서 호출
```bash
# 배치 처리
while IFS= read -r file; do
  claude -p "Migrate $file from CommonJS to ESM" \
    --allowedTools "Edit" --output-format json
done < files.txt
```

### 4.4 유용한 옵션
- `--max-budget-usd 5.00`: 예산 제한
- `--max-turns 3`: 턴 제한
- `--allowedTools "Read,Edit"`: 도구 제한
- `--append-system-prompt "..."`: 시스템 프롬프트 추가

---

## 5. 보안 고려사항

### 5.1 권한 모드별 의미
| 모드 | 파일 수정 | 명령 실행 |
|------|---------|---------|
| default | 매번 확인 | 매번 확인 |
| acceptEdits | 자동 승인 | 확인 |
| plan | 불가 | 불가 |
| dontAsk | 사전 허용만 | 사전 허용만 |
| bypassPermissions | 자동 | 자동 (위험) |

### 5.2 민감 파일 보호
```json
{
  "permissions": {
    "deny": [
      "Read(**/.env)", "Read(**/.env.*)",
      "Read(~/.ssh/**)", "Read(~/.aws/**)",
      "Read(**/*credential*)", "Read(**/*secret*)"
    ]
  }
}
```

### 5.3 API 키 관리
- 환경 변수로 관리 (파일 저장 X)
- macOS Keychain 활용
- `--allowedTools`로 도구 제한

---

## 6. 팁 & 트릭

### 6.1 컨텍스트 관리
- `/context`로 사용량 확인
- `/compact focus on API changes`로 정리
- 2번 이상 수정하면 `/clear` 후 재시작

### 6.2 Subagent 활용
```
Use subagents to investigate:
- Authentication module
- Database schema
- API patterns
```

### 6.3 세션 관리
```bash
/rename oauth-migration      # 이름 지정
claude --resume oauth-migration  # 재개
```

### 6.4 CLAUDE.md 최적화
- 50-100줄 간결하게
- 빌드 명령, 코드 스타일, 테스트 규칙 중심
- 상세 가이드는 rules/ 또는 skills로 분리

### 6.5 흔한 실수
1. **Kitchen Sink 세션**: 무관한 작업 혼합 → `/clear`로 분리
2. **반복 수정**: 2번 이상이면 더 정확한 프롬프트로 새 세션
3. **과도한 CLAUDE.md**: 300줄+ → Claude가 중요 규칙 무시

### 6.6 Worktree 병렬 작업
```bash
# 터미널 1: Feature
claude --worktree feature-auth

# 터미널 2: Bugfix
claude --worktree bugfix-session

# 터미널 3: Review
claude --worktree review-code
```
