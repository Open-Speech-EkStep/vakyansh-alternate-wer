import argparse

def create_alternate_spellings(line, word_and_char_replacement_dict):
    keys = word_and_char_replacement_dict.keys()
    if any([k in line for k in keys]):
        keys_present = [k for k in keys if k in line]
        words = line.split()
        new_line=[]
        add_ind = 0
        for ind, word in enumerate(words):
            new_line.append(word)
            for key in keys_present:
                if key in word:
                    new_line[-1] =  new_line[-1].replace(new_line[-1] ,new_line[-1]+"]")
                    new_word = words[ind].replace(key, word_and_char_replacement_dict[key])
                    new_line.insert(ind+add_ind,"["+new_word+ "/")
                    add_ind+=1

        return (" ".join(new_line)).replace("/ ","/")
    else:
        return line

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Make modeified txt')
    parser.add_argument('-i', '--input', required=True, help='Original(Referenece) File path')
    parser.add_argument('-o', '--output', required=True, help='Output File path')
    parser.add_argument('-d', '--dict',required=True,  help='dict file path')

    args_local = parser.parse_args()
    inp_file = args_local.input
    op_file = args_local.output
    dict_file = args_local.dict

    with open(dict_file, encoding = "utf-8") as f:
        lines = f.readlines()
    word_and_char_replacement_dict= {}
    for line in lines:
        key = line.split(":")[0].replace(" ","").replace("\n","")
        value = line.split(":")[1].replace(" ","").replace("\n","")
        word_and_char_replacement_dict.update({key:value})


    with open (inp_file, encoding='utf-8') as f:
        lines = f.readlines()
    modified_lines=[]
    for line in lines:
        modified_lines.append(create_alternate_spellings(line.strip(), word_and_char_replacement_dict))

    modified_lines= [l+"\n" for l in modified_lines]
    with open(op_file, mode= "w+" ,encoding='utf-8') as out_f:
        for line in modified_lines:
            out_f.write(line)


