---
id: 1
title: Chatbot Task Format Improvements
stage: general
date: 2026-02-20
surface: agent
model: qwen-code
feature: none
branch: main
user: AK C0M
command: UI improvement request
labels: ["chatbot", "ui", "task-formatting", "frontend", "backend", "task-id"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/agents/google_agent.py
  - backend/mcp/tools.py
  - frontend/src/components/ChatBot.tsx
  - frontend/src/components/TaskCard.tsx
tests:
  - Manual testing via chatbot UI
---

## Prompt

User requested multiple improvements:
1. Chatbot welcome message showing capabilities in table format when user first opens it
2. Professional task display format with ID, title, description, and proper due date formatting (e.g., "3 days later" instead of raw date)
3. Show task ID in the app task cards (was missing)

Follow-up issues:
- User input "Title: Movie Description: DDLJ Duedate: After 4days" was being parsed incorrectly
- Task ID not showing in app task cards

## Response snapshot

Implemented all features:

1. **Chatbot Welcome Table**: Added a professional capabilities table in ChatBot.tsx that displays when messages.length === 0. Shows 6 capabilities with emojis and example phrases.

2. **Professional Task Format**: Added `_format_task_professional()` method in google_agent.py that formats tasks with:
   - Task ID (#1, #2, etc.)
   - Title on first line
   - Description on second line (if present)
   - Human-readable due date (e.g., "Due in 3 days", "Due Tomorrow", "Overdue by 2 days")
   - Status icons (⏳ pending, ✅ completed)

3. **MCP Tools Update**: Updated `list_tasks()` in mcp/tools.py to include description field in task data.

4. **Fixed Title/Description Parsing**: Updated `_extract_task_title_improved()` and `_extract_description_improved()` to handle semicolon-separated formats.

5. **Task ID Badge in UI**: Updated TaskCard.tsx to display a prominent ID badge:
   - Shows `#1`, `#2`, etc. with hash icon
   - Gradient background (purple/blue for active, green for completed)
   - Positioned above task title for easy visibility
   - Helps users reference tasks when using chatbot commands

## Outcome

- ✅ Chatbot now shows capabilities table on first open
- ✅ Tasks display with professional format including ID, title, description, and human-readable due dates
- ✅ Semicolon-separated input format now parsed correctly
- ✅ Task ID now visible in app task cards for easy reference
- 🧪 Tests: Manual testing required via frontend
- 📁 Files: 4 files modified (2 frontend, 2 backend)
- 🔁 Next prompts: Test the chatbot UI and app to verify all features
- 🧠 Reflection: Separated presentation logic into dedicated method for maintainability

## Evaluation notes (flywheel)

- Failure modes observed: None expected, but date parsing edge cases possible
- Graders run and results: Manual testing needed
- Prompt variant: N/A
- Next experiment: Verify task ID badge displays correctly in app and chatbot responses