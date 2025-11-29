# Design System & Styling Guide

## Overview

This document defines the visual design system, styling guidelines, and component specifications for **Sphincs ERP** and **Sphincs POS** applications.

---

## Design Philosophy

### Core Principles

1. **Professional & Trustworthy**: Clean, modern design that inspires confidence
2. **Fast & Efficient**: Visual design that supports speed and productivity
3. **Accessible**: High contrast, readable fonts, clear hierarchy
4. **Consistent**: Same design language across both applications
5. **Functional**: Design serves function, not the other way around

---

## Color Palette

### Primary Colors

#### Sphincs Brand Colors

**Primary Blue** (Trust, Professionalism)

- **Hex**: `#2563EB`
- **RGB**: `rgb(37, 99, 235)`
- **Usage**: Primary buttons, links, active states, brand elements
- **Variants**:
  - Light: `#3B82F6` (hover states)
  - Dark: `#1D4ED8` (pressed states)
  - Lighter: `#DBEAFE` (backgrounds, highlights)

**Primary Green** (Success, Money, Growth)

- **Hex**: `#10B981`
- **RGB**: `rgb(16, 185, 129)`
- **Usage**: Success messages, positive actions, financial indicators
- **Variants**:
  - Light: `#34D399` (hover states)
  - Dark: `#059669` (pressed states)
  - Lighter: `#D1FAE5` (backgrounds)

**Accent Orange** (Energy, Attention)

- **Hex**: `#F59E0B`
- **RGB**: `rgb(245, 158, 11)`
- **Usage**: Warnings, important notifications, call-to-action
- **Variants**:
  - Light: `#FBBF24` (hover states)
  - Dark: `#D97706` (pressed states)
  - Lighter: `#FEF3C7` (backgrounds)

### Semantic Colors

#### Status Colors

**Success** (Green)

- Primary: `#10B981`
- Background: `#D1FAE5`
- Text: `#065F46`
- **Usage**: Success messages, completed states, positive indicators

**Warning** (Orange/Amber)

- Primary: `#F59E0B`
- Background: `#FEF3C7`
- Text: `#92400E`
- **Usage**: Warnings, cautions, pending actions

**Error** (Red)

- Primary: `#EF4444`
- Background: `#FEE2E2`
- Text: `#991B1B`
- **Usage**: Errors, failures, destructive actions
- **Variants**:
  - Light: `#F87171`
  - Dark: `#DC2626`
  - Lighter: `#FEE2E2`

**Info** (Blue)

- Primary: `#3B82F6`
- Background: `#DBEAFE`
- Text: `#1E40AF`
- **Usage**: Informational messages, tips, help

### Neutral Colors

#### Grayscale Palette

**Black** (Text, Headings)

- **Hex**: `#111827`
- **RGB**: `rgb(17, 24, 39)`
- **Usage**: Primary text, headings, important elements

**Dark Gray** (Secondary Text)

- **Hex**: `#374151`
- **RGB**: `rgb(55, 65, 81)`
- **Usage**: Secondary text, labels, descriptions

**Medium Gray** (Borders, Dividers)

- **Hex**: `#6B7280`
- **RGB**: `rgb(107, 114, 128)`
- **Usage**: Borders, dividers, disabled states

**Light Gray** (Backgrounds)

- **Hex**: `#E5E7EB`
- **RGB**: `rgb(229, 231, 235)`
- **Usage**: Backgrounds, input borders, subtle dividers

**Lighter Gray** (Subtle Backgrounds)

- **Hex**: `#F3F4F6`
- **RGB**: `rgb(243, 244, 246)`
- **Usage**: Card backgrounds, alternate row colors

**White** (Primary Background)

- **Hex**: `#FFFFFF`
- **RGB**: `rgb(255, 255, 255)`
- **Usage**: Main backgrounds, cards, modals

### Application-Specific Colors

#### POS Colors (Fast-Paced, High Energy)

**POS Primary**: `#2563EB` (Blue - Trust)
**POS Accent**: `#10B981` (Green - Money/Success)
**POS Action**: `#F59E0B` (Orange - Urgency)

#### ERP Colors (Professional, Analytical)

**ERP Primary**: `#2563EB` (Blue - Professional)
**ERP Accent**: `#6366F1` (Indigo - Analytics)
**ERP Action**: `#10B981` (Green - Growth)

