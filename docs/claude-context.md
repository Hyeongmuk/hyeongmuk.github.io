# 웹사이트 작업 맥락 — 수정 이력, 데이터 구조, QA

> 원본: 사용자가 제공한 `01_WEBSITE_HANDOFF_KO.md`, `03_QA_AND_WORKFLOW.md`를 요약·정리한 문서.
> 기준 시점: 2026-10-29 18:34 KST, `main` 커밋 `8784e2a36e68e14ba2253eeae5780a23b4abe2a0`.
> **실제 파일과 최신 커밋이 이 문서보다 우선한다.** 작업 규칙 자체는 루트의 `CLAUDE.md`를 따른다.
> 방문자에게 공개되는 파일이 아니다 (Astro는 `src/pages/`와 `public/`만 빌드한다).

## 1. 프로젝트 개요

| 항목 | 값 |
|---|---|
| 공개 사이트 | https://mookphysics.org |
| 저장소 | https://github.com/Hyeongmuk/hyeongmuk.github.io (기본 브랜치 `main`) |
| 스택 | Astro 5 정적 사이트, Node.js 22, npm, CSS, 소량의 브라우저 JS, KaTeX/Markdown 수식 |
| 배포 | `main` push → GitHub Actions(테스트·빌드·QA) → GitHub Pages |
| 사용자 로컬 환경 | Mac, GitHub Desktop → Repository → Open in Terminal; `npm ci`, `npm run dev` |

"배포 성공"은 HTML이 빌드·업로드되었다는 뜻일 뿐, 데스크톱·모바일 시각 검수 완료를 뜻하지 않는다.

## 2. 수정 이력 (2026-10, KST)

GitHub PR/커밋과 이전 협업 대화를 종합한 재구성이며, 모든 중간 단계가 남아 있지는 않다.

| 시기 | 변화/결정 | 주의점 |
|---|---|---|
| 10/25 | 정식 H 디자인 확립: B안의 좌측 고정 사이드바 + A안의 논문·노트 카드. PR #6 `hybrid-design-release` | 시각적 기준선 |
| 10/26 | Home/Research/About, CV, 사진, 논문·Notes 데이터, 모바일, SEO를 PR #7–17로 확장·복원 (PR #12 `restore-astro-pages-404` 포함) | 과거 ZIP 전체 덮어쓰기로 누락·충돌 발생 |
| 10/26 | Home 대표 논문 2편, Research 3개 범주, Notes PDF·본문·자동 필터 | 확립된 성과와 향후 관심 구분 |
| 10/27 | PR #18 `261027-research`: Research 페이지·메타데이터 통합. CI 실패 후 PR #19 `fix-ci-20261027` | Home/Research/Publications가 같은 BibTeX + 메타데이터 사용 |
| 10/29 오후 | PR #20 `261029-students`: For Students / Physics Stories 에세이, 도해, 공통 제목 위계 | Students와 Research가 같은 QK SVG 경로 참조 |
| 10/29 18:15 | PR #21 `261029-patch`: UX/코드/그림 후속 패치. 배포 실패 (§3 오류 A) | 링크를 지우지 않고 금지 테스트만 추가 |
| 10/29 18:18 | `9b9a3f2` Students 링크 수정 → 배포 성공 | |
| 10/29 18:22 | `9586337` `node_modules`, `dist`, `.astro` Git 추적 해제 | `.gitignore`만으로는 이미 추적된 파일이 해제되지 않음 |
| 10/29 18:31 | `2a73851` Research SVG·캡션을 `18f71e4` 기준으로 복원. 테스트 1개 실패 (§3 오류 B) | 복원이 아니라 오래된 테스트가 문제 |
| 10/29 18:34 | `8784e2a` `tests/visitor-polish.test.mjs` 수정 → 29/29 통과, 빌드·배포 성공 (run `40850677396`) | 마지막으로 검증된 상태 |

### 이전 AI 작업에서 반복된 사고

