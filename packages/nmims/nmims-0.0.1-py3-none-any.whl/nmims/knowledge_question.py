def knowledge_question():
    print('''
    
############################# Knowledge Base 

######### HP1

# from logic import *

rain=Symbol("rain") # It is raining.
hagrid=Symbol("hagrid") # Harry visited Hagrid
dumbledore=Symbol("dumbledore") # Harry visited Dumbledore

knowledge=And(Implication(Not(rain),hagrid), # If it didn’t rain, Harry visited Hagrid today.
             Or(hagrid,dumbledore), # Harry visited Hagrid or Dumbledore today, but not both.
             Not(And(hagrid,dumbledore)), 
             dumbledore) #Harry visited Dumbledore today.
print(model_check(knowledge,rain))

########### HP2

# from logic import *

houses=['gryffindor','slytherin','hufflepuff','ravenclaw'] # four different houses, Gryffindor, Hufflepuff, Ravenclaw, and Slytherin. 
people=['gilderoy','minerva','pomona','horace'] #four different people, Gilderoy, Pomona, Minerva, and Horace
symbols=[]
knowledge_base=And()

for p in people:
    for h in houses:
        symbols.append(Symbol(f'{p}{h}'))

# There is exactly one person in each house.         
for p in people:
    knowledge_base.add(Or
                        (Symbol(f'{p}gryffindor'),
                        Symbol(f'{p}slytherin'),
                        Symbol(f'{p}hufflepuff'),
                        Symbol(f'{p}ravenclaw'))
                       )
for p in people:
    for h1 in houses:
        for h2 in houses:
            if h1!=h2:
                knowledge_base.add(Implication
                                   (Symbol(f'{p}{h1}'),
                                        Not(Symbol(f'{p}{h2}')))
                                   )
for h in houses:
    for p1 in people:
        for p2 in people:
            if p1!=p2:
                knowledge_base.add(Implication
                                   (Symbol(f'{p1}{h}'),
                                        Not(Symbol(f'{p2}{h}')))
                                   )
                
knowledge_base.add(Not(Symbol('pomonaslytherin'))) #pomana not in slytherin
knowledge_base.add(Symbol('minervagryffindor')) #Minerva belongs to Gryffindor
knowledge_base.add(Or(Symbol('gilderoygryffindor'),Symbol('gilderoyravenclaw'))) # gilderoy in gryffindor or in ravenclaw

for symbol in symbols:
    if model_check(knowledge_base,symbol):
        print(symbol)

#####kinght and knaves
from logic import *

Aknight=Symbol('A is a knight')
Aknave=Symbol('A is a knave')
Bknight=Symbol('B is a knight')
Bknave=Symbol('B is a knave')
Cknight=Symbol('C is a knight')
Cknave=Symbol('C is a knave')

symbols=[Aknight,Aknave,Bknight,Bknave,Cknight,Cknave]

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge_base=And(
    Or(Aknight,Aknave),
    Not(And(Aknight,Aknave)),
    Or(Bknight,Bknave),
    Not(And(Bknight,Bknave)),
    Or(Cknight,Cknave),
    Not(And(Cknight,Cknave)),
    Implication(Aknight,And(Aknight,Aknave)),
    Implication(Aknave,Not(And(Aknight,Aknave)))
)
for symbol in symbols:
    if model_check(knowledge_base,symbol):
        print(symbol)


# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge_base2=And(
    Or(Aknight,Aknave),
    Not(And(Aknight,Aknave)),
    Or(Bknight,Bknave),
    Not(And(Bknight,Bknave)),
    Or(Cknight,Cknave),
    Not(And(Cknight,Cknave)),
    Implication(Aknight,And(Aknave,Bknave)),
    Implication(Aknave,Not(And(Aknave,Bknave))))


for symbol in symbols:
    if model_check(knowledge_base2,symbol):
        print(symbol)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge_base3=And(
    Or(Aknight,Aknave),
    Not(And(Aknight,Aknave)),
    Or(Bknight,Bknave),
    Not(And(Bknight,Bknave)),
    Or(Cknight,Cknave),
    Not(And(Cknight,Cknave)),
    Implication(Aknight,Or(And(Aknight,Bknight),And(Aknave,Bknave))),
    Implication(Aknave,Not(Or(And(Aknight,Bknight),And(Aknave,Bknave)))),
    Implication(Bknight,Or(And(Aknight,Bknave),And(Aknave,Bknight))),
    Implication(Bknave,Not(Or(And(Aknight,Bknave),And(Aknave,Bknight))))
)


for symbol in symbols:
    if model_check(knowledge_base3,symbol):
        print(symbol)


# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge_base4=And(
    Or(Aknight,Aknave),
    Not(And(Aknight,Aknave)),
    Or(Bknight,Bknave),
    Not(And(Bknight,Bknave)),
    Or(Cknight,Cknave),
    Not(And(Cknight,Cknave)),
    Implication(Aknight,Or(Aknight,Aknave)),
    Implication(Aknave,Not(Or(Aknight,Aknave))),
    Implication(Bknight,Implication(Aknight,Bknave)),
    Implication(Bknave,Implication(Aknave,Not(Bknave))),
    Implication(Bknight,Cknave),
    Implication(Bknave,Cknight),
    Implication(Cknight,Aknight),
    Implication(Cknave,Not(Aknight))

)


for symbol in symbols:
    if model_check(knowledge_base4,symbol):
        print(symbol)

        
############## Color

# from logic import *

colours=["Red","Blue","Green","Yellow"]
positions=["1","2","3","4"]

symbols=[]

for colour in colours:
    for number in positions:
        symbols.append(Symbol(f"{colour}{number}"))
        
print(symbols)

knowledge=And()

for colour in colours:
    knowledge.add(Or(Symbol(f"{colour}1"),
                    Symbol(f"{colour}2"),
                    Symbol(f"{colour}3"),
                    Symbol(f"{colour}4")
    ))

knowledge

for colour in colours:
    for n1 in positions:
        for n2 in positions:
            if n1!=n2:
                knowledge.add(Implication(Symbol(f"{colour}{n1}"),Not(Symbol(f"{colour}{n2}"))))

for number in positions:
    for c1 in colours:
        for c2 in colours:
            if c1!=c2:
                knowledge.add(Implication(Symbol(f"{c1}{number}"),Not(Symbol(f"{c2}{number}"))))

# for first condition all pnc
knowledge.add(Or(
    And(Symbol("Red1"),Symbol("Blue2"),Not(Symbol("Green3")),Not(Symbol("Yellow4"))),
    And(Symbol("Red1"),Symbol("Green3"),Not(Symbol("Yellow4")),Not(Symbol("Blue2"))),
    And(Symbol("Red1"),Symbol("Yellow4"),Not(Symbol("Green3")),Not(Symbol("Blue2"))),
    And(Symbol("Blue2"),Symbol("Green3"),Not(Symbol("Red1")),Not(Symbol("Yellow4"))),
    And(Symbol("Blue2"),Symbol("Yellow4"),Not(Symbol("Green3")),Not(Symbol("Red1"))),
    And(Symbol("Green3"),Symbol("Yellow4"),Not(Symbol("Red1")),Not(Symbol("Blue2")))
))

# by seeing other conditions
knowledge.add(And(
    Not(Symbol("Blue1")),
    Not(Symbol("Red2")),
    Not(Symbol("Green3")),
    Not(Symbol("Yellow4"))
))

for symbol in symbols:
    if model_check(knowledge,symbol):
        print(symbol)

################### roomweapon

# from logic import *

# creating symbols
mustard=Symbol("mustard")
plum=Symbol("plum")
scarlet=Symbol("scarlet")
ballroom=Symbol("ballroom")
kitchen=Symbol("kitchen")
library=Symbol("library")
knife=Symbol("knife")
revolver=Symbol("revolver")
wrench=Symbol("wrench")

people=[mustard,plum,scarlet]
rooms=[ballroom,kitchen,library]
weapons=[knife,revolver,wrench]
symbols=people+rooms+weapons


knowledge=And(
Or(mustard,plum,scarlet),
    Or(ballroom,kitchen,library),
    Or(knife,revolver,wrench),
    Not(plum), # plum has not done murder
    Or(Not(scarlet),Not(library),Not(revolver))  # scarlet is not,library is not and not revolver.
    )

def check_knowledge(knowledge):
    for symbol in symbols:
        if model_check(knowledge,symbol):
            print(f'{symbol}:yes')
        elif model_check(knowledge,symbol)==False:
            print(f'{symbol}:maybe')
            
check_knowledge(knowledge)

knowledge.add(Not(mustard)) # not mustard
knowledge.add(Not(kitchen)) # not kitchen
knowledge.add(Not(revolver)) # not revolver
knowledge.add(Not(ballroom)) # not ballroom
knowledge.add(Not(wrench)) # not wrench

check_knowledge(knowledge)

for symbol in symbols:
    if model_check(knowledge,symbol):
        print(symbol)


################ music 
      
music =Symbol('music')
flowers=Symbol('flowers')
painting=Symbol('painting')
running=Symbol('running')

knowledge=And()

knowledge.add(Implication(painting,flowers))
knowledge.add(Implication(running,music))
knowledge.add(Implication(Not(music),Not(flowers)))

query1=Implication(running,flowers)
model_check(knowledge,query1)

query2=Implication(painting,music)
model_check(knowledge,query2)

query3=Implication(flowers,Not(running))
model_check(knowledge,query3)

query4=Implication(running,Not(painting))
model_check(knowledge,query4)

query5=Implication(painting,running)
model_check(knowledge,query5)

##################### Satvik Krishna

# Each symbol meaning that the concerned person is guilty
Satvik=Symbol('Satvik')
Krishna=Symbol('Krishna')
Sharky=Symbol('Sharky')
knowledge=And()

# If krishna is guilty then either satvik or sharky is guilty
knowledge.add(Implication(Krishna,Or(Satvik,Sharky)))
# if krishna is guilty then both satvik and sharky are guilty
knowledge.add(Implication(Krishna,And(Satvik,Sharky)))
# if krishna is not guilty then either satvik or sharky is guilty
knowledge.add(Implication(Not(Krishna),Or(Satvik,Sharky)))
# if krishna not guilty then both satvik and sharky are guilty
knowledge.add(Implication(Not(Krishna),And(Satvik,Sharky)))

#Sharky never does a job without using Satvik
knowledge.add(Implication(Sharky,Satvik))
knowledge.add(Implication(Not(Sharky),Satvik))
model_check(knowledge,Krishna)
model_check(knowledge,sharky)
model_check(knowledge,satvik)

####################### Aria Barney

aria=Symbol("Aria")
barney=Symbol("Barney")
carie=Symbol("Carie")
knowledge2=And()

#If Aria went to the school play, then Barney also went to the school play.
knowledge2.add(Implication(aria, barney))
#If Barney went to the school play, then Carie also went to the school play.
knowledge2.add(Implication(barney, carie))
#If Barney did not go to the school play
knowledge2.add(Not(barney))

model_check(knowledge2,aria)

######################## Alady Blady

Alady=Symbol('Lady in room A')
Atiger=Symbol('Tiger in room A')
Blady=Symbol('Lady in room B')
Btiger=Symbol('Tiger in room B')
knowledge=And()

#from a,b either one is true
# a - There is a lady in room A, and a tiger in room B
knowledge.add(Implication(Alady,Not(Atiger)))
knowledge.add(Implication(Atiger,Not(Alady)))
# b - There is a lady in one room, and a tiger in another room
knowledge.add(Implication(Blady,Not(Btiger)))
knowledge.add(Implication(Btiger,Not(Blady)))
knowledge.add(Or(And(Alady,Btiger),And(Atiger,Blady)))

signA=And(Alady,Btiger)
signB=Or(And(Alady,Btiger),And(Atiger,Blady))
knowledge.add(Implication(signA,Not(signB)))
knowledge.add(Implication(signB,Not(signA)))

model_check(knowledge,Blady)

###################### AHKRV
# some person is chatting.
A=Symbol("A")
H=Symbol("H")
K=Symbol("K")
R=Symbol("R")
V=Symbol("V")

people=[A, H, K, R, V]

knowledge5=And()

#Either K or H or both are chatting.
knowledge5.add(Or(
Or(K,H),
    And(K,H)
))

#Either R or V but not both are chatting.
knowledge5.add(
    And(
        Or(R,V),
        Not(And(R,V))
    )
)

#If A is chatting, then R is chatting.
knowledge5.add(Implication(A, R))

#V is chatting if and only if K is chatting.
knowledge5.add(Implication(K, V))

#If H is chatting, then both A and K are chatting.
knowledge5.add(Implication(H, And(A, K)))

for person in people:
    print(model_check(knowledge5, person))
    
##################### mythical

mythical=Symbol("mythical")
immortal=Symbol("immortal")
mammal=Symbol("mammal")
horned=Symbol("horned")
magical=Symbol("magical")

knowledge=And()
knowledge.add(Implication(mythical, immortal))
knowledge.add(Implication(Not(mythical), And(Not(immortal), mammal)))
knowledge.add(Implication(Or(immortal, mammal), horned))
knowledge.add(Implication(horned, magical))

model_check(knowledge, mythical)

########################## boy girl white black

boy=Symbol("boy")
girl=Symbol("girl")
white=Symbol("white")
black=Symbol("black")

knowledge3=And(
Implication(boy,black),
Implication(girl,white),
Implication(Not(girl),white),
Implication(Not(boy),black),
Implication(girl,Not(white)),
Implication(boy,Not(black)),  
)

print(model_check(knowledge3, girl))
print(model_check(knowledge3, boy))

''')

knowledge_question()