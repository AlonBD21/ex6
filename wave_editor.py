import wave_helper

# EDIT wave
MIN_VAL = -32768
MAX_VAL = 32767
INPUT_CHOOSE_FILE = "What's the name of the file you wish to edit? \n"
INPUT_CHOOSE_FILE_ERR = "This file does not exist. Please try again.\n"
INPUT_ACTION_MENU = "What would you like to do?\n1. Flip\n2. Negative\n" \
                    "3. Accelerate\n4. Decelerate\n5. Increase Vol\n6." \
                    "Decrease Vol\n7.Low pass filter\n8. Finish Editing\n"
INPUT_ACTION_ERR = "Please enter a digit between 1 to 8."
MSG_SUCCESS = "Your file have been edited successfully."


def get_action_num_from_user():
    action_input = input(INPUT_ACTION_MENU)
    while not (action_input.isdigit() and 1 <= int(action_input) <= 8):
        action_input = input(INPUT_ACTION_ERR)
    return int(action_input)


def get_wave_from_user():
    file_name = input(INPUT_CHOOSE_FILE)
    wave = wave_helper.load_wave(file_name)
    while wave == -1:
        file_name = input(INPUT_CHOOSE_FILE_ERR)
        wave = wave_helper.load_wave(file_name)
    return file_name, wave


def edit_wave():
    file_name, wave = get_wave_from_user()
    action_num = get_action_num_from_user()

    sample_rate, audio_data = wave
    while action_num != 8:
        success = True
        if action_num == 1:
            audio_data = edit_1_flip(audio_data)
        elif action_num == 2:
            audio_data = edit_2_negative(audio_data)
        elif action_num == 3:
            audio_data = edit_3_accelerate(audio_data)
        elif action_num == 4:
            audio_data = edit_4_decelerate(audio_data)
        elif action_num == 5:
            audio_data = edit_5_increase_vol(audio_data)
        elif action_num == 6:
            audio_data = edit_6_decrease_vol(audio_data)
        elif action_num == 7:
            audio_data = edit_7_low_pass_filter(audio_data)
        else:
            success = False
        if success:
            print(MSG_SUCCESS)
        action_num = get_action_num_from_user()

    wave_helper.save_wave(sample_rate, audio_data, file_name)


def average_pair(pairs):
    new_pair = [0, 0]
    for i in range(1):
        sum = 0
        for pair in pairs:
            sum += pair[i]
        new_pair[i] = sum / (len(pairs))
    return new_pair


def regulate_and_round_pair(pair):
    for i in range(len(pair)):
        pair[i] = int(pair[i])
        if pair[i] < MIN_VAL:
            pair[i] = MIN_VAL
        if pair[i] > MAX_VAL:
            pair[i] = MAX_VAL


def edit_1_flip(audio_data):
    return audio_data[::-1]


def edit_2_negative(audio_data):
    for pair in audio_data:
        for i in range(len(pair)):
            pair[i] = -pair[i]
        regulate_and_round_pair(pair)
    return audio_data


def edit_3_accelerate(audio_data):
    return audio_data[0::2]


def edit_4_decelerate(audio_data):
    for i in range(len(audio_data) - 1, 0, -1):
        audio_data.insert(i, average_pair(audio_data[i - 1:i + 1]))
    return audio_data


def edit_5_increase_vol(audio_data):
    for pair in audio_data:
        for i in range(len(pair)):
            pair[i] = 1.2 * pair[i]
        regulate_and_round_pair(pair)
    return audio_data


def edit_6_decrease_vol(audio_data):
    for pair in audio_data:
        for i in range(len(pair)):
            pair[i] = pair[i] / 1.2
        regulate_and_round_pair(pair)
    return audio_data


def edit_7_low_pass_filter(audio_data):
    audio_data[0] = average_pair(audio_data[:2])  # First pair
    audio_data[-1] = average_pair(audio_data[-2:])  # Last pair
    for i in range(1, len(audio_data) - 1):  # Rest of the pairs
        audio_data[i] = average_pair(audio_data[i - 1:i + 2])
    return audio_data