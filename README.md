Basic Setup
- Create a venv such as `py312-env` and activate it
- `pip install poetry`
- `poetry install`
- `brew install --cask iterm2`
- Open Iterm2 settings. In General -> Magic, turn on "Enable Python API" ([docs](https://iterm2.com/python-api-auth.html)
- Run a script, e.g. `python simulate.py --filename examples/http.md`.

Common ones
"Ctrl+U": '\x15', # Kill (cut) text from the cursor to the beginning of the line
"Ctrl+L": '\x0c', # Clear the screen
