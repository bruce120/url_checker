# URL Checker

URL Checker is a simple Python tool to verify the availability of URLs listed in a given file.

## Installation

Ensure you have Python and pip installed. Next, install the required dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python url_checker.py -f [path_to_file]
```

Example:

```bash
python url_checker.py -f urls.txt
```

Upon completion, live URLs will be written to live.txt.

## Notes

This tool employs multiprocessing for URL checks, with the number of processes based on your CPU's core count.
If there's an exception during the checking process or if manually interrupted, the tool will attempt to terminate all processes and exit safely.

