# partial-duplicate-text-finder

Find text files in a folder that are partial duplicates of each other.

## What it does

The tool reads every file in one folder and compares each pair with
`difflib.SequenceMatcher`. A pair whose similarity ratio is at or above the
threshold is reported as a partial duplicate. The ratio is 1.0 for identical
text and 0.0 for text with nothing in common.

Subfolders are not searched.

## Requirements

Python 3.10 or newer. The tool itself uses only the standard library.
`pytest` is needed for the tests.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt -e .
```

This adds the `partial-duplicate-text-finder` command to the virtualenv.
Without installing, `python3 finder.py` takes the same arguments.

## Usage

```bash
partial-duplicate-text-finder /path/to/folder --threshold 0.8
```

`--threshold` is the similarity ratio between 0 and 1 at or above which two
files count as partial duplicates. The default is 0.8.

## Example

`examples/` holds four invented text files: a notice, an exact copy of it, a
revised version with a few changed dates and one added sentence, and an
unrelated recipe.

```bash
partial-duplicate-text-finder examples
```

Output:

```
File 0 garden-notice-copy.txt
File 1 garden-notice-revised.txt
File 2 garden-notice.txt
File 3 soup-recipe.txt
Partial duplicate files found:
garden-notice-copy.txt partial duplicates: ['garden-notice-revised.txt', 'garden-notice.txt']
garden-notice-revised.txt partial duplicates: ['garden-notice.txt']
```

The notice and its revision have a ratio of 0.92, the copy scores 1.0, and the
recipe scores 0.04 against each of them. With `--threshold 0.99` only the exact
copy is reported.

Run the tests with `python -m pytest`.

## Limitations

- Every pair of files is compared in full, so the run time grows with the
  square of the file count and with file length. Large folders are slow.
- Files are read as UTF-8 and undecodable bytes are dropped, so binary files
  are compared as well and produce meaningless ratios.
- A subfolder inside the folder makes the run fail, because the tool tries
  to open it as a file.
- Untested on Windows.

## License

MIT, see `LICENSE`.
