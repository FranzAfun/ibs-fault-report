# IBS Fault Report Design System

## Core Styles (Current)

### Typography
- **Body Font**: "IBM Plex Sans", "Trebuchet MS", sans-serif
- **Mono Font**: "IBM Plex Mono", monospace
- **Weights**: 400 (Regular), 500 (Medium), 600 (Semi-Bold), 700 (Bold)

### Colors
| Token | Hex Code | Purpose |
|-------|----------|---------|
| `--color-primary-900` | `#128a60` | Deep green (Brand primary) |
| `--color-primary-700` | `#1fbf84` | Main action color |
| `--color-primary-500` | `#47dca5` | Highlight / Glow |
| `--color-secondary-900` | `#0f1f34` | Dark navy (Header text) |
| `--color-secondary-700` | `#233a59` | Secondary buttons |
| `--color-secondary-500` | `#4b5f79` | Muted secondary |
| `--color-accent-700` | `#1fbf84` | Accents |
| `--color-accent-500` | `#47dca5` | Accents (Light) |
| `--color-neutral-0` | `#f3f5f8` | Background base |
| `--color-neutral-100` | `#d9e0e9` | Borders / Dividers |
| `--color-neutral-700` | `#303c4d` | Body text |
| `--color-neutral-900` | `#151c25` | Headlines |
| `--color-info` | `#274b76` | Information |
| `--color-danger` | `#a93737` | Error / Alert |

### Spacing & Layout
- **Radii**: `8px` (sm), `14px` (md), `20px` (lg)
- **Shadows**: `0 14px 34px rgba(20, 28, 38, 0.12)` (Panel)
- **Max Width**: `1680px`

### Components
- **Panels**: White semi-transparent background (`rgba(255, 255, 255, 0.9)`), large radius, rising animation.
- **Tables**: Full width, horizontal scrollable, linear gradient headers (Greens), alternating row colors, hover state (Light green).
- **Status Pills**: Rounded pills with light background and dark text corresponding to state (Open, In Progress, Resolved, Closed).
- **Buttons**: Linear gradient backgrounds for primary actions, solid for secondary.

---

## AI Improvement Prompt (for Stitch)

Copy and use the prompt below to refine the design system.

```text
As a UI/UX expert, analyze the existing design system for the "IBS Fault Report" application. The current aesthetic is "Professional Operational Tool" with a green/navy palette and IBM Plex typography.

Task: Provide a modernized and more cohesive version of this design system with the following improvements:

1. Color Palette:
   - Refine the green/navy combination to be more professional and less "standard bootstrap-like".
   - Introduce a better semantic color scale (Primary, Success, Warning, Danger, Info) that works well on both light and dark backgrounds.
   - Suggest a more sophisticated neutral scale that avoids "muddy" grays.

2. Table Design:
   - Provide CSS/Styling rules for a high-density data table that remains readable.
   - Focus on better typography hierarchy, row padding, and subtle borders.
   - Suggest a better "Hover" and "Selected" state that isn't just a flat color.

3. Semantics & Structure:
   - Improve the layout semantics.
   - Suggest better use of white space and "visual breathing room" in the panel-based layout.

4. Component Polish:
   - Provide updated styles for Buttons (including transitions, states, and shadows).
   - Redesign the "Status Pills" to be more distinctive and modern (e.g., using subtle glows or borders instead of flat fills).
   - Suggest a better font pairing if IBM Plex isn't the best fit for a high-density dashboard.

Output: 
- A full set of CSS variables (`:root`).
- Updated component CSS for .panel, .data-table, .status-pill, and .btn.
- A brief explanation of the "Design Language" chosen (e.g., Glassmorphism, Brutalism, Minimalist SaaS, etc.).
```
