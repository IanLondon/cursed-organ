# Cursed Organ

This is a project to use digital sheet music to drive a bottle organ, which is an instrument like a pipe organ that uses glass bottles instead of pipes.

Through a Micropython script, a MIDI file is used to drive servo motors that control valves to each bottle. Each note corresponds to one valve.

# Setup

- Install `pipx` ([link](https://pipx.pypa.io/stable/installation/))
- Install `mpremote` via `pipx install mpremote`

- Connect to a Pi Pico board, download the `uf2` from https://www.raspberrypi.com/documentation/microcontrollers/micropython.html and drag and drop the file to the board.
- Check that everything is working by running `mpremote` to get a REPL to the board and do `from machine import Pin; led = Pin(25, Pin.OUT)` Then doing `led.toggle()` in the REPL should toggle the onboard LED on pin 25.

## Dependencies

Currently manually installed directly to your Pico board with `mprimote mip`. Do:

- `mpremote mip install github:bixb922/umidiparser`

## Linting

I don't have a real lint setup for this project. I'm just using the [Ruff VSCode extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)

Do `poetry install` to get micropython stubs and other dependencies. This is only useful locally for linting.

## Simulation Setup

I sometimes use Wokwi simulator to test the Micropython code.

- Install Wokwi VSCode extension (and get a license set up following their instructions)
- Make sure VSCode is pointing to the right virtualenv (for linting)

With the simulator running and the "Wokwi Simulator" tab open in VSCode, open a terminal into this repo's root. `cd src/` and then `mpremote connect port:rfc2217://localhost:4000 cp -r . : + run main.py` (it seems that Wokwi doesn't support `mount`?? TODO.)

## Iterating on the board

To copy local files to the board and run in one command:

`mpremote fs cp -r src : + exec 'import os; os.chdir("src"); import app; app.run()'`

### Problem with `mount`

TODO. Seems like `mount` doesn't give a full file API, and `umidiparser` is incompatible with it??

```
File "/lib/umidiparser/umidiparser.py", line 958, in __init__
AttributeError: 'RemoteFile' object has no attribute 'tell'
```

- https://github.com/micropython/micropython/issues/14218
- https://github.com/bixb922/umidiparser/issues/6

### Nice to have

`mpremote mount src repl --inject-code "import app; app.run()\n"` then `Ctrl+J` to run. When you make changes, do `CTRL+C+D+J`...

- `Ctrl+C` to exit the run loop (if you're in one)
- `Ctrl+D` to reset the interpreter state
- `Ctrl+J` to do `import app; app.run()` again.

Finally, `Ctrl+X` (maybe preceded by `Ctrl+C` in a run loop) to exit.

(OR similarly: just `mpremote mount src exec "import app; app.run()"` then to exit do `Ctrl+C` twice.)

# Reference Quick Links

Pinout and MicroPython API: https://docs.micropython.org/en/latest/rp2/quickref.html

`mpremote` tool: https://docs.micropython.org/en/latest/reference/mpremote.html

# MIDI

https://onlinesequencer.net/ is great because you don't have to install it. Create your notes and click the cloud download icon and do "Export MIDI". Save in `data/`
