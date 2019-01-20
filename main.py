#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pycuber as pc
import string


# In[ ]:


SCRAMBLE = "D'  L'  R'  U  D  B2  U'  D2  B2  L'  F'  L'  D'  R  F2  B2  L2  D  F  D  B  R'  U2  B  L2"
mycube = pc.Cube()
mycube(SCRAMBLE)


# In[ ]:


ALPHABETX = string.ascii_uppercase[:24]

COLOR2FACE = {
    "red": 'B',
    "yellow": 'U',
    "green": 'L',
    "white": 'D',
    "orange" : 'F',
    "blue": 'R'
}


# In[ ]:


# piece: in notation of alphabet
# piece_ff : in notation of RU, FR, BD, etc
# seq: actual position of the piece in the slot


# In[ ]:


EDGE_FF = 'UBURUFULFUFRFDFLRURBRDRFBUBLBDBRLULFLDLBDFDRDBDL'
EDGE_FF = [EDGE_FF[i:i+2] for i in range(0, len(EDGE_FF), 2)]
EDGE_FF_SET = set(frozenset(list(i)) for i in EDGE_FF)

EDGE_MAP = {i[0]:i[1] for i in zip(ALPHABETX, EDGE_FF)}

edge_ff_solved = set([frozenset(list('RU'))])
e_available_slots_ff = EDGE_FF_SET - edge_ff_solved

def e_slot2seq(slot):
    slot_ff = EDGE_MAP[slot]
    piece_cc = mycube.__getitem__(slot_ff)
    piece_ff = COLOR2FACE[piece_cc[slot_ff[0]].colour] + COLOR2FACE[piece_cc[slot_ff[1]].colour]
    _slot_ff = piece_ff
    seq = ALPHABETX[EDGE_FF.index(_slot_ff)]
    return seq

def e_getEmptySlot():
    asff = next(iter(e_available_slots_ff))
    tmp = ''.join(asff)
    return ALPHABETX[EDGE_FF.index(tmp)]


# In[ ]:


def get_e_sequence(input_seq='B'):
    sequence = ''
    while len(e_available_slots_ff) > 0:
        seq = e_slot2seq(input_seq)
        if seq in ['B', 'I']:
            sequence += '-'
            seq = e_getEmptySlot() #find next slot
        elif frozenset(list(EDGE_MAP[seq])) not in e_available_slots_ff:
            seq = e_getEmptySlot()
            e_available_slots_ff.remove(frozenset(list(EDGE_MAP[seq])))
        elif seq == input_seq:
            e_available_slots_ff.remove(frozenset(list(EDGE_MAP[seq])))
            seq = e_getEmptySlot()
        else:
            e_available_slots_ff.remove(frozenset(list(EDGE_MAP[seq])))
        sequence += seq
        input_seq = seq
            
    return sequence


# In[ ]:


CORNER_FF = 'UBLUBRUFRUFLFLUFRUFDRFDLRFURBURBDRDFBRUBLUBDLBDRLBULFULDFLBDDFLDFRDBRDBL'
CORNER_FF = [CORNER_FF[i:i+3] for i in range(0, len(CORNER_FF), 3)]
CORNER_FF_SET = set(frozenset(i) for i in CORNER_FF)

CORNER_MAP = {i[0]:i[1] for i in zip(ALPHABETX, CORNER_FF)}

corner_ff_solved = set([frozenset(list('LUB'))])
c_available_slots_ff = CORNER_FF_SET - corner_ff_solved

def c_slot2seq(slot):
    slot_ff = CORNER_MAP[slot]
    piece_cc = mycube.__getitem__(slot_ff)
    piece_ff = ''.join(sorted(COLOR2FACE[piece_cc[slot_ff[0]].colour] + COLOR2FACE[piece_cc[slot_ff[1]].colour] + COLOR2FACE[piece_cc[slot_ff[2]].colour]))
    _slot_ff = piece_ff
    seq = ALPHABETX[CORNER_FF.index(_slot_ff)]
    return seq

def c_getEmptySlot():
    asff = next(iter(c_available_slots_ff))
    tmp = ''.join(sorted(asff))
    return ALPHABETX[CORNER_FF.index(tmp)]


# In[ ]:


def get_c_sequence(input_seq='A'):
    sequence = ''
    while len(c_available_slots_ff) > 0:
        seq = c_slot2seq(input_seq)
        if seq in ['A', 'N', 'Q']:
            sequence += '-'
            seq = c_getEmptySlot() #find next slot
        elif frozenset(list(CORNER_MAP[seq])) not in c_available_slots_ff:
            seq = c_getEmptySlot()
            c_available_slots_ff.remove(frozenset(list(CORNER_MAP[seq])))
        elif seq == input_seq:
            c_available_slots_ff.remove(frozenset(list(CORNER_MAP[seq])))
            seq = c_getEmptySlot()
        else:
            c_available_slots_ff.remove(frozenset(list(CORNER_MAP[seq])))
        sequence += seq
        input_seq = seq
    
    return sequence


# In[ ]:


c_sequence = get_c_sequence()
e_sequence = get_e_sequence()

