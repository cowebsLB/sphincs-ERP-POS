# User Workflows & UI/UX Design

## Overview

This document defines user workflows, screen flows, and UI/UX design principles for **Sphincs ERP** and **Sphincs POS** applications.

---

## Design Principles

### Core Principles

1. **Speed First**: POS operations must be fast—minimize clicks, maximize keyboard shortcuts
2. **Clarity**: Clear visual hierarchy, obvious actions, minimal cognitive load
3. **Error Prevention**: Validate inputs, confirm critical actions, prevent mistakes
4. **Offline Resilience**: System works offline, syncs when online
5. **Consistency**: Same patterns across both applications
6. **Accessibility**: Support keyboard navigation, clear labels, readable fonts
7. **Responsive Feedback**: Immediate visual feedback for all actions

### Visual Design Guidelines

- **Color Scheme**:
  - Primary: Professional blue/green for trust
  - Success: Green for confirmations
  - Warning: Orange/yellow for cautions
  - Error: Red for errors (use sparingly)
  - Neutral: Gray for secondary elements
- **Typography**: Clear, readable fonts (Segoe UI, Arial, or similar)
- **Spacing**: Generous padding, clear separation between elements
- **Icons**: Consistent icon set, clear meaning
- **Buttons**: Large, touch-friendly (minimum 44x44px for touch)
- **Forms**: Clear labels, inline validation, helpful error messages

---

## User Roles & Access

### Role Hierarchy

1. **Admin** - Full system access
2. **Manager** - Reports, inventory, staff management
3. **Cashier** - POS operations, basic reports
4. **Chef** - Kitchen orders, waste logging
5. **Waiter/Server** - Table management, order taking
6. **Staff** - View-only access, clock in/out
7. **Cleaner** - Task logging, cleaning records

---

## Sphincs POS - User Workflows

### 1. Application Launch & Splash Screen

#### Screen: Splash Screen

**Layout**:

```
┌─────────────────────────────────────┐
│                                     │
│         [Sphincs POS Logo]          │
│                                     │
│         Sphincs POS                 │
│         Version 1.2.3               │
│                                     │
│            [Loading...]             │
│         Initializing...             │
│                                     │
└─────────────────────────────────────┘
```

**Workflow**:

1. User launches Sphincs POS or Sphincs ERP
2. Splash screen appears immediately
3. Application performs initialization tasks:
   - Load configuration
   - Connect to database
   - Initialize services
   - **Check for updates** (GitHub releases API)
4. Status text updates during initialization:
   - "Initializing..."
   - "Loading database..."
   - "Checking for updates..."
   - "Ready!"
5. If update detected:
   - Update notification module appears on splash screen
   - User can choose "Install Later" or "Install Now"
   - App continues to launch regardless of choice
6. Splash screen fades out when ready
7. Main application window appears

**Update Notification Module** (if update detected):

```
┌─────────────────────────────────────┐
│  [Sphincs POS Logo]                 │
│                                     │
│  ┌───────────────────────────────┐ │
│  │ 🔄 New Update Available       │ │
│  │                               │ │
│  │ Current version: v1.2.3       │ │
│  │ New version: v1.3.0           │ │
│  │                               │ │
│  │ Bug fixes and improvements    │ │
│  │                               │ │
│  │ [Install Later] [Install Now] │ │
│  └───────────────────────────────┘ │
│                                     │
│         [Loading...]                │
└─────────────────────────────────────┘
```

**Update Module Workflow**:

1. **If Update Detected**:
   - Update module appears on splash screen
   - Shows current and new version
   - Displays brief update description
   - Non-blocking (app continues to launch)

2. **User Choice - "Install Later"**:
   - Update module dismisses
   - App launches normally
   - Update notification can be shown again in main app
   - User can update later via Help → Check for Updates

3. **User Choice - "Install Now"**:
   - Update process begins
   - Download progress shown
   - App closes
   - Installer runs
   - App restarts with new version

4. **If No Update**:
   - Splash screen shows normal initialization
   - No update module appears
   - App launches normally

**Keyboard Shortcuts** (on splash screen):
- `Esc` - Close splash screen (if allowed)
- `Enter` - Accept default action (if applicable)

---

### 2. Application Login

#### Screen: Login Window

**Layout**:

```
┌─────────────────────────────────────┐
│  [Sphincs POS Logo]                 │
│                                     │
│  ┌───────────────────────────────┐ │
│  │ Username: [____________]      │ │
│  └───────────────────────────────┘ │
│                                     │
│  ┌───────────────────────────────┐ │
│  │ Password: [____________]      │ │
│  └───────────────────────────────┘ │
│                                     │
│  [Remember Me] [Forgot Password?]  │
│                                     │
│  [Login Button]                     │
│                                     │
│  Status: [Online/Offline]           │
└─────────────────────────────────────┘
```

**Workflow**:

1. After splash screen, login screen appears
2. Enter username and password
3. System validates credentials
4. If valid → Load POS interface
5. If invalid → Show error, allow retry
6. Show online/offline status indicator

**Keyboard Shortcuts**:

- `Tab` - Navigate between fields
- `Enter` - Submit login
- `Esc` - Cancel/close

---

### 3. POS Main Interface (Cashier Workflow)

#### Screen: POS Main Window

**Layout**:

