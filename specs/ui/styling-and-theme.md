# Styling and Theme Specification: Todo Application Frontend

## Overview
This document defines the visual design system, color palette, typography, and animation guidelines for the Todo application frontend. All styling follows Tailwind CSS conventions with subtle animations for enhanced user experience.

## Color Palette

### Primary Colors
- **Primary 50**: #eff6ff (lightest shade)
- **Primary 100**: #dbeafe
- **Primary 200**: #bfdbfe
- **Primary 300**: #93c5fd
- **Primary 400**: #60a5fa
- **Primary 500**: #3b82f6 (main brand color)
- **Primary 600**: #2563eb (darker shade)
- **Primary 700**: #1d4ed8 (darker shade)
- **Primary 800**: #1e40af (darkest shade)
- **Primary 900**: #1e3a8a (darkest shade)

### Secondary Colors
- **Secondary 50**: #f0f9ff
- **Secondary 100**: #e0f2fe
- **Secondary 200**: #bae6fd
- **Secondary 300**: #7dd3fc
- **Secondary 400**: #38bdf8
- **Secondary 500**: #0ea5e9 (complementary color)
- **Secondary 600**: #0284c7
- **Secondary 700**: #0369a1
- **Secondary 800**: #075985
- **Secondary 900**: #0c4a6e

### Status Colors
- **Success**: #10b981 (green - for completed tasks, success messages)
- **Warning**: #f59e0b (amber - for due soon tasks, warnings)
- **Error**: #ef4444 (red - for errors, overdue tasks)
- **Info**: #3b82f6 (blue - for information, neutral actions)

### Neutral Colors
- **Gray 50**: #f9fafb
- **Gray 100**: #f3f4f6
- **Gray 200**: #e5e7eb
- **Gray 300**: #d1d5db
- **Gray 400**: #9ca3af
- **Gray 500**: #6b7280
- **Gray 600**: #4b5563
- **Gray 700**: #374151
- **Gray 800**: #1f2937
- **Gray 900**: #111827

## Typography

### Font Stack
- **Primary Font**: Inter, system-ui, sans-serif (for body text)
- **Heading Font**: Inter, system-ui, sans-serif (for headings)
- **Monospace Font**: JetBrains Mono, ui-monospace, SFMono-Regular, monospace (for code elements)

### Font Sizes
- **xs**: 0.75rem (12px) - captions, helper text
- **sm**: 0.875rem (14px) - small text, labels
- **base**: 1rem (16px) - body text
- **lg**: 1.125rem (18px) - larger body text
- **xl**: 1.25rem (20px) - small headings
- **2xl**: 1.5rem (24px) - medium headings
- **3xl**: 1.875rem (30px) - large headings
- **4xl**: 2.25rem (36px) - extra large headings

### Font Weights
- **font-thin**: 100
- **font-light**: 300
- **font-normal**: 400
- **font-medium**: 500
- **font-semibold**: 600
- **font-bold**: 700

### Line Heights
- **leading-tight**: 1.25
- **leading-snug**: 1.375
- **leading-normal**: 1.5
- **leading-relaxed**: 1.625
- **leading-loose**: 2

## Spacing System

### Base Unit
- 1 unit = 0.25rem (4px)
- Powers of 2 progression: 0, 1, 2, 4, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96

### Common Spacings
- **Space 1**: 0.25rem (4px) - small internal element spacing
- **Space 2**: 0.5rem (8px) - component padding, small margins
- **Space 3**: 0.75rem (12px) - medium spacing
- **Space 4**: 1rem (16px) - standard component spacing
- **Space 5**: 1.25rem (20px) - section spacing
- **Space 6**: 1.5rem (24px) - larger section spacing
- **Space 8**: 2rem (32px) - major section separation
- **Space 10**: 2.5rem (40px) - large layout spacing
- **Space 12**: 3rem (48px) - maximum spacing

## Component Styling

