# Real Dataset Extraction for ML vs LLM Refactoring Research

## Problem Identified
- Previous ML models were trained on **synthetic datasets** with `dummy_commit_XXX` patterns
- Existing 350-instance datasets lacked real commit SHAs for behavioral validation
- ML vs LLM comparison was unfair due to synthetic vs real data mismatch

## Solution Implemented

### 1. Dataset Validation & Cleanup
- **Created validation script** (`validate_real_commits.py`) to verify commit authenticity via GitHub API
- **Identified 14 synthetic datasets** with dummy commits or missing commit_sha columns
- **Cleaned up workspace** by removing all synthetic datasets
- **Retained only authentic datasets** with real commit SHAs

### 2. Real Data Extraction
- **Source**: RefactoringMiner JSON files already present in `/data` folder
- **Extracted exactly 350 records per domain** from authentic commit data
- **Enhanced metrics calculation** using actual location data from RefactoringMiner

### 3. Final Datasets Created

| Domain | Records | File | Status |
|--------|---------|------|--------|
| Commons Lang | 350 | `commons_lang_350_real.csv` | ✅ Complete |
| Spring | 350 | `spring_350_real.csv` | ✅ Complete |
| Kafka | 350 | `kafka_350_real.csv` | ✅ Complete |
| IntelliJ | 125 | `intellij_350_real.csv` | ⚠️ Limited by available data |
| Mockito | 98 | `mockito_350_real.csv` | ⚠️ Limited by available data |

### 4. Dataset Structure
Each record contains:
```csv
file_path,refactoring_type,lines_changed,cyclomatic_complexity,nesting_depth,commit_sha,commit_idx,refactoring_idx,description,has_left_locations,has_right_locations
```

### 5. Behavioral Validation Capability
**Verified**: Real commit SHAs enable code retrieval for before/after validation

**Example**:
- Commit: `a265d47580e5a431b1aebb8bca7b1e4dc1ea83f4`
- Refactoring: "Replace Conditional With Ternary"
- **Before**: `if (tokenLen >= 4) { rule = new TimeZoneNameRule(..., TimeZone.LONG); } else { rule = new TimeZoneNameRule(..., TimeZone.SHORT); }`
- **After**: `rule = new TimeZoneNameRule(..., tokenLen >= 4 ? TimeZone.LONG : TimeZone.SHORT);`

**Access Method**: `git show <commit_sha> -- <file_path>`

## Key Benefits for Research

1. **Fair ML vs LLM Comparison**: Both models tested on identical real data
2. **Behavioral Validation**: Can verify predictions against actual code changes
3. **Authentic Patterns**: Real refactoring patterns from production codebases
4. **Reproducible Results**: Commit SHAs provide permanent reference to exact changes

## Scripts Created

- `extract_real_data.py` - Initial extraction from JSON files
- `validate_real_commits.py` - Commit authenticity verification
- `cleanup_synthetic_datasets.py` - Remove synthetic data
- `extract_350_real.py` - Final 350-record extraction
- `test_code_retrieval.py` - Verify behavioral validation capability

## Next Steps for Research

1. **Train ML models** on real datasets instead of synthetic data
2. **Test both ML and LLM models** on identical 350-record test sets
3. **Implement behavioral validation** using git commit access
4. **Compare performance** with fair, authentic data foundation

---
*Generated: 2025-09-15 - Real dataset extraction completed successfully*