```
┌─────────────────────────────────────────────────────────────────┐
│ [Menu] [Reports] [Settings] [Logout]    User: John | Shift: 8h │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PRODUCTS (Grid/Buttons)          │  CURRENT ORDER              │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐     │  ┌───────────────────────┐ │
│  │Item│ │Item│ │Item│ │Item│     │  │ Item        Qty  Price│ │
│  │ 1  │ │ 2  │ │ 3  │ │ 4  │     │  ├───────────────────────┤ │
│  └────┘ └────┘ └────┘ └────┘     │  │ Burger       2   $20  │ │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐     │  │ Fries        1   $5   │ │
│  │Item│ │Item│ │Item│ │Item│     │  └───────────────────────┘ │
│  │ 5  │ │ 6  │ │ 7  │ │ 8  │     │                            │
│  └────┘ └────┘ └────┘ └────┘     │  Subtotal:        $25.00  │
│  [Categories: All ▼]              │  Tax:             $2.50   │
│  [Search: ________] [🔍]          │  ─────────────────────────│
│                                   │  TOTAL:           $27.50  │
│                                   │                            │
│                                   │  [Clear] [Discount]        │
│                                   │  [Payment] [Hold Order]    │
└─────────────────────────────────────────────────────────────────┘
│ [F1-F12: Quick Items] [Ctrl+C: Cash] [Ctrl+D: Card] [Esc: Cancel]
└─────────────────────────────────────────────────────────────────┘
```

**Workflow: Making a Sale**

1. **Add Items to Cart**:
   - Click product button OR
   - Scan barcode OR
   - Press hotkey (F1-F12) OR
   - Search and select
   - Item appears in order panel
   - Quantity defaults to 1, can be adjusted

2. **Modify Order**:
   - Click item in order panel to edit quantity
   - Remove item button
   - Apply discount (percentage or fixed)

3. **Complete Transaction**:
   - Click "Payment" button
   - Payment screen appears
   - Select payment method
   - Enter amount (if cash)
   - Confirm payment
   - Receipt prints automatically
   - Transaction saved
   - Order cleared, ready for next customer

**Keyboard Shortcuts**:

- `F1-F12` - Quick product selection
- `Ctrl+C` - Cash payment
- `Ctrl+D` - Card payment
- `Ctrl+S` - Split payment
- `Ctrl+H` - Hold order
- `Ctrl+X` - Clear order
- `Esc` - Cancel current action
- `Enter` - Confirm/Proceed
- `+/-` - Increase/decrease quantity
- `Del` - Remove selected item

---

### 4. Payment Screen

#### Screen: Payment Window

**Layout**:

```
┌─────────────────────────────────────┐
│  Payment                            │
├─────────────────────────────────────┤
│                                     │
│  Total Amount:        $27.50        │
│                                     │
│  Payment Method:                    │
│  ○ Cash                             │
│  ○ Card                             │
│  ○ Mobile Payment                   │
│  ○ Split Payment                    │
│                                     │
│  Amount Tendered: [________]        │
│                                     │
│  Change:              $0.00         │
│                                     │
│  [Cancel]  [Process Payment]        │
│                                     │
└─────────────────────────────────────┘
```

**Workflow**:

1. Select payment method
2. If cash: Enter amount tendered, change calculated automatically
3. If card: Process card payment (integrate with card reader)
4. Confirm payment
5. Receipt prints
6. Return to main POS screen

---

### 5. Waiter/Server Workflow

#### Screen: Table Management View

**Layout**:

```
┌─────────────────────────────────────────────────────────────┐
│ [Tables] [Orders] [Kitchen] [Clock Out]                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  TABLE LAYOUT                                               │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                          │
│  │  1  │ │  2  │ │  3  │ │  4  │                          │
│  │[2]  │ │[4]  │ │[0]  │ │[1]  │                          │
│  └─────┘ └─────┘ └─────┘ └─────┘                          │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                          │
│  │  5  │ │  6  │ │  7  │ │  8  │                          │
│  │[0]  │ │[2]  │ │[0]  │ │[0]  │                          │
│  └─────┘ └─────┘ └─────┘ └─────┘                          │
│                                                             │
│  Legend: [0] = Empty | [1-4] = Guests | [Red] = Needs Help │
└─────────────────────────────────────────────────────────────┘
```

**Workflow: Taking an Order**

1. **Select Table**:
   - Click on table number
   - Table detail screen opens

2. **Add Items**:
   - Select items from menu
   - Items added to table order
   - Order sent to kitchen automatically

3. **Monitor Order Status**:
   - View order status (pending, cooking, ready)
   - Get notification when order ready
   - Mark items as served

4. **Process Payment**:
   - When customer ready to pay
   - Click "Payment" on table
   - Process payment
   - Clear table

---

### 6. Kitchen Display Workflow

#### Screen: Kitchen Order Display

**Layout**:

