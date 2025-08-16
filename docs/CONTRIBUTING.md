# Contributing to CAT-MIP

Thank you for your interest in contributing to the Consortium for AI Terminology for MSPs & IT Pros (CAT-MIP)!

## How to Contribute

We welcome contributions in several areas:

### 1. Adding New Terms

The most common contribution is adding new terminology to our vocabulary.

#### Before You Start

- **Search first**: Check if the term already exists in `terms.json`
- **Review existing terms**: Look at similar terms to understand the format
- **Consider relationships**: Think about how your term relates to existing ones

#### Required Information for Each Term

Every term MUST include:

- **id**: A unique identifier (use UUID format or descriptive ID)
- **canonical_term**: The official name (starts with capital letter)
- **definition**: Clear explanation of what the term means (50-2000 characters)
- **metadata**: Including:
  - `author`: Your name
  - `version`: Start with "1.0"
  - `date_added`: Today's date in format `YYYY-MM-DDTHH:MM:SSZ`
  - `registry`: Should be "cat-mip.org"

#### Optional but Recommended

- **synonyms**: Alternative names or spellings
- **relationships**: How this term connects to others (e.g., "Agent isInstalledOn Device")
- **prompt_examples**: Sample uses of the term in natural language
- **agent_execution**: How AI agents should interpret this term

#### Example Term Structure

```json
{
  "id": "unique-id-here",
  "canonical_term": "Your Term",
  "definition": "A clear explanation of what this term means in the MSP/IT Pro context.",
  "synonyms": [
    "Alternative Name 1",
    "Alternative Name 2"
  ],
  "relationships": [
    "Your Term belongsTo Category",
    "Your Term isUsedBy Role"
  ],
  "prompt_examples": [
    "Show me all Your Terms in the system",
    "Update the Your Term configuration"
  ],
  "agent_execution": {
    "interpretation": "When this term is used, the AI agent will:",
    "actions": [
      "Identify the specific component",
      "Apply the requested action"
    ]
  },
  "metadata": {
    "author": "Your Name",
    "source_url": "",
    "version": "1.0",
    "date_added": "2025-01-16T00:00:00Z",
    "registry": "cat-mip.org",
    "term_type": ""
  }
}
```

### 2. Improving Existing Terms

You can help improve existing terms by:

- Adding missing synonyms
- Clarifying definitions
- Adding prompt examples
- Fixing typos or formatting issues
- Adding relationships to other terms

### 3. Reporting Issues

If you find problems but aren't sure how to fix them:

- Open an issue on GitHub
- Describe the problem clearly
- Suggest a solution if you have one

## Submission Process

### Step 1: Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/cat-mip.git
   cd cat-mip
   ```

### Step 2: Create a Branch

Create a descriptive branch name:
```bash
git checkout -b add-term-backup-policy
```

### Step 3: Make Your Changes

1. Edit `terms.json` to add or modify terms
2. Ensure proper JSON formatting (commas, brackets, etc.)

### Step 4: Validate Your Changes

Run the linter to check for errors:

```bash
# First time setup
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync

# Run validation
uv run python lint_catmip.py --stats
```

Fix any errors (❌) before proceeding. Warnings (⚠️) should be reviewed but aren't blocking.

### Step 5: Commit Your Changes

```bash
git add terms.json
git commit -m "Add term: Backup Policy"
```

### Step 6: Push and Create Pull Request

1. Push to your fork:
   ```bash
   git push origin add-term-backup-policy
   ```

2. Go to GitHub and create a Pull Request
3. Describe what you've added or changed
4. Wait for review and automated checks

## Guidelines

### Writing Good Definitions

- **Be clear and concise**: Avoid jargon where possible
- **Be specific to MSP/IT context**: Focus on how the term is used in our industry
- **Include examples**: Help others understand practical usage
- **Think about AI interpretation**: How would an AI agent use this term?

### Naming Conventions

- **Canonical terms**: Start with capital letter, use proper spacing
- **IDs**: Use descriptive IDs or UUIDs
- **Relationships**: Follow patterns like `Subject verb Object`

### What Makes a Good Contribution?

- ✅ Fills a gap in our vocabulary
- ✅ Improves clarity or accuracy
- ✅ Adds valuable context or examples
- ✅ Follows our format standards
- ✅ Passes linter validation

### What to Avoid

- ❌ Duplicate terms (search first!)
- ❌ Vendor-specific proprietary terms (unless widely adopted)
- ❌ Overly technical definitions without context
- ❌ Breaking changes to existing widely-used terms

## Questions?

- Check existing issues and discussions on GitHub
- Review the [Linter Documentation](LINTER.md) for validation details
- Contact the CAT-MIP team through GitHub issues

## Recognition

All contributors will be recognized in our project. Your author name in the metadata helps track contributions.

Thank you for helping build a standard vocabulary for MSP and IT Pro AI agents!