#############
# FORMAT:
# [0] - Dialog in order
# [1] - Target of left choice button at intersection
# [2] - Target of right choice button at intersection
#############
name = "Default"

def determine_dialog(target, progress, name="Default"):
    match target:
        case "dialog_start_2":
            dialog_start_2[0][0][1] = "Your name is "+ name +"."
            dialog_start_2[0][1][1] = "Hello, "+name+"!"
            return dialog_start_2
        case "cave_exit":
            return outside_cave_1
        case "martial_choice":
            outside_cave_2[0][0][1] = "You have chosen a Martial background."
            outside_cave_2[0][1][1] = "Let me guess. You only have one brain cell, and it only fires sometimes. But that's okay, I guess."
            return outside_cave_2
        case "bookish_choice":
            outside_cave_2[0][0][1] = "You have chosen a Bookish background."
            outside_cave_2[0][1][1] = "What are you, some kind of nerd? Do books keep you company at night? Make those lonely nights warm or what?"
            return outside_cave_2
        case "inn":
            if progress < 2:
                return inn_dialog_1
            else:
                return outside_cave_1
        case "town":
            return [[[None, "[Returning to town.]"]]]
        case "nsteen":
            if progress >= 2:
                return nsteen_neutral
        case "radish":
            if progress >= 2:
                return radish_neutral
        case "intro_2":
            temp = intro_2
            for x in temp:
                for y in x:
                    if y[0] == "Player":
                        y[0] = name
            return temp
        case "intro_3":
            temp = intro_3
            for x in temp:
                for y in x:
                    if y[0] == "Player":
                        y[0] = name
            return temp

def process_state(dungeon, state):
    if dungeon == "cave_dungeon":
        if state == "WIN":
            return recruit_keeper

dialog_start = [[
    [None, """You find yourself in a dark cave."""],
    [None, """You try to remember your name."""],
    [None, "Please type into the box."],
], "dialog_start_2"]

dialog_start_2 = [[
    [None, "Your name is name."],
    [None, "Hello name!"],
    [None, "Let's get you out of this cave."],
    [None, "SELECTION"],
    [None, "Exit Cave"],
    [None, "Don't Exit Cave"]
], "cave_exit", "cave_exit"]

outside_cave_1 = [[
    [None, "Regardless of your choice, I'm taking you outside."],
    [None, "That's better. Smell that forest air!"],
    [None, "The fresh air is good for you, after all."],
    [None, "Did you really think breathing cave air for all this time was good for you?"],
    [None, "If you thought that, you would be completely wrong."],
    [None, "You feel the urge to think really hard about what kind of person you built yourself into."],
    [None, "SELECTION"],
    [None, "Martial (Physical, Melee)"],
    [None, "Bookish (Magic, Ranged)"]
], "martial_choice", "bookish_choice"]

outside_cave_2 = [[
    [None, "You have chosen Class."],
    [None, "Judgmental line!"],
    [None, "Anyway, we should find our way out of here."],
    [None, "Maybe you should just follow that road over there until you run into something."],
    [None, "Ah, here we are. Some kind of city."],
    [None, "I'll leave you to figuring out where you should be going."],
    [None, "Please select a destination."]
], "town_choices"]

inn_dialog_1 = [[
    [None, "You walk into an inn."],
    [None, "There is a very confused looking bear looking around."],
    ["N. Steen", "Well, look who we have here!"],
    ["N. Steen", "If it isn't our disgraced ruler themself."],
    ["N. Steen", "Well, I won't let you walk about on your own. I'm coming with you."],
    [None, "[Bear N. Steen has joined your party.]"],
    [None, "[Returning to town.]"]
]]

nsteen_neutral = [[
    ["N. Steen", "Hey, how's it going?"],
    [None, "[You leave him to his devices.]"]
]]

radish_neutral = [[
    ["Radish", "You. What do you want, oh high and mighty lord of the manor?"],
    [None, "[You leave her to her devices.]"]
]]

