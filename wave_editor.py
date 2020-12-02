import math
import wave_helper as helper

sample_rate = 2000
MAX_VOLUME = 32767

def make_song():
    """this function return a wav file of a song using a given composition"""
    filename = input("please enter your composition file")
    file = open(filename)
    composition = file.read()
    file.close()

    #taking the frequencies from the composition
    tmp = composition
    frequencies = []
    while not tmp == "":
        if tmp[0].isalpha():
            frequencies.append(tmp[0])
        tmp = tmp[1:]

    # taking the durations from the composition
    durations = []
    while not composition == "":
        num = ""
        while composition[0].isnumeric():
            num += composition[0]
            composition = composition[1:]
            if composition == "":
                break
        if not num == "":
            durations.append(int(num))
        composition = composition[1:]

    samples = []

    for n in range(len(frequencies)):
        samples_per_cycle = sample_rate / get_frequency_value(frequencies[n])
        for i in range(durations[n] * 125):
            value = MAX_VOLUME * math.sin(math.pi*2*(i/samples_per_cycle))
            samples.append([int(value), int(value)])

    return samples

def get_frequency_value(f):
    if f == 'A':
        return 440
    if f == 'B':
        return 494
    if f == 'C':
        return 523
    if f == 'D':
        return 587
    if f == 'E':
        return 659
    if f == 'F':
        return 698
    if f == 'G':
        return 784

helper.save_wave(sample_rate, make_song(), "check.wav")