### Color Usage Guidelines

#### Do's ✅

- Use primary blue for main actions and navigation
- Use green for success and positive financial indicators
- Use red sparingly (only for errors and destructive actions)
- Maintain sufficient contrast (WCAG AA minimum)
- Use semantic colors consistently

#### Don'ts ❌

- Don't use red for warnings (use orange/amber)
- Don't use too many colors (stick to palette)
- Don't use low contrast combinations
- Don't use colors alone to convey information (add icons/text)

---

## Typography

### Font Family

**Primary Font**: Segoe UI (Windows native)

- **Fallback**: Arial, Helvetica, sans-serif
- **Reason**: Native Windows font, excellent readability, professional appearance

**Monospace Font**: Consolas (for code, numbers, receipts)

- **Fallback**: Courier New, monospace
- **Usage**: Receipt printing, transaction IDs, code display

### Font Sizes

#### Heading Hierarchy

**H1 - Page Title**

- Size: `32px` (2rem)
- Weight: `700` (Bold)
- Line Height: `1.2`
- Usage: Main page titles, dashboard headers

**H2 - Section Title**

- Size: `24px` (1.5rem)
- Weight: `600` (Semi-bold)
- Line Height: `1.3`
- Usage: Section headers, card titles

**H3 - Subsection Title**

- Size: `20px` (1.25rem)
- Weight: `600` (Semi-bold)
- Line Height: `1.4`
- Usage: Subsection headers, form section titles

**H4 - Card Title**

- Size: `18px` (1.125rem)
- Weight: `600` (Semi-bold)
- Line Height: `1.4`
- Usage: Card headers, table column headers

**H5 - Small Heading**

- Size: `16px` (1rem)
- Weight: `600` (Semi-bold)
- Line Height: `1.5`
- Usage: Small section titles, labels

**H6 - Tiny Heading**

- Size: `14px` (0.875rem)
- Weight: `600` (Semi-bold)
- Line Height: `1.5`
- Usage: Captions, small labels

#### Body Text

**Body Large**

- Size: `16px` (1rem)
- Weight: `400` (Regular)
- Line Height: `1.6`
- Usage: Main body text, descriptions

**Body Regular**

- Size: `14px` (0.875rem)
- Weight: `400` (Regular)
- Line Height: `1.5`
- Usage: Standard text, form labels

**Body Small**

- Size: `12px` (0.75rem)
- Weight: `400` (Regular)
- Line Height: `1.5`
- Usage: Helper text, captions, timestamps

#### Special Text

**Button Text**

- Size: `14px` (0.875rem)
- Weight: `600` (Semi-bold)
- Line Height: `1.4`
- Usage: All button labels

**Input Text**

- Size: `14px` (0.875rem)
- Weight: `400` (Regular)
- Line Height: `1.5`
- Usage: Form inputs, text fields

**Monospace Numbers**

- Size: `14px` (0.875rem)
- Font: Consolas
- Weight: `400` (Regular)
- Usage: Prices, transaction IDs, codes

### Font Weights

- **100**: Thin (not used)
- **300**: Light (not used)
- **400**: Regular (body text, labels)
- **500**: Medium (emphasis)
- **600**: Semi-bold (headings, buttons)
- **700**: Bold (strong emphasis, important headings)

### Typography Guidelines

#### Do's ✅

- Use consistent font sizes (stick to scale)
- Maintain proper line height for readability
- Use font weight to create hierarchy
- Use monospace for numbers and codes
- Ensure minimum 12px font size

#### Don'ts ❌

- Don't use too many font sizes
- Don't use font weight > 700
- Don't use font size < 12px
- Don't mix too many font families

---

## Spacing & Layout

### Spacing Scale

**Base Unit**: `4px`

| Name | Size | Usage |
|------|------|-------|
| XS | `4px` | Tight spacing, icon padding |
| SM | `8px` | Small gaps, compact layouts |
| MD | `16px` | Standard spacing, form fields |
| LG | `24px` | Section spacing, card padding |
| XL | `32px` | Large gaps, page sections |
| 2XL | `48px` | Major sections, page margins |
| 3XL | `64px` | Page-level spacing |

### Layout Grid

**POS Layout**:

- Container padding: `16px` (MD)
- Grid gap: `16px` (MD)
- Card padding: `16px` (MD)
- Button spacing: `8px` (SM)