```
┌─────────────────────────────────────────────────────────────┐
│ KITCHEN ORDERS                    [Filter: All ▼] [Refresh] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ORDER #1234 - Table 5 - 2:30 PM                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 2x Burger - [Pending] [Start Cooking]              │   │
│  │ 1x Fries - [Pending] [Start Cooking]               │   │
│  │ 1x Salad - [Pending] [Start Cooking]               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ORDER #1235 - Table 2 - 2:32 PM                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 1x Pizza - [Cooking] [Mark Ready]                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ORDER #1236 - Takeout - 2:35 PM                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 3x Sandwich - [Ready] [Mark Served]                │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Workflow**:

1. Orders appear automatically when placed
2. Chef clicks "Start Cooking" → Status changes to "Cooking"
3. When ready, click "Mark Ready" → Status changes to "Ready"
4. Waiter gets notification
5. When served, click "Mark Served" → Order removed from display

---

## Sphincs ERP - User Workflows

### 1. Application Launch & Splash Screen

**Note**: Same splash screen workflow as POS (see POS section above), but with ERP branding and logo.

**ERP-Specific**:
- Logo shows "Sphincs ERP" branding
- Update check is independent (ERP and POS check separately)
- If both apps need updates, each shows its own update notification

---

### 2. ERP Dashboard (Manager/Admin)

#### Screen: ERP Main Dashboard

**Layout**:

```
┌─────────────────────────────────────────────────────────────────┐
│ [Dashboard] [Inventory] [Staff] [Sales] [Reports] [Settings]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TODAY'S SUMMARY                                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐         │
│  │ Sales    │ │ Orders   │ │ Staff    │ │ Alerts   │         │
│  │ $1,250   │ │   45     │ │   12/15  │ │    3     │         │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘         │
│                                                                 │
│  QUICK ACTIONS                                                  │
│  [New Product] [Add Staff] [View Reports] [Sync Data]         │
│                                                                 │
│  RECENT ACTIVITY                                                │
│  • Order #1234 completed - $27.50                              │
│  • Low stock alert: Tomatoes (5kg remaining)                   │
│  • Staff clock-in: John Doe (2:00 PM)                          │
│                                                                 │
│  ALERTS & NOTIFICATIONS                                         │
│  ⚠ Low Stock: 3 items need reordering                         │
│  ⚠ Sync Pending: 12 transactions waiting                      │
│  ✓ Last sync: 1 hour ago                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Workflow**:

1. Manager logs into ERP
2. Dashboard shows key metrics
3. Quick access to common tasks
4. Alerts for urgent items
5. Navigate to specific modules as needed

---

### 3. Inventory Management

#### Screen: Inventory List

**Layout**:

```
┌─────────────────────────────────────────────────────────────────┐
│ Inventory Management          [Search: ______] [Filter: All ▼] │
│ [Add Ingredient] [Bulk Import] [Export] [Low Stock Report]     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Name          │ Unit │ Current │ Reorder │ Status │ Actions   │
│  ──────────────────────────────────────────────────────────────│
│  Tomatoes      │ kg   │   5.0   │   10.0  │ ⚠ Low │ [Edit]    │
│  Onions        │ kg   │  25.0   │   15.0  │ ✓ OK  │ [Edit]    │
│  Beef          │ kg   │   8.0   │   20.0  │ ⚠ Low │ [Edit]    │
│  Chicken       │ kg   │  30.0   │   25.0  │ ✓ OK  │ [Edit]    │
│                                                                 │
│  [< Previous] [1] [2] [3] [Next >]                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Workflow: Add/Edit Ingredient**

1. Click "Add Ingredient" or edit existing
2. Form appears:

   ```
   ┌─────────────────────────────┐
   │ Ingredient Details          │
   ├─────────────────────────────┤
   │ Name: [____________]        │
   │ Unit: [kg ▼]                │
   │ Current Stock: [____]       │
   │ Reorder Level: [____]       │
   │ Supplier: [Select ▼]        │
   │ Notes: [____________]       │
   │                            │
   │ [Cancel] [Save]            │
   └─────────────────────────────┘
   ```

3. Fill in details
4. Validate inputs
5. Save → Returns to list

---

### 4. Staff Management

#### Screen: Staff List

**Layout**:

```
┌─────────────────────────────────────────────────────────────────┐
│ Staff Management              [Add Staff] [Import] [Export]     │
│ [All] [Kitchen] [Floor] [Cleaning] [Management]                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Name          │ Department │ Position │ Status │ Actions      │
│  ──────────────────────────────────────────────────────────────│
│  John Doe      │ Floor      │ Waiter   │ Active │ [Edit]       │
│  Jane Smith    │ Kitchen    │ Chef     │ Active │ [Edit]       │
│  Bob Johnson   │ Cleaning   │ Janitor  │ Active │ [Edit]       │
│                                                                 │
│  [< Previous] [1] [2] [3] [Next >]                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Workflow: Add New Staff**

1. Click "Add Staff"
2. Multi-step form:
   - **Step 1: Personal Info**
     - First Name, Last Name
     - Date of Birth
     - Phone, Email
     - Address
   - **Step 2: Employment**
     - Department
     - Position
     - Hire Date
     - Employment Type
     - Hourly Rate
   - **Step 3: Account Setup**
     - Username
     - Password
     - Role/Permissions
3. Save → Staff added, account created

---

### 5. Staff Scheduling

#### Screen: Schedule Calendar

**Layout**:

