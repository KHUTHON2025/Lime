# Lime

## 규칙

### 코드 스타일

- Python 코드는 [PEP 8](https://peps.python.org/pep-0008/)을 따릅니다.
- 들여쓰기는 4칸 공백을 사용합니다.
- 변수와 함수 이름은 `snake_case`를 사용합니다.

### Git 커밋 메시지

- 형식: `<type>: <subject>`, 예: `feat: add readme`.
  - **예시**:
    - `feat: 사용자 로그인 구현`
    - `fix: 시작 시 충돌 해결`
    - `docs: API 문서 업데이트`
- 자주 사용하는 타입: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.
- 명령형 어조를 사용합니다 (예: "기능 추가" 대신 "기능 추가하기").
- 제목은 50자 이내로 작성합니다.
- 필요시 본문에 상세 설명을 포함합니다.

### 파일 구성

- 모든 Python 스크립트는 `src` 디렉토리에 배치합니다.
- 단위 테스트는 `tests` 폴더에 작성합니다.
- 설정 파일은 `config` 디렉토리에 저장합니다.

### 문서화

- README 및 기타 문서 파일은 Markdown 형식을 사용합니다.
- 코드 변경 시 문서를 최신 상태로 유지합니다.
