# 노트 작성 브리프: 3차 곡면 위 직선의 가상 개수

> 이 문서는 새 채팅 세션에서 LaTeX 노트를 함께 작성하기 위한 배경 설명서입니다.
> 첫 메시지에 이 파일 전체를 붙여 넣고, 함께 첨부할 파일은 §8을 참고하세요.

---

## 1. 작성자와 목적

- **작성자:** Hyeongmuk Lim (Mook). 서울대학교 물리천문학부 이론물리 박사과정. 연구 분야는 양자 기하, 밴드 위상, 상관 양자 물질.
- **노트의 용도:** 개인 연구 홈페이지(mookphysics.org)의 *Study notes → Mathematics*에 PDF로 공개할 학습 노트. 동료 심사를 거친 논문이 아니라 개인 학습 노트이며, 사이트에도 그렇게 표시됩니다.
- **이 노트를 쓰는 이유:**
  1. 이미 공개한 두 노트를 잇는 후속편입니다.
     - *The 27 Lines on a Smooth Cubic Surface* (8쪽): 결론의 "Next steps"에서 Behrend–Fantechi의 가상 기본류와 Illusie의 cotangent complex를 다음 공부 방향으로 제시했습니다.
     - *Cotangent complex* (10쪽): Kähler 미분, cotangent complex, André–Quillen 코호몰로지, regular embedding과 conormal 모듈, 특이점에서 cotangent complex가 잡아내는 것.
  2. 장기 목표는 거울 대칭을 통한 열거 기하(Candelas–de la Ossa–Green–Parkes의 5차 3-fold 계산, Gromov–Witten 불변량)까지 가는 것입니다. 그 경로에서 가상류는 수학 쪽의 핵심 도구이고, 물리 쪽에서는 세계면 instanton의 "장애 다발 = 상쇄되지 않은 페르미온 영모드"에 해당합니다. 이 노트는 그 경로의 첫 단계로, 물리 배경 없이 순수 수학으로 완결되게 씁니다.

## 2. 핵심 질문

매끄러운 3차 곡면은 정확히 27개의 직선을 가집니다. 특이점이 있으면 서로 다른 직선의 개수가 줄거나, 직선이 무한히 많을 수도 있습니다. 그럼에도 **어떤 3차 곡면에 대해서도 직선을 "가상적으로" 세면 항상 27**이 되는 이유를, 영점 집합의 cotangent complex와 가상 기본류로 설명합니다.

## 3. 범위: 작게, 예제 중심으로

- **다룰 것:** 매끄러운 다양체 $M$ 위의 벡터다발 $E$와 단면 $s$의 영점 집합 $Z=Z(s)$로 주어지는 경우만 다룹니다. 이 경우 다음이 모두 구체적으로 정의됩니다.
  - 2항 복합체 $[E^\vee|_Z \to \Omega_M|_Z]$와 이것에서 $L_Z$(의 절단)로 가는 사상 (완전 장애 이론)
  - 가상류 $[Z]^{\mathrm{vir}}$ (Fulton의 localized top Chern class로 정의)
  - $\deg [Z]^{\mathrm{vir}} = \int_M c_{\mathrm{top}}(E)$ ($M$이 고유(proper)할 때)
- **개관만 할 것:** Behrend–Fantechi의 intrinsic normal cone 일반 구성, 일반적인 완전 장애 이론. 마지막 절에서 "일반적으로는 이렇게 된다" 수준으로만.
- **다루지 않을 것:** 물리(A-model, instanton)는 마지막 절에서 한두 문단 예고만 합니다. 5차 3-fold, stable map, Gromov–Witten 이론도 전망 수준으로만.
- **목표 분량:** 10~15쪽.

## 4. 27 lines 노트에서 가져올 설정과 표기

새 노트는 이전 노트의 표기를 그대로 이어 씁니다.

