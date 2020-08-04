import argparse
import os
from collections import Counter
import pickle


"""Huffman coding relative function"""


# Creating tree nodes
class NodeTree(object):

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return self.left, self.right

    def nodes(self):
        return self.left, self.right

    def __str__(self):
        return '%s_%s' % (self.left, self.right)


def huffman_code_tree(node, bin_string=''):
    if type(node) is float or type(node) is str:
        return {node: bin_string}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, bin_string + '0'))
    d.update(huffman_code_tree(r, bin_string + '1'))

    return d


def huffman_coding_compression(input_string: object):
    print("[INFO] Encoding ...")
    # Calculating frequency
    freq = dict(Counter(input_string))
    freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    nodes = freq

    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]
        node = NodeTree(key1, key2)
        nodes.append((node, c1 + c2))
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

    huffman_code = huffman_code_tree(nodes[0][0])

    output_freq = ' Char | Huffman code \n'
    for (char, frequency) in freq:
        output_freq = output_freq + ('%r | %s' % (char, huffman_code[char])) + '\n'
    encoded_string = ''
    for char in input_string:
        encoded_string += huffman_code[char]

    print(output_freq)

    print("--> The encoded with code is {}".format({encoded_string}))
    return huffman_code, encoded_string


def huffman_coding_decompression(huffman_code: dict, encoded_string: str, type_input="str"):
    print("[INFO] Decompressing ...")
    key_list = list(huffman_code.keys())
    val_list = list(huffman_code.values())
    s = ''
    if type_input == "str":
        result = ''
        for char in encoded_string:
            s += char
            if s in val_list:
                result += str(key_list[val_list.index(s)])
                s = ''
    else:
        result = []
        for char in encoded_string:
            s += char
            if s in val_list:
                result.append(key_list[val_list.index(s)])
                s = ''

    print("--> The decoded with code is {}".format({result}))
    return result


def compression_ratio(input_string: str, encoded_string: str):
    b0 = len(input_string) * 8
    b1 = len(encoded_string)
    return b0 / b1


"""Processing Function"""


def get_arguments():
    parser = argparse.ArgumentParser(description='The Huffman Coding algorithms')
    parser.add_argument('--mode', '-m', default='compression',
                        choices=['compression', 'decompression'],
                        help='The mode for the algorithm work')
    parser.add_argument('--input', '-i', default='./input/input_huffman.txt',
                        help='The input file path')
    parser.add_argument('--output', '-o', default='./output/output_huffman.pl',
                        help='The output file path')
    return vars(parser.parse_args())


def main(_args):
    # Check the input path is exist whether or not
    if not os.path.isfile(_args['input']):
        print("The input file is not exist")
        exit(1)

    if _args['mode'] == 'compression':
        # Read the text data from file
        with open(_args['input'], 'r') as f:
            string = f.read()

        (huffman_code, encoded_string) = huffman_coding_compression(input_string=string)

        compress_ratio = compression_ratio(input_string=string, encoded_string=encoded_string)
        print("[INFO] The compression ratio is {}".format(compress_ratio))
        # Store the output data to disk
        with open(_args['output'], 'wb') as f:
            pickle.dump((huffman_code, encoded_string), f)

    elif _args['mode'] == 'decompression':
        with open(_args['input'], 'rb') as f:
            (huffman_code, encoded_string) = pickle.load(f)
        huffman_coding_decompression(huffman_code=huffman_code, encoded_string=encoded_string)
    else:
        print("The selected mode is not valid")
        exit(0)


if __name__ == '__main__':
    args = get_arguments()
    main(args)
