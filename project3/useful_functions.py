import numpy as np
import re
import copy
import random

def convert_text_to_array(path):
    # open the file at the path and read it into a string
    with open(path) as file:
        content = file.read()
    # pull out only the alpha char and whitespace
    text = re.sub('[^a-zA-Z \n]', '', content)
    # convert newline to space
    text = re.sub('\n', ' ', text)
    # remove repeated spaces
    text = re.sub(' +', ' ', text)
    # convert everything to lowercase
    text = text.lower()
    # turn a string into a character array
    text = [char for char in text]
    # turn our character array into a numpy array
    text = np.array(text)

    return text

def calculate_difference(x1, x2):
    return np.sum(np.abs(np.subtract(x1, x2)))

def calculate_likelyhood(text, prob_array):
    likelyhood = 0.0
    # intitial value is 0 (or ' ')
    old_char_iterator = 0
    # read each character from the text
    for i in text:
        # get the "integer equivalent" (probably ascii) of the character and adjust for our scheme
        char_iterator = ord(i)
        if char_iterator == 32:
            char_iterator = 0
        else:
            char_iterator = char_iterator - 96
        likelyhood += np.log(prob_array[old_char_iterator, char_iterator])
        old_char_iterator = char_iterator
    return likelyhood

def swap_char(key):
    our_key = copy.copy(key)
    position = random.randrange(our_key.size)
    new_position = random.randrange(our_key.size)
    while position == new_position:
        new_position = random.randrange(our_key.size)
    #swap_direction = random.choice([-1, 1])
    #new_position = position + swap_direction
    #if new_position < 0:
    #    new_position = our_key.size - 1
    #elif new_position >= our_key.size:
    #    new_position = 0
    our_key[position], our_key[new_position] = our_key[new_position], our_key[position]
    return our_key, (our_key[new_position], our_key[position])

def find_probability_array(text):
    unknown_prob_array = np.ones([27, 27])
    # the mapping of char to integer is "' ', a, b, c, ..., z" to "0, 1, 2, 3, ..., 26"

    # stores the old integer representation of a character
    # intitial value is 0 (or ' ')
    old_char_iterator = 0
    # read each character from the text
    for i in text:
        # get the "integer equivalent" (probably ascii) of the character and adjust for our scheme
        char_iterator = ord(i)
        if char_iterator == 32:
            char_iterator = 0
        else:
            char_iterator = char_iterator - 96
        # increment the probability array for each character
        unknown_prob_array[old_char_iterator, char_iterator] += 1
        # assign the old character iterator to repeat the cycle
        old_char_iterator = char_iterator
    # normalize the array
    normalizing_array = np.sum(unknown_prob_array, axis=1)
    for i in range(27):
        unknown_prob_array[i, :] /= normalizing_array[i]

    return unknown_prob_array

def translate_text(text, key):
    original_index = np.array([' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])

    for i in range(text.size):
        text[i] = key[list(original_index).index(text[i])]

    return text

def other_translate_text(text, key):
    original_index = np.array([' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])

    for i in range(text.size):
        text[i] = original_index[list(key).index(text[i])]

    return text

def swap_text(text, swapped_chars):
    x1, x2 = swapped_chars
    text = ''.join(text)
    text = re.sub(x1, '\n', text)
    text = re.sub(x2, x1, text)
    text = re.sub('\n', x2, text)
    text = [char for char in text]

    return text