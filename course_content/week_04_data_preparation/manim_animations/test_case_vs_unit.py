"""
Test file for CaseVsUnitReveal with zone-based layout.
All elements have explicit Y coordinates to prevent overlap.

Zone Layout:
  Zone 1: Y = +3.0 to +4.0  (Title)
  Zone 2: Y = +1.8 to +3.0  (Subtitle)
  Zone 3: Y = -1.0 to +1.8  (Main content)
  Zone 4: Y = -2.5 to -1.0  (Secondary)
  Zone 5: Y = -4.0 to -2.5  (Footer)

To render:
    manim -pql test_case_vs_unit.py CaseVsUnitReveal
"""

from manim import *


class CaseVsUnitReveal(Scene):
    """THE critical 'aha' moment - zone-based layout version"""

    def construct(self):
        # ============================================
        # PHASE 1: Show the Problem
        # ============================================

        # Zone 1: Title at Y = +3.5
        title = Text("The Discovery", font_size=40, color=YELLOW)
        title.move_to(UP * 3.5)
        self.play(Write(title))

        # Zone 2: Subtitle at Y = +2.5
        subtitle = Text("Inconsistent Pack Size Reporting", font_size=22)
        subtitle.move_to(UP * 2.5)
        self.play(Write(subtitle))
        self.wait(0.5)

        # Zone 3: Main content - LEFT side (BC) at X = -3.5
        bc_title = Text("Best Choice", font_size=18, color=GREEN)
        bc_title.move_to(LEFT * 3.5 + UP * 1.2)

        bc_pack = Text("Pack = 12", font_size=16, color=ORANGE)
        bc_pack.move_to(LEFT * 3.5 + UP * 0.8)

        # 12 boxes in 3x4 grid, centered at Y = +0.1
        case_boxes = VGroup()
        for _ in range(12):
            box = Square(side_length=0.25, color=ORANGE, fill_opacity=0.5)
            case_boxes.add(box)
        case_boxes.arrange_in_grid(rows=3, cols=4, buff=0.05)
        case_boxes.move_to(LEFT * 3.5 + UP * 0.1)

        bc_price = Text("BSP: $28.80", font_size=16)
        bc_price.move_to(LEFT * 3.5 + DOWN * 0.6)

        bc_section = VGroup(bc_title, bc_pack, case_boxes, bc_price)

        # Zone 3: Main content - RIGHT side (NB) at X = +3.5
        nb_title = Text("National Brand", font_size=18, color=RED)
        nb_title.move_to(RIGHT * 3.5 + UP * 1.2)

        nb_pack = Text("Pack = 1", font_size=16, color=BLUE)
        nb_pack.move_to(RIGHT * 3.5 + UP * 0.8)

        # 1 box centered at Y = +0.1
        unit_box = Square(side_length=0.5, color=BLUE, fill_opacity=0.5)
        unit_box.move_to(RIGHT * 3.5 + UP * 0.1)

        nb_price = Text("BSP: $3.50", font_size=16)
        nb_price.move_to(RIGHT * 3.5 + DOWN * 0.6)

        nb_section = VGroup(nb_title, nb_pack, unit_box, nb_price)

        # Zone 3: Center - "vs" at ORIGIN
        vs_text = Text("vs", font_size=24, color=GREY)
        vs_text.move_to(ORIGIN)

        # Animate Phase 1 main content
        self.play(Create(bc_section), Create(nb_section))
        self.wait(0.5)
        self.play(Write(vs_text))

        # Zone 4: Problem message at Y = -1.8
        problem = Text("Comparing 12 units to 1 unit!", font_size=20, color=RED)
        problem.move_to(DOWN * 1.8)
        self.play(Write(problem), Flash(problem, color=RED))
        self.wait(1.5)

        # ============================================
        # PHASE 2: Show the Fix (after clearing)
        # ============================================

        # FadeOut Phase 1 content (keep title)
        self.play(
            FadeOut(subtitle),
            FadeOut(bc_section),
            FadeOut(nb_section),
            FadeOut(vs_text),
            FadeOut(problem)
        )

        # Zone 2: New subtitle at Y = +2.5
        fix_subtitle = Text("The Fix: Normalize to Per-Unit", font_size=22, color=GREEN)
        fix_subtitle.move_to(UP * 2.5)
        self.play(Write(fix_subtitle))

        # Zone 3: Formula at Y = +0.5
        formula = MathTex(
            r"\text{BC per unit} = \frac{\$28.80}{12} = \$2.40",
            font_size=28
        )
        formula.move_to(UP * 0.5)
        self.play(Write(formula))
        self.wait(0.5)

        # Zone 4: Comparison at Y = -0.5
        comparison = VGroup(
            Text("BC: $2.40/unit", font_size=20, color=GREEN),
            Text("vs", font_size=16, color=GREY),
            Text("NB: $3.50/unit", font_size=20, color=RED),
        ).arrange(RIGHT, buff=0.4)
        comparison.move_to(DOWN * 0.5)
        self.play(Write(comparison))
        self.wait(0.5)

        # Zone 4: Result at Y = -1.5
        result = VGroup(
            Text("Correct Gap:", font_size=18),
            MathTex(r"31.4\%", font_size=28, color=GREEN)
        ).arrange(RIGHT, buff=0.3)
        result.move_to(DOWN * 1.5)
        self.play(Write(result))
        self.wait(0.5)

        # Zone 5: Success message at Y = -3.0
        success = Text("BC IS cheaper - we just measured wrong!", font_size=20, color=GREEN)
        success.move_to(DOWN * 3.0)
        self.play(Write(success))
        self.wait(2)


# Run instructions
if __name__ == "__main__":
    print("Run with: manim -pql test_case_vs_unit.py CaseVsUnitReveal")
