"""
Week 4, Video 1: Wide-to-Long Transformation Animations
========================================================
Manim animations explaining the melt/reshape operation.

To render all scenes:
    manim -pql video1_wide_to_long.py

To render specific scene in high quality:
    manim -pqh video1_wide_to_long.py WideDataProblem

Scenes:
1. WideDataProblem - Shows the problem with 229 columns
2. GranularityExplainer - Explains what granularity means
3. MeltConceptual - High-level view of the melt operation
4. MeltStepByStep - Detailed step-by-step transformation
5. MeltWithCode - Shows the Python code alongside visualization
"""

from manim import *
import numpy as np

# Color scheme for consistency
COLORS = {
    'id_cols': BLUE,
    'value_cols': ORANGE,
    'header': YELLOW,
    'data': WHITE,
    'highlight': GREEN,
    'warning': RED,
    'bg_table': DARK_GREY,
}


class WideDataProblem(Scene):
    """Scene 1: Demonstrates the problem with wide data (229 columns)"""

    def construct(self):
        # Title
        title = Text("The Problem: Wide Data", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create a wide table representation
        # Show only partial columns scrolling
        col_headers = [
            "Item", "Cat", "KC_Q1_BSP", "KC_Q2_BSP", "KC_Q3_BSP", "KC_Q4_BSP",
            "SP_Q1_BSP", "SP_Q2_BSP", "...", "UM_Q4_SRP"
        ]

        # Create header row
        header_cells = VGroup()
        for i, h in enumerate(col_headers):
            cell = VGroup(
                Rectangle(width=1.2, height=0.5, stroke_color=WHITE, fill_color=COLORS['header'], fill_opacity=0.3),
                Text(h, font_size=14)
            )
            header_cells.add(cell)

        header_cells.arrange(RIGHT, buff=0)
        header_cells.move_to(UP * 1)

        # Create data rows
        data_rows = VGroup()
        sample_data = [
            ["A001", "Cereal", "24.00", "24.50", "25.00", "24.75", "23.50", "24.00", "...", "3.49"],
            ["A002", "Dairy", "18.00", "18.00", "18.50", "18.25", "17.50", "17.75", "...", "2.99"],
        ]

        for row_data in sample_data:
            row_cells = VGroup()
            for val in row_data:
                cell = VGroup(
                    Rectangle(width=1.2, height=0.4, stroke_color=WHITE, fill_opacity=0),
                    Text(val, font_size=12)
                )
                row_cells.add(cell)
            row_cells.arrange(RIGHT, buff=0)
            data_rows.add(row_cells)

        data_rows.arrange(DOWN, buff=0)
        data_rows.next_to(header_cells, DOWN, buff=0)

        # Group table
        table = VGroup(header_cells, data_rows)
        table.scale(0.9)

        self.play(Create(table), run_time=2)
        self.wait(1)

        # Show column counter
        counter_text = Text("Columns: ", font_size=36).to_edge(DOWN).shift(UP * 0.5)
        counter = Integer(0, font_size=48).next_to(counter_text, RIGHT)

        self.play(Write(counter_text), Write(counter))
        self.play(ChangeDecimalToValue(counter, 229), run_time=2)

        # Flash warning
        warning = Text("229 columns!", font_size=48, color=RED).next_to(counter, RIGHT, buff=0.5)
        self.play(Write(warning), Flash(counter, color=RED))
        self.wait(1)

        # Show the problems
        problems = VGroup(
            Text("✗ Can't easily filter by division", font_size=24, color=RED),
            Text("✗ Can't easily filter by quarter", font_size=24, color=RED),
            Text("✗ Hard to aggregate", font_size=24, color=RED),
            Text("✗ Hard to merge with other data", font_size=24, color=RED),
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT).shift(DOWN * 0.5)

        for problem in problems:
            self.play(Write(problem), run_time=0.5)

        self.wait(2)

        # Transition out
        self.play(FadeOut(VGroup(table, counter_text, counter, warning, problems, title)))


class GranularityExplainer(Scene):
    """Scene 2: Explains the concept of data granularity"""

    def construct(self):
        # Title
        title = Text("What is Granularity?", font_size=48).to_edge(UP)
        self.play(Write(title))

        # Definition
        definition = Text(
            "Granularity = What does ONE ROW represent?",
            font_size=32
        ).next_to(title, DOWN, buff=0.5)
        self.play(Write(definition))
        self.wait(1)

        # Wide format example
        wide_title = Text("Wide Format", font_size=28, color=ORANGE).shift(LEFT * 3 + UP * 1)
        wide_box = Rectangle(width=5, height=1.5, color=ORANGE).next_to(wide_title, DOWN)
        wide_content = VGroup(
            Text("One Row = One Product", font_size=20),
            Text("(all divisions, all quarters)", font_size=16, color=GREY),
        ).arrange(DOWN).move_to(wide_box)

        wide_group = VGroup(wide_title, wide_box, wide_content)

        # Long format example
        long_title = Text("Long Format", font_size=28, color=GREEN).shift(RIGHT * 3 + UP * 1)
        long_box = Rectangle(width=5, height=1.5, color=GREEN).next_to(long_title, DOWN)
        long_content = VGroup(
            Text("One Row = One Observation", font_size=20),
            Text("(one product, one division, one quarter)", font_size=16, color=GREY),
        ).arrange(DOWN).move_to(long_box)

        long_group = VGroup(long_title, long_box, long_content)

        self.play(Create(wide_group))
        self.wait(1)
        self.play(Create(long_group))
        self.wait(1)

        # Show example transformation
        example_title = Text("Example:", font_size=28).shift(DOWN * 1.5)
        self.play(Write(example_title))

        # Wide example
        wide_ex = Text(
            "Product A → [KC_Q1: $5, KC_Q2: $6, SP_Q1: $4, ...]",
            font_size=20, color=ORANGE
        ).next_to(example_title, DOWN, buff=0.3)

        self.play(Write(wide_ex))
        self.wait(1)

        # Arrow
        arrow = Arrow(DOWN * 0.5, DOWN * 1.5, color=WHITE).next_to(wide_ex, DOWN)
        self.play(Create(arrow))

        # Long example
        long_ex = VGroup(
            Text("Product A, KC, Q1 → $5", font_size=18, color=GREEN),
            Text("Product A, KC, Q2 → $6", font_size=18, color=GREEN),
            Text("Product A, SP, Q1 → $4", font_size=18, color=GREEN),
            Text("...", font_size=18, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(arrow, DOWN)

        for line in long_ex:
            self.play(Write(line), run_time=0.4)

        self.wait(1)

        # Key insight
        insight = VGroup(
            Rectangle(width=10, height=1, color=YELLOW, fill_opacity=0.2),
            Text("Long format: Each row answers ONE specific question", font_size=24, color=YELLOW)
        ).arrange(ORIGIN).to_edge(DOWN)

        self.play(Create(insight))
        self.wait(2)


class MeltConceptual(Scene):
    """Scene 3: High-level conceptual view of the melt operation"""

    def construct(self):
        # Title
        title = Text("The Melt Operation", font_size=48).to_edge(UP)
        self.play(Write(title))

        # Analogy
        analogy = Text(
            "Like melting a wide ice block into a tall, thin column",
            font_size=24, color=GREY
        ).next_to(title, DOWN)
        self.play(Write(analogy))
        self.wait(1)

        # Wide block (ice)
        wide_block = Rectangle(width=8, height=2, color=BLUE, fill_opacity=0.5)
        wide_block.shift(UP * 0.5)
        wide_label = Text("Wide: 4,300 rows × 229 columns", font_size=20).next_to(wide_block, DOWN)

        self.play(Create(wide_block), Write(wide_label))
        self.wait(1)

        # Transform animation
        long_block = Rectangle(width=2, height=6, color=BLUE, fill_opacity=0.5)
        long_block.shift(DOWN * 1)
        long_label = Text("Long: 155,000 rows × 8 columns", font_size=20).next_to(long_block, DOWN)

        self.play(
            Transform(wide_block, long_block),
            Transform(wide_label, long_label),
            run_time=2
        )
        self.wait(1)

        # Show what happened
        explanation = VGroup(
            Text("Column headers became row values", font_size=24),
            Text("More rows, fewer columns", font_size=24),
            Text("Same information, different shape", font_size=24),
        ).arrange(DOWN).to_edge(RIGHT).shift(UP * 0.5)

        for line in explanation:
            self.play(Write(line), run_time=0.5)

        self.wait(2)


class MeltStepByStep(Scene):
    """Scene 4: Detailed step-by-step melt transformation"""

    def construct(self):
        # Title
        title = Text("Melt: Step by Step", font_size=40).to_edge(UP)
        self.play(Write(title))

        # Create "before" table
        before_headers = ["Item", "Cat", "KC_Q1", "KC_Q2", "SP_Q1", "SP_Q2"]
        before_data = [
            ["A", "Cereal", "24", "25", "23", "24"],
            ["B", "Dairy", "18", "18", "17", "18"],
        ]

        before_table = self.create_table(before_headers, before_data)
        before_table.scale(0.7).shift(UP * 1.5)

        before_label = Text("BEFORE (Wide)", font_size=24).next_to(before_table, UP)
        self.play(Create(before_table), Write(before_label))
        self.wait(1)

        # Step 1: Identify ID columns
        step1 = Text("Step 1: Identify ID columns (keep as-is)", font_size=20).to_edge(LEFT).shift(DOWN * 0.5)
        self.play(Write(step1))

        # Highlight ID columns (first 2)
        id_highlight = SurroundingRectangle(
            VGroup(before_table[0][0], before_table[0][1], before_table[1][0], before_table[1][1],
                   before_table[2][0], before_table[2][1]),
            color=BLUE, buff=0.05
        )
        id_label = Text("ID columns", font_size=16, color=BLUE).next_to(id_highlight, UP)
        self.play(Create(id_highlight), Write(id_label))
        self.wait(1)

        # Step 2: Identify value columns
        step2 = Text("Step 2: Identify value columns (to melt)", font_size=20).next_to(step1, DOWN, aligned_edge=LEFT)
        self.play(Write(step2))

        # Highlight value columns
        value_highlight = SurroundingRectangle(
            VGroup(*[before_table[row][col] for row in range(3) for col in range(2, 6)]),
            color=ORANGE, buff=0.05
        )
        value_label = Text("Value columns → become rows", font_size=16, color=ORANGE).next_to(value_highlight, UP)
        self.play(Create(value_highlight), Write(value_label))
        self.wait(1)

        # Step 3: Show the transformation
        step3 = Text("Step 3: Transform!", font_size=20).next_to(step2, DOWN, aligned_edge=LEFT)
        self.play(Write(step3))

        # Create "after" table
        after_headers = ["Item", "Cat", "Div_Qtr", "Price"]
        after_data = [
            ["A", "Cereal", "KC_Q1", "24"],
            ["A", "Cereal", "KC_Q2", "25"],
            ["A", "Cereal", "SP_Q1", "23"],
            ["A", "Cereal", "SP_Q2", "24"],
            ["B", "Dairy", "KC_Q1", "18"],
            ["B", "Dairy", "KC_Q2", "18"],
            ["...", "...", "...", "..."],
        ]

        after_table = self.create_table(after_headers, after_data)
        after_table.scale(0.6).shift(DOWN * 2)

        after_label = Text("AFTER (Long)", font_size=24).next_to(after_table, UP)

        # Animate transformation
        self.play(
            FadeOut(id_highlight), FadeOut(value_highlight),
            FadeOut(id_label), FadeOut(value_label)
        )

        # Arrow indicating transformation
        arrow = Arrow(before_table.get_bottom(), after_table.get_top(), color=GREEN)
        arrow_label = Text("melt()", font_size=20, color=GREEN).next_to(arrow, RIGHT)

        self.play(Create(arrow), Write(arrow_label))
        self.play(Create(after_table), Write(after_label))
        self.wait(1)

        # Row count comparison
        row_compare = VGroup(
            Text("2 rows → 8 rows", font_size=24, color=GREEN),
            Text("(would be ~155,000 with full data)", font_size=16, color=GREY)
        ).arrange(DOWN).to_edge(RIGHT).shift(DOWN)

        self.play(Write(row_compare))
        self.wait(2)

    def create_table(self, headers, data):
        """Helper to create a simple table"""
        table = VGroup()

        # Header row
        header_row = VGroup()
        for h in headers:
            cell = VGroup(
                Rectangle(width=1.3, height=0.4, stroke_color=WHITE, fill_color=YELLOW, fill_opacity=0.3),
                Text(h, font_size=14)
            )
            header_row.add(cell)
        header_row.arrange(RIGHT, buff=0)
        table.add(header_row)

        # Data rows
        for row_data in data:
            row = VGroup()
            for val in row_data:
                cell = VGroup(
                    Rectangle(width=1.3, height=0.35, stroke_color=WHITE),
                    Text(str(val), font_size=12)
                )
                row.add(cell)
            row.arrange(RIGHT, buff=0)
            table.add(row)

        table.arrange(DOWN, buff=0)
        return table


class MeltWithCode(Scene):
    """Scene 5: Shows Python code alongside visualization"""

    def construct(self):
        # Title
        title = Text("Melt in Python", font_size=40).to_edge(UP)
        self.play(Write(title))

        # Split screen: code on left, visualization on right
        code_lines = [
            "# Step 1: Identify ID columns",
            "id_cols = ['Item Code', 'Category']",
            "",
            "# Step 2: Identify value columns",
            "price_cols = [c for c in df.columns",
            "              if '_BSP' in c]",
            "",
            "# Step 3: Melt!",
            "long_df = pd.melt(",
            "    df,",
            "    id_vars=id_cols,",
            "    value_vars=price_cols,",
            "    var_name='Division_Quarter',",
            "    value_name='BSP'",
            ")"
        ]

        code_text = VGroup()
        for line in code_lines:
            code_text.add(Text(line, font_size=16, font="Courier"))
        code_text.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        code_text.scale(0.8).to_edge(LEFT).shift(DOWN * 0.5)

        # Animate code appearing
        code_box = SurroundingRectangle(code_text, color=GREY, buff=0.2)
        self.play(Create(code_box))

        for line in code_text:
            self.play(Write(line), run_time=0.3)

        self.wait(1)

        # Show result on right
        result_title = Text("Result:", font_size=24).to_edge(RIGHT).shift(UP * 2 + LEFT)

        result_lines = [
            "Wide: 4,300 × 229",
            "     ↓",
            "Long: 155,000 × 8",
            "",
            "Columns now:",
            "• Item Code",
            "• Category",
            "• Division_Quarter",
            "• BSP",
        ]

        result_text = VGroup()
        for line in result_lines:
            result_text.add(Text(line, font_size=18))
        result_text.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        result_text.next_to(result_title, DOWN, aligned_edge=LEFT)

        self.play(Write(result_title))
        for line in result_text:
            self.play(Write(line), run_time=0.3)

        self.wait(2)

        # Key insight
        insight = VGroup(
            Rectangle(width=12, height=0.8, color=GREEN, fill_opacity=0.2),
            Text("Column names (KC_Q1_BSP) became data values!", font_size=20, color=GREEN)
        ).to_edge(DOWN)

        self.play(Create(insight))
        self.wait(2)


class ColumnPatternAnimation(Scene):
    """Bonus: Shows how 216 pricing columns are structured"""

    def construct(self):
        # Title
        title = Text("Understanding the Column Pattern", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Formula
        formula = MathTex(
            r"9 \text{ divisions} \times 4 \text{ quarters} \times 6 \text{ price types} = 216 \text{ columns}",
            font_size=32
        ).next_to(title, DOWN, buff=0.5)
        self.play(Write(formula))
        self.wait(1)

        # Divisions
        divisions = VGroup(
            Text("Divisions:", font_size=20, color=BLUE),
            Text("KC, SP, OK, NA, GC, NE, GL, HN, UM", font_size=18)
        ).arrange(RIGHT).shift(UP * 0.5)

        # Quarters
        quarters = VGroup(
            Text("Quarters:", font_size=20, color=GREEN),
            Text("Q1, Q2, Q3, Q4", font_size=18)
        ).arrange(RIGHT).next_to(divisions, DOWN)

        # Price types
        price_types = VGroup(
            Text("Price Types:", font_size=20, color=ORANGE),
            Text("List Cost, BSP, SRP, Deal, TPR, Retail", font_size=18)
        ).arrange(RIGHT).next_to(quarters, DOWN)

        self.play(Write(divisions))
        self.play(Write(quarters))
        self.play(Write(price_types))
        self.wait(1)

        # Show example column name
        example = VGroup(
            Text("Example column: ", font_size=24),
            Text("KC", font_size=24, color=BLUE),
            Text("_", font_size=24),
            Text("Q1", font_size=24, color=GREEN),
            Text("_", font_size=24),
            Text("BSP", font_size=24, color=ORANGE),
        ).arrange(RIGHT, buff=0.1).shift(DOWN * 1.5)

        self.play(Write(example))
        self.wait(1)

        # Highlight pattern
        pattern_box = SurroundingRectangle(example[1:], color=YELLOW)
        pattern_label = Text("Division_Quarter_PriceType", font_size=20, color=YELLOW).next_to(pattern_box, DOWN)

        self.play(Create(pattern_box), Write(pattern_label))
        self.wait(2)


# Run all scenes for testing
if __name__ == "__main__":
    # This file should be run with manim command, not directly
    print("Run with: manim -pql video1_wide_to_long.py")
    print("\nAvailable scenes:")
    print("  - WideDataProblem")
    print("  - GranularityExplainer")
    print("  - MeltConceptual")
    print("  - MeltStepByStep")
    print("  - MeltWithCode")
    print("  - ColumnPatternAnimation")