intro_1 = [[
    [None, "The city of [city]. A peaceful place, at the moment."],
    [None, "Here, animalkind can live its best life under the caring rule of [King and Queen]."],
    [None, "The King and Queen make plenty of social visits and are well loved across their kingdom as benevolent and relatable leaders."],
    [None, "However... one day, disaster struck."],
    [None, "The King and Queen were mysteriously killed while [out doing something]."],
    [None, "This shocking news rocked the kingdom to its core. How could they live without the guidance of their beloved rulers?"],
    [None, "But, fret not, citizens of [city], for there is one hope that remains."],
    [None, "Deep in the recesses of the castle lives a youth with a heart as peaceful and benevolent as their recently departed ancestors."],
    [None, "The child of [king and queen] awakens one day, unaware of any goings-on..."],
    [None, "[Character creation]"]
]]

intro_1_quick = [[
    [None, "[Character creation]"]
]]

intro_2 = [[
    [None, "You get out of bed and stretch your arms. Today seems like a good day to do nothing as usual."],
    ["Player", "Ah... another day in [city]. Another day of hiding away..."],
    [None, "As a matter of fact, you have never met the people of [city] yourself. Your parents are content to hide you away to ensure that you stay alive in the case of their unlikely demise."],
    [None, "Suddenly, there is a rapid knock at on your door. It seems as if the force behind it is likely to break it down."],
    ["Player", "Yes? Come in, there's no need to ruin my furniture."],
    [None, "A craggily old fox enters the room with a smirk, practically twirling his moustache with glee."],
    ["Vizier", "Yes, yes, child. I have come to deliver some news that you may be interested in."],
    ["Player", "Oh, it's you. You know, speaking of, I've found better company in my furnishings than I have in you."],
    ["Vizier", "No need for the open hostilities, your highness. Didn't your parents ever teach you better?"],
    ["Player", "As it stands, they told me not to talk to strangers, and frankly, you look stranger every time I see you."],
    ["Vizier", "Yes, of course, your snideness. Before you burn the rest of me to a crisp, I have some unfortunate news."],
    ["Player", "I woke up and you appeared in my room. It appears I've already been met with some... unfortunate news."],
    ["Vizier", "Would you just let me finish? Your parents are dead."],
    ["Vizier", "See? Now you've taken all the steam out of my big reveal. I hope you can relish in that fact."],
    ["Player", "D-d-dead? My parents? W-what happened to them?"],
    ["Vizier", "Do you think someone like me would know that? It's not like I was there."],
    ["Player", "Actually, if anyone was there to do that deed, it probably would be you, huh?"],
    ["Vizier", "This is no time for jokes. We have to get you out of here before the killer finds you."],
    ["Player", "What? But I've never really left the castle... what life exists for me out there? I need to rule my kingdom."],
    ["Vizier", "No, no. You can come back and rule the kingdom later once we apprehend the one who did this. In the meantime, you will be delivered somewhere safe instead."],
    [None, "You feel quite confused, especially on account of just waking up to your dead parents. Before you have time to collect your thoughts, a hulking brute enters the room, taking the door off of its hinges."],
    ["Vizier", "Don't you worry. I will rule over [city] in your stead. In the meantime, this man will take you somewhere safe."],
    ["Player", "You'll what?? You are beyond suspici--"],
    [None, "Before you have a chance to accuse and waggle your finger at the fox, the brutish creature picks you up and starts running."],
    ["VIZGONE", "After a short time of jostling and confusing, you are deposited out the back door of the castle. The brute laughs at you and runs off, locking the door behind him."],
    [None, "You crash down to your knees. All of this is beyond overwhelming, especially to someone who has been sheltered their whole life."],
    ["Player", "I have nothing, and outside of this city I am nothing... what am I supposed to do now?"],
    [None, "A guard walks up and taps your shoulder with the hilt of his sword."],
    ["Guard", "Oi. I don't know who you are, but we're on orders to keep someone with your description out."],
    ["Player", "I am the child of [king and queen]! You must let me back in, this is my city!"],
    ["Guard", "Yeah, yeah, sure thing, boss. I'm Big Beefington, Captain of the Royal Dawn Brigade."],
    ["Player", "Oh, uh, nice to meet you, Mr. Beefington."],
    ["Guard", "Hahahaha! You vagabond fools will fall for anything. Do I need to stick this in you to get you moving?"],
    [None, "From behind you, leaning on the castle wall, a large bear wearing plate armor meanders into your conversational space."],
    ["Mysterious Bear", "That will be quite enough, ah, Captain Beefington..."],
    ["Guard", "What? Another one? You don't look like a vagabond, though."],
    ["Mysterious Bear", "My identity is none of your business. I'm here to collect my client. He's been through a bit of a rough patch, you see. Just lost his parents."],
    ["Guard", "Is that so? Well, get him off of the property. I'm under orders to dispose of him, and I'm not much in the mood to make a kebob out of this pitiful creature."],
    ["Mysterious Bear", "This way, your highness..."],
    ["GUARDGONE", "Having nowhere else to go, you follow the large, cheerful looking bear across a field and onto a road. The two of you climb up a hill and he turns back to look at you."],
    ["Mysterious Bear", "Bear N. Steen, at your service. I'm sure you have questions, but now isn't the time to ask them."],
    [None, "SELECTION"],
    [None, "What are you doing here?"],
    [None, "Who are you?"]
], "intro_3", "intro_3"]