**ERP Layout**:

- Container padding: `24px` (LG)
- Grid gap: `24px` (LG)
- Card padding: `24px` (LG)
- Section spacing: `32px` (XL)

### Component Spacing

**Buttons**:

- Padding: `12px 24px` (vertical, horizontal)
- Gap between buttons: `8px` (SM)
- Icon + text gap: `8px` (SM)

**Form Fields**:

- Label margin bottom: `8px` (SM)
- Input padding: `12px 16px`
- Input margin bottom: `16px` (MD)
- Error message margin top: `4px` (XS)

**Cards**:

- Padding: `24px` (LG)
- Margin bottom: `16px` (MD)
- Border radius: `8px`

**Tables**:

- Cell padding: `12px 16px`
- Row spacing: `1px` (border)
- Header padding: `16px`

---

## Icons

### Icon System

**Icon Library**: Material Icons / Font Awesome / Custom SVG

- **Size**: 16px, 20px, 24px, 32px
- **Style**: Outlined (primary), Filled (active states)
- **Color**: Inherit from parent or use semantic colors

### Icon Sizes

- **XS**: `16px` - Inline with small text
- **SM**: `20px` - Buttons, form fields
- **MD**: `24px` - Standard buttons, navigation
- **LG**: `32px` - Large buttons, feature icons
- **XL**: `48px` - Hero sections, empty states

### Common Icons

**Navigation**:

- Home: `home`
- Dashboard: `dashboard`
- Settings: `settings`
- Menu: `menu`
- Close: `close`

**Actions**:

- Add: `add`
- Edit: `edit`
- Delete: `delete`
- Save: `save`
- Cancel: `cancel`
- Search: `search`
- Filter: `filter`

**Status**:

- Success: `check_circle`
- Error: `error`
- Warning: `warning`
- Info: `info`

**POS Specific**:

- Cash: `attach_money`
- Card: `credit_card`
- Receipt: `receipt`
- Shopping Cart: `shopping_cart`
- Barcode: `qr_code_scanner`

**ERP Specific**:

- Inventory: `inventory`
- Staff: `people`
- Reports: `assessment`
- Calendar: `calendar`
- Sync: `sync`

### Icon Guidelines

- **Consistent Style**: Use same icon set throughout
- **Appropriate Size**: Match icon size to context
- **Color**: Use semantic colors or inherit
- **Accessibility**: Always pair with text labels
- **Touch Targets**: Minimum 44x44px for touch

---

## Buttons

### Button Types

#### Primary Button

- **Background**: Primary Blue (`#2563EB`)
- **Text**: White (`#FFFFFF`)
- **Padding**: `12px 24px`
- **Border Radius**: `6px`
- **Font**: 14px, Semi-bold
- **Usage**: Main actions, primary CTAs

**States**:

- Default: `#2563EB`
- Hover: `#3B82F6` (lighter)
- Active/Pressed: `#1D4ED8` (darker)
- Disabled: `#E5E7EB` (gray), text `#9CA3AF`

#### Secondary Button

- **Background**: Transparent
- **Border**: `1px solid #E5E7EB`
- **Text**: Dark Gray (`#374151`)
- **Padding**: `12px 24px`
- **Border Radius**: `6px`
- **Usage**: Secondary actions, cancel

**States**:

- Default: Transparent with border
- Hover: Light gray background (`#F3F4F6`)
- Active: Medium gray background (`#E5E7EB`)
- Disabled: Light gray border, light gray text

#### Success Button

- **Background**: Green (`#10B981`)
- **Text**: White
- **Usage**: Confirm, save, positive actions

#### Danger Button

- **Background**: Red (`#EF4444`)
- **Text**: White
- **Usage**: Delete, cancel, destructive actions

#### Ghost Button

- **Background**: Transparent
- **Text**: Primary Blue
- **Usage**: Tertiary actions, links styled as buttons

### Button Sizes

**Small**:

- Padding: `8px 16px`
- Font: `12px`
- Icon: `16px`

**Medium** (Default):

- Padding: `12px 24px`
- Font: `14px`
- Icon: `20px`

**Large**:

- Padding: `16px 32px`
- Font: `16px`
- Icon: `24px`

**Extra Large** (POS Touch):

