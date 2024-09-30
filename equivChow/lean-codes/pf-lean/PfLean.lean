-- This module serves as the root of the `PfLean` library.
-- Import modules here that should be built as part of the library.
import PfLean.Basic
import Mathlib
import Mathlib.Data.Matroid.Basic
import Mathlib.Data.Set.Basic


-- Define the structure of a matroid on a ground set E, with flats as subsets of E
structure MatroidF (E : Type) where
  flats : Set (Set E)                 -- Set of flats, where each flat is a set of elements from E
  empty_flat : ∅ ∈ flats              -- The empty set is a flat
  univ_flat : (Set.univ : Set E) ∈ flats  -- The universal set (ground set) is a flat
  flat_inter : ∀ {F₁ F₂ : Set E}, F₁ ∈ flats → F₂ ∈ flats → (F₁ ∩ F₂) ∈ flats  -- Intersection of flats is a flat
  closure : Set E → Set E             -- Closure function, mapping a set to its closure
  closure_extends : ∀ (X : Set E), X ⊆ closure X  -- The closure of X contains X
  flat_iff_closure : ∀ (F : Set E), F ∈ flats ↔ closure F = F  -- A flat is its own closure
  closure_minimal : ∀ (X : Set E) (F : Set E), F ∈ flats → X ⊆ F → closure X ⊆ F  -- The closure is the smallest flat containing X

-- Closure as the intersection of all flats containing X
def matroid_closure {E : Type} (flats : Set (Set E)) (X : Set E) : Set E :=
  ⋂₀ { F | F ∈ flats ∧ X ⊆ F }  -- Intersection of all flats that contain X