- $k=\bar k$, 기본적으로 $\operatorname{char}k \neq 3$ (필요하면 0으로 가정해도 됨).
- 3차 형식의 공간 $\mathbb{P}^{19}$, Grassmannian $\mathbb{G}(1,3)=\mathrm{Gr}(2,4)$, 접속 대응 $Z=\{(X,l): l\subset X\}\subset \mathbb{P}^{19}\times\mathbb{G}(1,3)$, 사영 $\mathrm{pr}_1, \mathrm{pr}_2$.
- 이전 노트에서 보인 것:
  - $\mathrm{pr}_2$는 $\mathbb{P}^{15}$-다발이고 $Z$는 매끄럽고 기약이며 19차원.
  - Proposition 3.1: 매끄러운 3차 곡면 위의 직선은 1차 변형을 갖지 않음 (좌표 계산으로 증명).
  - Theorem 4.1: $\mathrm{pr}_1$이 매끄러운 3차 곡면들의 열린 집합 위에서 유한 étale이고, Fermat 3차 곡면이 27개 직선을 가지므로 27.
  - Remark 4.2 (Schubert calculus): $S$를 $\mathbb{G}(1,3)$의 tautological 계수 2 부분다발이라 할 때, 3차식 $F$를 각 직선에 제한하면 계수 4인 다발 $E=\mathrm{Sym}^3S^\vee$의 단면 $s_F$가 되고, 그 영점 집합이 $\mathrm{pr}_1^{-1}(X)$. $\int_{\mathbb{G}(1,3)}c_4(E)=18+9=27$.
  - §6 (전망): 특이 3차 곡면에서는 $s_F$의 영점 집합이 축소되지 않거나 양의 차원일 수 있으며(예: 매끄러운 평면 3차 곡선 위의 원뿔은 직선의 1-모수 족을 가짐), 도출된 영점 집합이 여전히 차수 27인 가상 기본류를 가진다고 인용만 했습니다. **이번 노트가 이 문장을 실제로 풀어내는 것입니다.**
- Fano scheme 표기: $F(X) := Z(s_F)\subset\mathbb{G}(1,3)$.

## 5. 노트 구성안

1. **Introduction.** 27 lines 노트의 Remark 4.2와 §6이 남긴 질문. 매끄러운 경우에는 $Z(s_F)$가 축소된 27개 점이고, 특이한 경우에는 무엇이 남는가. 노트의 결론(어떤 3차 곡면이든 가상 개수는 27, 두 예제에서 그 27이 어떻게 나뉘는지)을 미리 요약.
2. **Normal bundles and deformations of lines.** 이전 노트 §3의 좌표 계산을 내재적으로 다시 쓰기.
   - Fano scheme의 $l$에서의 접공간은 $H^0(l, N_{l/X})$, 장애 공간은 $H^1(l, N_{l/X})$.
   - 매끄러운 3차 곡면에서 $N_{l/X}\cong\mathcal{O}_l(-1)$ (adjunction 또는 $l^2=-1$로부터)이므로 $H^0=H^1=0$. 이것이 Proposition 3.1의 정체.
   - $\mathbb{G}(1,3)$에서 $T_{[l]}\mathbb{G}=\mathrm{Hom}(S,Q)|_{[l]} = H^0(N_{l/\mathbb{P}^3})$와 $E|_{[l]}=H^0(\mathcal{O}_l(3))$, 그리고 $ds_F$가 $H^0(N_{l/\mathbb{P}^3})\to H^0(N_{X/\mathbb{P}^3}|_l)$와 같다는 것.
3. **The cotangent complex of a zero locus.** Cotangent complex 노트의 regular embedding 절과 연결.
   - $Z=Z(s)\subset M$이고 $I$가 이상층일 때, $s^\vee: E^\vee|_Z\to I/I^2$는 전사이고, $L_Z$의 절단 $\tau_{\ge -1}L_Z\simeq[I/I^2\to\Omega_M|_Z]$.
   - 따라서 $\phi: [E^\vee|_Z\to\Omega_M|_Z]\to\tau_{\ge-1}L_Z$가 $h^0$에서 동형, $h^{-1}$에서 전사. 이것이 완전 장애 이론의 정의를 만족함을 확인.
   - $Z$가 기대 차원($\dim M-\operatorname{rk}E$)이고 regular embedding이면 $\phi$는 quasi-isomorphism이고, 장애 층 $\mathrm{Ob}=\operatorname{coker}(T_M|_Z\to E|_Z)$는 0. 이것이 27 lines 노트의 "유한 étale" 논증과 같은 내용임을 설명.
4. **The virtual class.**
   - 정의: Fulton의 localized top Chern class $[Z]^{\mathrm{vir}} := 0^!_E[C_{Z}M] \in A_{\dim M-\operatorname{rk}E}(Z)$ (법원뿔 $C_ZM\subset E|_Z$를 영단면과 교차).
   - $M$이 고유하면 $\iota_*[Z]^{\mathrm{vir}} = c_{\mathrm{top}}(E)\cap[M]$, 따라서 $\deg[Z]^{\mathrm{vir}}=\int_M c_{\mathrm{top}}(E)$.
   - 따름정리: 어떤 3차 곡면 $X$에 대해서도 $\deg[F(X)]^{\mathrm{vir}}=27$. $\mathbb{G}(1,3)$은 고유하고 $s_F$는 늘 정의되므로, 특이점과 무관.
   - 두 특수 경우: (a) $Z$가 0차원이면 $[Z]^{\mathrm{vir}}$의 각 점의 기여는 그 점의 국소환의 길이. (b) $Z$가 매끄럽지만 기대 차원보다 크면 $[Z]^{\mathrm{vir}} = c_{\mathrm{top}}(\mathrm{Ob})\cap[Z]$ (초과 교차 공식, Fulton 6.3).