- Padding: `20px 40px`
- Font: `18px`
- Icon: `28px`
- Minimum: `80x80px` for touch

### Button Guidelines

- **One Primary Action**: Only one primary button per screen
- **Clear Labels**: Use action verbs (Save, Delete, Cancel)
- **Icons**: Optional, but helpful for common actions
- **Loading States**: Show spinner when processing
- **Disabled States**: Clearly indicate when disabled

---

## Forms & Inputs

### Input Fields

**Text Input**:

- Height: `40px`
- Padding: `12px 16px`
- Border: `1px solid #E5E7EB`
- Border Radius: `6px`
- Font: `14px`, Regular
- Background: White

**States**:

- Default: Gray border
- Focus: Blue border (`#2563EB`), blue shadow
- Error: Red border (`#EF4444`), red shadow
- Disabled: Light gray background, gray border

**Textarea**:

- Min Height: `80px`
- Padding: `12px 16px`
- Same border and states as text input

**Select/Dropdown**:

- Height: `40px`
- Padding: `12px 16px`
- Same styling as text input
- Dropdown arrow icon on right

**Checkbox**:

- Size: `20x20px`
- Border: `2px solid #E5E7EB`
- Checked: Blue background (`#2563EB`), white checkmark
- Border Radius: `4px`

**Radio Button**:

- Size: `20x20px`
- Border: `2px solid #E5E7EB`
- Checked: Blue fill (`#2563EB`)
- Shape: Circle

### Form Layout

**Label**:

- Font: `14px`, Semi-bold
- Color: Dark Gray (`#374151`)
- Margin bottom: `8px`

**Helper Text**:

- Font: `12px`, Regular
- Color: Medium Gray (`#6B7280`)
- Margin top: `4px`

**Error Message**:

- Font: `12px`, Regular
- Color: Red (`#EF4444`)
- Margin top: `4px`
- Icon: Error icon before text

---

## Cards & Containers

### Card Component

**Default Card**:

- Background: White
- Border: `1px solid #E5E7EB`
- Border Radius: `8px`
- Padding: `24px`
- Shadow: Subtle shadow on hover

**Elevated Card**:

- Same as default
- Shadow: `0 4px 6px rgba(0, 0, 0, 0.1)`
- Usage: Important content, modals

**Outlined Card**:

- Background: Transparent
- Border: `2px solid #E5E7EB`
- Usage: Secondary content

### Container Sizes

**Small**: Max width `640px`
**Medium**: Max width `768px`
**Large**: Max width `1024px`
**Extra Large**: Max width `1280px`
**Full Width**: 100%

---

## Tables

### Table Styling

**Header**:

- Background: Light Gray (`#F3F4F6`)
- Font: `14px`, Semi-bold
- Padding: `16px`
- Border bottom: `2px solid #E5E7EB`

**Rows**:

- Padding: `12px 16px`
- Border bottom: `1px solid #E5E7EB`
- Hover: Light gray background (`#F9FAFB`)

**Alternate Rows**:

- Background: `#F9FAFB` (very light gray)

**Selected Row**:

- Background: Light blue (`#DBEAFE`)
- Border: `2px solid #2563EB`

### Table Guidelines

- **Sortable Headers**: Show sort icon, change on hover
- **Action Buttons**: In last column, icon buttons
- **Responsive**: Horizontal scroll on small screens
- **Pagination**: Bottom of table

---

## Modals & Dialogs

### Modal Styling

**Overlay**:

- Background: `rgba(0, 0, 0, 0.5)` (semi-transparent black)
- Full screen coverage

**Modal Container**:

- Background: White
- Border Radius: `8px`
- Padding: `24px`
- Max Width: `500px` (small), `800px` (medium), `1200px` (large)
- Shadow: Large shadow for depth

**Modal Header**:

- Font: `20px`, Semi-bold
- Padding bottom: `16px`
- Border bottom: `1px solid #E5E7EB`
- Close button: Top right

**Modal Body**:

- Padding: `24px 0`
- Max height: `70vh` (scrollable if needed)

**Modal Footer**:

- Padding top: `16px`
- Border top: `1px solid #E5E7EB`
- Button alignment: Right
- Button spacing: `8px`

---

## Navigation

### Top Navigation Bar

**Height**: `64px`
**Background**: White
**Border**: `1px solid #E5E7EB` (bottom)
**Padding**: `0 24px`

