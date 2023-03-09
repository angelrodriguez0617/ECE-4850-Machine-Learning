import numpy as np
import re
import copy
import random

# this function takes the path to a text file and converts it into an array we can use for our work
def convert_text_to_array(path):
    # open the file at the path and read it into a string
    with open(path) as file:
        content = file.read()
    # convert everything but alpha characters and whitespace to whitespace
    text = re.sub('[^a-zA-Z \n]', '', content)
    # convert newline to space
    text = re.sub('\n', ' ', text)
    # remove repeated/extra spaces
    text = re.sub(' +', ' ', text)
    # convert everything to lowercase
    text = text.lower()
    # turn a string into a character array
    text = [char for char in text]
    # turn our character array into a numpy array
    text = np.array(text)
    return text

# calculates the log likelyhood the text occurs in the order it does based off of the supplied probability array
def calculate_likelyhood(text, prob_array):
    likelyhood = 0.0
    # intitial value is 0 (or ' ')
    old_char_iterator = 0
    # read each character from the text
    for i in text:
        # get the "integer equivalent" (probably convert from ascii) of the character and adjust for our scheme
        char_iterator = ord(i)
        if char_iterator == 32:
            char_iterator = 0
        else:
            char_iterator = char_iterator - 96
        # the algorighm calls for us to take the all of the sequential likelyhoods
        # this number becomes very small and we are unable to work with it
        # luckily we can just convert to log and make it much easier to work with
        # (summing logs is multiplying what is inside)
        likelyhood += np.log(prob_array[old_char_iterator, char_iterator])
        # sets up for the next character
        old_char_iterator = char_iterator
    return likelyhood

# swaps two random letters in our key
def swap_char(key):
    our_key = copy.copy(key)
    position = random.randrange(our_key.size)
    new_position = random.randrange(our_key.size)
    # this makes sure we don't try to swap a letter with itself
    while position == new_position:
        new_position = random.randrange(our_key.size)
    # actual swapping
    our_key[position], our_key[new_position] = our_key[new_position], our_key[position]
    # we also return which letters we swap to make things a little easier down the road
    return our_key, (our_key[new_position], our_key[position])

# finds the conditional probability array (probabilty a certain character is followed by another) of a text
def find_probability_array(text):
    # start with ones to avoid cases that we don't see in the text (maybe x really does follow q in our text, just very unlikely)
    unknown_prob_array = np.ones([27, 27])
    # the mapping of char to integer is "' ', a, b, c, ..., z" to "0, 1, 2, 3, ..., 26"

    # stores the old integer representation of a character
    # intitial value is 0 (or ' ')
    old_char_iterator = 0
    # read each character from the text
    for i in text:
        # get the "integer equivalent" (probably convert from ascii) of the character and adjust for our scheme
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

# full fat translation of a text via decryption keys!
def translate_text(text, key):
    # 'default' order of the alphabet
    original_index = np.array([' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])

    # cycle through each line in the text and swap it out
    for i in range(text.size):
        text[i] = key[list(original_index).index(text[i])]
    return text

# a sneaky function that just swaps two letters in a text so we don't have to do a full translation
def swap_text(text, swapped_chars):
    # unwrap the characters we want to swap
    x1, x2 = swapped_chars
    # convert the array to a string
    text = ''.join(text)
    # use regex to convert all instances of a character to a temp character ('\n' should not appear in our text, we already removed it)
    text = re.sub(x1, '\n', text)
    # actual swapping
    text = re.sub(x2, x1, text)
    text = re.sub('\n', x2, text)
    # convert string back to array
    text = [char for char in text]
    return text