1. Research 그림 아래 한 줄 캡션과 논문 링크를 키우고 긴 설명 문단(`figure-explainer`)을 추가해 화면을 어지럽힘.
2. `public/research/quaternion-kahler-geometry.svg`의 "제목 수정"을 이유로 SVG 내부 텍스트 좌표를 옮겨 `Quaternion–Kähler geometry` 제목이 수학식과 겹침.
3. 사용자가 삭제를 요청한 Students의 `Browse study notes ↗`를 그대로 둔 채 CI 금지 검사만 추가해 배포 실패.
4. 원본 그림을 복원하자, AI가 만든 테스트가 정상 원본을 실패로 판정해 배포를 막음.
5. 방문자 화면에 `Publication metadata is maintained in BibTeX`, `New papers are added by editing src/data/publications.bib` 같은 개발자용 문구 노출.

## 3. CI 실패 이력과 교훈

**오류 A — 금지 문구가 실제 HTML에 남음** (run [40848277632](https://github.com/Hyeongmuk/hyeongmuk.github.io/actions/runs/40848277632))

```text
students/index.html: developer-only copy appears publicly (Browse study notes ↗)
Error: Public-site verification found 1 problem(s).
```

원인: `src/data/students-landing.html`의 링크는 그대로 두고 검사만 추가. 해결: 원문에서 링크 제거(`9b9a3f2`).

**오류 B — 정상 원본 복원을 테스트가 거부** (run [40850282470](https://github.com/Hyeongmuk/hyeongmuk.github.io/actions/runs/40850282470))

29개 중 `geometry figure title is real editable vector text, not split words` 1개 실패. 이전 AI의 테스트가 잘못 바뀐 SVG 제목과 `figure-explainer`를 강제하고 있었음. 해결: 원본 그림·캡션 보존을 확인하도록 테스트 수정(`8784e2a`).

**원칙:** 테스트가 실패하면 방문자 콘텐츠나 연구 그림을 바꾸기 전에 *테스트의 전제가 정당한지* 먼저 판단한다. 테스트는 사용자의 결정을 보호해야 하며, 실수로 만든 구현을 고정해서는 안 된다.

### Actions 실패 스텝 해석

워크플로: `pr-check.yml`(PR to `main` 검증), `deploy.yml`(push to `main` → 검증 → Pages 배포).

| 실패 스텝 | 의미 |
|---|---|
| `Install dependencies` | npm lock/registry/Node 문제. `package.json`/lock 대조 |
| `Test metadata and BibTeX parser` (`npm test`) | 콘텐츠·회귀 테스트 실패. 어느 테스트인지, 전제가 타당한지 확인 |
| `Verify site source files` | bib 메타데이터, 노트 링크·PDF·관계 문제 |
| `Build Astro` | Astro/JS/Markdown 컴파일 오류 |
| `Verify generated site pages` | dist route 또는 공개 노트 route 누락 |
| `Check public-facing links and copy` | 빌드된 HTML의 내부 링크 깨짐 또는 금지된 개발자 문구 |
| `Upload Pages artifact` / `Deploy` | 앞 단계가 모두 성공했다면 Pages 환경·권한 로그 확인 |

## 4. 페이지별 역할과 변경 경계

| URL | 파일 | 유지할 내용 |
|---|---|---|
| `/` | `src/pages/index.astro` | 연구 질문, 프로필 사진, 소속/학위 예정, 연구 분야 3개, 대표 논문 2편, 대표 Study Notes |
| `/research/` | `src/pages/research.astro` | `#geometry` / `#topology` / `#manybody`, QK 원본 그림 + 원래 캡션 |
| `/publications/` | `src/pages/publications.astro` | 논문 4편, 검색·분야·키워드 필터, 연도별 분류. 개발자 안내 금지 |
| `/notes/` | `src/pages/notes/index.astro` | 공개 노트 7개, 검색/필터, PDF 새 탭 읽기·다운로드 |
| `/notes/[slug]/` | `src/pages/notes/[slug].astro` | 노트 상세, Markdown 본문, PDF, 관련 노트 |
| `/students/` | `src/pages/students/index.astro`, `src/data/students-landing.html` | Physics Stories 목록/소개. Notes CTA 추가 금지 |
| `/students/band-theory/` | `src/pages/students/band-theory.astro`, `src/data/students-essay.html` | "How Does an Electron See Its Universe?" 에세이, 도해 6개, 참고문헌 |
| `/about/` | `src/pages/about.astro` | 소개, 학위/지도교수, CV 보기·다운로드, 연락처/학술 프로필 |
| `/sitemap.xml` | `src/pages/sitemap.xml.ts` | 정적 색인 (노트 route 포함) |

### Research의 세 범주

1. **Quantum Geometry (established):** Chern band의 Kähler 기하, 시간반전 대칭 Kramers 쌍의 quaternion-Kähler / 비가환 양자기하. 이 기하 프레임워크가 상관 위상 상태 자체를 입증했다고 과장하지 않는다.
2. **Band Topology (established):** Real Hopf insulator, 점유/비점유 상태의 전체 wave-function 구조와 delicate topology, unconventional transitions.
3. **Correlated Quantum Matter (broader interests):** many-body correlations, topological order, SPT, generalized symmetries. **확립된 성과가 아닌 향후 방향**임을 분명히 구분한다.

`CONTENT_REVIEW_EN.md`에 사용자가 검토한 영문 카피와 과학적 표현 범위가 기록되어 있다. 전문적 주장을 바꿀 때는 사용자 확인을 받는다.

### Research의 Quaternion–Kähler 그림 (회귀 방지 핵심)

- 자산: `public/research/quaternion-kahler-geometry.svg`, 복원 기준 커밋 `18f71e41d8de66483cba4b8add7b4ff445b0eba0`. `src/pages/research.astro`와 SVG는 이 커밋과 blob SHA가 일치하도록 복원되었다.
- `src/data/students-essay.html`도 같은 SVG를 참조한다. 이 파일을 바꾸면 두 화면 모두 영향을 받는다.
- 원래 캡션 (문자열 그대로 보존):
  - `Comparison of Kähler geometry in Chern bands with quaternion-Kähler geometry of Kramers pairs.`
  - `View larger ↗` (SVG를 새 탭으로; 가능하면 캡션과 같은 행, 좁은 화면에서는 자연스럽게 줄바꿈)
  - `Associated paper: Quaternion-Kähler geometry of time reversal symmetric crystals (2026) ↗`
- 캡션 스타일은 `src/pages/research.astro`의 scoped CSS(`.geometry-research-figure figcaption` 12px/1.6, `.figure-source` 11.5px). 요청 없이 바꾸지 않는다.
- 이 SVG는 벡터와 내장 raster image가 섞여 있다. 제목·label·transform 좌표를 자동 검색/치환하거나 파일을 재생성하지 않는다. 변경이 꼭 필요하면 사용자에게 정확한 원본/요청을 받고 → 여러 뷰포트에서 비교 → 작은 diff → 검증.
- 과거 사용자가 새 그림을 별도로 제공했는데 반영되지 않았다는 지적이 있었다. 현재 저장소의 SVG가 그 최신 파일인지는 **확인된 바 없다**. 임의로 생성·대체하지 말고 필요하면 사용자 제공 원본과 비교한다.

## 5. 데이터 출처

### Publications

- `src/data/publications.bib`: BibTeX 원본 (현재 4편)
- `src/data/publication-meta.json`: `featured`, `summary`, `tags`, `areas`(복수) 등 수동 큐레이션. 논문 순서는 모든 탭에서 출판 연월 최신순(`publications.bib`의 `year`, `month`)
- `src/lib/bibtex.mjs`: BibTeX 파서
- `src/lib/publications.mjs`: 단일 `publications` 집합, Home의 `featuredPublications`, Research의 `researchPublications(area)`
- `src/components/PaperCard.astro`: 공통 논문 카드. URL/출처를 중복 구현하지 않는다 (PDF 링크 중복 문제를 고친 이력 있음).
- Featured는 정확히 2편: `lim2026quaternion`, `lim2023hopf`.
- Google Scholar와 자동 동기화하지 않는다. 근거는 `PUBLICATION_SOURCES.md` (Scholar 429, 4편 수기 대조). 새 논문의 출판 상태는 임의로 확정하지 않는다.

### Notes

- `src/content/notes/*.md`: Astro 콘텐츠 컬렉션, `src/content.config.ts`의 Zod schema.
- 필드: `title`, `description`, `date`, `topic`, `category`, `tags`, `relations`, `featured`, `complete`, `pages`, `status`, `pdf`, `downloads`.
- `status: published`만 공개. `complete: true`는 작성 완결을 뜻하며 peer review가 아니다.
- PDF는 `public/downloads/`. `src/components/NoteCard.astro`의 Read PDF/Download 동작과 상세 페이지 연결을 유지한다.
- 범주: qft, mathematics, condensed (`src/data/categories.mjs`).
- 공개 노트 7개: `bv-formalism`, `cotangent-complex`, `haldane-gap-lsm`, `noncommutative-geometry`, `planar-diagram-algebra-3d-tqft`, `quantization-constrained-systems-abelian-higgs`, `toric-code-demystified`.
- `src/components/SearchFilter.astro` + `public/scripts/search-filter.js`: Publications/Notes 공유 필터 (텍스트·분야·키워드, 결과 수, 초기화).

### Students 에세이 그림

- `public/students/fig*.webp` 6개는 `figures-source/`의 matplotlib 스크립트로 생성한다. 그림을 고칠 때는 webp를 직접 편집하지 말고 스크립트를 고친 뒤 다시 빌드한다 (절차: `figures-source/README.md`의 "Website export").
- 2026-10-29: 예전 webp는 원본 PNG 위에 글자를 덧그린 편집본이었고 FIG. 05 제목 위에 잔상이 있었다. 소스에서 글자 1.5배(`WEB_TEXT_SCALE`)로 다시 생성해 교체했다.

### About / 신원 정보 (현재 공개 소스 기준)

- 이름: **Hyeongmuk Lim (Mook)**. Ph.D. Candidate, 서울대학교 물리천문학부 석박사통합과정, 지도교수 **Prof. Bohm-Jung Yang**.
- 학위 완료 예상: **August 2027** (시간이 지나면 사용자 확인 후 수정).
- 프로필 `public/profile-hyeongmuk-lim.webp`, CV `public/downloads/Hyeongmuk_Lim_CV.pdf`, ORCID `https://orcid.org/0009-0001-0036-5355`.
- 이메일·Google Scholar 링크·경력 정보는 사용자 확인 없이 바꾸지 않는다.

## 6. 디자인 기준

- H안: 데스크톱 좌측 고정 내비게이션, 모바일 상단 햄버거 메뉴, Publications/Notes는 읽기 쉬운 editorial 카드/행 목록.
- 따뜻한 오프화이트 배경, 차분한 녹색 강조, 간결한 학술 분위기. 장식용 그림, 과한 강조문/배지는 피한다.
- 사용자는 전반적 글자 크기가 작다고 지적한 적이 있다. 다만 국소 수정을 이유로 다른 페이지의 글꼴·밀도를 일괄 바꾸지 않는다.
- `mailto:`는 새 탭 링크가 아니므로 `↗`를 붙이지 않는다.
- 키보드 포커스, 모바일 터치 영역, `prefers-reduced-motion`, alt 텍스트, 좁은 폭에서의 줄바꿈을 확인한다.

## 7. 기술부채 (별도 승인 전에는 손대지 않음)

- `src/styles/site.css`: `BASE`, `B`, `HYBRID`, `PRODUCTION`, `REFINEMENT`, `VISITOR POLISH` 등 역사적 오버라이드가 누적됨. 정리는 사이트 전역 변경이므로 범위 승인과 전후 비교가 필수.
- `src/data/students-essay.html`: 큰 raw HTML. 자동 포매터나 정규식 치환이 도해·인용·수식을 망가뜨릴 수 있으므로 부분 수정 후 검증.
- `.gitignore`에 `node_modules/`, `dist/`, `.astro/`, `.DS_Store`가 중복 선언됨 (기능상 문제 없음).
- `.DS_Store` 4개(`/`, `public/`, `src/content/`, `src/pages/`)가 여전히 Git에 추적됨.
- `README.md`의 "title typography repaired" 표현은 원본 SVG 복원 이후 맥락과 맞지 않는다. 고친다면 문서 표현만 고치고, SVG를 그 문구에 맞추지 않는다.
- `package.json`, `package-lock.json`은 계속 추적해야 한다 (`node_modules`, `dist`, `.astro`만 추적 해제 대상).

## 8. 열린 검토 항목 (자동으로 전부 고칠 목록이 아님)

1. **브라우저 시각 검수:** 원본 복원 후 QK 그림의 제목·수식 겹침이 사라졌는지 데스크톱/모바일 스크린샷으로 확인.
2. **연구 그림 최신성:** §4 참조. 사용자 제공 최신 원본과 대조 필요.
3. **디자인 세부:** 글자 크기·정보 밀도, 모바일 메뉴, 캡션을 여러 뷰포트에서 점검.
4. **기술부채:** §7. 독립된 소규모 패치로 제안.
5. **콘텐츠 정합성:** 논문/학위/CV 정보가 최신인지 사용자 확인.

## 9. 브라우저 QA 체크리스트

`npm run dev` 후 권장 뷰포트: 1440×900, 1280×800, 768×1024, 390×844, 320×700.

- [ ] Home: 사진이 얼굴을 어색하게 자르거나 텍스트와 겹치지 않음. Featured 논문 정확히 2편.
- [ ] Research: 세 범주의 established / broader interests 구분 정확.
- [ ] Research QK 그림: 제목과 `k_t + k_y J` 등 수식이 겹치지 않음. 내부 label이 잘리거나 덮이지 않음.
- [ ] QK 캡션: 한 줄 비교 문장 + `View larger ↗`, 다음 행 `Associated paper`만. `figure-explainer` 없음.
- [ ] Research "Related publications": 제목 대소문자 자연스러움, 중복 링크 없음.
- [ ] Publications: 제목/저자/연도 검색, area, keyword, 복합 필터, reset, 결과 수, no-results. 개발자 문구 없음.
- [ ] Notes: 7개 route, 필터·reset, PDF 새 탭/다운로드, 상세·관련 노트 링크.
- [ ] Students: 제목 위계, 에세이 도해 6개·참고문헌·공유 SVG 링크. `Browse study notes ↗` 없음.
- [ ] About: 프로필, CV 열기/다운로드, 이메일/ORCID/Scholar 링크.
- [ ] 모바일: 햄버거 메뉴 열기/닫기/Escape, 포커스 표시, 가로 스크롤 없음.
- [ ] `↗`(새 탭) / `→`(내부 이동) 표시와 실제 동작 일치.
- [ ] 요청하지 않은 페이지에서 간격·글자 크기·색·이미지 너비가 바뀌지 않았는지 전후 스크린샷 비교. 결과를 고쳤다면 같은 뷰포트의 before/after와 커밋 SHA를 남긴다.

## 10. 보고 양식

- **요구사항:** 바꾸라고 한 것과 바꾸지 말라고 한 것.
- **Diff:** 변경 파일, 핵심 변경, 다른 화면에 영향이 없는 이유.
- **테스트:** 실행 명령, 결과, 통과 개수, 실행하지 않은 항목.
- **시각 QA:** 실제 브라우저 확인 여부, 뷰포트, 스크린샷.
- **배포:** PR/커밋/Actions run ID와 성공 여부. 코드만 작성했다면 배포 완료라고 하지 않는다.
- **롤백:** 새 커밋 revert 또는 특정 파일 복구 방법. 사용자의 미커밋 변경을 파괴하지 않는다.

## 11. 참고 링크

- 최종 성공 CI/배포: https://github.com/Hyeongmuk/hyeongmuk.github.io/actions/runs/40850677396
- 그림·캡션 복원 기준: https://github.com/Hyeongmuk/hyeongmuk.github.io/commit/18f71e41d8de66483cba4b8add7b4ff445b0eba0
- 검증 기준 HEAD: https://github.com/Hyeongmuk/hyeongmuk.github.io/commit/8784e2a36e68e14ba2253eeae5780a23b4abe2a0
- PR #20 Students: https://github.com/Hyeongmuk/hyeongmuk.github.io/pull/20
- PR #21 Oct 29 patch: https://github.com/Hyeongmuk/hyeongmuk.github.io/pull/21
