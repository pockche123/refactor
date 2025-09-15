# Commit SHA Validation for Behavioral Testing

## Critical Requirement: commit_sha Column

**ESSENTIAL**: All datasets MUST contain the `commit_sha` column for behavioral validation in ML vs LLM research.

## Verification Results

✅ **All 350-record datasets contain commit_sha**:

| Dataset | commit_sha Present | Sample SHA |
|---------|-------------------|------------|
| `commons_lang_350_real.csv` | ✅ YES | `a265d47580e5a431b1aebb8bca7b1e4dc1ea83f4` |
| `spring_350_real.csv` | ✅ YES | `d421f61a4ac2a323fbaa3e5b9b619a99069e09c0` |
| `kafka_350_real.csv` | ✅ YES | `42f74a1c3afd693a16c3980ee022e82872e4bfa2` |
| `intellij_350_real.csv` | ✅ YES | `e6c9306615f1ecb1c375eda4df01efe3dd901cd9` |
| `mockito_350_real.csv` | ✅ YES | `bc06f214c0c9505a1887e4422a449c6304993ff5` |

## Why commit_sha is Critical

1. **Behavioral Validation**: Enables retrieval of actual before/after code
2. **Reproducibility**: Permanent reference to exact refactoring changes  
3. **Fair Comparison**: Both ML and LLM tested on identical real cases
4. **Code Access**: `git show <commit_sha> -- <file_path>` retrieves changes

## Dataset Schema Confirmation

```csv
file_path,refactoring_type,lines_changed,cyclomatic_complexity,nesting_depth,commit_sha,commit_idx,refactoring_idx,description,has_left_locations,has_right_locations
```

**Position 6**: `commit_sha` - Real GitHub commit hash (40 characters)

## Usage for Behavioral Validation

```bash
# Clone repository
git clone https://github.com/apache/commons-lang.git

# Get actual refactoring changes
git show a265d47580e5a431b1aebb8bca7b1e4dc1ea83f4 -- src/main/java/org/apache/commons/lang3/time/FastDatePrinter.java

# Shows exact before/after code for validation
```

## Status: READY FOR RESEARCH

All datasets are properly formatted with commit_sha for behavioral validation in ML vs LLM refactoring prediction research.

---
*Verified: 2025-09-15 - commit_sha present in all datasets*
