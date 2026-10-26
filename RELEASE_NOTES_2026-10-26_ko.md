# Mook Academic Website — 2026-10-26 개편

이 릴리스는 사용자가 확정한 H 디자인(B안의 좌측 고정 메뉴 + A안의 Publication/Note 카드)을 유지한 콘텐츠·사용성·SEO 개편입니다. 별도 이미지가 준비되지 않은 연구 영역에 임의의 학술 그림을 추가하지 않았습니다.

## 실제 수정 내용

- Home에 사용자 제공 사진과 현재 연구 질문 추가. 기재된 박사 졸업 예정 시점은 2027년 8월.
- 대표 논문 **Quaternion-Kähler geometry of time reversal symmetric crystals** 와 **Real Hopf insulator** 두 편 지정. 나머지 논문 2편은 Publications 전체 목록에 보존.
- Research를 Quantum Geometry / Band Topology / Correlated Quantum Matter로 구성. 앞 두 영역은 기존 연구 성과, 세 번째 영역은 **앞으로 탐구하려는 방향**으로 명시. Quaternion-Kähler 연구가 상관 위상 상태의 안정화를 이미 증명했다는 주장 금지.
- About에 지도교수 Bohm-Jung Yang, 석박사통합과정, 2027년 8월 박사 졸업 예정, 사용자 제공 프로필 사진, CV 보기·다운로드, ORCID 링크 추가.
- CV: 마지막으로 확정된 **Hyeongmuk_Lim_CV_Mook_APS_2025.pdf** 사용. 실제 사이트 파일명은 `public/downloads/Hyeongmuk_Lim_CV.pdf`.
- Notes의 다섯 PDF 유지/포함: BV formalism, noncommutative geometry, Haldane gap/LSM, cotangent complex, planar diagram algebra/3D TQFT. 다섯 노트 모두 `complete: true`, 공개 상태 유지.
- Publications/Notes가 공유하는 `SearchFilter.astro` 및 기존 키워드 자동수집 방식을 변경 없이 유지.
- 검색엔진용 canonical URL, 소셜 메타데이터, Person JSON-LD, 동적 sitemap.xml 및 robots.txt를 추가.
- 기존 GitHub Pages/GitHub Actions 설정 보존.

## 확인된 자료와 검증 제한

- `npm test`: 총 11개 테스트 모두 성공.
- PDF 다섯 편, CV PDF, 프로필 사진 파일의 실재와 참조 메타데이터 검사 성공.
- npm/Astro 의존성 설치가 현재 실행 환경에서 불가능하여 실제 `npm run build` 완료 여부는 아직 확인하지 못함. `astro: not found`는 사이트 오류가 아니라 설치되지 않은 로컬 환경에서 실행했기 때문임.
- 브라우저의 데스크톱·모바일 렌더링은 자동화된 실제 화면 검증을 완료하지 못함. Pull Request의 CI 빌드와 웹 브라우저에서 추가 점검해야 함.
- ORCID URL은 사용자가 제공한 번호를 표준 공개 주소로 정규화함(`https://orcid.org/0009-0001-0036-5355`).

## GitHub Desktop 적용

1. 현재 `main`을 Pull.
2. 새 브랜치 `research-about-profile-2026` 생성.
3. **부분 업데이트 ZIP**을 압축 해제하여 내부 파일을 동일 경로로 덮어쓰기. `src`, `public`, `tests` 등의 폴더를 **병합 복사**, 다른 파일 삭제하지 않음. (전체 소스 ZIP은 재현·백업용.)
4. 변경 목록과 새 PDF/사진 파일을 확인하여 Commit → Push.
5. PR 검사(`npm test`, `npm run build`)가 녹색인지 확인한 후 `main`에 병합.
6. 배포 성공 후 `/`, `/research/`, `/publications/`, `/notes/`, `/about/`, `/downloads/Hyeongmuk_Lim_CV.pdf`, `/sitemap.xml` 확인.

**주의:** AI가 직접 GitHub에 Push하거나 라이브 사이트를 교체하지 않았습니다.

## 추후 자료 준비 시 개선할 것

- 연구 그림은 각 논문에서 사용을 허락받은 정확한 원본이 확보되면 추가.
- 연구별 2–3문장짜리 대표 성과 설명은 현재 버전을 바탕으로 계속 다듬을 수 있음.
- Google Scholar/CV와 journal publication status 주기적 대조.