intro_3 = [[
    ["MYSTBEARGONE", "N. Steen walks away and puts his head in his hands, then shakes it around. He wanders back towards you."],
    ["N. Steen", "Didn't I just ask you not to ask any questions? I know I'm a forgetful bear, but that was approximately... ten seconds ago."],
    ["N. Steen", "That is, unless you lingered unnecessarily staring at me on this hill before your pointless attempt at querying me. I wasn't really paying attention."],
    [None, "He chuckles to himself as he continues walking, expecting you to follow him."],
    ["N. Steen", "All you need to know about me is that I come from far away, and I'm here to help you."],
    ["N. Steen", "I know all about your situation. Your parents just died and you presumably just got kicked out of your own castle by a wily fox with a twirly moustache."],
    ["N. Steen", "No need to worry about that right now. All solutions will come in due time, my friend!"],
    [None, "You cross what feels like an endless number of hills until you come upon a single building in a clearing."],
    ["N. Steen", "Ah, yes. Here we are! Welcome to Habbitt."],
    [None, "You look around, quite puzzled by the lack of city in front of you. Is Habbitt the name of the region? You've studied many maps in your isolation, but Habbitt was not a name that comes to your mind."],
    ["Player", "There's... just an inn. Is the inn called 'Habbitt'? Does someone live inside named 'Habbitt'?"],
    ["N. Steen", "Oh, I can understand your confusion, especially since I just revealed to you that I have a somewhat unreliable memory. But do not worry."],
    ["N. Steen", "This area is going to become a town named Habbitt. Does that make more sense?"],
    ["Player", "So, let me get this straight. An armored bear picked me up from certain doom, chastised me for asking a question, and then took me to a construction site?"],
    ["N. Steen", "You know as well as me that there's more nuance to this situation than that. Besides, I have a name! I have it for a reason!"],
    ["Player", "Can I at least stay in this inn until I find somewhere to go?"],
    ["N. Steen", "Friend, you're thinking too small. You've been raised to be a ruler in the event of your parents' demise, correct?"],
    [None, "The little wires in your head representing logic finally connect. This bear wants you to do your job!"],
    ["Player", "You want me to rule over this inn? That seems a little... short-sighted. And tyrannical, to be honest."],
    ["N. Steen", "I suppose you'll get better at the whole ruling thing after you get some experience."],
    ["N. Steen", "Additionally, I hate to tell you this, but we don't actually have anyone to run the inn."],
    [None, "You stare blankly back at the bear. Nobody running the inn? What kind of city has only one abandoned building?"],
    ["Player", "What kind of city has only one abandoned building?"],
    [None, "N. Steen scoffs at you."],
    ["N. Steen", "Now now, you can't possibly think I don't have a plan here. I just built this inn myself with some help. We just have to find someone to run it."],
    ["Player", "Do you know any innkeepers? Surely where you come from, there must have been someone. What about the help you had?"],
    ["N. Steen", "Ah, well, actually, they aren't much of an innkeeper. They gave me a hard time about having to come here and build it, too."],
    ["N. Steen", "But, fear not, I have some reports of an adventurous tavernkeeper who gave up their innkeeping job to be... an adventurer, as it sounds."],
    ["Player", "So your plan is to tear them away from their new adventurous life and thrust them back into the fold?"],
    ["N. Steen", "I don't think I've ever heard someone refer to innkeeping as 'the fold'. How exciting do you think innkeeping is?"],
    ["Player", "Look, Bear, I've been cooped up in a castle for a long time. I don't think I've ever even met an innkeeper."],
    ["N. Steen", "Well, rest assured that I will teach you what it takes to find this innkeeper, and I will help you with this new town."],
    ["N. Steen", "Follow me. I know where they are."],
    [None, "He wanders off in a direction, away from the inn. You quickly step into the inn, drop off what belongings you have, and follow the bear."],
    [None, "You eventually come upon the entrance to a dangerous looking cave."],
    ["N. Steen", "Let me guess. They never taught you how to fight in the castle?"],
    [None, "You shake your head dejectedly."],
    ["Player", "Not a whole lot to fight in a castle that is constantly cleaned by attendants. I'm guessing you know how to?"],
    ["N. Steen", "Of course."],
    [None, "N. Steen tosses you a stick."],
    ["N. Steen", "Just wave this around and we'll see what happens."],
    ["Player", "Wave it around? What, do you think some fireballs are going to come out of this piece of wood?"],
    ["N. Steen", "Us sophisticated folk call that a stick, friend."],
    ["Player", "That doesn't make it any better!"],
    ["N. Steen", "If anything threatening comes near you, just whack it with the stick and hopefully it'll go away."],
    ["Player", "Go away? You mean we aren't going to kill anything?"],
    ["N. Steen", "No. Why would we? These creatures have lives of their own. We're just persuading them to leave us alone."],
    ["Player", "Why are they going to bother us in the first place?"],
    ["N. Steen", "Wouldn't you want to defend your home? We are intruding on their domicile."],
    ["Player", "That is... a resoundingly good point. I suppose this stick will have to do."],
    ["N. Steen", "Oh, and I'll have you lead the way. It should be good practice for leading."],
    ["Player", "What? I've never navigated a dungeon before."],
    ["N. Steen", "A dungeon? You've been playing too many fantasy games. Who calls a cave a dungeon?"],
    ["N. Steen", "Just imagine it this way. The cave is made up of sections. Look around if you'd like, and then move on to the next section."],
    ["N. Steen", "I'll be with you in case any creatures need persuading. Maybe we'll find something fun in here other than our new friend."],
    ["Player", "Fun? What kind of demented bear are you?"],
    ["N. Steen", "Now, now, no need for name calling. I mean, maybe we'll find you a better weapon than a stick."],
    ["N. Steen", "Or, even better, we'll find some materials for making you a better weapon."],
    ["N. Steen", "Although, we don't have a blacksmith, so that might have to wait. Better collect stuff just in case."],
    [None, "You nod and walk forward into the dark cave."],
    [None, "[Dungeon]"]
], "cave", "recruit_keeper"]

