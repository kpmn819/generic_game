
from random import randrange, shuffle, random, sample

just_q= ['Whales are what type of animal', 'Cetaceans do not have ', 'The largest animal on earth is a',
 'The second largest animal on earth is a', 'Moby Dick was', 'Which of the cetaceans is the shortest in length as adults',
  'Which of these is extinct', 'Whales were / are primarly hunted for', 'The behavior of a whale jumping out of the water is',
   'Baleen whales feed by', 'Why did we launch a program to recycle fishing line', 
   'The only cetacean that occurs near shore year-round in NC is', 'In order to get our whale bones we', 
   'Bonehenge was primarily funded by', 'We call the process of putting a whale skeleton back together', 
   'Teeth NC beaked whales occur ', 'Bonehenge is']

just_a= [['Mammals', 'Fish', 'Reptiles'], ['A Gall Bladder', 'A Lung', 'Courage'], 
['Blue Whale', 'Humpback Whale', 'Elephant'], ['Fin Whale', 'Giraffe', 'Elephant'], 
['Sperm Whale', 'Pilot Whale', 'Jam Band'], ['Dwarf Sperm Whale', 'Bottlenose Dolphin', "Risso's Dolphin"], 
['Basilosaurus', 'Humpback Whale', 'Mesoplodon'], ['Oil', 'Leather', 'Perfume'], ['Breaching', 'Chuffing', 'Surfing'], 
['Filtering their food from seawater', 'Using suction to feed on seagrass', 'Ordering take-out'], 
['To prevent sealife from becoming entangled', 'It makes great decorations', 'It can be untangled and reused'], 
['bottlenose dolphin', 'pilot whale', 'porpoise'], ['Bury the whale for several years', 'Wait for them to decompose on the beach', 
'Employ a team of surgeons to extract the bones'], ['Contributions from hundreds of doners and volunteers', 'A huge Federal grant', 
'A lucky lottery ticket'], ['Rearticulation', 'Solving a jig saw puzzle', 'Reanimation'], ['Only in lower jaws', 'Only in upper jaws',
 'In both upper and lower jaws'], ['A non-profit organization', 'A for profit enterprise', 'A fishing competition']]

# get 5 (number of turns) 
turn_picks = sample(range( 0, len(just_q)), 5)
print(turn_picks)# a list of index numbers for q & a
# take turns
for index in turn_picks:
    print(just_q[index])
    turn_ans = (just_a[index])
    print(turn_ans[0])
    # need to go through questions and randomize answers
    display_list = turn_ans[:] # make a copy
    shuffle(display_list)
    print(display_list)
    resp = input('Select 1 2 or 3 ')
    if display_list[int(resp)-1] == turn_ans[0]:
        print('got it')
    else:
        print('wrong')
