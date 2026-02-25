# UI Components Specification: Todo Application Frontend

## Overview
This document defines the reusable UI components for the Todo application frontend. All components follow Next.js 16+ conventions, use TypeScript for type safety, and implement Tailwind CSS for styling.

## Component Categories

### 1. Atoms (Basic Elements)

#### 1.1 Button
- **Props**: variant (primary, secondary, danger, ghost), size (sm, md, lg), disabled, loading, icon
- **Behavior**: Hover, focus, active, disabled states
- **Accessibility**: Proper ARIA attributes, keyboard navigation
- **Animation**: Smooth transitions on state changes

#### 1.2 Input
- **Props**: type, placeholder, value, onChange, error, label, required
- **Behavior**: Focus states, validation feedback
- **Accessibility**: Associated labels, proper ARIA attributes
- **Variants**: Text, email, password, textarea

#### 1.3 Checkbox
- **Props**: checked, onChange, label, disabled
- **Behavior**: Toggle state, indeterminate state (if applicable)
- **Accessibility**: Proper ARIA attributes, keyboard navigation
- **Animation**: Smooth transition when toggled

#### 1.4 Badge
- **Props**: variant (success, warning, error, info), size (sm, md, lg)
- **Behavior**: Static display of status or category
- **Accessibility**: Proper contrast ratios

#### 1.5 Spinner
- **Props**: size (sm, md, lg), variant (primary, secondary)
- **Behavior**: Animated loading indicator
- **Accessibility**: ARIA live region for screen readers

### 2. Molecules (Compound Elements)

#### 2.1 Form Field
- **Composition**: Label + Input + Error Message
- **Behavior**: Integrated validation display
- **Accessibility**: Proper form associations

#### 2.2 Card
- **Composition**: Header + Body + Footer sections
- **Props**: title, subtitle, actions, padding
- **Behavior**: Flexible content container
- **Variants**: With/without shadows, borders

#### 2.3 Modal
- **Composition**: Overlay + Container + Header + Body + Footer
- **Props**: isOpen, onClose, title, size
- **Behavior**: Overlay click to close, ESC key to close
- **Accessibility**: Focus trap, ARIA attributes

#### 2.4 Dropdown
- **Composition**: Trigger button + Menu list
- **Props**: options, onSelect, placement
- **Behavior**: Open/close animation, keyboard navigation
- **Accessibility**: Proper ARIA attributes

#### 2.5 Alert
- **Composition**: Icon + Message + Close button
- **Props**: variant (success, warning, error, info), closable
- **Behavior**: Dismissible, auto-dismiss option
- **Animation**: Fade in/out transitions

### 3. Organisms (Complex Components)

#### 3.1 TaskCard
- **Composition**: Title, truncated description, status badge, created date
- **Props**: task object, onToggleComplete, onDelete, onEdit
- **Behavior**: Hover effects, status indicator, relative time display
- **Animation**: Smooth transitions when state changes
- **Accessibility**: Keyboard navigation, ARIA attributes

#### 3.2 TaskForm
- **Composition**: Input fields for title, description, due date
- **Props**: initialData, onSubmit, onCancel
- **Behavior**: Form validation, submission handling
- **Accessibility**: Proper form associations, error messaging

#### 3.3 TaskList
- **Composition**: Multiple TaskCards with filtering/search
- **Props**: tasks array, onTaskUpdate, onTaskDelete
- **Behavior**: Sorting, filtering, infinite scroll/pagination
- **Animation**: Staggered card appearance

#### 3.4 NavigationSidebar
- **Composition**: Logo, navigation links, user profile
- **Props**: navItems, user, onLogout
- **Behavior**: Active state highlighting, collapsible on mobile
- **Animation**: Smooth expand/collapse transitions

#### 3.5 AuthForm
- **Composition**: Form fields, submit button, social login options
- **Props**: type (login/register), onSubmit, onSocialLogin
- **Behavior**: Form validation, loading states
- **Accessibility**: Proper form structure, error messaging

### 4. Templates (Page Structures)

#### 4.1 AuthTemplate
- **Composition**: Background, centered form container, brand elements
- **Behavior**: Responsive layout, loading states
- **Animation**: Fade transitions between auth states

#### 4.2 DashboardTemplate
- **Composition**: Sidebar, header, main content area
- **Behavior**: Responsive sidebar, breadcrumb navigation
- **Animation**: Smooth transitions between sections

## Component Guidelines

### Styling
- Use Tailwind CSS utility classes exclusively (no inline styles)
- Follow consistent spacing scale (using Tailwind's spacing system)
- Maintain consistent color palette across all components

### Animation & Transitions
- Use subtle animations for state changes (opacity, transform)
- Implement consistent duration and easing (e.g., 200ms ease-in-out)
- Use Framer Motion for complex animations where needed
- Ensure animations respect user's reduced motion preferences

### TypeScript
- Define clear prop interfaces for all components
- Use generic types where appropriate
- Implement proper error handling with TypeScript

### Accessibility
- All interactive elements must be keyboard accessible
- Proper ARIA attributes for complex components
- Sufficient color contrast ratios
- Focus management for dynamic content

### Reusability
- Components should be configurable via props
- Avoid hardcoding values; use theme variables
- Design components to work in multiple contexts
- Separate concerns (presentation vs. logic)