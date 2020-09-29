"""
This version is implemented based on the codes from https://github.com/LSoldo/wavelet
I implement the access and select function by myself.
"""
import resource


class WaveletTree(object):
    def __init__(self, data):
        self.data = data
        self.root_node = WaveletTreeNode()

        self.root_node.create_tree(self.data)

    def rank(self, position, character):
        return self.root_node.rank(position, character)

    def access(self, position):
        return self.root_node.access(position)

    def select(self, frequency, character):
        return self.root_node.select(frequency, character) - 1


class WaveletTreeNode(object):
    def __init__(self):
        """
        Initialization of the class attributes
        :attribute char_dictionary: every character of the alphabet
            gets a bit value (0 or 1)
        :attribute bit_vector: list of values (0 or 1) for every
            character in the string
        :attribute left and right: references to left and right (child) nodes
        :attribute bit_pointer: pointer to (child) node reference
            for every character of the alphabet in the current node
        """
        self.char_dictionary = {}
        self.bit_vector = []
        self.alphabet_length = 0
        self.left = None
        self.right = None
        self.bit_pointer = {}

    def dictionary_init(self, alphabet):
        """
        Initialization of the alphabet dictionary
        :param alphabet: list of all the (different) characters in the data
        """
        if self.alphabet_length > 2:
            """
            even-length alphabets get sliced in the middle,
            at odd-length ones left node gets one character more
            """
            # if len(alphabet) % 2 == 0:
            #     middle_index = (len(alphabet) / 2)
            # else:
            #     middle_index = ((len(alphabet) + 1) / 2)
            middle_index = int(((len(alphabet) + 1) / 2))
        else:
            middle_index = 1

        for char in alphabet[0: middle_index]:
            self.char_dictionary[char] = 0

        for char in alphabet[middle_index:]:
            self.char_dictionary[char] = 1

    def create_tree(self, string):
        """
        Recursively creates wavelet tree for input string
        :param string: data from which we're creating the node
        """
        alphabet = []
        left_string = ""
        right_string = ""

        # create alphabet
        for char in string:
            if char not in alphabet:
                alphabet.append(char)

        alphabet.sort()
        self.alphabet_length = len(alphabet)
        self.dictionary_init(alphabet)

        if self.alphabet_length > 2:
            # this is not a leaf
            for char in string:
                bit_value = self.char_dictionary[char]
                self.bit_vector.append(bit_value)

                if bit_value is 0:
                    left_string += char
                else:
                    right_string += char

            self.left = WaveletTreeNode()
            self.bit_pointer[0] = self.left
            self.left.create_tree(left_string)

            self.right = WaveletTreeNode()
            self.bit_pointer[1] = self.right
            self.right.create_tree(right_string)

        else:
            # this is a leaf
            for char in string:
                bit_value = self.char_dictionary[char]
                self.bit_vector.append(bit_value)

    def rank(self, index, character):
        """
        Returns the number of occurrences
        of character up to specified index in a string.
        """
        bit = self.char_dictionary[character]
        bit_counter = 0

        for char in self.bit_vector[0: index + 1]:
            if char == bit:
                bit_counter += 1

        if self.alphabet_length > 2:
            return self.bit_pointer[bit].rank(bit_counter - 1, character)
        else:
            return bit_counter

    def access(self, index):
        """
        Returns the character of certain index in a string
        """
        bit = self.bit_vector[index]
        bit_counter = 0
        for char in self.bit_vector[0: index + 1]:
            if char == bit:
                bit_counter += 1

        if self.alphabet_length > 2:
            return self.bit_pointer[bit].access(bit_counter - 1)
        else:
            inv_dict = {v: k for k, v in self.char_dictionary.items()}
            return inv_dict[bit]

    def select(self, freq, character):
        """
        Returns the index of a certain character when this character
        appears freq times
        """
        bit = self.char_dictionary[character]
        if self.alphabet_length > 2:
            count = self.bit_pointer[bit].select(freq, character)
            index = 0
            for char in self.bit_vector:
                if char == bit:
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
                if char == bit:
                    count -= 1
                    if count == 0:
                        return index + 1
                    index += 1
                else:
                    index += 1


if __name__ == "__main__":
    tree = WaveletTree("abcafcgbagcb")
    print("Memory used: " + str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) + " bytes")

    print(tree.rank(7, 'a'))
