"""
Week 4, Video 2: The Unit Discovery - Critical Animation Set
=============================================================
Zone-based layout with explicit Y coordinates to prevent overlap.

Zone Layout:
  Zone 1: Y = +3.0 to +4.0  (Title)
  Zone 2: Y = +1.8 to +3.0  (Subtitle)
  Zone 3: Y = -1.0 to +1.8  (Main content)
  Zone 4: Y = -2.5 to -1.0  (Secondary)
  Zone 5: Y = -4.0 to -2.5  (Footer)

To render all: manim -pql video2_unit_discovery.py
To render one: manim -pql video2_unit_discovery.py CaseVsUnitReveal
"""

from manim import *
import numpy as np


class TheMystery(Scene):
    """Scene 1: Shows the mysterious wrong results"""

    def construct(self):
        # Zone 1: Title at Y = +3.5
        title = Text("The Mystery", font_size=42)
        title.move_to(UP * 3.5)
        self.play(Write(title))
        self.wait(0.5)

        # Zone 2: Expected at Y = +2.3
        expect = VGroup(
            Text("Expected:", font_size=20, color=GREEN),
            Text("BC ~20% cheaper than NB", font_size=18)
        ).arrange(RIGHT, buff=0.3)
        expect.move_to(UP * 2.3)
        self.play(Write(expect))

        # Zone 3 top: Found at Y = +1.3
        found = VGroup(
            Text("Found:", font_size=20, color=RED),
            Text("Avg gap only 13.8%", font_size=18)
        ).arrange(RIGHT, buff=0.3)
        found.move_to(UP * 1.3)
        self.play(Write(found))
        self.wait(0.5)

        # Zone 3 bottom: Alarm at Y = +0.3
        alarm = VGroup(
            Text("Negative gaps:", font_size=18),
            Text("3,005 items (9.7%)", font_size=20, color=RED)
        ).arrange(RIGHT, buff=0.2)
        alarm.move_to(UP * 0.3)
        self.play(Write(alarm), Flash(alarm[1], color=RED))
        self.wait(1)

        # Phase 2: Clear and show chart
        self.play(FadeOut(expect), FadeOut(found), FadeOut(alarm))

        # Zone 2: Condensed stat
        stat = Text("9.7% of products show BC > NB", font_size=18, color=RED)
        stat.move_to(UP * 2.5)
        self.play(Write(stat))

        # Zone 3-4: Axes centered at Y = -0.3
        axes = Axes(
            x_range=[0, 100, 25],
            y_range=[-30, 50, 20],
            x_length=9,
            y_length=4,
            axis_config={"include_numbers": True, "font_size": 12},
        )
        axes.move_to(DOWN * 0.3)
        self.play(Create(axes))

        # Reference lines
        target = axes.plot(lambda x: 20, x_range=[0, 100], color=GREEN, stroke_width=2)
        zero = axes.plot(lambda x: 0, x_range=[0, 100], color=YELLOW, stroke_width=2)
        t_label = Text("20%", font_size=10, color=GREEN).next_to(axes.c2p(100, 20), RIGHT, buff=0.1)
        z_label = Text("0%", font_size=10, color=YELLOW).next_to(axes.c2p(100, 0), RIGHT, buff=0.1)
        self.play(Create(target), Create(zero), Write(t_label), Write(z_label))

        # Scatter points
        np.random.seed(42)
        points = VGroup()
        for _ in range(30):
            x = np.random.uniform(5, 95)
            y = np.random.normal(-5, 10) if np.random.random() < 0.3 else np.random.normal(18, 8)
            y = np.clip(y, -28, 48)
            points.add(Dot(axes.c2p(x, y), radius=0.04, color=RED if y < 0 else WHITE))
        self.play(Create(points), run_time=1.5)

        # Zone 5: Question at Y = -3.2
        question = Text("Why are so many showing BC > NB?", font_size=20, color=YELLOW)
        question.move_to(DOWN * 3.2)
        self.play(Write(question))
        self.wait(2)


