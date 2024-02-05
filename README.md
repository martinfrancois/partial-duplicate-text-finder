# partial-duplicate-text-finder

This is a simple tool to find partial duplicate text files in a folder of text files.

Note: 
- It does NOT search recursively!
- Untested on Windows
- `faster.py` is a faster version that is still work in progress and not 100 % functional

## Usage

1. Change the following lines in `finder.py` to match the folder and the similarity threshold (between 0 and 1) that is necessary for one file to be considered a partial duplicate of another file you want to use:
```python
    folder_path = "/home/user/docs"
    similarity_threshold = 0.8
```

2. Run the script:
```bash
python3 finder.py
```