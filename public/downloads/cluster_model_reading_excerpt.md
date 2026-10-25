# The 1D Cluster Model as a Symmetry-Protected Topological Phase

This is a reading-only extract of the explanatory cells from the public notebook. For executable code and plots, download the original Jupyter Notebook.

## Sanity checks

Three facts underpin everything. Each is one line of code.

1. the stabilizers $S_j=Z_{j-1}X_jZ_{j+1}$ mutually commute, so the model is exactly solvable;
2. the symmetry generators commute with every $S_j$;
3. on a **ring**, $\prod_{j\ \mathrm{odd}}S_j = U_{\mathrm{odd}}$ — the symmetry is a product of stabilizers, hence acts trivially on the ground state. On an **open chain** this identity fails by boundary terms, and that failure is the whole story.

## Fig. 1 — the model

The chain, one stabilizer, the two sublattice symmetries, and the edge operators that will turn out to carry the degeneracy.

## Fig. 2 — spectra

An open chain of $N$ sites admits stabilizers $S_j$ only for $j=2,\dots,N-1$, that is $N-2$ of them, so

$$\dim(\text{ground space}) = \frac{2^N}{2^{N-2}} = 4 .$$

This holds for **both parities of $N$**. On a ring all $N$ stabilizers exist and the ground state is unique. The contrast is the point: the degeneracy is an *edge* phenomenon, not a bulk one.

## Fig. 3 — degeneracy versus system size

The ground-space dimension is $4$ for every open chain and $1$ for every ring, independently of $N$ and of its parity. A degeneracy that does not grow with $N$ and disappears when the boundary is removed is the signature of edge modes.

## Fig. 4 — what "protected" means

Add a field and watch the four ground levels.

$$H(\lambda)=-\sum_j Z_{j-1}X_jZ_{j+1}\;-\;\lambda\sum_j P_j ,\qquad P=X\ \text{or}\ Z .$$

* $P=X$ **preserves** $\mathbb{Z}_2\times\mathbb{Z}_2$, since $X_j$ commutes with both $\prod X$.
* $P=Z$ **breaks** it, since $Z_j$ anticommutes with the $X$ on its own sublattice.

The prediction is that the splitting of the four ground levels is exponentially small in $N$ in the first case and linear in $\lambda$ in the second.

### Is it really *exponentially* small?

A splitting that shrinks with system size is a finite-size artefact; one that does not is a genuine lifting of the degeneracy. Fixing $\lambda$ and increasing $N$ separates the two.

## Fig. 5 — entanglement spectrum

Cut the ring in half and record $-\ln\lambda_i$ for the Schmidt weights. At the fixed point the spectrum is exactly flat with four equal levels — one factor of two for each of the two cuts, and each factor of two is the projective representation carried by that cut.

Switching on a perturbation, the spectrum spreads. The rate at which it spreads distinguishes the two cases.

## Fig. 6 — the projective representation

On the open chain the symmetry generators, restricted to the ground space, factorise into a left piece and a right piece:

$$U_{\mathrm{odd}}\big|_{\mathrm{GS}}=\underbrace{(X_1Z_2)}_{L_{\mathrm{odd}}}\cdot\underbrace{(\cdots)}_{R_{\mathrm{odd}}},
\qquad
U_{\mathrm{even}}\big|_{\mathrm{GS}}=\underbrace{(Z_1)}_{L_{\mathrm{even}}}\cdot\underbrace{(\cdots)}_{R_{\mathrm{even}}} .$$

The two full operators **commute**, but each edge factor pair **anticommutes**. A $\mathbb{Z}_2\times\mathbb{Z}_2$ acting with an anticommuting pair has no one-dimensional representation, so each edge must carry at least two states. That is the protection, and $2\times2=4$ is the degeneracy of Fig. 2.

## Fig. 7 — decorated domain walls

Reading the stabilizer for odd $j$ as
$$X_j = Z_{j-1}Z_{j+1}$$
says: the odd spin at $j$ is flipped exactly when the two even neighbours disagree, i.e. **exactly on a domain wall of the even sublattice**. The cluster state is the domain walls of one $\mathbb{Z}_2$ decorated with charges of the other.

This is the construction that generalises: in the "Higgs $=$ SPT" setting the domain walls belong to a higher-form symmetry, but the logic is unchanged.

## Summary

| observation | figure | meaning |
|---|---|---|
| ground space is 4-fold on an open chain, for both parities of $N$ | 2, 3 | two protected states per edge |
| ground state is unique on a ring | 2 | the degeneracy lives on the boundary, not in the bulk |
| splitting is $\sim10^{-6}$ under $-\lambda\sum X$, $\sim10^{-1}$ under $-\lambda\sum Z$ | 4 | the symmetry, not the gap, is what protects |
| entanglement spectrum is exactly flat and 4-fold at $\lambda=0$ | 5 | the same projective structure, seen from the cut |
| the generators commute globally but anticommute on each edge | 6 | $H^2(\mathbb{Z}_2\times\mathbb{Z}_2,U(1))=\mathbb{Z}_2$ is nontrivial |
| odd-site charges sit on even-sublattice domain walls | 7 | decorated domain wall construction |

### Things to try next

* replace $-\lambda\sum Z_j$ by $-\lambda\sum Z_jZ_{j+1}$: it also breaks the symmetry, and the quartet splits again;
* push the symmetric field to $\lambda>1$: the bulk gap closes and reopens, and the system leaves the SPT phase — the degeneracy is lost through a **bulk** transition rather than an edge one;
* gauge one of the two $\mathbb{Z}_2$'s and watch the SPT turn into a symmetry-breaking phase with two bulk ground states.

