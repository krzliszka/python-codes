import random
import string


def random_sequences():
    random_variable = []
    for i in range(0, 19):
        while True:
            unique = True
            tmp_str1 = random.sample(string.ascii_lowercase, k=2)
            tmp_str2 = random.sample(string.digits + string.ascii_lowercase, k=6)
            tmp_str = tmp_str1[0] + tmp_str1[1] + tmp_str2[0] + tmp_str2[1] + tmp_str2[2] + tmp_str2[3] + tmp_str2[4] + tmp_str2[5]
            for tmp in random_variable:
                if tmp == tmp_str:
                    unique = False
                    break
            if unique:
                random.append(tmp_str)
                break
    return random

def arg(outfile):
    argv = sys.argv
    number = len(argv)
    if number == 3:
        filename = argv[1].replace('"', "")

