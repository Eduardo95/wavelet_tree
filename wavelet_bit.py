"""
Author: Feng Dai
This version is totally implemented by myself.
"""
import math


class WaveletTreeB(object):
    def __init__(self, data, alphabet):
        self.data = data
        self.alphabet = alphabet
        self.root_node = WaveletTreeBNode()
        self.root_node.create_tree(self.data, self.alphabet, 0)

    def depth_first_print(self):
        self.root_node.print_node()

    def rank(self, position, character):
        return self.root_node.rank(position, self.alphabet.char2string(character))

    def access(self, position):
        return self.alphabet.string2char(self.root_node.access(position))

    def select(self, frequency, character):
        return self.root_node.select(frequency, self.alphabet.char2string(character)) - 1


class WaveletTreeBNode(object):
    def __init__(self):
        self.bit_vector = []
        # self.bit_pointer = {}
        self.left = None
        self.right = None

    def create_tree(self, data, alphabet, depth):
        current_depth = depth
        if current_depth < alphabet.get_depth() - 1:
            left_string = ""
            right_string = ""
            for i in data:
                bit = alphabet.char2string(i)[current_depth]
                if bit == '0':
                    self.bit_vector.append(0)
                    left_string += i
                else:
                    self.bit_vector.append(1)
                    right_string += i

            self.left = WaveletTreeBNode()
            self.left.create_tree(left_string, alphabet, current_depth + 1)
            self.right = WaveletTreeBNode()
            self.right.create_tree(right_string, alphabet, current_depth + 1)
        else:
            for i in data:
                bit = alphabet.char2string(i)[current_depth]
                if bit == '0':
                    self.bit_vector.append(0)
                else:
                    self.bit_vector.append(1)

    def print_node(self):
        print(self.bit_vector)
        if self.left is not None:
            self.left.print_node()
        if self.right is not None:
            self.right.print_node()

    def rank(self, index, character):
        count = 0
        cursor = 0 if character[0] == '0' else 1
        for i in range(index + 1):
            if self.bit_vector[i] == cursor:
                count += 1

        if cursor == 0:
            if self.left is not None:
                return self.left.rank(count-1, character[1:])
            else:
                return count
        else:
            if self.right is not None:
                return self.right.rank(count-1, character[1:])
            else:
                return count

    def access(self, index):
        bit = self.bit_vector[index]
        count = 0
        for i in range(index + 1):
            if self.bit_vector[i] == bit:
                count += 1
        if bit == 0:
            if self.left is not None:
                return "0" + self.left.access(count-1)
            else:
                return "0"
        if bit == 1:
            if self.right is not None:
                return "1" + self.right.access(count-1)
            else:
                return "1"

    def select(self, freq, character):
        bit = 0 if character[0] == '0' else 1
        if bit == 0:
            if self.left is not None:
                count = self.left.select(freq, character[1:])
                index = 0
                for char in self.bit_vector:
                    if bit == char:
                        count -= 1
                        if count == 0:
                            return index + 1
                        index += 1
                    else:
                        index += 1
            else:
                count = freq
                index = 0
                for char in self.bit_vector:
                    if bit == char:
                        count -= 1
                        if count == 0:
                            return index + 1
                        index += 1
                    else:
                        index += 1
        else:
            if self.right is not None:
                count = self.right.select(freq, character[1:])
                index = 0
                for char in self.bit_vector:
                    if bit == char:
                        count -= 1
                        if count == 0:
                            return index + 1
                        index += 1
                    else:
                        index += 1
            else:
                count = freq
                index = 0
                for char in self.bit_vector:
                    if bit == char:
                        count -= 1
                        if count == 0:
                            return index + 1
                        index += 1
                    else:
                        index += 1


class WaveletAlphabet(object):
    def __init__(self, characters):
        self.characters = characters
        self.alphabet = {}
        self.num_alphabet = 0
        self.tree_depth = 0
        self.alphabet_init()
        self.reverse_alphabet = {v: k for k, v in self.alphabet.items()}

    def alphabet_init(self):
        alphabet_1 = []
        for char in self.characters:
            if char not in alphabet_1:
                alphabet_1.append(char)
        alphabet_1.sort()
        self.num_alphabet = len(alphabet_1)
        self.tree_depth = math.ceil(math.log(self.num_alphabet, 2))
        full_length = math.pow(2, self.tree_depth)
        tree_index = []
        for i in range(self.num_alphabet):
            tree_index.append(i)
        for i in alphabet_1:
            self.alphabet[i] = ""
        for i in range(self.tree_depth):
            pivot = full_length / math.pow(2, i + 1)
            for j in range(self.num_alphabet):
                if tree_index[j] < pivot:
                    self.alphabet[alphabet_1[j]] += "0"
                else:
                    self.alphabet[alphabet_1[j]] += "1"
                    tree_index[j] -= pivot
        # print(self.alphabet)

    def char2string(self, char):
        return self.alphabet[char]

    def string2char(self, string):
        return self.reverse_alphabet[string]

    def get_depth(self):
        return self.tree_depth


if __name__ == "__main__":
    alphabet1 = WaveletAlphabet("abcdefg$")
    tree = WaveletTreeB("abcafcgbagcb$", alphabet1)
    # tree.depth_first_print()
    # print(tree.rank(12, 'g'))
    # print(tree.access(10))
    print(tree.select(2, 'g'))
