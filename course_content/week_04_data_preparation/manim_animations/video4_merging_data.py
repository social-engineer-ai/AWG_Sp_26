"""
Week 4, Video 4: Merging Datasets
=================================
Animations explaining how to join pricing and sales data.

To render:
    manim -pql video4_merging_data.py

Scenes:
1. WhyMerge - Motivation for combining datasets
2. MergeTypes - Inner, Left, Right, Outer joins
3. KeyMatching - Visual of how keys match between tables
4. AWGMergeStrategy - Specific AWG merge approach
5. MergeIssues - Common problems and solutions
"""

from manim import *


class WhyMerge(Scene):
    """Scene 1: Motivation for merging datasets"""

    def construct(self):
        # Title
        title = Text("Why Merge Datasets?", font_size=40).to_edge(UP)
        self.play(Write(title))

        # Two separate datasets
        pricing_box = VGroup(
            Rectangle(width=4, height=2.5, color=BLUE, fill_opacity=0.2),
            Text("PRICING DATA", font_size=20, color=BLUE).shift(UP * 0.8),
            Text("• Product codes", font_size=14).shift(UP * 0.3),
            Text("• List Cost", font_size=14).shift(DOWN * 0),
            Text("• BSP, SRP", font_size=14).shift(DOWN * 0.3),
            Text("• By division, quarter", font_size=14).shift(DOWN * 0.6),
        )
        pricing_box.shift(LEFT * 3)

        sales_box = VGroup(
            Rectangle(width=4, height=2.5, color=GREEN, fill_opacity=0.2),
            Text("SALES DATA", font_size=20, color=GREEN).shift(UP * 0.8),
            Text("• Product codes", font_size=14).shift(UP * 0.3),
            Text("• Dollar sales", font_size=14).shift(DOWN * 0),
            Text("• Unit sales", font_size=14).shift(DOWN * 0.3),
            Text("• By division, quarter", font_size=14).shift(DOWN * 0.6),
        )
        sales_box.shift(RIGHT * 3)

        self.play(Create(pricing_box), Create(sales_box))
        self.wait(1)

        # Question marks
        question = Text("How do price changes affect sales?", font_size=24, color=YELLOW)
        question.shift(DOWN * 2)
        self.play(Write(question))
        self.wait(1)

        # Arrow showing need to combine
        merge_arrow = Arrow(pricing_box.get_right(), sales_box.get_left(), color=YELLOW, buff=0.3)
        merge_label = Text("MERGE", font_size=20, color=YELLOW).next_to(merge_arrow, UP)

        self.play(Create(merge_arrow), Write(merge_label))
        self.wait(1)

        # Combined insight
        combined = VGroup(
            Rectangle(width=6, height=1, color=PURPLE, fill_opacity=0.3),
            Text("Price + Sales = Complete Picture", font_size=20, color=PURPLE)
        ).shift(DOWN * 3.2)

        self.play(Create(combined))
        self.wait(2)