```
┌─────────────────────────────────────────────────────────────────┐
│ Staff Schedule - Week of Jan 15, 2024                          │
│ [Previous Week] [Today] [Next Week] [Add Shift]                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Staff        │ Mon │ Tue │ Wed │ Thu │ Fri │ Sat │ Sun       │
│  ──────────────────────────────────────────────────────────────│
│  John Doe     │ 9-5 │ 9-5 │ Off │ 9-5 │ 9-5 │ 12-8│ Off       │
│  Jane Smith   │ 6-2 │ 6-2 │ 6-2 │ Off │ 6-2 │ 6-2 │ Off       │
│  Bob Johnson  │ 8-4 │ 8-4 │ 8-4 │ 8-4 │ 8-4 │ Off │ Off       │
│                                                                 │
│  Click on cell to edit shift                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Workflow: Create Schedule**

1. Select week
2. Click on staff/day cell
3. Shift editor appears:

   ```
   ┌─────────────────────────────┐
   │ Edit Shift                  │
   ├─────────────────────────────┤
   │ Staff: John Doe             │
   │ Date: Monday, Jan 15        │
   │ Start: [09:00]              │
   │ End: [17:00]                │
   │ Break: [30] minutes         │
   │                            │
   │ [Cancel] [Save]            │
   └─────────────────────────────┘
   ```

4. Set times
5. Save → Schedule updated

---

### 6. Sales Reports

#### Screen: Sales Report

**Layout**:

```
┌─────────────────────────────────────────────────────────────────┐
│ Sales Reports                                                   │
│ [Daily] [Weekly] [Monthly] [Custom Range]                      │
│ Date Range: [01/15/2024] to [01/21/2024] [Generate]            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SALES SUMMARY                                                  │
│  Total Sales:        $8,450.00                                 │
│  Total Transactions: 245                                        │
│  Average Transaction: $34.49                                    │
│                                                                 │
│  PAYMENT METHODS                                                │
│  Cash:        $3,200 (38%)                                     │
│  Card:        $4,500 (53%)                                     │
│  Mobile:      $750 (9%)                                        │
│                                                                 │
│  TOP PRODUCTS                                                   │
│  1. Burger - 120 sold - $2,400                                 │
│  2. Pizza - 85 sold - $1,700                                   │
│  3. Fries - 200 sold - $1,000                                  │
│                                                                 │
│  [Export to Excel] [Print] [Email]                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Workflow**:

1. Select report type and date range
2. Click "Generate"
3. Report displays with charts and tables
4. Export, print, or email as needed

---

### 7. Waste Logging (Kitchen Staff)

#### Screen: Waste Entry

**Layout**:

```
┌─────────────────────────────────────────────────────────────────┐
│ Log Waste                                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Ingredient: [Select Ingredient ▼]                             │
│  Quantity: [____] [kg ▼]                                       │
│  Reason: [Select Reason ▼]                                     │
│    • Spoiled                                                   │
│    • Overcooked                                                │
│    • Expired                                                   │
│    • Other: [____________]                                     │
│                                                                 │
│  Date: [01/15/2024] [2:30 PM]                                  │
│  Logged by: John Doe (Chef)                                    │
│                                                                 │
│  [Cancel] [Save]                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Workflow**:

1. Kitchen staff logs waste
2. Select ingredient from dropdown
3. Enter quantity
4. Select reason
5. Save → Stock automatically updated

---

### 8. Attendance Tracking (All Staff)

#### Screen: Clock In/Out

**Layout**:

```
┌─────────────────────────────────────────────────────────────────┐
│ Attendance                                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Current Status: [Clocked Out]                                 │
│                                                                 │
│  Today's Schedule:                                              │
│  Shift: 9:00 AM - 5:00 PM                                      │
│  Break: 30 minutes                                              │
│                                                                 │
│  [Clock In]                                                     │
│                                                                 │
│  Recent Activity:                                               │
│  • Jan 14: Clocked in 8:55 AM, Clocked out 5:10 PM            │
│  • Jan 13: Clocked in 9:00 AM, Clocked out 5:00 PM            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Workflow**:

1. Staff opens attendance screen
2. See current status and schedule
3. Click "Clock In" at start of shift
4. Click "Clock Out" at end of shift
5. System validates against schedule
6. Overtime calculated automatically

---

## Common UI Components

### Splash Screen

**Design Specifications** (see `design.md` for detailed styling):
- Centered on screen
- Logo, app name, version displayed
- Loading indicator (spinner or progress bar)
- Status text updates during initialization
- Smooth fade in/out animations

**Update Notification Module**:
- Overlay on splash screen when update detected
- Shows version information
- "Install Later" and "Install Now" buttons
- Non-blocking (app launches regardless)

### Buttons

- **Primary Action**: Large, prominent, primary color
- **Secondary Action**: Medium, outlined or gray
- **Danger Action**: Red, with confirmation dialog
- **Icon Buttons**: Clear icons with tooltips

### Forms

- **Input Fields**: Clear labels, placeholder text, validation messages
- **Dropdowns**: Searchable when many options
- **Date Pickers**: Calendar widget for date selection
- **Time Pickers**: Clock widget or time input
- **File Upload**: Drag-and-drop or browse button

### Tables

- **Sortable Columns**: Click header to sort
- **Filterable**: Search and filter options
- **Pagination**: Page numbers, items per page
- **Actions**: Edit, Delete, View buttons per row

### Modals/Dialogs

