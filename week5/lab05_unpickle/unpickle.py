import pickle
def most_common():
    freq = {}
    with open('shapecolour.p', 'rb') as FILE:
        data = pickle.load(FILE)
        #print(data)
        for item in data:
            shape = str(item.get('shape'))
            colour = str(item.get('colour'))
            shapecolour = [shape, colour]
            sc_string = " ".join(shapecolour)
            if(sc_string in freq):
                freq[sc_string] += 1
            else:
                freq[sc_string] = 1
        keymax = max(freq, key = lambda x: freq[x])
        string_list = keymax.split()
        #print(string_list)
        dict = {"shape": string_list[0], "colour" : string_list[1]}
        #print(dict)
        return dict


if __name__ == "__main__":
    most_common()