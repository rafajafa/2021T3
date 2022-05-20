from tamagotchi import Tamagotchi
import operator

#list of dict in a list, key = name, value = object
dict_list = []
name_list = []
def check_death():
    #print(name_list)
    #new_list = sorted(dict_list, key = lambda i : i['name'])
    for dict in dict_list:
        name = dict['name']
        object = dict['object']
        dead_status = dict['dead']
        if object.is_dead() and dead_status == False:
            dict['dead'] = True
            name_list.remove(name)

def create(in_name):
    #if the input name is a key in the list of dict
    check_death()
    if in_name not in name_list:
        
        for dict in dict_list:
            object = dict['object']
            object.increment_time()
        
        object_dict = {'name' : in_name, 'object': Tamagotchi(in_name), 'dead': False}
        dict_list.append(object_dict)
        name_list.append(in_name)

        dict_list.sort(key=operator.itemgetter('name'))
        for dict in dict_list:
            object = dict['object']
            print(object)
        
    else:
        print("You already have a Tamagotchi called that.")
    

def feed(in_name):
    check_death()
    if in_name in name_list:
        for dict in dict_list:
            object = dict['object']
            object.increment_time()
            if dict['name'] == in_name:
                object.feed()
            print(object)
        
    else:
        print("No Tamagotchi with that name")

def play(in_name):
    check_death()
    if in_name in name_list:
        for dict in dict_list:
            object = dict['object']
            object.increment_time()
            if dict['name'] == in_name:
                object.play()
            print(object)
    else:
        print("No Tamagotchi with that name")

def wait():
    check_death()
    for dict in dict_list:
        object = dict['object']
        object.increment_time()
        print(object)

if __name__ == "__main__":
    command_list = [create, feed, play, wait]
    while True:
        input_command = input("Command: ")
        command = input_command.split()
        if len(command) >= 2: 
            first_word = command[0]
            second_word = command[1]
        elif len(command) == 1:
            first_word = command[0]
        else:
            break
            

        if first_word == "create":
            create(second_word)
        elif first_word == "feed":
            feed(second_word)
        elif first_word == "play":
            play(second_word)
        elif first_word == "wait":
            wait()
        else:
            print("Invalid command.")
            pass