### Buttons
- **Primary**: bg-primary-600, text-white, hover:bg-primary-700
- **Secondary**: bg-gray-200, text-gray-800, hover:bg-gray-300
- **Danger**: bg-red-600, text-white, hover:bg-red-700
- **Ghost**: bg-transparent, text-primary-600, hover:bg-gray-100
- **Padding**: px-4 py-2
- **Rounded**: rounded-md
- **Transition**: transition-colors duration-200 ease-in-out
- **Focus**: ring-2 ring-primary-500 ring-offset-2

### Cards
- **Background**: white or gray-50
- **Border**: border-gray-200
- **Shadow**: shadow-sm (for subtle elevation)
- **Padding**: p-4 or p-6 depending on content
- **Rounded**: rounded-lg
- **Hover**: shadow-md transition-shadow duration-200 ease-in-out

### Forms
- **Input Fields**: 
  - Border: border-gray-300
  - Focus: border-primary-500, ring-1 ring-primary-500
  - Padding: px-3 py-2
  - Rounded: rounded-md
  - Transition: border-color 200ms ease-in-out
- **Labels**: font-medium text-gray-700
- **Error State**: border-red-500, text-red-600

### Navigation
- **Active Link**: text-primary-600, font-medium
- **Inactive Link**: text-gray-600, hover:text-gray-900
- **Sidebar**: bg-white, border-r border-gray-200
- **Topbar**: bg-white, border-b border-gray-200

## Animation Guidelines

### Transition Durations
- **Instant**: 0ms (immediate changes)
- **Fast**: 100ms (quick feedback)
- **Normal**: 200ms (standard transitions)
- **Slow**: 300ms (more noticeable animations)
- **Slowest**: 500ms (major state changes)

### Easing Functions
- **ease-linear**: linear (constant speed)
- **ease-in**: cubic-bezier(0.4, 0, 1, 1) (slow start)
- **ease-out**: cubic-bezier(0, 0, 0.2, 1) (slow end)
- **ease-in-out**: cubic-bezier(0.4, 0, 0.2, 1) (slow start and end)

### Animation Patterns

#### Micro-interactions
- **Button Hover**: Scale(1.02) or background color change
- **Checkbox Toggle**: Smooth opacity change with checkmark animation
- **Task Card Hover**: Lift effect with slight scale and shadow increase
- **Focus Rings**: Smooth transition to primary color ring

#### State Transitions
- **Modal Open/Close**: Fade in/out with scale transformation
- **Task Addition/Removal**: Slide in/out with fade
- **Form Submission**: Loading spinner with opacity transition
- **Tab Switching**: Fade between content with subtle slide

#### Loading States
- **Skeleton Loading**: Shimmer animation on placeholder elements
- **Progress Indicators**: Smooth progress bar or spinner
- **Data Fetching**: Subtle pulsing animation

### Animation Examples
```css
/* Button hover effect */
.btn-transition {
  transition: all 200ms ease-in-out;
}

.btn-hover:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

/* Task card animation */
.task-card {
  transition: transform 200ms ease, box-shadow 200ms ease;
}

.task-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

/* Fade in/out */
.fade-enter {
  opacity: 0;
  transform: translateY(10px);
}

.fade-enter-active {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 300ms, transform 300ms;
}
```

## Responsive Design

### Breakpoints
- **sm**: 640px (mobile to tablet)
- **md**: 768px (tablet portrait)
- **lg**: 1024px (tablet landscape to desktop)
- **xl**: 1280px (desktop)
- **2xl**: 1536px (large desktop)

### Responsive Behavior
- **Typography**: Slightly larger text on larger screens
- **Spacing**: More generous spacing on larger screens
- **Layout**: Column-based on mobile, row-based on desktop
- **Components**: Adjust size and arrangement based on screen width

## Dark Mode Considerations
- **Backgrounds**: Darken backgrounds (gray-800 to gray-900)
- **Text**: Lighten text colors (white to gray-200)
- **Borders**: Use darker border colors
- **Accents**: Adjust primary colors to maintain contrast

## Accessibility
- **Color Contrast**: Maintain minimum 4.5:1 contrast ratio
- **Focus Indicators**: Visible focus rings on interactive elements
- **Reduced Motion**: Respect user's reduced motion preferences
- **Semantic HTML**: Proper use of heading hierarchy and landmarks