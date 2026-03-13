# 챕터 8: Git 워크플로우

> **학습 목표**
> - Claude Code로 커밋을 생성할 수 있다
> - PR(Pull Request)을 자동 생성할 수 있다
> - 브랜치 관리를 Claude Code에 맡길 수 있다
> - gh CLI 통합을 활용할 수 있다

---

Git은 개발자의 일상입니다.
코드를 쓰는 시간만큼, 커밋하고
PR을 만들고, 리뷰하는 시간도 깁니다.

Claude Code는 이 과정을 함께합니다.
변경사항을 분석하고, 커밋 메시지를 쓰고,
PR 설명까지 자동으로 생성해줍니다.

이번 챕터에서는 Git의 전 과정을
Claude Code와 함께 진행하는 법을 배웁니다.

---

## 8.1 스마트 커밋

### 커밋 메시지, 직접 쓰지 마세요

여러분은 코드를 수정했습니다.
이제 커밋할 차례입니다.
메시지를 고민하는 대신 이렇게 해보세요.

```bash
$ claude
> 변경사항을 확인하고 커밋해줘
```

Claude Code는 다음 단계를 자동으로 수행합니다.

1. `git diff`로 staged 변경사항을 분석합니다
2. 변경의 목적과 범위를 파악합니다
3. 적절한 커밋 메시지를 생성합니다
4. 여러분의 승인 후 커밋을 실행합니다

### 슬래시 커맨드로 더 빠르게

대화형 세션에서는 슬래시 커맨드가 편합니다.

```bash
> /commit
```

이 한 줄이면 충분합니다.
Claude Code가 staged 변경사항을 분석하고
커밋 메시지를 제안합니다.

### 커밋 메시지 스타일 지정

프로젝트마다 커밋 규칙이 다릅니다.
`CLAUDE.md`에 규칙을 적어두면
Claude Code가 그에 맞춰 메시지를 작성합니다.

```markdown
# CLAUDE.md
커밋 메시지는 한글로 작성합니다.
Conventional Commits 형식을 따릅니다.
예: feat: 로그인 API 추가
```

> **팁**: Claude Code는 최근 커밋 이력도 참고합니다. 기존 메시지 스타일과 자연스럽게 어울리는 메시지를 생성합니다.

---

## 8.2 PR 만들기

### 한 마디로 PR 생성

기능 개발을 마쳤습니다.
이제 PR을 만들어야 합니다.

```bash
$ claude
> PR 만들어줘
```

Claude Code는 `gh` CLI를 활용해
다음을 자동으로 처리합니다.

1. 현재 브랜치의 전체 커밋 히스토리를 분석합니다
2. base 브랜치와의 diff를 확인합니다
3. PR 제목과 본문을 자동 생성합니다
4. `gh pr create` 명령으로 PR을 등록합니다

### PR 설명의 품질

자동 생성된 PR 설명에는 다음이 포함됩니다.

- 변경 사항 요약 (Summary)
- 주요 수정 파일 목록
- 테스트 계획 (Test Plan)

더 구체적인 지시도 가능합니다.

```bash
> 이 PR은 인증 모듈 리팩토링이야.
> 보안 관련 변경사항을 강조해서 PR 만들어줘
```

### 기존 PR에서 작업 시작

이미 열린 PR을 기반으로 작업할 수도 있습니다.

```bash
$ claude --from-pr 142
```

해당 PR의 컨텍스트를 불러온 상태에서
세션이 시작됩니다.
리뷰 피드백을 반영하기에 좋습니다.

> **주의**: `gh` CLI가 설치되어 있어야 합니다. `brew install gh`로 설치한 뒤 `gh auth login`으로 인증하세요.

---

## 8.3 코드 리뷰 보조

### PR 리뷰 요청하기

동료의 PR을 리뷰해야 합니다.
Claude Code에게 도움을 요청해보세요.

```bash
$ claude
> gh pr diff 42를 보고 코드 리뷰해줘
```

Claude Code는 diff를 분석하고
다음 관점에서 리뷰 코멘트를 제안합니다.

- 잠재적 버그나 엣지 케이스
- 성능 이슈
- 네이밍과 가독성
- 테스트 커버리지 부족

### Writer/Reviewer 패턴

더 체계적인 리뷰 방법도 있습니다.
두 개의 Claude Code 세션을 활용하세요.