class InvestigationBegins(Scene):
    """Scene 2: Looking at a specific product"""

    def construct(self):
        # Zone 1: Title at Y = +3.5
        title = Text("Let's Investigate One Product", font_size=36)
        title.move_to(UP * 3.5)
        self.play(Write(title))

        # Zone 2: Product name at Y = +2.5
        product = Text("FROSTED FLAKES 15OZ", font_size=22, color=YELLOW)
        product.move_to(UP * 2.5)
        self.play(Write(product))
        self.wait(0.5)

        # Zone 3: Left side - BC at X = -3.5
        bc_header = Text("Best Choice", font_size=20, color=GREEN)
        bc_header.move_to(LEFT * 3.5 + UP * 1.3)

        bc_data = VGroup(
            Text("Pack: 12", font_size=16, color=ORANGE),
            Text("BSP: $28.80", font_size=16),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        bc_box = SurroundingRectangle(bc_data, color=GREEN, buff=0.15)
        bc_group = VGroup(bc_box, bc_data)
        bc_group.move_to(LEFT * 3.5 + UP * 0.4)

        # Zone 3: Right side - NB at X = +3.5
        nb_header = Text("National Brand", font_size=20, color=RED)
        nb_header.move_to(RIGHT * 3.5 + UP * 1.3)

        nb_data = VGroup(
            Text("Pack: 1", font_size=16, color=BLUE),
            Text("BSP: $3.50", font_size=16),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        nb_box = SurroundingRectangle(nb_data, color=RED, buff=0.15)
        nb_group = VGroup(nb_box, nb_data)
        nb_group.move_to(RIGHT * 3.5 + UP * 0.4)

        self.play(Write(bc_header), Write(nb_header))
        self.play(Create(bc_group), Create(nb_group))
        self.wait(1)

        # Zone 4 top: Highlight at Y = -1.3
        highlight = Text("Pack sizes are DIFFERENT!", font_size=20, color=YELLOW)
        highlight.move_to(DOWN * 1.3)
        self.play(Write(highlight))
        self.wait(0.5)

        # Zone 4 bottom: Calc at Y = -2.0
        calc = MathTex(r"\frac{\$3.50 - \$28.80}{\$3.50} = -723\%", font_size=24, color=RED)
        calc.move_to(DOWN * 2.0)
        self.play(Write(calc))

        nonsense = Text("Nonsense!", font_size=18, color=RED)
        nonsense.move_to(DOWN * 2.7)
        self.play(Write(nonsense))
        self.wait(1)

        # Zone 5: Transition at Y = -3.3
        transition = Text("We're comparing CASE price to UNIT price!", font_size=20, color=YELLOW)
        transition.move_to(DOWN * 3.3)
        self.play(Write(transition))
        self.wait(2)


class CaseVsUnitReveal(Scene):
    """Scene 3: THE critical 'aha' moment"""

    def construct(self):
        # Zone 1: Title at Y = +3.5
        title = Text("The Discovery", font_size=40, color=YELLOW)
        title.move_to(UP * 3.5)
        self.play(Write(title))

        # Zone 2: Subtitle at Y = +2.5
        subtitle = Text("Inconsistent Pack Size Reporting", font_size=22)
        subtitle.move_to(UP * 2.5)
        self.play(Write(subtitle))
        self.wait(0.5)

        # Zone 3 Left: BC at X = -3.5
        bc_title = Text("Best Choice", font_size=18, color=GREEN)
        bc_title.move_to(LEFT * 3.5 + UP * 1.2)

        bc_pack = Text("Pack = 12", font_size=16, color=ORANGE)
        bc_pack.move_to(LEFT * 3.5 + UP * 0.8)

        case_boxes = VGroup(*[Square(side_length=0.25, color=ORANGE, fill_opacity=0.5) for _ in range(12)])
        case_boxes.arrange_in_grid(rows=3, cols=4, buff=0.05)
        case_boxes.move_to(LEFT * 3.5 + UP * 0.1)

        bc_price = Text("BSP: $28.80", font_size=16)
        bc_price.move_to(LEFT * 3.5 + DOWN * 0.6)

        bc_section = VGroup(bc_title, bc_pack, case_boxes, bc_price)

        # Zone 3 Right: NB at X = +3.5
        nb_title = Text("National Brand", font_size=18, color=RED)
        nb_title.move_to(RIGHT * 3.5 + UP * 1.2)

        nb_pack = Text("Pack = 1", font_size=16, color=BLUE)
        nb_pack.move_to(RIGHT * 3.5 + UP * 0.8)

        unit_box = Square(side_length=0.5, color=BLUE, fill_opacity=0.5)
        unit_box.move_to(RIGHT * 3.5 + UP * 0.1)

        nb_price = Text("BSP: $3.50", font_size=16)
        nb_price.move_to(RIGHT * 3.5 + DOWN * 0.6)

        nb_section = VGroup(nb_title, nb_pack, unit_box, nb_price)

        # Zone 3 Center: "vs"
        vs_text = Text("vs", font_size=24, color=GREY)
        vs_text.move_to(ORIGIN)

        self.play(Create(bc_section), Create(nb_section))
        self.wait(0.5)
        self.play(Write(vs_text))

        # Zone 4: Problem at Y = -1.8
        problem = Text("Comparing 12 units to 1 unit!", font_size=20, color=RED)
        problem.move_to(DOWN * 1.8)
        self.play(Write(problem), Flash(problem, color=RED))
        self.wait(1.5)

        # Phase 2: Clear and show fix
        self.play(FadeOut(subtitle), FadeOut(bc_section), FadeOut(nb_section), FadeOut(vs_text), FadeOut(problem))

        # Zone 2: Fix subtitle
        fix_sub = Text("The Fix: Normalize to Per-Unit", font_size=22, color=GREEN)
        fix_sub.move_to(UP * 2.5)
        self.play(Write(fix_sub))

        # Zone 3: Formula at Y = +0.5
        formula = MathTex(r"\text{BC per unit} = \frac{\$28.80}{12} = \$2.40", font_size=28)
        formula.move_to(UP * 0.5)
        self.play(Write(formula))
        self.wait(0.5)

        # Zone 4 top: Comparison at Y = -0.5
        comp = VGroup(
            Text("BC: $2.40/unit", font_size=20, color=GREEN),
            Text("vs", font_size=16, color=GREY),
            Text("NB: $3.50/unit", font_size=20, color=RED),
        ).arrange(RIGHT, buff=0.4)
        comp.move_to(DOWN * 0.5)
        self.play(Write(comp))

        # Zone 4 bottom: Result at Y = -1.5
        result = VGroup(
            Text("Correct Gap:", font_size=18),
            MathTex(r"31.4\%", font_size=28, color=GREEN)
        ).arrange(RIGHT, buff=0.3)
        result.move_to(DOWN * 1.5)
        self.play(Write(result))

        # Zone 5: Success at Y = -3.0
        success = Text("BC IS cheaper - we just measured wrong!", font_size=20, color=GREEN)
        success.move_to(DOWN * 3.0)
        self.play(Write(success))
        self.wait(2)


class NormalizationFix(Scene):
    """Scene 4: Shows the fix"""

    def construct(self):
        # Zone 1: Title at Y = +3.5
        title = Text("The Fix: Normalize Prices", font_size=36)
        title.move_to(UP * 3.5)
        self.play(Write(title))

        # Zone 2: Insight at Y = +2.3
        insight = Text("BC Pack = case size | NB Pack = 1 unit", font_size=20, color=YELLOW)
        insight_box = SurroundingRectangle(insight, color=YELLOW, buff=0.15)
        insight_group = VGroup(insight_box, insight)
        insight_group.move_to(UP * 2.3)
        self.play(Create(insight_group))
        self.wait(0.5)

        # Zone 3 top: Formula at Y = +1.0
        formula = MathTex(r"\text{Unit Price} = \frac{\text{Price}}{\text{Pack}}", font_size=28)
        formula.move_to(UP * 1.0)
        self.play(Write(formula))
        self.wait(0.5)

        # Zone 3 bottom: Code at Y = -0.3
        code = VGroup(
            Text("df['BSP_per_unit'] = df['BSP'] / df['Pack']", font_size=14, font="Consolas"),
            Text("df['Cost_per_unit'] = df['List Cost'] / df['Pack']", font_size=14, font="Consolas"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        code_box = SurroundingRectangle(code, color=GREY, buff=0.1)
        code_group = VGroup(code_box, code)
        code_group.move_to(DOWN * 0.3)
        self.play(Create(code_group))
        self.wait(0.5)

        # Zone 4: Example at Y = -1.8
        example = Text("$28.80 / 12 = $2.40 per unit", font_size=18, color=GREEN)
        example.move_to(DOWN * 1.8)
        self.play(Write(example))
        self.wait(2)


class BeforeAfterImpact(Scene):
    """Scene 5: Before/after comparison"""

    def construct(self):
        # Zone 1: Title at Y = +3.5
        title = Text("The Impact", font_size=40)
        title.move_to(UP * 3.5)
        self.play(Write(title))

        # Zone 2-3 Left: BEFORE at X = -3.2
        before_title = Text("BEFORE", font_size=24, color=RED)
        before_title.move_to(LEFT * 3.2 + UP * 2.3)

        before_content = VGroup(
            Text("Avg Gap: 13.8%", font_size=18),
            Text("(below target)", font_size=12, color=GREY),
            Text("Negative: 3,005", font_size=18, color=RED),
        ).arrange(DOWN, buff=0.15)
        before_box = SurroundingRectangle(before_content, color=RED, buff=0.2, fill_opacity=0.05)
        before_group = VGroup(before_box, before_content)
        before_group.move_to(LEFT * 3.2 + UP * 0.5)

        self.play(Write(before_title), Create(before_group))

        # Zone 3 Center: Arrow at ORIGIN
        arrow = Arrow(LEFT * 0.8, RIGHT * 0.8, color=YELLOW, stroke_width=5)
        arrow.move_to(ORIGIN)
        arrow_label = Text("Normalize", font_size=14, color=YELLOW)
        arrow_label.move_to(UP * 0.5)
        self.play(Create(arrow), Write(arrow_label))

        # Zone 2-3 Right: AFTER at X = +3.2
        after_title = Text("AFTER", font_size=24, color=GREEN)
        after_title.move_to(RIGHT * 3.2 + UP * 2.3)

        after_content = VGroup(
            Text("Avg Gap: 32.3%", font_size=18),
            Text("(exceeds target!)", font_size=12, color=GREEN),
            Text("Negative: 40", font_size=18, color=GREEN),
        ).arrange(DOWN, buff=0.15)
        after_box = SurroundingRectangle(after_content, color=GREEN, buff=0.2, fill_opacity=0.05)
        after_group = VGroup(after_box, after_content)
        after_group.move_to(RIGHT * 3.2 + UP * 0.5)

        self.play(Write(after_title), Create(after_group))
        self.wait(1)

        # Zone 4: Impact lines at Y = -1.8 and -2.3
        impact1 = Text("Gap DOUBLED: 13.8% -> 32.3%", font_size=18, color=YELLOW)
        impact1.move_to(DOWN * 1.8)
        self.play(Write(impact1))

        impact2 = Text("Problems reduced 98.7%", font_size=18, color=YELLOW)
        impact2.move_to(DOWN * 2.3)
        self.play(Write(impact2))

        # Zone 5: Final at Y = -3.2
        final = Text("One discovery changed everything!", font_size=22, color=YELLOW)
        final.move_to(DOWN * 3.2)
        self.play(Write(final))
        self.wait(2)


class AlwaysCheckUnits(Scene):
    """Scene 6: Final takeaway"""

    def construct(self):
        # Zone 1-2: Main message at Y = +2.5
        main = Text("ALWAYS CHECK YOUR UNITS", font_size=42, color=YELLOW)
        main.move_to(UP * 2.5)
        self.play(Write(main), run_time=1.5)
        self.play(Flash(main, color=YELLOW, line_length=0.3, flash_radius=1.2))
        self.wait(0.5)

        # Zone 3: Lessons at Y = +0.8 to -1.2
        lessons = VGroup(
            Text("1. BC Pack = case size (e.g., 12)", font_size=18),
            Text("2. NB Pack = 1 (single unit)", font_size=18),
            Text("3. Direct comparison mixed cases with units", font_size=18),
            Text("4. Normalizing revealed the truth", font_size=18, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        lessons.move_to(DOWN * 0.2)

        for lesson in lessons:
            self.play(Write(lesson), run_time=0.5)
        self.wait(1)

        # Zone 5: Wisdom at Y = -3.0
        wisdom = Text("Data doesn't lie, but units can deceive.", font_size=22)
        wisdom.move_to(DOWN * 3.0)
        self.play(Write(wisdom))
        self.wait(2)


class HistogramMorph(Scene):
    """Scene 7: Animated histogram showing before/after"""

    def construct(self):
        # Zone 1: Title at Y = +3.5
        title = Text("Price Gap Distribution", font_size=32)
        title.move_to(UP * 3.5)
        self.play(Write(title))

        # Zone 2: State label at Y = +2.5
        state = Text("Before Normalization", font_size=18, color=RED)
        state.move_to(UP * 2.5)
        self.play(Write(state))

        # Zone 3-4: Axes centered at Y = -0.2
        axes = Axes(
            x_range=[-20, 60, 20],
            y_range=[0, 700, 200],
            x_length=10,
            y_length=4,
            axis_config={"include_numbers": True, "font_size": 12},
        )
        axes.move_to(DOWN * 0.2)

        x_label = Text("Price Gap (%)", font_size=12)
        x_label.move_to(DOWN * 2.5)
        self.play(Create(axes), Write(x_label))

        # Reference lines
        target = DashedLine(axes.c2p(20, 0), axes.c2p(20, 650), color=GREEN, stroke_width=2)
        t_text = Text("20%", font_size=10, color=GREEN).next_to(axes.c2p(20, 650), UP, buff=0.05)
        zero = DashedLine(axes.c2p(0, 0), axes.c2p(0, 650), color=YELLOW, stroke_width=2)
        self.play(Create(target), Write(t_text), Create(zero))

        # Before bars
        before_h = [60, 120, 250, 450, 380, 550, 500, 320, 180, 90, 40, 20]
        centers = list(range(-15, 55, 5))

        before_bars = VGroup()
        for c, h in zip(centers[:len(before_h)], before_h):
            bar_h = (h / 700) * 4
            bar = Rectangle(width=0.35, height=bar_h, fill_color=RED, fill_opacity=0.7, stroke_color=RED, stroke_width=1)
            bar.move_to(axes.c2p(c, 0) + UP * bar_h / 2)
            before_bars.add(bar)

        self.play(Create(before_bars), run_time=1.5)
        self.wait(1)

        # Transform to after
        after_state = Text("After Normalization", font_size=18, color=GREEN)
        after_state.move_to(UP * 2.5)

        after_h = [10, 20, 40, 70, 130, 300, 500, 650, 550, 350, 180, 80]
        after_bars = VGroup()
        for c, h in zip(centers[:len(after_h)], after_h):
            shifted = c + 15
            if shifted > 50:
                continue
            bar_h = (h / 700) * 4
            bar = Rectangle(width=0.35, height=bar_h, fill_color=GREEN, fill_opacity=0.7, stroke_color=GREEN, stroke_width=1)
            bar.move_to(axes.c2p(shifted, 0) + UP * bar_h / 2)
            after_bars.add(bar)

        self.play(Transform(before_bars, after_bars), Transform(state, after_state), run_time=2.5)
        self.wait(1)

        # Zone 5: Note at Y = -3.2
        note = Text("Distribution shifted right - most now above 20%!", font_size=16)
        note.move_to(DOWN * 3.2)
        self.play(Write(note))
        self.wait(2)


if __name__ == "__main__":
    print("Run: manim -pql video2_unit_discovery.py")
    print("\nScenes: TheMystery, InvestigationBegins, CaseVsUnitReveal,")
    print("        NormalizationFix, BeforeAfterImpact, AlwaysCheckUnits, HistogramMorph")
