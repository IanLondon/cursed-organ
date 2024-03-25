# Setup

- Install `pipx` ([link](https://pipx.pypa.io/stable/installation/))
- Install `mpremote` via `pipx install mpremote`

## Development Setup

- Install Wokwi VSCode extension (and get a license set up following their instructions)
- `poetry install` to get micropython stubs for linting
- Make sure VSCode is pointing to the right virtualenv (for linting)

With the simulator running and the "Wokwi Simulator" tab open in VSCode, open a terminal into this repo's root. `cd src/` and then `mpremote connect port:rfc2217://localhost:4000 cp -r . : + run main.py`
