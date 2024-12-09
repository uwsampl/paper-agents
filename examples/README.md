# Paper Agents Usage

## Before Usage

Ensure that the `OPENAI_API_KEY` environment variable is set before using the tool.

## Configuration

Refer to the [config.json](config.json) file for configuration details.

## Commands

### Apply Changes

```bash
python -m paper_agent --role ROLE --apply --output_dir tmp/ --config config.json
```

This command performs actions on the LaTeX code, generating modified `.tex` files in the specified `output_dir`. It also creates patch files in the current directory, which can be applied later using `patch ***.tex < ***.text.patch`. When the `--apply` flag is specified, these patches are applied directly to the source `.tex` file.

### Undo Changes

```bash
python -m paper_agent --undo
```

This command reverts the changes made to the source `.tex` file.

## Polish Paper Writing

```bash
python -m paper_agent --role polish --apply
```

Use this command to polish the paper writing.

## Generate Pseudo Reviews

```bash
python -m paper_agent --role review
```

This command generates pseudo reviews for the paper.

## Revise Paper According to Reviews

```bash
python -m paper_agent --role revise
```

Use this command to revise the paper based on the reviews.

## Sanity Check (Format and References)

```bash
python -m paper_agent --role sanitizer
```

This command performs a sanity check for format and references.
