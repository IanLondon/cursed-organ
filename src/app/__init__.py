from machine import Pin, PWM
import machine
import sys
import umidiparser
import utime


def run():
    with open("data/example.txt") as f:
        data = f.read()

    print("example data: {}".format(data))

    board = sys.implementation._machine.split(" with")[0]
    print(f"Running on {board} ({sys.platform}) at {machine.freq() / 1000000} MHz")

    play_midi("data/C4-scale.mid")

    sawtooth_pwm_demo()


def play_midi(filename: str):
    for event in umidiparser.MidiFile(filename).play():
        # .play will sleep, avoiding time drift, before returning the event on time
        # Process the event according to type
        if event.status == umidiparser.NOTE_ON:
            print(event.note, event.channel, event.velocity)
        elif event.status == umidiparser.NOTE_OFF:
            print("stop", event.note)
        elif event.status == umidiparser.PROGRAM_CHANGE:
            print("change channel", event.program, event.channel)
        else:
            # Show all events not processed
            print("other event", event)


def sawtooth_pwm_demo(pin: Pin = Pin(25), cycle_time_ms=1000):
    # 60 Hz for human eye POV
    pwm0 = PWM(pin, freq=60)

    # duty_u16 is 16 bits, break that up into 256 steps:
    STEPS = 256
    for i in range(0, 2**16, 2**16 // (STEPS - 1)):
        pwm0.duty_u16(i)
        utime.sleep_ms(cycle_time_ms // STEPS)


if __name__ == "__main__":
    print("running app.py file directly")
    run()
