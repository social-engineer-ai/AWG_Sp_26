"""
Week 4, Video 3: Data Pipeline Best Practices
==============================================
Animations showing reproducible data pipeline concepts.

To render:
    manim -pql video3_data_pipeline.py

Scenes:
1. NightmareVsDream - Contrasts messy vs clean pipelines
2. PipelineFlowchart - Shows the standard pipeline stages
3. ConfigurationTop - Emphasizes config at top of notebook
4. IntermediateSaves - Shows checkpoint saving concept
5. AWGPipeline - The specific AWG data pipeline
"""

from manim import *


class NightmareVsDream(Scene):
    """Scene 1: Contrasts the nightmare of messy code with clean pipeline"""

    def construct(self):
        # Title
        title = Text("Two Approaches to Data Prep", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Left side: Nightmare
        nightmare_title = Text("The Nightmare", font_size=28, color=RED).shift(LEFT * 3.5 + UP * 1.5)
        nightmare_box = Rectangle(width=5, height=4, color=RED, fill_opacity=0.1)
        nightmare_box.shift(LEFT * 3.5 + DOWN * 0.5)

        nightmare_items = VGroup(
            Text("• Cells run out of order", font_size=16),
            Text("• Magic numbers everywhere", font_size=16),
            Text("• 'Which file is correct?'", font_size=16),
            Text("• No documentation", font_size=16),
            Text("• Can't reproduce results", font_size=16),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(nightmare_box)

        # Icon: explosion/chaos
        nightmare_icon = Text("💥", font_size=48).next_to(nightmare_box, UP).shift(DOWN * 0.3 + RIGHT * 2)

        self.play(Write(nightmare_title), Create(nightmare_box))
        self.play(Write(nightmare_items), Write(nightmare_icon))
        self.wait(1)

        # Right side: Dream
        dream_title = Text("The Dream", font_size=28, color=GREEN).shift(RIGHT * 3.5 + UP * 1.5)
        dream_box = Rectangle(width=5, height=4, color=GREEN, fill_opacity=0.1)
        dream_box.shift(RIGHT * 3.5 + DOWN * 0.5)

        dream_items = VGroup(
            Text("• Clear sections", font_size=16),
            Text("• Config at the top", font_size=16),
            Text("• Intermediate saves", font_size=16),
            Text("• Documented decisions", font_size=16),
            Text("• Click 'Run All' → works!", font_size=16, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(dream_box)

        dream_icon = Text("✨", font_size=48).next_to(dream_box, UP).shift(DOWN * 0.3 + LEFT * 2)

        self.play(Write(dream_title), Create(dream_box))
        self.play(Write(dream_items), Write(dream_icon))
        self.wait(2)

        # Transition message
        message = Text("Let's build pipelines that work every time.", font_size=24)
        message.to_edge(DOWN)
        self.play(Write(message))
        self.wait(2)


class PipelineFlowchart(Scene):
    """Scene 2: Shows the standard data pipeline stages"""

    def construct(self):
        # Title
        title = Text("The Standard Pipeline", font_size=40).to_edge(UP)
        self.play(Write(title))

        # Pipeline stages
        stages = ["RAW DATA", "LOAD", "VALIDATE", "TRANSFORM", "SAVE", "ANALYZE"]
        colors = [GREY, BLUE, YELLOW, ORANGE, GREEN, PURPLE]

        boxes = VGroup()
        arrows = VGroup()

        for i, (stage, color) in enumerate(zip(stages, colors)):
            box = VGroup(
                RoundedRectangle(width=2, height=0.8, corner_radius=0.1, color=color, fill_opacity=0.3),
                Text(stage, font_size=16)
            )
            boxes.add(box)

        boxes.arrange(RIGHT, buff=0.5)
        boxes.shift(UP * 0.5)

        # Create arrows between boxes
        for i in range(len(boxes) - 1):
            arrow = Arrow(
                boxes[i].get_right(),
                boxes[i + 1].get_left(),
                color=WHITE,
                buff=0.1,
                stroke_width=2
            )
            arrows.add(arrow)

        # Animate pipeline building
        for i, box in enumerate(boxes):
            self.play(Create(box), run_time=0.5)
            if i < len(arrows):
                self.play(Create(arrows[i]), run_time=0.3)

        self.wait(1)

        # Add descriptions below each stage
        descriptions = [
            "Never modify!",
            "Read files",
            "Check quality",
            "Reshape, clean",
            "Checkpoints",
            "Your analysis"
        ]

        desc_texts = VGroup()
        for i, (box, desc) in enumerate(zip(boxes, descriptions)):
            text = Text(desc, font_size=12, color=GREY)
            text.next_to(box, DOWN, buff=0.2)
            desc_texts.add(text)
            self.play(Write(text), run_time=0.3)

        self.wait(2)


class ConfigurationTop(Scene):
    """Scene 3: Emphasizes putting configuration at the top"""

    def construct(self):
        # Title
        title = Text("Principle: Configuration at the Top", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Code example
        code_good = VGroup(
            Text("# ===== CONFIGURATION =====", font_size=18, color=GREEN, font="Courier"),
            Text("RAW_PRICING = 'data/raw/pricing.xlsx'", font_size=16, font="Courier"),
            Text("RAW_SALES = 'data/raw/sales.xlsx'", font_size=16, font="Courier"),
            Text("OUTPUT_DIR = 'data/processed/'", font_size=16, font="Courier"),
            Text("HEADER_ROW = 2", font_size=16, font="Courier"),
            Text("", font_size=16),
            Text("# ===== LOAD DATA =====", font_size=18, color=BLUE, font="Courier"),
            Text("df = pd.read_excel(RAW_PRICING, header=HEADER_ROW)", font_size=16, font="Courier"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        code_good.shift(UP * 0.5)

        code_box = SurroundingRectangle(code_good, color=GREY, buff=0.2)

        self.play(Create(code_box))
        for line in code_good:
            self.play(Write(line), run_time=0.3)

        self.wait(1)

        # Benefits
        benefits = VGroup(
            Text("✓ Change paths in ONE place", font_size=20, color=GREEN),
            Text("✓ Easy to update for new data", font_size=20, color=GREEN),
            Text("✓ No 'magic numbers' buried in code", font_size=20, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(DOWN).shift(UP * 0.5)

        for benefit in benefits:
            self.play(Write(benefit), run_time=0.4)

        self.wait(2)


class IntermediateSaves(Scene):
    """Scene 4: Shows the concept of saving intermediate outputs"""

    def construct(self):
        # Title
        title = Text("Principle: Save Intermediate Outputs", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Pipeline with checkpoints
        stages = ["Load", "Reshape", "Normalize", "Merge", "Analyze"]

        pipeline = VGroup()
        checkpoints = VGroup()

        for i, stage in enumerate(stages):
            box = RoundedRectangle(width=1.8, height=0.7, corner_radius=0.1, color=BLUE, fill_opacity=0.3)
            label = Text(stage, font_size=14)
            stage_group = VGroup(box, label)
            pipeline.add(stage_group)

        pipeline.arrange(RIGHT, buff=0.8)
        pipeline.shift(UP * 1)

        # Arrows
        arrows = VGroup()
        for i in range(len(pipeline) - 1):
            arrow = Arrow(
                pipeline[i].get_right(),
                pipeline[i + 1].get_left(),
                buff=0.1,
                stroke_width=2
            )
            arrows.add(arrow)

        self.play(Create(pipeline), Create(arrows))
        self.wait(0.5)

        # Add checkpoint saves (after reshape, normalize, merge)
        save_points = [1, 2, 3]  # After Reshape, Normalize, Merge

        for idx in save_points:
            checkpoint = VGroup(
                Circle(radius=0.2, color=GREEN, fill_opacity=0.5),
                Text("💾", font_size=16)
            )
            checkpoint.next_to(pipeline[idx], DOWN, buff=0.3)

            save_label = Text(f"Save .csv", font_size=10, color=GREEN)
            save_label.next_to(checkpoint, DOWN, buff=0.1)

            self.play(Create(checkpoint), Write(save_label), run_time=0.5)

        self.wait(1)

        # Show benefit
        benefit_box = VGroup(
            Rectangle(width=10, height=1.5, color=YELLOW, fill_opacity=0.2),
            Text("If Step 5 fails, don't re-run Steps 1-4!", font_size=22),
            Text("Load from checkpoint and continue", font_size=18, color=GREY)
        ).arrange(DOWN, buff=0.1).to_edge(DOWN)

        self.play(Create(benefit_box))
        self.wait(2)


class AWGPipeline(Scene):
    """Scene 5: The specific AWG data pipeline"""

    def construct(self):
        # Title
        title = Text("AWG Data Pipeline", font_size=40).to_edge(UP)
        self.play(Write(title))

        # Pipeline diagram (vertical for clarity)
        steps = [
            ("RAW FILES", "Pricing Excel + Sales Excel", GREY),
            ("LOAD", "header=2 for pricing, header=1 for sales", BLUE),
            ("RESHAPE", "Wide → Long (melt pricing columns)", ORANGE),
            ("NORMALIZE", "BSP/Pack, List Cost/Pack", YELLOW),
            ("MERGE", "Pricing + Sales by Item, Division, Quarter", PURPLE),
            ("VALIDATE", "Check duplicates, missing, impossible values", RED),
            ("SAVE", "pricing_long.csv, sales_long.csv, merged.csv", GREEN),
        ]

        pipeline = VGroup()

        for i, (step_name, description, color) in enumerate(steps):
            step_box = VGroup(
                RoundedRectangle(width=9, height=0.7, corner_radius=0.1, color=color, fill_opacity=0.3),
                Text(step_name, font_size=16, color=color).shift(LEFT * 3),
                Text(description, font_size=12).shift(RIGHT * 1),
            )
            pipeline.add(step_box)

        pipeline.arrange(DOWN, buff=0.15)
        pipeline.scale(0.85).shift(DOWN * 0.3)

        # Arrows between steps
        arrows = VGroup()
        for i in range(len(pipeline) - 1):
            arrow = Arrow(
                pipeline[i].get_bottom(),
                pipeline[i + 1].get_top(),
                buff=0.05,
                stroke_width=2,
                color=WHITE
            )
            arrows.add(arrow)

        # Animate step by step
        for i, step in enumerate(pipeline):
            self.play(Create(step), run_time=0.5)
            if i < len(arrows):
                self.play(Create(arrows[i]), run_time=0.2)

        self.wait(1)

        # Final output
        output = Text("→ Ready for Analysis!", font_size=24, color=GREEN)
        output.next_to(pipeline, DOWN, buff=0.3)
        self.play(Write(output))
        self.wait(2)


# Run instructions
if __name__ == "__main__":
    print("Run with: manim -pql video3_data_pipeline.py")
    print("\nAvailable scenes:")
    print("  - NightmareVsDream")
    print("  - PipelineFlowchart")
    print("  - ConfigurationTop")
    print("  - IntermediateSaves")
    print("  - AWGPipeline")
