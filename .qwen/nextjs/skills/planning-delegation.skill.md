# Feature Planning & Delegation Skill

## Description
This skill helps break down feature requests into clear, actionable phases with proper delegation to specialized sub-agents. It ensures systematic implementation following spec-driven development principles.

## Purpose
- Decompose feature requests into manageable phases/steps
- Identify relevant specifications to reference
- Assign tasks to appropriate sub-agents
- Plan dependencies and complexity considerations
- Include testing and integration checkpoints
- Output structured plans in clean markdown format

## Process
When given a feature request (e.g. "implement task CRUD with auth"):

1. **Read Relevant Specs**: Identify and reference relevant specifications such as @specs/features/..., @specs/api/..., @specs/database/..., @specs/ui/...

2. **Break Into Phases**: Create 5-8 clear phases/steps for implementation

3. **Step Details**: For each step, specify:
   - Target folder/file location
   - Which sub-agent/skill to delegate to
   - Dependencies on other steps/components
   - Estimated complexity (Low/Medium/High)

4. **Include Checkpoints**: Add testing & integration checkpoints throughout

5. **Output Format**: Provide results in clean markdown with:
   - Numbered phases
   - Table of delegations with agent assignments

## Output Template
```markdown
## Feature Implementation Plan: [Feature Name]

### Phases
1. [Phase 1 description]
2. [Phase 2 description]
...

### Delegation Table
| Phase | Component | Sub-Agent | Dependencies | Complexity | Test Checkpoint |
|-------|-----------|-----------|--------------|------------|-----------------|
| 1     | [detail]  | [agent]   | [deps]       | [low/med/high] | [test desc] |
...
```

## Guidelines
- Always reference relevant specs first
- Ensure phases build logically on each other
- Identify potential blockers early
- Include both unit and integration testing checkpoints
- Consider security implications in planning
- Account for error handling requirements