**Logo**:

- Left side
- Height: `40px`

**Navigation Items**:

- Font: `14px`, Semi-bold
- Color: Dark Gray (`#374151`)
- Active: Primary Blue (`#2563EB`)
- Hover: Light gray background
- Padding: `12px 16px`

**User Menu**:

- Right side
- Avatar + name
- Dropdown on click

### Sidebar Navigation (ERP)

**Width**: `240px`
**Background**: White
**Border**: `1px solid #E5E7EB` (right)
**Padding**: `16px`

**Menu Items**:

- Font: `14px`, Regular
- Padding: `12px 16px`
- Icon: `20px` on left
- Active: Blue background (`#DBEAFE`), blue text
- Hover: Light gray background

---

## Badges & Tags

### Badge Component

**Default Badge**:

- Background: Light Gray (`#E5E7EB`)
- Text: Dark Gray (`#374151`)
- Padding: `4px 8px`
- Border Radius: `12px`
- Font: `12px`, Semi-bold

**Status Badges**:

- Success: Green background (`#D1FAE5`), green text (`#065F46`)
- Warning: Orange background (`#FEF3C7`), orange text (`#92400E`)
- Error: Red background (`#FEE2E2`), red text (`#991B1B`)
- Info: Blue background (`#DBEAFE`), blue text (`#1E40AF`)

---

## Shadows & Elevation

### Shadow Levels

**Level 0** (No shadow):

- Usage: Flat elements

**Level 1** (Subtle):

- `0 1px 2px rgba(0, 0, 0, 0.05)`
- Usage: Cards, buttons

**Level 2** (Medium):

- `0 4px 6px rgba(0, 0, 0, 0.1)`
- Usage: Elevated cards, dropdowns

**Level 3** (Large):

- `0 10px 15px rgba(0, 0, 0, 0.1)`
- Usage: Modals, popovers

**Level 4** (Extra Large):

- `0 20px 25px rgba(0, 0, 0, 0.15)`
- Usage: Important modals

---

## Animations & Transitions

### Transition Timing

**Fast**: `150ms` - Hover states, small changes
**Medium**: `250ms` - Default transitions
**Slow**: `350ms` - Complex animations, page transitions

### Easing Functions

**Ease In Out**: `cubic-bezier(0.4, 0, 0.2, 1)` - Default
**Ease Out**: `cubic-bezier(0, 0, 0.2, 1)` - Entrances
**Ease In**: `cubic-bezier(0.4, 0, 1, 1)` - Exits

### Common Animations

**Button Hover**:

- Transition: `background-color 150ms ease`
- Scale: None (avoid scale on buttons)

**Modal Entrance**:

- Fade in: `opacity 0 → 1`
- Slide up: `translateY(20px) → 0`
- Duration: `250ms`

**Loading Spinner**:

- Rotation: `360deg`
- Duration: `1s`
- Timing: `linear`
- Repeat: `infinite`

---

## Responsive Design

### Breakpoints

**Mobile**: `0px - 640px`

- Single column layout
- Stacked elements
- Touch-optimized buttons

**Tablet**: `641px - 1024px`

- Two column layout
- Adjusted spacing

**Desktop**: `1025px+`

- Multi-column layout
- Full feature set

### DPI Scaling

**Standard (96 DPI)**:

- Base scaling: `1x`

**High DPI (120-144 DPI)**:

- Scaling: `1.25x - 1.5x`
- Adjust font sizes and spacing

**Very High DPI (160-240 DPI)**:

- Scaling: `1.67x - 2.5x`
- Use vector icons (SVG)
- Adjust all measurements

---

## Splash Screen

### Splash Screen Design

**Dimensions**:

- **Width**: `600px` (or responsive to screen size, max 800px)
- **Height**: `400px` (or responsive to screen size, max 600px)
- **Position**: Centered on screen
- **Border Radius**: `8px` (optional, for modern look)

**Background**:

- **Primary Background**: White (`#FFFFFF`) or light gradient
- **Gradient Option**: Light blue to white (`#DBEAFE` → `#FFFFFF`)
- **Shadow**: Level 3 shadow (`0 10px 15px rgba(0, 0, 0, 0.1)`)

**Layout Structure**:

- **Top Section**: Logo area (centered)
- **Middle Section**: App name and version
- **Bottom Section**: Loading indicator and status text

