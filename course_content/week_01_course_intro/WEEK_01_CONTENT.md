# Week 1: Course Introduction & Platform Onboarding

## Overview
**Theme:** Getting Started
**Duration:** First week of semester
**Deliverables:** None (orientation week)

---

## Learning Objectives

By the end of this week, students will be able to:
1. Navigate the course platform and understand submission workflows
2. Set up their Python/Colab environment for data analysis
3. Understand the structure and expectations of the practicum course
4. Form effective project teams with clear roles

---

## Content to Create

### Video 1: Course Overview (5-7 min)
**Purpose:** Set expectations and excite students about the practicum experience

**Script Outline:**
1. Welcome & instructor introduction (30 sec)
2. What is BADM 550? The practicum experience (1 min)
   - Real client, real problems, real impact
   - Different from case studies - you're creating new insights
3. Course structure overview (1.5 min)
   - 15-week timeline
   - Weekly milestones
   - Two client presentations (mid-term, final)
4. Grading breakdown (1 min)
   - Team deliverables
   - Individual contributions
   - Peer evaluations
5. What makes a successful team (1 min)
   - Communication
   - Accountability
   - Diverse perspectives
6. Preview of the AWG project (1 min)
   - Teaser of the business problem
   - Why this matters

**Animation Ideas:**
- Timeline animation showing 15 weeks with key milestones highlighted
- Flowchart of deliverable → feedback → iteration cycle

**Assets Needed:**
- [ ] Course timeline graphic
- [ ] Grading breakdown pie chart
- [ ] AWG logo/branding (with permission)

---

### Video 2: Platform Tour (5 min)
**Purpose:** Show students how to navigate the course site

**Script Outline:**
1. Logging in and dashboard overview (1 min)
2. Finding your project and team (1 min)
3. Viewing weekly milestones (1 min)
4. Accessing resources (videos, notebooks, documents) (1 min)
5. Submitting deliverables (1 min)

**Animation Ideas:**
- Screen recording with animated callouts
- Highlight boxes around key UI elements

**Assets Needed:**
- [ ] Screen recordings of course platform
- [ ] Animated cursor/highlight overlays

---

### Video 3: Tool Setup Guide (10 min)
**Purpose:** Ensure all students have working environments

**Script Outline:**
1. Why Colab? (1 min)
   - No local setup needed
   - GPU access for future projects
   - Easy sharing and collaboration
2. Google Account & Drive setup (2 min)
   - Using university account
   - Creating project folder structure
3. Opening a Colab notebook (2 min)
   - From Drive
   - From GitHub link
   - From course platform
4. Colab interface tour (3 min)
   - Code cells vs text cells
   - Running cells (Shift+Enter)
   - Saving to Drive
5. Installing packages (1 min)
   - !pip install
   - Common packages we'll use
6. Connecting to data (1 min)
   - Mounting Google Drive
   - Uploading files

**Animation Ideas:**
- Side-by-side: local Python setup (complicated) vs Colab (simple)
- Animated Colab interface walkthrough
- File structure diagram for organizing project

**Assets Needed:**
- [ ] Colab screen recordings
- [ ] Recommended folder structure diagram
- [ ] Starter notebook for testing setup

---

## Notebooks to Create

### `week01_environment_test.ipynb`
A simple notebook students run to verify their setup works.

**Contents:**
```python
# Cell 1: Check Python version
import sys
print(f"Python version: {sys.version}")

# Cell 2: Import common packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
print("Core packages imported successfully!")

# Cell 3: Test data loading
# Create sample DataFrame
df = pd.DataFrame({
    'Product': ['Cereal A', 'Cereal B', 'Milk'],
    'Price': [4.99, 3.49, 2.99],
    'Category': ['Breakfast', 'Breakfast', 'Dairy']
})
print("Sample data created:")
display(df)

# Cell 4: Test visualization
df.plot(kind='bar', x='Product', y='Price')
plt.title('Sample Price Chart')
plt.show()
print("Visualization working!")

# Cell 5: Test Google Drive connection (optional)
# from google.colab import drive
# drive.mount('/content/drive')
# print("Google Drive connected!")

print("\n✅ All checks passed! You're ready for Week 2.")
```

---

## Documents to Create

### Team Charter Template
**File:** `team_charter_template.md`

Provide a template for students to complete in Week 2, including:
- Team name
- Member roles (lead, note-taker, etc.)
- Communication plan (Slack? Discord? Email?)
- Meeting schedule
- Working agreements
- Conflict resolution approach

---

## Animation Production Notes

### For Canvas/Motion Graphics:
- Use consistent color scheme (suggest AWG colors if available)
- 1920x1080 resolution
- Fade transitions between sections
- Lower thirds for key terms

### For Manim:
- Not needed for Week 1 (no complex data concepts yet)
- Save Manim for Weeks 3-4 when we visualize data transformations

---

## Production Checklist

- [ ] Video 1: Course Overview
  - [ ] Script written
  - [ ] Slides/animations created
  - [ ] Voice recorded
  - [ ] Final edit

- [ ] Video 2: Platform Tour
  - [ ] Screen recordings captured
  - [ ] Script written
  - [ ] Callouts/highlights added
  - [ ] Final edit

- [ ] Video 3: Tool Setup
  - [ ] Colab recordings
  - [ ] Script written
  - [ ] Animations created
  - [ ] Final edit

- [ ] Notebooks
  - [ ] Environment test notebook created
  - [ ] Tested in fresh Colab session

- [ ] Documents
  - [ ] Team charter template created

---

## Notes

Week 1 is foundational but relatively light on technical content. The goal is to:
1. Build excitement for the project
2. Reduce friction (everyone has working tools)
3. Set team dynamics early

Most of the heavy technical content starts in Week 3.
