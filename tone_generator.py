import pygame
import pygame.sndarray
import numpy


def play_for(sample_wave):
    global sound
    sound = pygame.sndarray.make_sound(sample_wave)
    sound.play(-1)


sample_rate = 44100
pygame.mixer.pre_init(sample_rate, -16, 1)
pygame.init()


def sine_wave(hz, peak, n_samples=sample_rate):
    """Compute N samples of a sine wave with given frequency and peak amplitude.
       Defaults to one second.
    """
    length = sample_rate / float(hz)
    omega = numpy.pi * 2 / length
    x_values = numpy.arange(int(length)) * omega
    one_cycle = peak * numpy.sin(x_values)
    return numpy.resize(one_cycle, (n_samples,)).astype(numpy.int16)


sound = pygame.sndarray.make_sound(sine_wave(1, 1))


def stop_tone():
    global sound
    sound.stop()


def play_digit(digit):
    if digit is 1:
        play_for(sum([sine_wave(697, 4096), sine_wave(1209, 4096)]))
    elif digit is 2:
        play_for(sum([sine_wave(697, 4096), sine_wave(1336, 4096)]))
    elif digit is 3:
        play_for(sum([sine_wave(697, 4096), sine_wave(1477, 4096)]))
    elif digit is 4:
        play_for(sum([sine_wave(770, 4096), sine_wave(1209, 4096)]))
    elif digit is 5:
        play_for(sum([sine_wave(770, 4096), sine_wave(1336, 4096)]))
    elif digit is 6:
        play_for(sum([sine_wave(770, 4096), sine_wave(1477, 4096)]))
    elif digit is 7:
        play_for(sum([sine_wave(852, 4096), sine_wave(1209, 4096)]))
    elif digit is 8:
        play_for(sum([sine_wave(852, 4096), sine_wave(1336, 4096)]))
    elif digit is 9:
        play_for(sum([sine_wave(852, 4096), sine_wave(1477, 4096)]))
    elif digit is 0:
        play_for(sum([sine_wave(941, 4096), sine_wave(1336, 4096)]))
    elif digit is "*":
        play_for(sum([sine_wave(941, 4096), sine_wave(1209, 4096)]))
    elif digit is "#":
        play_for(sum([sine_wave(941, 4096), sine_wave(1477, 4096)]))


def play_dial_tone():
    play_for(sum([sine_wave(350, 4096), sine_wave(440, 4096)]))