### Splash Screen Components

**Logo**:

- **Size**: `120x120px` (or proportional)
- **Position**: Centered, top section
- **Padding**: `32px` from top

**Application Name**:

- **Font**: `24px`, Semi-bold (`600`)
- **Color**: Primary Blue (`#2563EB`)
- **Line Height**: `1.2`
- **Position**: Below logo, centered
- **Margin**: `16px` below logo

**Version Number**:

- **Font**: `14px`, Regular (`400`)
- **Color**: Medium Gray (`#6B7280`)
- **Position**: Below app name
- **Margin**: `8px` below app name
- **Format**: `v1.2.3` or `Version 1.2.3`

**Loading Indicator**:

- **Type**: Spinner or progress bar
- **Color**: Primary Blue (`#2563EB`)
- **Size**: `40x40px` (spinner) or full width (progress bar)
- **Position**: Centered, bottom section
- **Animation**: Continuous rotation (spinner) or smooth progress (bar)

**Status Text**:

- **Font**: `12px`, Regular (`400`)
- **Color**: Medium Gray (`#6B7280`)
- **Position**: Below loading indicator
- **Margin**: `16px` above bottom
- **Examples**: "Initializing...", "Loading database...", "Checking for updates..."

### Splash Screen Animations

**Fade In**:

- **Duration**: `250ms`
- **Easing**: `ease-out`
- **Effect**: Opacity `0 → 1`

**Fade Out**:

- **Duration**: `250ms`
- **Easing**: `ease-in`
- **Effect**: Opacity `1 → 0`

**Loading Spinner**:

- **Duration**: `1s` per rotation
- **Timing**: `linear`
- **Repeat**: `infinite`
- **Rotation**: `360deg`

**Status Text Updates**:

- **Transition**: `opacity 150ms ease`
- **Effect**: Fade out old text, fade in new text

### Update Notification Module (Splash Screen)

**Module Container**:

- **Position**: Overlay on splash screen (centered or top-right)
- **Size**: `400x300px` (compact but readable)
- **Background**: White (`#FFFFFF`) with Level 3 shadow
- **Border**: `1px solid #E5E7EB`
- **Border Radius**: `8px`
- **Padding**: `24px`

**Module Header**:

- **Icon**: Update/download icon (`24px`)
- **Title**: "New Update Available"
  - Font: `18px`, Semi-bold (`600`)
  - Color: Dark Gray (`#374151`)
- **Position**: Top of module

**Version Information**:

- **Current Version**:
  - Label: "Current version:"
  - Value: `v1.2.3`
  - Font: `14px`, Regular
  - Color: Medium Gray (`#6B7280`)
- **New Version**:
  - Label: "New version:"
  - Value: `v1.3.0`
  - Font: `14px`, Semi-bold
  - Color: Primary Blue (`#2563EB`)

**Update Description**:

- **Font**: `12px`, Regular
- **Color**: Dark Gray (`#374151`)
- **Max Height**: `80px` (scrollable if needed)
- **Margin**: `16px` top and bottom

**Action Buttons**:

- **"Install Later" Button**:
  - Style: Secondary button
  - Background: Transparent
  - Border: `1px solid #E5E7EB`
  - Text: Dark Gray (`#374151`)
  - Padding: `12px 24px`
- **"Install Now" Button**:
  - Style: Primary button
  - Background: Primary Blue (`#2563EB`)
  - Text: White (`#FFFFFF`)
  - Padding: `12px 24px`
- **Button Layout**: Horizontal, right-aligned
- **Button Spacing**: `8px` between buttons

**Module Animation**:

- **Entrance**: Slide down + fade in (`250ms ease-out`)
- **Exit**: Fade out (`200ms ease-in`)

### Splash Screen Color Scheme

**ERP Splash Screen**:

- **Primary Color**: Primary Blue (`#2563EB`)
- **Accent**: Indigo (`#6366F1`)
- **Background**: White or light blue gradient

**POS Splash Screen**:

- **Primary Color**: Primary Blue (`#2563EB`)
- **Accent**: Green (`#10B981`)
- **Background**: White or light green gradient

---

## Dark Mode (Future)

### Dark Mode Colors

**Background**: `#111827` (Dark gray)
**Surface**: `#1F2937` (Lighter dark gray)
**Text**: `#F9FAFB` (Light gray)
**Border**: `#374151` (Medium gray)

