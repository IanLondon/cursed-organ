from machine import Pin, PWM, I2C
import machine
from micropython import const
from micropython_pca9685 import PCA9685
from micropython_pca9685 import Servo
import sys
import umidiparser
import utime


def get_mapping() -> list[int]:
    return [
        47,  # B3
        48,  # C4
        # 49,  # C#/Db4
        50,  #  D4
        # 51,  # D#/Eb4
        52,  # E4
        53,  # F4
        # 54,  # F#/Gb4
        55,  # G4
        # 56,  # G#/Ab4
        57,  # A4
        # 58,  # A#/Bb4
        59,  # B4
        60,  # C5
        # 61,  # C#/Db5
        62,  # D5
        # 63,  # D#/Eb5
        # 64,  # E5
    ]


def note_to_stepper_index(note: int) -> int | None:
    # NOTE: this is as defined by onlinesequencer.net which oddly defines C5 as 60,
    # though MIDI 60 is supposed to be "middle C" which is usually C4 (maybe C3) but C5 is odd.
    mapping = get_mapping()
    return mapping.index(note) if note in mapping else None


def _open_close_valve(note: int, servos: list[Servo], is_open: bool) -> None:
    stepper_index = note_to_stepper_index(note)
    print("{} valve".format("Open" if is_open else "Close"), note, stepper_index)
    if stepper_index is None:
        print("WARNING: no stepper index for note '{0}'".format(note))
        return
    if len(servos) <= stepper_index:
        print("WARNING: only {} servos, index out of range".format(len(servos)))
        return

    servo = servos[stepper_index]
    servo.fraction = 1.0 if is_open else 0.0


def close_valve(note: int, servos: list[Servo]) -> None:
    _open_close_valve(note, servos, is_open=False)


def open_valve(note: int, servos: list[Servo]) -> None:
    _open_close_valve(note, servos, is_open=True)


def play_midi(filename: str, servos: list[Servo]):
    for event in umidiparser.MidiFile(filename).play():
        # .play will sleep, avoiding time drift, before returning the event on time
        # Process the event according to type
        if event.status == umidiparser.NOTE_ON:
            # print(event.note, event.channel, event.velocity)
            open_valve(event.note, servos)
        elif event.status == umidiparser.NOTE_OFF:
            # print("stop", event.note)
            close_valve(event.note, servos)
        elif event.status == umidiparser.PROGRAM_CHANGE:
            print("change channel", event.program, event.channel)
        else:
            # Show all events not processed
            print("other event", event)


def reset_servos(servos: list[Servo], value: float = 0.0):
    print("reset servos to: {}".format(value))
    for servo in servos:
        servo.fraction = value


def sawtooth_pwm_demo(pin: Pin = Pin(25), cycle_time_ms=1000):
    # 60 Hz for human eye POV
    pwm0 = PWM(pin, freq=60)

    # duty_u16 is 16 bits, break that up into 256 steps:
    STEPS = 256
    for i in range(0, 2**16, 2**16 // (STEPS - 1)):
        pwm0.duty_u16(i)
        utime.sleep_ms(cycle_time_ms // STEPS)


def run():
    board = sys.implementation._machine
    print(f"Running on {board} ({sys.platform}) at {machine.freq() / 1000000} MHz")

    num_servos = len(get_mapping())

    i2c = I2C(1, scl=Pin(3), sda=Pin(2))
    print("I2C Scan:")
    print(i2c.scan())
    print("=========")

    pca = PCA9685(i2c, address=0x40)
    pca.frequency = 50
    servos = [Servo(pca.channels[i]) for i in range(num_servos)]

    reset_servos(servos)

    # TODO: this is slow, the servos reset semi-sequentially in ~500ms-1000ms in a sloppy way.
    # Does the driver expose the PCA9685's "set all PWM to one value" command?
    # Or is this a power supply issue?
    # utime.sleep(10)
    # reset_servos(servos, 1.0)
    # utime.sleep(10)
    # reset_servos(servos)

    play_midi("data/C4-scale.mid", servos)

    reset_servos(servos)

    pca.deinit()

    # sawtooth_pwm_demo()


if __name__ == "__main__":
    print("running app.py file directly")
    run()
