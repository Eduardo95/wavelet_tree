class MultiTree:
    def __init__(self, str, left_most_child, right_sibling):
        self.key = str
        self.leftMostChild = left_most_child
        self.rightSibling = right_sibling

    def get_key(self):
        return self.key

    def get_left_most_child(self):
        return self.leftMostChild

    def get_right_sibling(self):
        return self.rightSibling

    def set_key(self, str):
        self.key = str

    def set_left_most_child(self, obj):
        self.leftMostChild = obj

    def set_right_sibling(self, obj):
        self.rightSibling = obj

    def get_dfs(self):
        dfs_list = list()
        dfs_list.append(self.key)
        if self.leftMostChild is not None:
            dfs_list.extend(self.leftMostChild.get_dfs())
        if self.rightSibling is not None:
            dfs_list.extend(self.rightSibling.get_dfs())
        return dfs_list


def main():
    n1 = MultiTree('1', None, None)
    n2 = MultiTree('2', None, None)
    n3 = MultiTree('3', None, None)
    n4 = MultiTree('4', None, None)
    n5 = MultiTree('5', None, None)
    n6 = MultiTree('6', None, None)
    n7 = MultiTree('7', None, None)
    n8 = MultiTree('8', None, None)
    n9 = MultiTree('9', None, None)
    n10 = MultiTree('10', None, None)
    n11 = MultiTree('11', None, None)
    n1.set_left_most_child(n2)
    n2.set_right_sibling(n6)
    n6.set_right_sibling(n8)
    n2.set_left_most_child(n3)
    n6.set_left_most_child(n7)
    n8.set_left_most_child(n9)
    n3.set_right_sibling(n4)
    n4.set_right_sibling(n5)
    n9.set_right_sibling(n10)
    n4.set_left_most_child(n11)
    print(n1.get_dfs())


if __name__ == '__main__':
    main()
