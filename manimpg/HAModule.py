# Save this code as e.g., matroid_viz_delete_animate.py
# Run from terminal using: manim -pql matroid_viz_delete_animate.py MatroidLatticesDeleteAnimate

from manim import *
import itertools

class MatroidLatticesDeleteAnimate(Scene):
    def construct(self):
        # --- Define Matroids (U(2,4) and U(2,3)) ---
        # M = U(2,4)
        ground_set_M = {1, 2, 3, 4}
        e_to_delete = 4
        flats_M = {
            0: [frozenset()],
            1: [frozenset({i}) for i in ground_set_M],
            2: [frozenset(ground_set_M)]
        }
        covers_M = []
        for r_low in range(2): # Ranks 0, 1
            r_high = r_low + 1
            for F_low in flats_M[r_low]:
                for F_high in flats_M[r_high]:
                    if F_low.issubset(F_high):
                        covers_M.append((F_low, F_high))

        # M' = M \ e = U(2,3) (delete element 4)
        ground_set_M_del = ground_set_M - {e_to_delete}
        flats_M_del = {
            0: [frozenset()],
            1: [frozenset({i}) for i in ground_set_M_del],
            2: [frozenset(ground_set_M_del)]
        }
        covers_M_del = []
        for r_low in range(2): # Ranks 0, 1
            r_high = r_low + 1
            for F_low in flats_M_del[r_low]:
                for F_high in flats_M_del[r_high]:
                    if F_low.issubset(F_high):
                        covers_M_del.append((F_low, F_high))

        # --- Manim Visualization Setup ---
        node_radius = 0.25 # Slightly larger nodes
        level_distance = 2.0
        h_spacing = 1.8

        # Modified function to create nodes and highlights together, no labels, colored nodes
        def create_lattice_diagram_final(flats_dict, covers_list):
            nodes = {}
            edges = {}
            mobjects_to_draw = VGroup() # Combined group for animation
            node_highlight_group = VGroup() # Nodes + Highlights
            edge_group = VGroup()

            max_rank = max(flats_dict.keys()) if flats_dict else 0

            # Create nodes and highlights, apply color gradient
            for rank, flat_list in flats_dict.items():
                y_pos = rank * level_distance - (max_rank * level_distance / 2.0)
                num_flats = len(flat_list)
                total_width = (num_flats - 1) * h_spacing if num_flats > 1 else 0
                start_x = -total_width / 2.0

                for i, flat in enumerate(flat_list):
                    x_pos = start_x + i * h_spacing
                    pos = np.array([x_pos, y_pos, 0])
                    # Color gradient from BLUE (rank 0) to RED (max_rank)
                    color_ratio = rank / max_rank if max_rank > 0 else 0.5
                    node_color = interpolate_color(BLUE, RED, color_ratio)
                    node = Dot(point=pos, radius=node_radius, color=node_color)

                    nodes[flat] = node
                    node_highlight_group.add(node)

                    # Create highlight if flat is not empty
                    if flat:
                        highlight_circle = Circle(radius=node_radius + 0.1, color=YELLOW, stroke_width=3).move_to(node.get_center())
                        node_highlight_group.add(highlight_circle) # Add highlight

            # Create edges
            for F_low, F_high in covers_list:
                if F_low in nodes and F_high in nodes: # Ensure nodes exist
                    edge = Line(nodes[F_low].get_center(), nodes[F_high].get_center(), stroke_width=2, color=WHITE)
                    edges[(F_low, F_high)] = edge
                    edge_group.add(edge)

            mobjects_to_draw.add(edge_group, node_highlight_group)

            # Return components separately for manipulation
            return nodes, edges, node_highlight_group, edge_group

        # --- Create L(M) ---
        title_M = Text("L(M) for M = U(2,4)", font_size=36).to_edge(UP)
        nodes_M, edges_M, node_highlights_M, edge_group_M = create_lattice_diagram_final(flats_M, covers_M)
        lattice_M = VGroup(edge_group_M, node_highlights_M) # Combine for positioning

        self.play(Write(title_M))
        self.play(Create(edge_group_M))
        self.play(FadeIn(node_highlights_M, scale=0.5))
        self.wait(1)

        # --- Animate Deletion ---
        deletion_text = Text(f"Deleting element {e_to_delete}", font_size=24).next_to(title_M, DOWN)
        self.play(Write(deletion_text))

        # Identify objects related to element 'e_to_delete' (element 4)
        flat_e = frozenset({e_to_delete})
        flat_E = frozenset(ground_set_M)
        node_e = nodes_M.get(flat_e)
        node_E = nodes_M.get(flat_E) # Top node
        flat_empty = frozenset()
        node_empty = nodes_M.get(flat_empty)

        # Edges connected to node_e and node_E involving e implicitly
        edges_to_fade = VGroup()
        nodes_to_fade = VGroup()
        other_M_objects = VGroup() # Objects that remain but might transform

        if node_e:
            nodes_to_fade.add(node_e)
            # Find highlights associated with node_e
            for highlight in node_highlights_M:
                if isinstance(highlight, Circle) and np.allclose(highlight.get_center(), node_e.get_center()):
                    nodes_to_fade.add(highlight)
                    break
            # Find edges connected to node_e
            edge_key_0_e = (flat_empty, flat_e)
            edge_key_e_E = (flat_e, flat_E)
            if edge_key_0_e in edges_M: edges_to_fade.add(edges_M[edge_key_0_e])
            if edge_key_e_E in edges_M: edges_to_fade.add(edges_M[edge_key_e_E])

        # Identify edges connecting rank 1 nodes (not e) to the top node E
        for flat1 in flats_M.get(1, []):
             if flat1 != flat_e: # Edges from {1}, {2}, {3} to E
                 edge_key_1_E = (flat1, flat_E)
                 if edge_key_1_E in edges_M:
                     edges_to_fade.add(edges_M[edge_key_1_E]) # These edges will be replaced

        # Flash the node representing the element being deleted
        if node_e:
            self.play(Flash(node_e, color=RED, flash_radius=node_radius+0.3))
            self.wait(0.5)

        # --- Create L(M\e) structure (initially invisible) ---
        nodes_M_del, edges_M_del, node_highlights_M_del, edge_group_M_del = create_lattice_diagram_final(flats_M_del, covers_M_del)
        lattice_M_del = VGroup(edge_group_M_del, node_highlights_M_del)
        lattice_M_del.fade(1) # Make it transparent initially

        # Position M_del lattice centered
        # (Adjust position if needed, perhaps slightly offset from M's original spot)

        # --- Cross-Fade Animation ---
        # Identify objects in L(M) that correspond to objects in L(M\e)
        # In this simple case, empty set node stays, rank 1 nodes {1},{2},{3} stay, top node E transforms to E'
        nodes_to_transform = VGroup()
        highlights_to_transform = VGroup()
        target_mobjects = VGroup() # Nodes+Highlights+Edges of M_del

        node_empty_del = nodes_M_del.get(frozenset())
        if node_empty and node_empty_del:
            node_empty.save_state() # Keep empty node state

        for flat, node in nodes_M.items():
             if e_to_delete not in flat: # These flats exist in M \ e
                 if flat != flat_empty: # Exclude empty node, handle separately
                    target_node = nodes_M_del.get(flat)
                    if target_node:
                         # Add node and its highlight for transformation
                        nodes_to_transform.add(node)
                        for highlight in node_highlights_M:
                             if isinstance(highlight, Circle) and np.allclose(highlight.get_center(), node.get_center()):
                                 highlights_to_transform.add(highlight)
                                 break
                         # Find corresponding target node and highlight
                        target_mobjects.add(target_node)
                        for target_highlight in node_highlights_M_del:
                             if isinstance(target_highlight, Circle) and np.allclose(target_highlight.get_center(), target_node.get_center()):
                                 target_mobjects.add(target_highlight)
                                 break
             elif flat == flat_E: # Handle top node separately if needed (or include above)
                 target_node = nodes_M_del.get(frozenset(ground_set_M_del))
                 if target_node:
                     nodes_to_transform.add(node) # Add E node
                     for highlight in node_highlights_M: # Add E highlight
                         if isinstance(highlight, Circle) and np.allclose(highlight.get_center(), node.get_center()):
                              highlights_to_transform.add(highlight)
                              break
                     target_mobjects.add(target_node) # Add E' node
                     for target_highlight in node_highlights_M_del: # Add E' highlight
                         if isinstance(target_highlight, Circle) and np.allclose(target_highlight.get_center(), target_node.get_center()):
                             target_mobjects.add(target_highlight)
                             break


        # Group objects to fade out from M (excluding empty node and its highlight)
        m_fade_out_group = VGroup(nodes_to_fade, edges_to_fade)

        # Group objects in M that will transform (nodes + highlights, excluding empty)
        m_transform_group = VGroup(nodes_to_transform, highlights_to_transform)

        # Group target objects in M_del (nodes + highlights + edges, excluding empty node/highlight)
        m_del_fade_in_group = VGroup()
        empty_del_highlight = None
        for mob in node_highlights_M_del: # Separate empty highlight
             if isinstance(mob, Circle) and np.allclose(mob.get_center(), node_empty_del.get_center()):
                 empty_del_highlight = mob
                 continue
             if mob != node_empty_del:
                 m_del_fade_in_group.add(mob)
        m_del_fade_in_group.add(edge_group_M_del)


        title_M_del = Text("L(M \\ e) for M \\ e = U(2,3)", font_size=36).to_edge(UP)

        # Perform the animation
        self.play(
            FadeOut(m_fade_out_group, shift=DOWN*0.5),
            Transform(m_transform_group, target_mobjects), # Transform nodes/highlights
            # Fade out old edges connected to transforming nodes
            # FadeIn(m_del_fade_in_group), # Fade in new structure (nodes/highlights already handled by Transform)
            FadeIn(edge_group_M_del), # Fade in new edges
            FadeOut(title_M, shift=UP*0.5),
            FadeIn(title_M_del, shift=UP*0.5),
            FadeOut(deletion_text)
        )
        # Ensure empty node is restored if it faded (shouldn't have based on logic, but just in case)
        # self.play(node_empty.animate.restore(), run_time=0.1) # Might not be needed

        self.wait(2)