5. **Example 1: a cubic surface with one node.** (경우 (a))
   - 예: $A_1$ 마디점 하나를 가진 3차 곡면. 서로 다른 직선 21개: 마디점을 지나는 6개, 지나지 않는 15개.
   - 목표: 마디점을 지나는 직선에서 $F(X)$의 국소환 길이가 2, 지나지 않는 직선에서 1임을 보여 $15\cdot1+6\cdot2=27$.
   - 방법 후보: (i) 구체적인 방정식을 골라 $\mathbb{G}(1,3)$의 아핀 좌표에서 $s_F$의 4개 성분을 쓰고 국소환을 계산. (ii) $N_{l/X}$ 대신 $H^1$ 계산으로 접공간이 1차원임을 보이고 길이를 따로 확정. (i)이 더 확실함.
   - 마디점 3차 곡면을 $\mathbb{P}^2$의 6점 blow-up의 퇴화(6점이 한 원뿔곡선 위에 놓이는 경우)로 보는 해석도 한 문단으로 소개하면 좋음.
6. **Example 2: the cone over a smooth plane cubic.** (경우 (b))
   - $X=\{F(x_0,x_1,x_2)=0\}\subset\mathbb{P}^3$, $C=\{F=0\}\subset\mathbb{P}^2$ 매끄러운 평면 3차 곡선(타원곡선). 모든 직선이 꼭짓점 $[0:0:0:1]$을 지나며, 직선들의 집합은 $C$와 동형.
   - 목표: $F(X)$가 $C$와 동형인 매끄러운(축소된) 곡선인지 확인한 뒤, $\mathrm{Ob}$를 구체적으로 구하고 $\int_C c_1(\mathrm{Ob}) = 27$을 확인.
   - 계산 단서: $\int_C c_1(\mathrm{Ob}) = \int_C c_1(E|_C) - \int_C c_1(T_{\mathbb{G}}|_C) + \int_C c_1(T_C)$ (정확열 $0\to T_C\to T_{\mathbb{G}}|_C\to E|_C\to\mathrm{Ob}\to0$이 성립한다면). $C\subset\mathbb{G}(1,3)$이 꼭짓점을 지나는 직선들의 $\mathbb{P}^2$ 안에 놓인 3차 곡선이므로, $S$, $Q$의 $C$로의 제한을 $\mathcal{O}_{\mathbb{P}^2}(-1)$ 등으로 표현할 수 있을 것.
   - **주의:** 이 계산은 사전에 끝까지 확인되지 않았습니다. (1) $F(X)$의 scheme 구조가 정말 축소되었는지, (2) 위 정확열이 성립하는지(즉 $ds$의 핵이 정확히 $T_C$인지), (3) 최종 적분이 27인지를 노트 작성 과정에서 직접 확인해야 합니다. 축소되지 않았다면 초과 교차 공식 대신 일반적인 localized Chern class 계산이 필요하고, 그 경우 그렇게 서술을 바꿉니다.
7. **Outlook.**
   - Behrend–Fantechi의 intrinsic normal cone과 일반적인 완전 장애 이론 개관.
   - 같은 틀이 Gromov–Witten 불변량(stable map 모듈라이)의 기초라는 것, 5차 3-fold의 2875개 직선이 $\int_{\mathbb{G}(1,4)}c_6(\mathrm{Sym}^5S^\vee)$라는 것, 다중 피복의 $1/d^3$ 기여.
   - 물리 예고(한 문단): 위상 끈 이론의 A-model에서 차수 1 세계면 instanton이 직선이고, 장애 다발의 Euler류가 상쇄되지 않은 페르미온 영모드의 적분에 해당. 다음 노트(QFT 범주)로 이어짐.

## 6. 증명/계산해야 할 명제 체크리스트

- [ ] 매끄러운 3차 곡면의 직선에서 $N_{l/X}\cong\mathcal{O}(-1)$.
- [ ] $T_{[l]}F(X) = H^0(N_{l/X})$, 장애가 $H^1(N_{l/X})$에 놓임.
- [ ] 영점 집합에 대해 $[E^\vee|_Z\to\Omega_M|_Z]\to\tau_{\ge-1}L_Z$가 완전 장애 이론.
- [ ] $\iota_*[Z]^{\mathrm{vir}}=c_{\mathrm{top}}(E)\cap[M]$ (Fulton 14.1을 인용해도 됨).
- [ ] 0차원 경우: 각 점의 기여 = 국소환의 길이.
- [ ] 초과 경우: $[Z]^{\mathrm{vir}}=c_{\mathrm{top}}(\mathrm{Ob})\cap[Z]$.
- [ ] 마디점 곡면: 직선 21개, 중복도 2와 1, 합 27.
- [ ] 원뿔: $F(X)\cong C$ (scheme으로), $\int_C c_1(\mathrm{Ob})=27$.