- **Confirmation**: "Are you sure?" for destructive actions
- **Forms**: Large forms in modal
- **Information**: Alerts and notifications
- **Progress**: Show progress for long operations

### Notifications

- **Toast Notifications**: Non-intrusive, auto-dismiss
- **Alert Banners**: Important information at top
- **Status Indicators**: Online/offline, sync status

---

## Error Handling & Validation

### Input Validation

- **Real-time**: Validate as user types
- **Clear Messages**: Specific, actionable error messages
- **Visual Indicators**: Red borders, error icons
- **Help Text**: Guidance for correct input

### Error Messages

- **User-Friendly**: No technical jargon
- **Actionable**: Tell user what to do
- **Consistent**: Same format throughout
- **Non-Blocking**: Allow correction without losing data

### Confirmation Dialogs

- **Destructive Actions**: Always confirm (delete, override)
- **Large Changes**: Confirm bulk operations
- **Financial**: Confirm payment processing
- **Clear Options**: "Cancel" and "Confirm" buttons

---

## Responsive Design Considerations

### Screen Sizes

- **POS Terminal**: 1024x768 minimum (touch-friendly)
- **Desktop ERP**: 1280x720 minimum
- **High DPI**: Support 4K displays
- **Multiple Monitors**: Support extended displays

### Touch vs Mouse

- **Touch Targets**: Minimum 44x44px
- **Hover States**: For mouse users
- **Gestures**: Swipe, pinch (where appropriate)
- **Keyboard**: Full keyboard navigation

---

## Accessibility

### Keyboard Navigation

- **Tab Order**: Logical flow through interface
- **Shortcuts**: Keyboard shortcuts for common actions
- **Focus Indicators**: Clear focus states
- **Skip Links**: Skip to main content

### Visual Accessibility

- **Color Contrast**: WCAG AA compliance
- **Font Sizes**: Adjustable, minimum 12px
- **Icons**: Text labels with icons
- **Screen Readers**: Proper ARIA labels

---

## Performance Considerations

### Loading States

- **Skeleton Screens**: Show structure while loading
- **Progress Indicators**: For long operations
- **Lazy Loading**: Load data as needed
- **Caching**: Cache frequently accessed data

### Responsiveness

- **Immediate Feedback**: Button press feedback
- **Smooth Animations**: 60fps animations
- **Optimized Queries**: Fast database queries
- **Background Processing**: Don't block UI

---

## UI/UX Pitfalls & Solutions

### Critical Issues That WILL Happen (And How to Prevent Them)

This section addresses real-world UI/UX problems that occur in production and provides practical solutions to prevent them.

---

### 1. UI/UX Scope Creep

#### Problem: Feature Explosion

You have:

- POS screens
- ERP screens
- Kitchen screens
- Table management
- Scheduling
- Reporting
- Payment flows
- Inventory
- Attendance
- Waste logs
- Multi-role accounts
- Notifications
- Sync states
- Error handling
- Offline logic
- High DPI
- Keyboard shortcuts
- Touch layouts
- Accessibility

**Something WILL be left half-done. Something WILL break. Something WILL turn into spaghetti.**

#### Solution: Ruthless Feature Control

- **Split into Modules**: ERP/POS into separate modules, not one giant application
- **Feature Tickets Only**: Add features only via feature tickets, not "random ideas at 2AM"
- **MVP → Iteration**: Follow MVP → Iteration 1 → Iteration 2 progression
- **Priority Rule**: If a feature doesn't affect money, stock, or orders, delay it

**Hard Rule**: *"If it doesn't affect cash flow, it can wait."*

---

### 2. Keyboard Shortcuts vs Touch Input Conflict

#### Problem: Input Method Chaos

You're designing for:

- POS cashiers (touch)
- Waiters (touch)
- Managers (mouse)
- Kitchen (touch but messy hands)
- Accountants (mouse + keyboard heavy)
- Admin (everything)

**You will accidentally bind "Delete" to "Clear entire cart" and make someone cry during a lunch rush.**

#### Solution: Smart UI Strategy

- **Mode Switching**: Add a "Touch Mode" vs "Desk Mode" toggle
- **POS = Touch First**: Large touch buttons + minimal keyboard shortcuts
- **Admin/ERP = Keyboard Heavy**: Full keyboard support
- **Prevent Accidents**:
  - All destructive shortcuts → require confirmation modal
  - No hidden shortcuts — show cheat sheet in UI (F1 for help)
  - Visual indicators on buttons showing keyboard shortcuts

**Implementation**:

```python
# Example: Mode-aware shortcuts
if ui_mode == "touch":
    disable_keyboard_shortcuts()
    show_touch_buttons()
elif ui_mode == "desk":
    enable_keyboard_shortcuts()
    show_shortcut_hints()
```

---

### 3. Kitchen Screen Chaos

#### Problem: Kitchen Display War Zone

Kitchen display screens are chaos:

- Orders pile up
- Chefs slam buttons with greasy fingers
- Someone clicks "Mark Ready" on the wrong table
- Two dishes get swapped
- One burns
- A waiter gets yelled at
- You get a phone call at 11PM on a Tuesday

#### Solution: Idiot-Proof Kitchen UI

- **Gigantic Buttons**: Minimum 80x80px touch targets
- **No Small Touch Zones**: Everything must be easily tappable
- **Color-Coded States**:
  - Red = Pending (urgent)
  - Yellow = Cooking
  - Green = Ready
