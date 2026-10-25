# Mook H안 Astro 정식 이식: 배포 안내

## 반영한 디자인 결정

- B안의 좌측 고정 메뉴(모바일에서는 상단 메뉴), A안의 따뜻한 논문·노트 카드.
- Publications와 Study Notes는 **하나의 SearchFilter.astro**를 공유. 입력창, 분야 버튼, 키워드 버튼의 크기·배경·간격·동작이 완전히 동일.
- 텍스트 검색, 분야 선택, 키워드 선택을 동시에 적용. 결과 수, 비어 있는 결과 안내, Clear filters 포함.
- 대표 키워드 6개를 먼저 보여주고 나머지는 More keywords 안에 배치해 항목이 늘어도 혼잡해지지 않도록 설계.
- 노트 PDF를 새 탭에서 열거나 내려받을 수 있음.
- BibTeX와 Markdown 메타데이터에서 목록·필터 항목을 빌드 시 자동 생성.
- 연구 소개에서 관련 Publication으로 직접 연결.

## 확인된 데이터

- BV Formalism (23쪽), Non-commutative Geometry (19쪽), Haldane Gap & LSM (16쪽).
- 기존 네 편의 BibTeX 기록 보존. Google Scholar 전체 목록 자동 연동 아님.
- Cluster Model 및 Notion 연결은 정식 사이트의 Notes 목록에서 제외.

## 설치 시 주의

1. GitHub Desktop에서 `main`을 Pull하여 현재 버전 확보, 별도 브랜치 생성.
2. 전체 소스 ZIP 내용물을 저장소 루트에 복사. **`.git` 삭제 금지.**
3. 과거 UI 파일 `src/styles/global.css`, `src/styles/notes-compact.css`, 과거 `src/content/notes/cluster-model.md` 및 더는 공개하지 않을 cluster 다운로드 파일 제거. 다른 사용자 수정 파일이 있다면 무조건 지우지 말고 비교.
4. PR을 만들고 `Verify Astro pull request` 빌드가 통과하면 `main`으로 Merge.
5. `Deploy academic homepage` 성공 후 https://mookphysics.org 방문.

**중요:** 로컬 환경의 npm registry 접근이 차단되어 Astro 전체 컴파일은 아직 검증하지 못했습니다. GitHub PR 빌드 검사 결과를 반드시 확인해 주세요. 예전 ZIP을 단순 덮어쓴 뒤 일부 파일이 누락되는 문제를 피하기 위해 위 전체 변경 파일을 GitHub Desktop에서 확인하는 것이 좋습니다.