## 7. 확인이 필요한 사실 (기억에 의존한 부분)

다음은 고전적 결과로 알려져 있지만, 노트에 쓰기 전에 문헌으로 확인해야 합니다.

- 마디점 하나인 3차 곡면의 직선이 21개이고, 마디점을 지나는 것이 6개이며 각각 중복도 2. (Eisenbud–Harris *3264 and All That* 6장 또는 Dolgachev *Classical Algebraic Geometry* 9장)
- 5차 3-fold의 일반적인 경우 2875개 직선, 법다발 $\mathcal{O}(-1)\oplus\mathcal{O}(-1)$ (Katz).
- 다중 피복 $1/d^3$ (Aspinwall–Morrison; Manin).
- 문헌 정보(연도, 쪽수, arXiv 번호)는 bib 파일에 넣기 전에 모두 확인.

## 8. 형식 요구사항

- **LaTeX:** 27 lines 노트와 같은 서식을 쓰면 사이트의 노트들과 통일됩니다. 새 세션에 `27lines.tex`와 `refs.bib`를 함께 첨부하고 서문(preamble)을 그대로 재사용하세요. 주요 사항은 다음과 같습니다.
  - `\documentclass[12pt]{article}`, `\linespread{1.241}`, A4, `geometry`로 total 170×257mm
  - `lmodern`, `mathrsfs`, `mathalpha`(scr=boondox, cal=esstix), `amsmath/amssymb/amsthm/mathtools`, `tikz-cd`
  - `hyperref` (링크 색: linkcolor red, citecolor magenta, urlcolor purple)
  - `biblatex`(backend=biber, style=alphabetic)
  - 정리 환경: note, remark, theorem, lemma, corollary, proposition, example, definition (모두 section 번호를 따라감)
  - 매크로: `\op`, `\set`, `\eq`, `\bb`
  - 초록 다음에 tocdepth 1의 목차, 그다음 `\clearpage`
- **참고문헌 주의:** bib의 URL 필드에는 `~`를 그대로 쓰세요. `\textasciitilde`를 쓰면 링크가 깨집니다(27 lines 노트에서 실제로 생긴 문제).
- **컴파일:** `latexmk -pdf` (biber)로 경고 없이 컴파일되어야 합니다.
- **결과물:** `.tex`와 `.bib`. 이것을 받아서 사이트에 올리는 작업(PDF 컴파일, 노트 항목 작성, 27 lines 노트 및 Cotangent complex 노트와의 연결)은 별도로 진행합니다.
- **문체:** 이전 노트처럼 영어로, 증명은 자세히, 인용만 하는 결과는 그렇다고 분명히 밝힙니다. 확립된 결과와 아직 확인하지 않은 계산을 구분합니다.

## 9. 참고문헌 후보

- W. Fulton, *Intersection Theory*, 2nd ed., Springer, 1998. 특히 6장(초과 교차)과 14장(localized top Chern class).
- D. Eisenbud, J. Harris, *3264 and All That*, Cambridge University Press, 2016. 3장(Grassmannian), 6장(직선과 Fano scheme).
- K. Behrend, B. Fantechi, "The intrinsic normal cone", *Invent. Math.* 128 (1997), 45–88.
- L. Illusie, *Complexe Cotangent et Déformations I*, LNM 239, Springer, 1971.
- R. Hartshorne, *Deformation Theory*, GTM 257, Springer, 2010. Hilbert scheme과 법다발.
- I. Dolgachev, *Classical Algebraic Geometry: A Modern View*, Cambridge University Press, 2012. 9장(3차 곡면).
- 이전 노트 두 편: *The 27 Lines on a Smooth Cubic Surface*, *Cotangent complex* (같은 저자, mookphysics.org Study notes).

## 10. 새 세션에 요청할 진행 방식

1. 먼저 §5 구성안과 §6 체크리스트를 검토하고, 빠지거나 잘못된 것이 있으면 지적해 주세요.
2. 예제 2(원뿔)의 계산을 가장 먼저 끝까지 해 보세요. 결과에 따라 6절의 서술 방식이 달라집니다.
3. 그다음 2~4절, 5절, 7절, 1절 순서로 작성합니다.
4. 확인하지 못한 계산이나 인용은 원고 안에 표시해 두고, 마지막에 목록으로 정리해 주세요.
