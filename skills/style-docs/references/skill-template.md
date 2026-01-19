# Skill Template

```yaml
---
name: skill-name
description: One-line description of what this skill does. Use when [trigger conditions].
allowed-tools: Read, Edit, Write, Bash, Grep, Glob, Task
---
```

# [Skill Name]

## Overview

Brief description of what this skill enables and when to use it.

## Prerequisites

- Prerequisite 1
- Prerequisite 2

## Workflow

### Step 1: [Action Name]

Description of what to do and why.

```bash
# Example command
command --flag value
```

### Step 2: [Action Name]

Description of next step.

```rust
// Example code
fn example() {
    // Implementation
}
```

### Step 3: [Verification]

How to verify the work is complete.

```bash
# Verification command
test-command
```

## Common Patterns

### Pattern 1: [Name]

When to use this pattern and example implementation.

```rust
// Pattern example
impl Pattern for Thing {
    fn method(&self) -> Result<()> {
        // Implementation
    }
}
```

### Pattern 2: [Name]

Another common pattern.

## Decision Points

| Situation | Recommendation |
|-----------|----------------|
| When X | Do Y |
| When A | Do B |

## Anti-Patterns

**DON'T:**
- Anti-pattern 1
- Anti-pattern 2

**DO:**
- Best practice 1
- Best practice 2

## Troubleshooting

### Issue 1: [Problem]

**Symptoms:** What you'll see

**Cause:** Why it happens

**Solution:**
```bash
fix-command
```

### Issue 2: [Problem]

**Solution:** How to fix

## Resources

- `references/additional-doc.md`: Supporting documentation
- `scripts/helper.sh`: Automation script

## Related Skills

- `other-skill`: Related functionality
