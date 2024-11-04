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

-- Example of a matroid on the ground set {0, 1, 2}
def exampleMatroid : MatroidF (Fin 3) :=
{ flats := {∅, {0}, {1}, {2}, {0, 1, 2}},  -- Define flats
  ground_set := {0, 1, 2},               -- Define the ground set explicitly
  empty_flat := by  simp,                 -- The empty set is a flat
  univ_flat := by simp,                   -- The ground set is in flats
  flat_iff_closure :=
    by
      intro F
      constructor
      unfold Set.sInter

  flat_inter :=
    by
      intros F₁ F₂ hF₁ hF₂
      simp [hF₁, hF₂]
      exact Set.inter_subset_left hF₁ hF₂
  closure_extends :=
    by
      intro X
      simp                    -- X is a subset of its closure
  closure_minimal :=
    by
      intros X F hF hXF
      unfold closure
      apply Set.sInter_subset_of_mem
      exact ⟨hF, hXF⟩                    -- Minimality of closure property
}