- **Auto-Sort**: Sort orders by "time waiting" (oldest first)
- **Prevent Accidental Dismiss**:
  - Hold-to-complete (hold button for 1 second)
  - Swipe-to-complete (swipe right to mark ready)
- **Fail-Safe**: "Undo last action" button available for 10 seconds after any action

**Layout**:

```
┌─────────────────────────────────────────────────────────────┐
│ KITCHEN ORDERS - [HOLD TO MARK READY]                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ⚠ ORDER #1234 - Table 5 - WAITING 5 MIN                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ [2x Burger] [1x Fries] [1x Salad]                  │   │
│  │ [HOLD TO START] [HOLD TO MARK READY] [UNDO]        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 4. Table Management UI Nightmare

#### Problem: Table Layout Complexity Explosion

Table layout UI looks simple until:

- They change the restaurant layout
- Add a patio
- Add new tables
- Want drag-n-drop
- Want floor plan editor
- Want custom shapes
- Want labels
- Want occupancy heatmaps
- Want waiter assignment overlays
- Want reservations tied to them

**"This was supposed to be a simple grid... what the actual f—?"**

#### Solution: Table Layout Engine

- **Keep It Simple First**:
  - 3 shapes: circle, square, rectangle
  - Drag-drop placement
  - Save layout locally + cloud sync
- **Layers System**:
  - Base layer (tables)
  - Waiter assignment layer
  - Status colors layer
- **Optional Advanced Mode**: Floor plan builder (only if needed)
- **Start SMALL, expand ONLY when stable**

**Implementation**:

```python
# Simple table layout structure
table_layout = {
    "tables": [
        {"id": 1, "shape": "square", "x": 100, "y": 100, "size": 80},
        {"id": 2, "shape": "circle", "x": 200, "y": 100, "size": 80},
    ],
    "version": 1
}
```

---

### 5. Sales Reporting UI Complexity

#### Problem: Power BI in PyQt

Managers will want:

- More filters
- Custom range
- Export (CSV, Excel, PDF)
- Print
- Year-over-year
- Graphs
- Breakdown by staff
- Breakdown by hour
- Breakdown by product

**Then you realize you built Power BI in PyQt and start chain-smoking.**

#### Solution: Hybrid Caching Strategy

- **Precompute Daily Summaries**: Store them in aggregated tables
- **On-Demand Reports**: Only fetch deltas, not full recalculation
- **Async Loading**:
  - Show spinner with "Report is generating…"
  - Use pagination for big tables
- **Background Worker**: Pre-calculate:
  - Best sellers
  - Peak hours
  - Staff performance
- **Range Limits**:
  - Default: 7 days
  - Manager override: unlimited (with warning)
- **Smart Notifications**:
  - "This report will take ~30 seconds. Generate in background?"
  - Offer to email when ready

---

### 6. Offline Sync UX Hell

#### Problem: Sync State Confusion

Your UI shows:

- "Online"
- "Offline"
- "Sync Pending"
- "Last Sync: X time"

**But reality:**

- Device THINKS it's online → can't sync
- Device THINKS it's offline → IS actually online
- Data gets stuck in the queue
- Chef punches screen
- Cashier blames you

**You will rewrite sync UI 3–5 times.**

#### Solution: Bulletproof Sync UI Rules

- **Sync Queue Table**: Every event = one JSON sync job
- **Don't Sync on Every Action**: Sync when:
  - Idle (no user activity for 30 seconds)
  - Connected (network available)
  - Manual request (user clicks "Sync Now")
  - Scheduled (EOD sync)
- **UI Indicators**:
  - 🟢 Green: Synced (all data up to date)
  - 🟡 Yellow: Pending (X items waiting)
  - 🔴 Red: Offline (no connection)
  - 🔵 Blue: Syncing (actively syncing)
- **Retry Logic**: Exponential backoff (1s, 2s, 4s, 8s, max 30s)
- **Sync Status Details**: Click indicator to see:
  - Items pending
  - Last successful sync
  - Errors (if any)
  - Manual retry option

**UI Component**:

```
┌─────────────────────────────────────┐
│ Status: 🟡 12 items pending sync    │
│ Last sync: 5 minutes ago            │
│ [View Details] [Sync Now]           │
└─────────────────────────────────────┘
```

---

### 7. Validation Errors That Gaslight Users

#### Problem: Mysterious Validation Failures

You plan:

- Clear error messages
- Good UX
- No jargon

**What you'll end with:**

- "Quantity must be > 0" even though it is > 0 (because SQLite farted in a transaction)
- "Username does not exist" even though it DOES (because sync lagged)
- "Payment Failed" but the card was actually charged

#### Solution: Validation Phases

**3-Phase Validation**:

1. **Client-Side Validation**: Immediate feedback (before submit)
2. **Server-Side Validation**: On sync/cloud operations
3. **Sync-Side Validation**: During data sync

**5 Rules**:

1. Same regex everywhere (shared validation functions)
2. Same validation messages everywhere (centralized messages)
3. No mysterious codes like "ERR221" — always human-readable
4. Always show what field failed (highlight the field)
5. Always suggest a fix ("Try entering a number between 1-100")

**Error Message Format**:

```
❌ Validation Error
Field: Quantity
Problem: Value must be greater than 0
Current value: 0
Fix: Enter a number between 1 and 999
[OK] [Help]
```

---

### 8. Accessibility Escaping the Modal

#### Problem: Focus Trap Failures

You support:

- Keyboard navigation
- Focus states
- ARIA labels
- Tab index order

**Then a modal opens. User hits Tab. Focus goes BEHIND the modal. Keyboard navigation escapes. User triggers a button they can't see. POS crashes. You cry.**

#### Solution: Correct Modal System

- **Disable Background Interaction**: Block all clicks outside modal
- **Trap Keyboard Focus**: Keep Tab/Shift+Tab inside modal
- **Return Focus**: When closing, return focus to element that opened modal
- **Escape Key**: Close modal (but require confirmation for destructive actions)

**Implementation** (PyQt):

```python
dialog = QDialog(parent)
dialog.setModal(True)  # Blocks parent window
dialog.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint)
# Focus trap is automatic with setModal(True)
```

---

### 9. Modal Hell

#### Problem: Modal Zombie Apocalypse

Every action needs:

- A modal
- Or a dialog
- Or a confirmation

**Suddenly there are 300+ modal variations. You forget which modal calls which logic. You find yourself debugging a "Delete" modal that opens when clicking "Clock In".**

#### Solution: Unified Modal Engine

**Build ONE reusable modal component**:

```python
# Unified modal system
class ModalSystem:
    def confirm(self, message, callback):
        # Confirmation dialog
        pass
    
    def prompt(self, message, fields, callback):
        # Input prompt
        pass
    
    def select(self, options, callback):
        # Selection dialog
        pass
    
    def alert(self, message, type="info"):
        # Alert/notification
        pass