1. **Writer 세션**: 코드를 작성합니다
2. **Reviewer 세션**: 별도 Worktree에서 리뷰합니다

```bash
# 터미널 1 — Writer
$ claude --worktree feature-auth
> 인증 미들웨어를 구현해줘

# 터미널 2 — Reviewer
$ claude --worktree review-auth
> feature-auth 브랜치의 변경사항을 리뷰해줘
```

Writer와 Reviewer가 분리되면
더 객관적인 피드백을 받을 수 있습니다.

> **팁**: Reviewer 세션의 `CLAUDE.md`에 리뷰 기준을 명시하면 일관된 품질의 리뷰를 받을 수 있습니다.

---

## 8.4 브랜치 전략

### Worktree로 병렬 작업하기

여러 작업을 동시에 진행해야 할 때가 있습니다.
Worktree를 활용하면 브랜치별로
격리된 작업 환경을 만들 수 있습니다.

```bash
# 기능 개발
$ claude --worktree feature-payments

# 버그 수정
$ claude --worktree bugfix-session-timeout

# 문서 작업
$ claude --worktree docs-api-guide
```

각 Worktree는 독립된 디렉토리에서 동작합니다.
파일 충돌 없이 병렬 작업이 가능합니다.

### 브랜치 생성과 전환

브랜치 작업도 자연어로 가능합니다.

```bash
$ claude
> feature/user-profile 브랜치를 만들고 전환해줘
```

Claude Code가 `git checkout -b`를 실행합니다.
여러분은 승인만 하면 됩니다.

### 브랜치 정리

작업이 끝난 브랜치가 쌓여 있나요?

```bash
> 머지된 브랜치를 정리해줘
```

Claude Code가 이미 머지된 로컬 브랜치를
찾아서 삭제를 제안합니다.

> **주의**: 브랜치 삭제는 되돌리기 어렵습니다. Claude Code가 삭제 전 목록을 보여주면 꼭 확인하세요.

---

## 8.5 비대화형 Git

### CI/CD에서 자동 커밋

배포 파이프라인에서 Claude Code를 활용할 수 있습니다.
`-p` 플래그로 비대화형 실행이 가능합니다.

```bash
claude -p "staged 변경사항을 분석하고 커밋해줘" \
  --allowedTools "Bash(git diff *),Bash(git commit *)"
```

`--allowedTools`로 허용할 도구를 제한하면
안전하게 자동화할 수 있습니다.

### GitHub Actions에서 PR 리뷰

CI 파이프라인에 자동 리뷰를 추가할 수 있습니다.

```yaml
# .github/workflows/claude-review.yml
name: Claude Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Claude 리뷰 실행
        run: |
          gh pr diff ${{ github.event.pull_request.number }} | \
          claude -p "이 PR을 리뷰해줘. 버그, 성능, 보안 관점으로." \
            --output-format json > review.json
```

### 예산과 턴 제한

자동화에서는 비용 관리가 중요합니다.

```bash
claude -p "커밋 메시지를 생성해줘" \
  --max-turns 3 \
  --max-budget-usd 1.00
```

- `--max-turns`: 최대 대화 턴 수를 제한합니다
- `--max-budget-usd`: 비용 상한을 설정합니다

> **팁**: CI/CD에서는 `--max-budget-usd`를 항상 설정하세요. 예상치 못한 비용 발생을 방지할 수 있습니다.

---

## 정리

이번 챕터에서 배운 내용을 정리합니다.

| 작업 | 명령/프롬프트 | 핵심 포인트 |
|------|-------------|------------|
| 스마트 커밋 | `/commit` | staged 분석, 메시지 자동 생성 |
| PR 생성 | `PR 만들어줘` | gh CLI 통합, 설명 자동 작성 |
| 코드 리뷰 | `gh pr diff N 리뷰해줘` | diff 분석, 다각도 피드백 |
| 병렬 작업 | `--worktree 이름` | 격리 환경, 충돌 없는 병렬 |
| CI 자동화 | `-p` + `--allowedTools` | 비대화형, 예산 제한 |

Git 워크플로우의 반복적인 부분을
Claude Code에 맡기세요.
여러분은 코드와 설계에 집중할 수 있습니다.

다음 챕터에서는 **프로젝트 설정과 CLAUDE.md**를
더 깊이 다루겠습니다.
