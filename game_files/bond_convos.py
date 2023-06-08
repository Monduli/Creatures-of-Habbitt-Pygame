from helpers import *

def retrieve_conversation(mc_name, char1, char2, rank, rom=False):
    char1_num = char1.which_num_party_member_bonds(char1.get_name(), mc_name)
    char2_num = char2.which_num_party_member_bonds(char2.get_name(), mc_name)