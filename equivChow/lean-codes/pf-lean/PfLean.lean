-- This module serves as the root of the `PfLean` library.
-- Import modules here that should be built as part of the library.
import PfLean.Basic
import Mathlib
import Mathlib.Data.Matroid.Basic
import Mathlib.Data.Set.Basic

-- Definition of the Matroid structure
structure MatroidF (E : Type) where
  flats : Set (Set E)                     -- The set of flats
  ground_set : Set E                      -- The ground set
  empty_flat : ∅ ∈ flats                  -- The empty set is a flat
  univ_flat : ground_set ∈ flats          -- The ground set is in flats
  closure : Set E → Set E := λ X => ⋂₀ { F | F ∈ flats ∧ X ⊆ F }  -- Closure definition
  flat_iff_closure : ∀ (F : Set E), F ∈ flats ↔ closure F = F  -- Flats are characterized by their closure
  flat_inter : ∀ {F₁ F₂ : Set E}, F₁ ∈ flats → F₂ ∈ flats → (F₁ ∩ F₂) ∈ flats -- Intersection of flats is a flat
  closure_extends : ∀ (X : Set E), X ⊆ closure X  -- Closure extends the set
  closure_minimal : ∀ (X : Set E) (F : Set E), F ∈ flats → X ⊆ F → closure X ⊆ F  -- Minimality of closure property

-- Example of a simple matroid on a set with three elements {a, b, c}
def exampleMatroid : MatroidF (Fin 3) :=
  { flats := { ∅, {0}, {1}, {2}, {0, 1}, {0, 2}, {1, 2}, {0, 1, 2} },
    ground_set := {0, 1, 2},
    empty_flat := by simp,
    univ_flat := by simp,
    closure := λ X => ⋂₀ { F | F ∈ { ∅, {0}, {1}, {2}, {0, 1}, {0, 2}, {1, 2}, {0, 1, 2} } ∧ X ⊆ F },
    flat_iff_closure := by
      intro F
      apply Iff.intro
      · intro h
        simp only [Set.mem_set_of_eq] at h
        exact h.2
      · intro h
        rw [Set.mem_set_of_eq]
        exact ⟨Set.mem_univ F, h⟩,
    flat_inter := by
      intros F₁ F₂ hF₁ hF₂
      simp [Set.mem_set_of_eq] at *
      exact Set.inter_subset_inter hF₁ hF₂,
    closure_extends := by
      intro X
      simp [Set.sInter_eq_Inter],
    closure_minimal := by
      intros X F hF hXF
      simp [Set.sInter_eq_Inter]
      exact Set.subset.trans hXF (Set.Inter_subset _ hF) }
