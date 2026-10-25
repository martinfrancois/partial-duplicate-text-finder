# partial-duplicate-text-finder

This is a simple tool to find partial duplicate text files in a folder of text files.

Note:
- It does NOT search recursively! Subfolders are skipped.
- Untested on Windows

## Usage

Run the script with the folder and, optionally, the similarity threshold (between 0 and 1) that is necessary for one file to be considered a partial duplicate of another file:
```bash
python3 finder.py /home/user/docs --threshold 0.9
```

`python3 finder.py --help` lists the options and the default threshold. Requires Python 3.10 or newer.

`faster.py` is a faster version that is still work in progress and not 100 % functional.

## Example

`examples/` holds four invented text files: a notice, an exact copy of it, a revised version of it and an unrelated recipe.
```bash
python3 finder.py examples
```
prints:
```
File 0 garden-notice-copy.txt
File 1 garden-notice-revised.txt
File 2 garden-notice.txt
File 3 soup-recipe.txt
Partial duplicate files found:
garden-notice-copy.txt partial duplicates: ['garden-notice-revised.txt', 'garden-notice.txt']
garden-notice-revised.txt partial duplicates: ['garden-notice.txt']
```

## Tests

```bash
python3 -m pip install -r requirements.txt
python3 -m pytest
```

## License

MIT, see `LICENSE`.