intro_cave_loss = [[
    ["Player", "Ouch..."],
    ["N. Steen", "Well, that could've gone better."],
    ["N. Steen", "Turns out we were persuaded to leave instead of them."],
    ["N. Steen", "Oh well. Muster your courage, we will try again. Here we go!"],
    [None, "[Dungeon]"]
], "cave", "recruit_keeper"]

recruit_keeper = [[
    [None, "You appear to be in the deepest part of the cave."],
    ["Player", "Well, looks like we're here."],
    ["N. Steen", "Look! There's someone in a cage over there!"],
    [None, "There is a figure collapsed in a cage in the far corner of the room. You approach the cage carefully."],
    ["Player", "It's a good thing we were here to save them when we... huh?"],
    [None, "Upon closer inspection, the cage is unlocked and the door is slightly ajar."],
    ["N. Steen", "What's the matter? ... Huh. The cage is not locked. This person is not a captive."],
    [None, "Your bear companion squints at the figure, pulls out a drawing on a scroll, then returns the drawing to his possessions pocket."],
    ["N. Steen", "This appears to be who we are searching for, and it appears that they are fast asleep."],
    ["Player", "Should we wake them up?"],
    ["N. Steen", "No, we should leave them here after coming all this way. After all, they appear to require rest."],
    [None, "N. Steen pinches the bridge of his snout."],
    ["N. Steen", "Yes, of course we should wake them up."],
    ["Player", "No need to be so snappy with me, it was just a question."],
    ["N. Steen", "Yes, yes, no stupid questions."],
    [None, "He pulls a tiny gong out of his posessions pocket and hits it with a tiny mallet."],
    [None, "END DIALOG"]
    ]]