**Note**: Dark mode is a future enhancement, not in MVP.

---

## Component Library

### Design Tokens

All design values should be defined as tokens for consistency:

```python
# Design tokens (example structure)
DESIGN_TOKENS = {
    "colors": {
        "primary": "#2563EB",
        "success": "#10B981",
        "error": "#EF4444",
        # ... etc
    },
    "spacing": {
        "xs": "4px",
        "sm": "8px",
        "md": "16px",
        # ... etc
    },
    "typography": {
        "font_family": "Segoe UI, Arial, sans-serif",
        "font_sizes": {
            "h1": "32px",
            "body": "14px",
            # ... etc
        }
    }
}
```

---

## Implementation Guidelines

### PyQt Styling

**Stylesheet Example**:

```python
STYLESHEET = """
QPushButton {
    background-color: #2563EB;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #3B82F6;
}

QPushButton:pressed {
    background-color: #1D4ED8;
}

QPushButton:disabled {
    background-color: #E5E7EB;
    color: #9CA3AF;
}
"""
```

### tkinter Styling

**Style Configuration**:

```python
import tkinter.ttk as ttk

style = ttk.Style()
style.configure('Primary.TButton',
    background='#2563EB',
    foreground='white',
    padding=(24, 12),
    font=('Segoe UI', 10, 'bold')
)
```

---

## Brand Identity

### Logo Guidelines

**Logo Placement**:

- Top left of navigation
- Height: `40px` (standard), `60px` (large)
- Maintain aspect ratio

**Logo Usage**:

- Use on white or light backgrounds
- Minimum clear space: `16px` around logo
- Don't stretch or distort

### Application Icons

**Sphincs POS Icon**:

- Primary color: Blue (`#2563EB`)
- Accent: Green (`#10B981`)
- Style: Modern, clean, recognizable at small sizes

**Sphincs ERP Icon**:

- Primary color: Blue (`#2563EB`)
- Accent: Indigo (`#6366F1`)
- Style: Professional, analytical

---

## Accessibility Standards

### Color Contrast

**WCAG AA Compliance**:

- Normal text: 4.5:1 contrast ratio
- Large text: 3:1 contrast ratio
- UI components: 3:1 contrast ratio

**Tested Combinations**:

- White text on Blue: ✅ Pass
- Dark text on White: ✅ Pass
- White text on Green: ✅ Pass
- White text on Red: ✅ Pass

### Focus Indicators

**Focus Ring**:

- Color: Primary Blue (`#2563EB`)
- Width: `2px`
- Offset: `2px`
- Style: Solid outline

**Visible on All Interactive Elements**:

- Buttons
- Links
- Form inputs
- Navigation items

---

## Print Styles (Receipts)

### Receipt Typography

**Font**: Consolas (monospace)
**Size**: `12px`
**Line Height**: `1.2`
**Width**: `80mm` (thermal printer standard)

**Receipt Layout**:

- Header: Company name, address
- Body: Items, prices, totals
- Footer: Thank you message, date/time

---

## Design Checklist

### Before Implementation

- [ ] All colors defined in palette
- [ ] Typography scale established
- [ ] Spacing system defined
- [ ] Component styles specified
- [ ] Icons selected and sized
- [ ] Responsive breakpoints set
- [ ] Accessibility standards met
- [ ] Design tokens created
- [ ] Style guide documented

### During Development

- [ ] Use design tokens (not hardcoded values)
- [ ] Follow spacing scale
- [ ] Maintain color consistency
- [ ] Test on multiple DPIs
- [ ] Verify accessibility
- [ ] Check contrast ratios
- [ ] Test with screen readers

---

## Resources

### Design Tools

- **Figma**: For mockups and prototypes
- **Adobe XD**: Alternative design tool
- **Inkscape**: For SVG icons
- **Color Contrast Checker**: WebAIM Contrast Checker

### Icon Resources

- Material Icons
- Font Awesome
- Custom SVG icons

### Font Resources

- Windows Font Library
- Google Fonts (if needed for web components)

---

## Next Steps

1. Create detailed component mockups
2. Build design token system
3. Create style guide documentation
4. Develop component library
5. Create UI asset library (icons, images)
6. Test design on actual devices
7. Gather user feedback on design
8. Iterate based on feedback
