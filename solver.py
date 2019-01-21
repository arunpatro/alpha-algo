import pycuber as pc
import string

class Solver():
    def __init__(self):
        self.cube = pc.Cube()
        self.ALPHABETX = string.ascii_uppercase[:24]

        self.COLOR2FACE = {
            "red": 'B',
            "yellow": 'U',
            "green": 'L',
            "white": 'D',
            "orange" : 'F',
            "blue": 'R'
        }

        __EDGE_FF__ = 'UBURUFULFUFRFDFLRURBRDRFBUBLBDBRLULFLDLBDFDRDBDL'
        self.EDGE_FF = [__EDGE_FF__[i:i+2] for i in range(0, len(__EDGE_FF__), 2)]
        self.EDGE_FF_SET = set(frozenset(list(i)) for i in self.EDGE_FF)

        self.EDGE_MAP = {i[0]:i[1] for i in zip(self.ALPHABETX, self.EDGE_FF)}

        __e_ff_solved__ = set([frozenset(list('RU'))])
        self.e_available_slots_ff = self.EDGE_FF_SET - __e_ff_solved__

        __CORNER_FF__ = 'UBLUBRUFRUFLFLUFRUFDRFDLRFURBURBDRDFBRUBLUBDLBDRLBULFULDFLBDDFLDFRDBRDBL'
        self.CORNER_FF = [__CORNER_FF__[i:i+3] for i in range(0, len(__CORNER_FF__), 3)]
        self.CORNER_FF_SET = set(frozenset(i) for i in self.CORNER_FF)

        self.CORNER_MAP = {i[0]:i[1] for i in zip(self.ALPHABETX, self.CORNER_FF)}

        __c_ff_solved__ = set([frozenset(list('LUB'))])
        self.c_available_slots_ff = self.CORNER_FF_SET - __c_ff_solved__

    def scramble(self, algo):
        self.cube(algo)

    def e_slot2seq(self, slot):
        slot_ff = self.EDGE_MAP[slot]
        piece_cc = self.cube.__getitem__(slot_ff)
        piece_ff = self.COLOR2FACE[piece_cc[slot_ff[0]].colour] + self.COLOR2FACE[piece_cc[slot_ff[1]].colour]
        _slot_ff = piece_ff
        seq = self.ALPHABETX[self.EDGE_FF.index(_slot_ff)]
        return seq

    def e_getEmptySlot(self):
        asff = next(iter(self.e_available_slots_ff))
        tmp = ''.join(asff)
        return self.ALPHABETX[self.EDGE_FF.index(tmp)]

    def get_e_sequence(self, input_seq='B'):
        sequence = ''
        while len(self.e_available_slots_ff) > 0:
            seq = self.e_slot2seq(input_seq)
            if seq in ['B', 'I']:
                sequence += '-'
                seq = self.e_getEmptySlot() #find next slot
            elif frozenset(list(self.EDGE_MAP[seq])) not in self.e_available_slots_ff:
                seq = self.e_getEmptySlot()
                self.e_available_slots_ff.remove(frozenset(list(self.EDGE_MAP[seq])))
            elif seq == input_seq:
                self.e_available_slots_ff.remove(frozenset(list(self.EDGE_MAP[seq])))
                seq = self.e_getEmptySlot()
            else:
                self.e_available_slots_ff.remove(frozenset(list(self.EDGE_MAP[seq])))
            sequence += seq
            input_seq = seq
                
        return sequence
    
    def c_slot2seq(self, slot):
        slot_ff = self.CORNER_MAP[slot]
        piece_cc = self.cube.__getitem__(slot_ff)
        piece_ff = ''.join(sorted(self.COLOR2FACE[piece_cc[slot_ff[0]].colour] + self.COLOR2FACE[piece_cc[slot_ff[1]].colour] + self.COLOR2FACE[piece_cc[slot_ff[2]].colour]))
        _slot_ff = piece_ff
        seq = self.ALPHABETX[self.CORNER_FF.index(_slot_ff)]
        return seq

    def c_getEmptySlot(self):
        asff = next(iter(self.c_available_slots_ff))
        tmp = ''.join(sorted(asff))
        return self.ALPHABETX[self.CORNER_FF.index(tmp)]

    def get_c_sequence(self, input_seq='A'):
        sequence = ''
        while len(self.c_available_slots_ff) > 0:
            seq = self.c_slot2seq(input_seq)
            if seq in ['A', 'N', 'Q']:
                sequence += '-'
                seq = self.c_getEmptySlot() #find next slot
            elif frozenset(list(self.CORNER_MAP[seq])) not in self.c_available_slots_ff:
                seq = self.c_getEmptySlot()
                self.c_available_slots_ff.remove(frozenset(list(self.CORNER_MAP[seq])))
            elif seq == input_seq:
                self.c_available_slots_ff.remove(frozenset(list(self.CORNER_MAP[seq])))
                seq = self.c_getEmptySlot()
            else:
                self.c_available_slots_ff.remove(frozenset(list(self.CORNER_MAP[seq])))
            sequence += seq
            input_seq = seq
        
        return sequence

    def get_parity():
        e_sequence = self.get_e_sequence()

if __name__ == '__main__':
    SCRAMBLE = "D'  L'  R'  U  D  B2  U'  D2  B2  L'  F'  L'  D'  R  F2  B2  L2  D  F  D  B  R'  U2  B  L2"
    solver = Solver()
    solver.scramble(SCRAMBLE)
    e, c = solver.get_e_sequence(), solver.get_c_sequence()
    print('SCRAMBLE', SCRAMBLE)
    print('EDGE SEQ:', e)
    print('CORNER SEQ:', c)