```

**No custom modals per feature.** Use the unified system everywhere.

---

### 10. Slow Reports

#### Problem: Report Loading Freeze

Managers WILL open a massive date range:

- "Show me ALL SALES FROM 2019 TO TODAY."

**Your app: loading… Your CPU: melting… Your UI: freezes for 11 seconds. Manager: "Why broken?"**

#### Solution: Turbo Mode

- **SQLite Indices**: Lots of them (foreign keys, timestamps, composite)
- **Precompute Stats**: Into summary tables (daily, weekly, monthly)
- **Pagination + Lazy Loading**: Load 100 rows at a time
- **Range Limits**:
  - Default: 7 days
  - Manager override: unlimited (with warning)
- **Smart Notifications**:
  - "This report will take ~30 seconds. Generate in background?"
  - Offer to email when ready
  - Show progress bar
- **Background Processing**: Don't block UI thread

**UI Pattern**:

```
┌─────────────────────────────────────┐
│ Generating Report...                │
│ ████████░░░░░░░░░░ 40%              │
│ Estimated time: 15 seconds          │
│ [Cancel] [Generate in Background]   │
└─────────────────────────────────────┘
```

---

### 11. Notification Spam

#### Problem: Notification Overload

The kitchen will see:

- "Order coming in"
- "Order cancelled"
- "Order modified"
- "Item returned"
- "Waste logged"
- "Stock low"
- "Sync pending"

**Soon they stop reading anything. Someone misses "urgent" notifications during a rush. Chaos ensues.**

#### Solution: Notification Priority System

**4 Priority Levels**:

1. **CRITICAL** (requires action) - Red, sound, persistent
2. **IMPORTANT** (informational) - Orange, brief sound, auto-dismiss
3. **NORMAL** (events) - Blue, no sound, auto-dismiss
4. **LOW** (logs) - Gray, silent, auto-dismiss

**Role-Based Filtering**:

- Kitchen screen: Only CRITICAL + IMPORTANT
- ERP/admin: All notifications
- POS cashier: CRITICAL only (payment issues, printer errors)

**Notification Settings**: Allow users to customize what they see

**UI**:

```
┌─────────────────────────────────────┐
│ 🔴 CRITICAL: Order #1234 cancelled │
│ 🟠 IMPORTANT: Low stock: Tomatoes  │
│ 🔵 NORMAL: Staff clocked in        │
│ [Settings] [Clear All]              │
└─────────────────────────────────────┘
```

---

### 12. Role Permission Chaos

#### Problem: Hybrid Role Nightmares

Someone WILL say:

- "Make the cleaner also have access to inventory but only read-only and also allow them to edit waste logs and also allow them to modify schedules but not view salaries."

**"WHAT THE SHIT KIND OF HYBRID ROLE IS THAT??" But you'll implement it anyway.**

#### Solution: Role Builder (RBAC)

**Permissions Matrix**:

| Permission | Cashier | Kitchen | Manager | Admin |
|------------|---------|---------|---------|-------|
| view_sales | ❌ | ❌ | ✔️ | ✔️ |
| edit_inventory | ❌ | ❌ | ✔️ | ✔️ |
| void_order | ✔️ | ❌ | ✔️ | ✔️ |
| log_waste | ❌ | ✔️ | ✔️ | ✔️ |
| view_salaries | ❌ | ❌ | ❌ | ✔️ |

**UI checks permissions BEFORE loading screens.**

**Custom Roles**: Allow creating custom roles with specific permissions (but limit to admins only)

**Implementation**:

```python
def check_permission(user, permission):
    role = user.role
    return PERMISSIONS_MATRIX[role][permission]

