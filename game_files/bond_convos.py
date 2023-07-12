########
# Holds bond conversation related functions.
# Created with the intention of separating from helpers.
########

from helpers import *

def retrieve_conversation(mc_name, char1, char2, rank, rom=False):
    """
    The function retrieves a conversation between two characters in a game, based on their names, the
    main character's name, their rank, and whether they are in a romantic relationship.
    
    :param mc_name: The name of the main character
    :param char1: The parameter `char1` represents the first character in the conversation
    :param char2: The parameter `char2` represents the second character in the conversation
    :param rank: The "rank" parameter is used to specify the rank or level of the conversation between
    the two characters. It could be an integer value representing the rank of the conversation
    :param rom: The `rom` parameter is a boolean value that indicates whether the conversation is taking
    place in a romantic context. If `rom` is `True`, it means the conversation is romantic in nature. If
    `rom` is `False` or not provided, it means the conversation is not romantic, defaults to False
    (optional)
    """
    char1_num = char1.which_num_party_member_bonds(char1.get_name(), mc_name)
    char2_num = char2.which_num_party_member_bonds(char2.get_name(), mc_name)