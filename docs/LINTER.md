# CAT-MIP Terms Linter Documentation

## Quick Start Guide

The CAT-MIP linter checks that all terms in `terms.json` follow the correct format and standards.

### What You Need

- A computer with Python installed (version 3.9 or higher)
- The CAT-MIP repository files
- UV package manager (instructions below)

### Setup (One-Time Only)

1. **Install UV** (if not already installed):

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Get the CAT-MIP files**:

   ```bash
   git clone https://github.com/nicolereineke/cat-mip.git
   cd cat-mip
   ```

3. **Set up the linter**:

   ```bash
   uv sync
   ```

That's it! You're ready to use the linter.

## Basic Usage

### Check Your Terms File

To validate the `terms.json` file, run:

```bash
uv run python lint_catmip.py
```

### See More Details

To see statistics about your terms:

```bash
uv run python lint_catmip.py --stats
```

## Understanding the Results

When you run the linter, you'll see results like this:

```text
============================================================
CAT-MIP Terms Linter Results
============================================================

✅ Validation PASSED

📊 STATISTICS:
  Total terms: 68
  Terms with synonyms: 65
  Terms with relationships: 62
```

### What the Symbols Mean

- **✅ Green checkmark** = Everything is good!
- **❌ Red X** = There are errors that must be fixed
- **⚠️ Yellow warning** = Something should be reviewed but isn't critical
- **ℹ️ Blue info** = Just information, no action needed

### If You See Errors

**ERRORS must be fixed** before your changes can be accepted. Common errors include:

- Missing required fields (every term needs: id, canonical_term, definition, metadata)
- Duplicate terms (each term must be unique)
- Invalid JSON format (missing commas, brackets, etc.)

### If You See Warnings

**WARNINGS are suggestions** that should be reviewed:

- Definition too short or too long
- Missing punctuation
- Non-standard formatting

## Common Issues and Solutions

### "JSON Parsing Error"

**Problem**: The file has a formatting error.

**Solution**: Check for:

- Missing commas between items
- Missing closing brackets `}` or `]`
- Extra commas at the end of lists

### "Duplicate canonical term"

**Problem**: Two terms have the same name.

**Solution**: Search for the duplicate term and ensure each has a unique name.

### "Missing required fields"

**Problem**: A term is missing important information.

**Solution**: Every term must have:

- `id` - A unique identifier
- `canonical_term` - The official name
- `definition` - What the term means
- `metadata` - Information about who added it and when

## When Adding New Terms

Before submitting your new terms:

1. Run the linter to check for errors
2. Fix any errors (red X items)
3. Review any warnings (yellow items)
4. Make sure your term has all required fields

## Getting Help

If you need assistance:

- Check the error message - it usually tells you what's wrong
- Look at existing terms in the file for examples
- Open an issue in the GitHub repository
- Contact the CAT-MIP team

---

## Advanced Options

<details>
<summary>Click to expand advanced options</summary>

### Additional Commands

#### Quiet Mode (Errors Only)

Show only errors, not warnings or info:

```bash
uv run python lint_catmip.py --quiet
```

#### JSON Output

Export results as JSON for automation:

```bash
uv run python lint_catmip.py --json > report.json
```

#### Using the Script Name

After installation, you can also use:

```bash
uv run catmip-lint
```

#### Specify a Different File

To check a different JSON file:

```bash
uv run python lint_catmip.py path/to/other/terms.json
```

### Developer Setup

#### Install Development Dependencies

For developers who want to contribute to the linter itself:

```bash
uv sync --all-extras
```

This installs:

- `pytest` - for testing
- `black` - for code formatting
- `mypy` - for type checking
- `ruff` - for linting
- `pre-commit` - for git hooks

#### Pre-commit Hooks

To automatically check files before committing:

1. Install pre-commit:

   ```bash
   pip install pre-commit
   ```

2. Install the git hooks:

   ```bash
   pre-commit install
   ```

3. The linter will now run automatically before each commit

4. Run manually on all files:

   ```bash
   pre-commit run --all-files
   ```

### GitHub Actions Integration

The linter runs automatically on:

- Push to `main`, `cam-dev`, or `develop` branches
- Pull requests to `main`
- Manual workflow dispatch

View results in:

- GitHub Actions tab
- Pull request comments (for PRs)
- Workflow summary
- Downloadable artifacts

### CI/CD Integration

The linter integrates with:

1. **GitHub Actions** - Automatic validation on push/PR
2. **Pre-commit hooks** - Local validation before commit
3. **JSON output** - Machine-readable results for automation

### Technical Details

#### Validation Checks

1. **JSON Syntax Validation**
   - Ensures valid JSON structure
   - Reports parsing errors with line/column numbers

2. **Structure Validation**
   - Verifies required fields: `id`, `canonical_term`, `definition`, `metadata`
   - Checks for unknown/unexpected fields
   - Validates ID and canonical term uniqueness
   - Ensures canonical terms start with capital letters

3. **Metadata Validation**
   - Verifies required metadata fields: `author`, `version`, `date_added`, `registry`
   - Validates ISO 8601 date format
   - Checks version format (X.Y)
   - Verifies registry value is 'cat-mip.org'

4. **Relationship Validation**
   - Ensures relationships follow standard patterns
   - Common patterns: `belongsTo`, `isConnectedTo`, `isManagedBy`, etc.
   - Validates relationship string format

5. **Content Quality Checks**
   - Definition length (warns if too short <50 chars or too long >2000 chars)
   - Proper capitalization and punctuation
   - Detects empty lists in optional fields
   - Validates agent_execution structure

6. **Cross-Reference Analysis**
   - Identifies references between terms
   - Helps maintain consistency across the vocabulary

#### Exit Codes

- `0` - Validation passed (no errors, warnings allowed)
- `1` - Validation failed (errors found)

#### Date Format Specification

Dates must use ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`

Example: `2025-08-07T00:00:00Z`

#### Relationship Pattern Specification

Relationships should follow patterns like:

- `Agent isInstalledOn Device`
- `Tenant belongsTo MSP`
- `API isExposedBy Platform`

</details>