class MergeTypes(Scene):
    """Scene 2: Visual explanation of join types using Venn diagrams"""

    def construct(self):
        # Title
        title = Text("Types of Merges (Joins)", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Create 4 Venn diagram scenarios
        def create_venn(left_color, right_color, intersection_color, label, position):
            left_circle = Circle(radius=0.8, color=BLUE, fill_opacity=0.3 if left_color else 0)
            right_circle = Circle(radius=0.8, color=GREEN, fill_opacity=0.3 if right_color else 0)
            right_circle.shift(RIGHT * 0.6)

            # Intersection highlight
            if intersection_color:
                intersection = Intersection(left_circle, right_circle, color=YELLOW, fill_opacity=0.5)
                venn = VGroup(left_circle, right_circle, intersection)
            else:
                venn = VGroup(left_circle, right_circle)

            label_text = Text(label, font_size=16)
            label_text.next_to(venn, DOWN, buff=0.2)

            group = VGroup(venn, label_text)
            group.move_to(position)
            return group

        # Inner Join - only intersection
        inner = VGroup(
            Circle(radius=0.8, color=BLUE, fill_opacity=0.1, stroke_opacity=0.5),
            Circle(radius=0.8, color=GREEN, fill_opacity=0.1, stroke_opacity=0.5).shift(RIGHT * 0.6),
        )
        # Highlight intersection for inner join
        inner_highlight = VGroup(
            Circle(radius=0.8, color=BLUE).shift(LEFT * 0.3),
            Circle(radius=0.8, color=GREEN).shift(RIGHT * 0.3),
        )

        # Position the 4 join types
        positions = [
            LEFT * 4.5 + UP * 0.5,
            LEFT * 1.5 + UP * 0.5,
            RIGHT * 1.5 + UP * 0.5,
            RIGHT * 4.5 + UP * 0.5,
        ]

        labels = ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "OUTER JOIN"]
        descriptions = [
            "Only matches",
            "All left + matches",
            "All right + matches",
            "Everything"
        ]

        join_visuals = []

        for pos, label, desc in zip(positions, labels, descriptions):
            # Create circles
            left_c = Circle(radius=0.6, color=BLUE, stroke_width=3)
            right_c = Circle(radius=0.6, color=GREEN, stroke_width=3)
            right_c.shift(RIGHT * 0.5)

            circles = VGroup(left_c, right_c)
            circles.move_to(pos)

            title_text = Text(label, font_size=14)
            title_text.next_to(circles, UP, buff=0.15)

            desc_text = Text(desc, font_size=12, color=GREY)
            desc_text.next_to(circles, DOWN, buff=0.15)

            join_visuals.append(VGroup(circles, title_text, desc_text))

        # Show all four
        for visual in join_visuals:
            self.play(Create(visual), run_time=0.7)

        self.wait(1)

        # Highlight each type
        highlights = []

        # Inner: highlight intersection
        inner_rect = Rectangle(width=0.5, height=1.2, color=YELLOW, fill_opacity=0.5)
        inner_rect.move_to(positions[0]).shift(RIGHT * 0.25)
        highlights.append(inner_rect)

        # Left: highlight left circle + intersection
        left_rect = Circle(radius=0.6, color=YELLOW, fill_opacity=0.5)
        left_rect.move_to(positions[1])
        highlights.append(left_rect)

        # Right: highlight right circle + intersection
        right_rect = Circle(radius=0.6, color=YELLOW, fill_opacity=0.5)
        right_rect.move_to(positions[2]).shift(RIGHT * 0.5)
        highlights.append(right_rect)

        # Outer: highlight both
        outer_rect = Ellipse(width=1.8, height=1.4, color=YELLOW, fill_opacity=0.3)
        outer_rect.move_to(positions[3]).shift(RIGHT * 0.25)
        highlights.append(outer_rect)

        for i, highlight in enumerate(highlights):
            self.play(Create(highlight), run_time=0.5)
            self.wait(0.5)

        self.wait(1)

        # Recommendation
        recommend = VGroup(
            Rectangle(width=10, height=0.8, color=BLUE, fill_opacity=0.2),
            Text("For AWG: Use LEFT JOIN (keep all pricing, add sales where available)", font_size=18)
        ).to_edge(DOWN)

        self.play(Create(recommend))
        self.wait(2)