# In UI
if check_permission(current_user, "edit_inventory"):
    show_edit_button()
else:
    hide_edit_button()
```

---

### 13. DPI Scaling Disaster

#### Problem: UI Looks Different on Every Device

On one device: UI looks perfect.
On another:

- Buttons shrink
- Icons pixelate
- Text scales weird
- POS grid misaligns
- Kitchen screen has a 20px ghost margin
- Manager laptop cuts off half the table

#### Solution: DPI-Proof UI Rules

- **Vector Icons**: Use SVG, not bitmap
- **Percentage-Based Margins**: Not fixed pixels
- **Test on Multiple DPIs**: 96, 120, 144, 160, 240
- **Detect Scaling on Startup**: Adjust layout automatically
- **PyQt DPI Awareness**:

  ```python
  QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
  QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
  ```

- **Responsive Layouts**: Use layouts that adapt to screen size
- **Minimum Sizes**: Set minimum button/icon sizes (don't let them shrink too much)

---

### 14. Human Error + Stress + UI = Apocalypse

#### Problem: Users Make Mistakes Under Pressure

Someone will:

- Forget to clock out
- Forget to sync
- Approve wrong dish
- Mis-enter stock
- Hit delete by accident
- Not read warnings
- Close the app mid-sync
- Double-tap an action out of panic

**And YOU get blamed.**

#### Solution: UX Safety Nets

- **Big Buttons**: Easy to tap, hard to miss
- **Undo Buttons**: "Undo last action" available for 10 seconds
- **Confirmation for Destructive Actions**: Always confirm delete/void/override
- **Input Defaults**: Don't let critical fields be empty
- **Auto-Save Drafts**: Save form data as user types
- **Always Show Warnings**: Before losing data
- **Double-Click Prevention**: Debounce rapid clicks
- **Processing Indicators**: Show "Processing..." to prevent double-submission
- **Session Recovery**: If app crashes, recover last state

**Example**:

```
┌─────────────────────────────────────┐
│ Delete Order #1234?                 │
│ This action cannot be undone.       │
│                                     │
│ [Cancel] [Delete Order]             │
└─────────────────────────────────────┘
```

---

### 15. Users Will Abuse Your UI

#### Problem: Users Don't Follow Your Beautiful Design

Your UI is:

- Elegant
- Clean
- Thoughtful

**Users:**

- Tap every button
- Spam Enter
- Shake the mouse violently
- Drag random things
- Click "Cancel" instead of "Confirm"
- Hit Esc 14 times
- Try to touch the screen on a non-touch monitor
- Block the barcode scanner with a coffee cup

**Your UI doesn't stand a chance.**

#### Solution: Anti-Chaos UI Protections

- **Double-Click Prevention**: Debounce inputs (ignore rapid clicks)
- **Disable Button While Processing**: Prevent multiple submissions
- **Debounce Inputs**: Wait 300ms after user stops typing before validating
- **Don't Allow Enter to Trigger Dangerous Actions**: Require explicit button click
- **Add Tooltips Everywhere**: Help users understand what buttons do
- **Add Logs for Every Action**: Track what users actually do
- **Add Visual Feedback for All Clicks**: Button press animation, loading spinner
- **Input Validation**: Prevent invalid data entry
- **Graceful Degradation**: If something fails, show helpful error, don't crash
- **User Education**: Show tooltips, help screens, onboarding

**If a user tries to do something insane, show:**

```
┌─────────────────────────────────────┐
│ ⚠️ Invalid Action                   │
│                                     │
│ You can't delete an order that's   │
│ already been paid.                  │
│                                     │
│ [OK] [Help]                         │
└─────────────────────────────────────┘
```

---

## UI/UX Implementation Checklist

### Before Launch

- [ ] Test all screens on multiple DPIs (96, 120, 144, 160, 240)
- [ ] Test keyboard navigation (Tab order, shortcuts, focus traps)
- [ ] Test touch input (all buttons tappable, no accidental triggers)
- [ ] Test offline mode (all features work, clear sync indicators)
- [ ] Test error handling (validation messages, recovery)
- [ ] Test modal system (focus traps, background blocking)
- [ ] Test notification system (priority levels, role filtering)
- [ ] Test role permissions (all roles, all screens)
- [ ] Test report generation (large date ranges, pagination)
- [ ] Test sync UI (all states, retry logic, error handling)
- [ ] User testing with real staff (kitchen, cashier, manager)
- [ ] Performance testing (reports, large datasets, concurrent users)

### Ongoing Maintenance

- [ ] Monitor user feedback (what's confusing, what's broken)
- [ ] Track error logs (what errors occur most often)
- [ ] A/B test UI changes (test with small group first)
- [ ] Regular UI audits (check for inconsistencies)
- [ ] Update documentation (as UI changes)
- [ ] Train new users (onboarding, help screens)

---

## Next Steps

1. Create detailed wireframes for each screen
2. Design high-fidelity mockups
3. Create UI component library (unified modals, buttons, forms)
4. Build interactive prototypes
5. User testing and iteration
6. Finalize design system
7. Implementation guidelines
8. **Add UI/UX testing to implementation phases**
9. **Create user training materials**
10. **Set up error tracking and user feedback system**
