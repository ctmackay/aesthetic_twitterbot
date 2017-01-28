import markovify
import os
import random
import re
import time

word_title_array = []
random_exercise_name_list = []


muscle_list = ["Biceps", "Shoulders", "Calves", "Neck", "Lats",
               "Triceps", "Hamstrings", "Adductors", "Quadriceps",
               "Chest", "Middle Back", "Abductors", "Lower Back",
               "Glutes", "Forearms", "Traps"]

DATA_DIR = r"C:\Users\Charl\Dropbox\Python scripts\twitterbot\laptop"

input_file_list = []
title_dict = dict()


#builds an array of titles
def build_title_array(title_path):
    wta = []
    # Get raw text as string.
    with open(title_path) as f:
        for line in f:
            for word in line.split():
                wta.append(word)
    return wta

#picks a random muscle group from the list
def generate_new_muscle_group():
    return muscle_list[random.randint(0, len(muscle_list)-1)]

#input a array of titles, outputs a randomly generated exercise name
def generate_new_exercise_name(wta):
    empty_list = []
    new_name=''
    for i in range (5):
        s = wta[random.randint(0,len(wta)-1)]
        if s not in empty_list:
            empty_list.append(s)
            new_name += s + ' '    
    return new_name

def build_paths_to_inputs(muscle_chosen):
    step1_exercise_path = DATA_DIR + '\\' + muscle_chosen +'1.txt'
    step2_exercise_path = DATA_DIR + '\\' + muscle_chosen +'2.txt'
    step3_exercise_path = DATA_DIR + '\\' + muscle_chosen +'3.txt'
    step4_exercise_path = DATA_DIR + '\\' + muscle_chosen +'4.txt'
    if os.path.exists(step1_exercise_path) and  os.path.exists(step2_exercise_path) and os.path.exists(step3_exercise_path) and os.path.exists(step4_exercise_path):
        return step1_exercise_path,step2_exercise_path,step3_exercise_path,step4_exercise_path
    else:
        raise Exception(IOError)
    

def build_text_files(p1,p2,p3,p4):
    with open(p1) as f:
        step1_text = f.read()
    with open(p2) as f:
        step2_text = f.read()
    with open(p3) as f:
        step3_text = f.read()
    with open(p4) as f:
        step4_text = f.read()
    return (step1_text, step2_text, step3_text, step4_text)

def build_markov_models(step1_text, step2_text, step3_text, step4_text):
    # Build the models.
    global step1_model
    global step2_model
    global step3_model
    global step4_model
    
    step1_model = markovify.Text(step1_text, state_size=3)
    step2_model = markovify.Text(step2_text, state_size=3)
    step3_model = markovify.Text(step3_text, state_size=3)
    step4_model = markovify.Text(step4_text, state_size=3)


#PUBLIC functions for twitter interface
def get_current_muscle():
    global muscle_chosen
    return muscle_chosen

def get_exercise_name():
    global random_exercise_name
    return random_exercise_name
def give_me_step1():
    return step1_model.make_short_sentence(140)

def give_me_step2():
    return step2_model.make_short_sentence(140)

def give_me_step3():
    return step3_model.make_short_sentence(140)

def give_me_step4():
    return step4_model.make_short_sentence(140)

def list_all_muscles():
    return muscle_list

def generate_specific_model(muscle):
    global muscle_chosen
    muscle_chosen = muscle
    print "building a markov chain based on: ",
    print muscle_chosen
    
    #find the corresponding titles file for that muscle
    title_path = title_dict[muscle_chosen]

    global random_exercise_name
    random_exercise_name = generate_new_exercise_name(build_title_array(title_path))

    #build paths to the description files
    (step1_path,step2_path,step3_path,step4_path) = build_paths_to_inputs(muscle_chosen)

    # now lets generate our workout markov chain
    # open the text files for reading
    (step1_text, step2_text, step3_text, step4_text) = build_text_files(step1_path,step2_path,step3_path,step4_path)

    # Build the models.
    build_markov_models(step1_text, step2_text, step3_text, step4_text)
    



## START MAIN PROGRAM ##        
#find titles and build dictionary
for f in os.listdir(DATA_DIR):
    if f.endswith("titles.txt"):
        mus = (os.path.splitext(f)[0])[:-7]
        full_path = os.path.abspath(os.path.join(DATA_DIR, f))
        title_dict[mus] = full_path

#find exercise description files        
for f in os.listdir(DATA_DIR):
    if f.endswith(".txt"):
        input_file_list.append(f)

#pick a muscle group
muscle_chosen = generate_new_muscle_group()
#print muscle_chosen

#find the corresponding titles file for that muscle
title_path = title_dict[muscle_chosen]

random_exercise_name = generate_new_exercise_name(build_title_array(title_path))

#build paths to the description files
(step1_path,step2_path,step3_path,step4_path) = build_paths_to_inputs(muscle_chosen)

# now lets generate our workout markov chain
# open the text files for reading
(step1_text, step2_text, step3_text, step4_text) = build_text_files(step1_path,step2_path,step3_path,step4_path)

# Build the models.
build_markov_models(step1_text, step2_text, step3_text, step4_text)

#now the program is ready to be used with a random muscle initialized


##print "Muscle group chosen: ",
##print get_current_muscle()
##print get_exercise_name()
##
##print give_me_step1()
##print give_me_step2()
##print give_me_step3()
##print give_me_step4()