class KeyMatching(Scene):
    """Scene 3: Visual showing how keys match between tables"""

    def construct(self):
        # Title
        title = Text("How Keys Match", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Left table (Pricing)
        pricing_title = Text("Pricing", font_size=20, color=BLUE).shift(LEFT * 4 + UP * 1.5)

        pricing_data = VGroup(
            self.create_row(["Item", "Div", "Qtr", "BSP"], header=True),
            self.create_row(["A", "KC", "Q1", "24"]),
            self.create_row(["A", "KC", "Q2", "25"]),
            self.create_row(["B", "KC", "Q1", "18"]),
        ).arrange(DOWN, buff=0).shift(LEFT * 4)

        # Right table (Sales)
        sales_title = Text("Sales", font_size=20, color=GREEN).shift(RIGHT * 4 + UP * 1.5)

        sales_data = VGroup(
            self.create_row(["Item", "Div", "Qtr", "Sales"], header=True, color=GREEN),
            self.create_row(["A", "KC", "Q1", "5000"], color=GREEN),
            self.create_row(["A", "KC", "Q2", "4800"], color=GREEN),
            self.create_row(["C", "KC", "Q1", "3000"], color=GREEN),  # No match in pricing!
        ).arrange(DOWN, buff=0).shift(RIGHT * 4)

        self.play(Write(pricing_title), Create(pricing_data))
        self.play(Write(sales_title), Create(sales_data))
        self.wait(1)

        # Show key columns
        key_text = Text("Keys: Item + Div + Qtr", font_size=18, color=YELLOW).shift(UP * 2.5)
        self.play(Write(key_text))

        # Animate matching lines
        # Match 1: A-KC-Q1
        line1 = Line(
            pricing_data[1].get_right() + LEFT * 0.5,
            sales_data[1].get_left() + RIGHT * 0.5,
            color=YELLOW
        )
        match1 = Text("✓", font_size=24, color=GREEN).move_to(line1.get_center())
        self.play(Create(line1), Write(match1))

        # Match 2: A-KC-Q2
        line2 = Line(
            pricing_data[2].get_right() + LEFT * 0.5,
            sales_data[2].get_left() + RIGHT * 0.5,
            color=YELLOW
        )
        match2 = Text("✓", font_size=24, color=GREEN).move_to(line2.get_center())
        self.play(Create(line2), Write(match2))

        # No match for B-KC-Q1 (no sales)
        no_match1 = Text("No sales data", font_size=12, color=RED)
        no_match1.next_to(pricing_data[3], RIGHT, buff=0.5)
        self.play(Write(no_match1))

        # No match for C-KC-Q1 (no pricing)
        no_match2 = Text("No pricing data", font_size=12, color=RED)
        no_match2.next_to(sales_data[3], LEFT, buff=0.5)
        self.play(Write(no_match2))

        self.wait(1)

        # Show result table
        result_title = Text("Result (Left Join)", font_size=20, color=PURPLE).shift(DOWN * 2)
        result_data = VGroup(
            self.create_row(["Item", "Div", "Qtr", "BSP", "Sales"], header=True, color=PURPLE),
            self.create_row(["A", "KC", "Q1", "24", "5000"], color=PURPLE),
            self.create_row(["A", "KC", "Q2", "25", "4800"], color=PURPLE),
            self.create_row(["B", "KC", "Q1", "18", "NaN"], color=PURPLE),  # No sales
        ).arrange(DOWN, buff=0).shift(DOWN * 3)

        self.play(Write(result_title), Create(result_data))
        self.wait(2)

    def create_row(self, values, header=False, color=BLUE):
        """Helper to create a table row"""
        row = VGroup()
        for val in values:
            cell = VGroup(
                Rectangle(
                    width=1,
                    height=0.4,
                    stroke_color=color,
                    fill_color=color if header else None,
                    fill_opacity=0.3 if header else 0
                ),
                Text(str(val), font_size=12)
            )
            row.add(cell)
        row.arrange(RIGHT, buff=0)
        return row


class AWGMergeStrategy(Scene):
    """Scene 4: Specific AWG merge approach"""

    def construct(self):
        # Title
        title = Text("AWG Merge Strategy", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Step 1: Combine sales sheets
        step1_title = Text("Step 1: Combine 9 Sales Sheets", font_size=24, color=BLUE)
        step1_title.shift(UP * 1.5 + LEFT * 3)

        sheets = VGroup()
        sheet_names = ["KC", "SP", "OK", "NA", "GC", "NE", "GL", "HN", "UM"]
        for i, name in enumerate(sheet_names):
            sheet = VGroup(
                Rectangle(width=0.6, height=0.4, color=GREEN, fill_opacity=0.3),
                Text(name, font_size=10)
            )
            sheets.add(sheet)
        sheets.arrange_in_grid(rows=3, cols=3, buff=0.1)
        sheets.next_to(step1_title, DOWN)

        self.play(Write(step1_title), Create(sheets))
        self.wait(0.5)

        # Arrow to combined
        arrow1 = Arrow(sheets.get_right(), sheets.get_right() + RIGHT * 1.5, color=WHITE)
        combined_sales = VGroup(
            Rectangle(width=1.5, height=1, color=GREEN, fill_opacity=0.5),
            Text("Combined\nSales", font_size=12)
        )
        combined_sales.next_to(arrow1, RIGHT)

        self.play(Create(arrow1), Create(combined_sales))
        self.wait(1)

        # Step 2: Reshape sales
        step2_title = Text("Step 2: Melt Sales to Long Format", font_size=24, color=ORANGE)
        step2_title.shift(DOWN * 0.5 + LEFT * 2)

        code_step2 = Text(
            "$ SALES, $ SALES.1, ... → Quarter column",
            font_size=14, font="Courier"
        ).next_to(step2_title, DOWN)

        self.play(Write(step2_title), Write(code_step2))
        self.wait(1)

        # Step 3: Merge
        step3_title = Text("Step 3: Merge Pricing + Sales", font_size=24, color=PURPLE)
        step3_title.shift(DOWN * 2 + LEFT * 2)

        merge_visual = VGroup(
            Rectangle(width=2, height=0.8, color=BLUE, fill_opacity=0.3),
            Text("Pricing\nLong", font_size=12),
        ).shift(DOWN * 3 + LEFT * 3)

        plus = Text("+", font_size=24).next_to(merge_visual, RIGHT)

        sales_visual = VGroup(
            Rectangle(width=2, height=0.8, color=GREEN, fill_opacity=0.3),
            Text("Sales\nLong", font_size=12),
        ).next_to(plus, RIGHT)

        equals = Text("=", font_size=24).next_to(sales_visual, RIGHT)

        merged_visual = VGroup(
            Rectangle(width=2, height=0.8, color=PURPLE, fill_opacity=0.5),
            Text("Merged!", font_size=12),
        ).next_to(equals, RIGHT)

        self.play(Write(step3_title))
        self.play(Create(merge_visual), Write(plus), Create(sales_visual), Write(equals), Create(merged_visual))

        # Key columns
        key_info = Text("Keys: Item Code, Division, Quarter", font_size=16, color=YELLOW)
        key_info.to_edge(DOWN)
        self.play(Write(key_info))

        self.wait(2)


class MergeIssues(Scene):
    """Scene 5: Common merge problems and solutions"""

    def construct(self):
        # Title
        title = Text("Common Merge Issues", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Issue 1: Non-matching keys
        issue1 = VGroup(
            Text("Issue 1: Non-Matching Keys", font_size=22, color=RED),
            Text("Some pricing items have no sales data", font_size=16),
            Text("Solution: Left join keeps all pricing, NaN for missing sales", font_size=14, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        issue1.shift(UP * 1.2 + LEFT * 2)

        self.play(Write(issue1))
        self.wait(1)

        # Issue 2: Row multiplication
        issue2 = VGroup(
            Text("Issue 2: Unexpected Row Multiplication", font_size=22, color=RED),
            Text("Rows increase after merge (duplicates in one table)", font_size=16),
            Text("Solution: Check for duplicates BEFORE merging", font_size=14, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        issue2.shift(DOWN * 0.5 + LEFT * 2)

        self.play(Write(issue2))
        self.wait(1)

        # Issue 3: Name mismatches
        issue3 = VGroup(
            Text("Issue 3: Key Value Mismatches", font_size=22, color=RED),
            Text("Sales uses 'GO' but pricing uses 'NA' for same division", font_size=16),
            Text("Solution: Fix before merging: {'GO': 'NA', 'NO': 'NE'}", font_size=14, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        issue3.shift(DOWN * 2.2 + LEFT * 2)

        self.play(Write(issue3))
        self.wait(2)

        # Verification code
        verify = VGroup(
            Text("Always verify after merge:", font_size=18, color=YELLOW),
            Text("print(f'Before: {len(pricing)}, After: {len(merged)}')", font_size=14, font="Courier"),
        ).arrange(DOWN).to_edge(DOWN)

        self.play(Write(verify))
        self.wait(2)


# Run instructions
if __name__ == "__main__":
    print("Run with: manim -pql video4_merging_data.py")
    print("\nAvailable scenes:")
    print("  - WhyMerge")
    print("  - MergeTypes")
    print("  - KeyMatching")
    print("  - AWGMergeStrategy")
    print("  - MergeIssues")
