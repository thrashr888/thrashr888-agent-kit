# Spec Template

## SPEC: [System/Component Name]

**Version:** 1.0
**Last Updated:** [YYYY-MM-DD]
**Owner:** [Name]

---

## Overview

One paragraph describing what this system/component is and its primary purpose.

## Architecture

### Components

```
[Diagram or ASCII art of system components]
```

### Key Entities

| Entity | Description | Constraints |
|--------|-------------|-------------|
| Entity1 | What it represents | Invariants it must maintain |

## Behavior

### Core Invariants

These MUST always hold true:

1. **Invariant 1**: Description
2. **Invariant 2**: Description

### State Machine (if applicable)

```
[Initial] --> [State1] --> [State2] --> [Final]
                 |
                 v
            [ErrorState]
```

### Operations

#### Operation 1: [Name]

**Preconditions:**
- Condition 1

**Postconditions:**
- Result 1

**Side Effects:**
- Effect 1

## Data Model

### Schema

```
Type/Table definition
```

### Relationships

- A has many B
- B belongs to A

## API (if applicable)

### Endpoints / Functions

| Endpoint/Function | Description | Input | Output |
|-------------------|-------------|-------|--------|
| `/api/thing` | Does X | Params | Response |

## Security Considerations

- Security constraint 1
- Security constraint 2

## Performance Characteristics

| Operation | Expected Performance |
|-----------|---------------------|
| Read | O(1) / < 10ms |
| Write | O(n) / < 100ms |

## Failure Modes

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Database down | Health check fails | Retry with backoff |

## Configuration

| Config | Default | Description |
|--------|---------|-------------|
| TIMEOUT | 30s | Request timeout |

## Dependencies

- External service 1
- Library 2

## References

- Link to related specs
- Link to implementation (skills)

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | Name | Initial spec |
