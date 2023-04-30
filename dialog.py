    #############
    # FORMAT:
    # [0] - Dialog in order
    # [1] - Target of left choice button at intersection
    # [2] - Target of right choice button at intersection
    #############

class Dialog():
    def __init__(self, player_name):
        self.player_name = player_name
        self.og_town = "CITICUS"
        p = self.player_name
        self.inn_dialog_1 = [[
            [None, "You walk into an inn."],
            [None, "There is a very confused looking bear looking around."],
            ["N. Steen", "Well, look who we have here!"],
            ["N. Steen", "If it isn't our disgraced ruler themself."],
            ["N. Steen", "Well, I won't let you walk about on your own. I'm coming with you."],
            [None, "[Bear N. Steen has joined your party.]"],
            [None, "[Returning to town.]"]
        ]]

        self.nsteen_neutral = [[
            ["N. Steen", "Hey, how's it going?"],
            [None, "[You leave him to his devices.]"]
        ]]

        self.radish_neutral = [[
            ["Radish", "You. What do you want, oh high and mighty lord of the manor?"],
            [None, "[You leave her to her devices.]"]
        ]]

        self.grapefart_neutral = [[
            ["Grapefart", "Hey, you! Me and my money were just having us a conversation! Hey, where are ya goin'??"],
            [None, "[You leave him to his devices.]"]
        ]]

        self.intro_1 = [[
            [None, "The city of " + self.og_town + ". A peaceful place, at the moment."],
            [None, "Here, animalkind can live its best life under the caring rule of [King and Queen]."],
            [None, "The King and Queen make plenty of social visits and are well loved across their kingdom as benevolent and relatable leaders."],
            [None, "However... one day, disaster struck."],
            [None, "The King and Queen were mysteriously killed while [out doing something]."],
            [None, "This shocking news rocked the kingdom to its core. How could they live without the guidance of their beloved rulers?"],
            [None, "But, fret not, citizens of [city], for there is one hope that remains."],
            [None, "Deep in the recesses of the castle lives a youth with a heart suppoedly as peaceful and benevolent as their recently departed ancestors."],
            [None, "The child of [king and queen] awakens one day, unaware of any goings-on..."],
            [None, "[Character creation]"]
        ], "intro_2"]

        self.intro_1_quick = [[
            [None, "[Character creation]"]
        ], "intro_3_quick"]

        self.choices_test = [[
            [None, "SELECTION"],
            [None, "Option 1"],
            [None, "Option 2"]
        ], "intro_3", "intro_3"]

        self.intro_2 = [[
            [None, "You get out of bed and stretch your arms. Today seems like a good day to do nothing as usual."],
            [p, "Ah... another day in [city]. Another day of hiding away..."],
            [None, "As a matter of fact, you have never met the people of [city] yourself. Your parents are content to hide you away to ensure that you stay alive in the case of their unlikely demise."],
            [None, "Suddenly, there is a rapid knock at on your door. It seems as if the force behind it is likely to break it down."],
            [p, "Yes? Come in, there's no need to ruin my furniture."],
            [None, "A craggily old fox enters the room with a smirk, practically twirling his moustache with glee."],
            ["Vizier", "Yes, yes, child. I have come to deliver some news that you may be interested in."],
            [p, "Oh, it's you. You know, speaking of, I've found better company in my furnishings than I have in you."],
            ["Vizier", "No need for the open hostilities, your highness. Didn't your parents ever teach you better?"],
            [p, "As it stands, they told me not to talk to strangers, and frankly, you look stranger every time I see you."],
            ["Vizier", "Yes, of course, your snideness. Before you burn the rest of me to a crisp, I have some unfortunate news."],
            [p, "I woke up and you appeared in my room. It appears I've already been met with some... unfortunate news."],
            ["Vizier", "Would you just let me finish? Your parents are dead."],
            ["Vizier", "See? Now you've taken all the steam out of my big reveal. I hope you can relish in that fact."],
            [p, "D-d-dead? My parents? W-what happened to them?"],
            ["Vizier", "Do you think someone like me would know that? It's not like I was there."],
            [p, "Actually, if anyone was there to do that deed, it probably would be you, huh?"],
            ["Vizier", "This is no time for jokes. We have to get you out of here before the killer finds you."],
            [p, "What? But I've never really left the castle... what life exists for me out there? I need to rule my kingdom."],
            ["Vizier", "No, no. You can come back and rule the kingdom later once we apprehend the one who did this. In the meantime, you will be delivered somewhere safe instead."],
            [None, "You feel quite confused, especially on account of just waking up to your dead parents. Before you have time to collect your thoughts, a hulking brute enters the room, taking the door off of its hinges."],
            ["Vizier", "Don't you worry. I will rule over [city] in your stead. In the meantime, this man will take you somewhere safe."],
            [p, "You'll what?? You are beyond suspici--"],
            [None, "Before you have a chance to accuse and waggle your finger at the fox, the brutish creature picks you up and starts running."],
            [None, "Everything is a blur as you are rushed down hallways, unable to determine your location in all of the confusion."],
            ["VIZGONE", "After a short time of severe jostling, you are deposited out the back door of the castle."],
            [None, "The brute laughs at you and runs off, locking the door behind him."],
            [None, "You crash down to your knees. All of this is beyond overwhelming, especially to someone who has been sheltered their whole life."],
            [p, "I have nothing, and outside of this city I am nothing... what am I supposed to do now?"],
            [None, "A guard walks up and taps your shoulder with the hilt of his sword."],
            ["Guard", "Oi. I don't know who you are, but we're on orders to keep someone with your description out."],
            [p, "I am the child of [king and queen]! You must let me back in, this is my city!"],
            ["Guard", "Yeah, yeah, sure thing, boss. I'm Big Beefington, Captain of the Royal Dawn Brigade."],
            [p, "Oh, uh, nice to meet you, Mr. Beefington."],
            ["Guard", "Hahahaha! You vagabond fools will fall for anything. Do I need to stick this in you to get you moving?"],
            [None, "From behind you, leaning on the castle wall, a large bear wearing plate armor meanders into your conversational space."],
            ["Mysterious Bear", "That will be quite enough, ah, Captain Beefington..."],
            ["Guard", "What? Another one? You don't look like a vagabond, though."],
            ["Mysterious Bear", "My identity is none of your business. I'm here to collect my client. He's been through a bit of a rough patch, you see. Just lost his parents."],
            ["Guard", "Is that so? Well, get him off of the property. I'm under orders to dispose of him, and I'm not much in the mood to make a kebob out of this pitiful creature."],
            ["Mysterious Bear", "This way, your highness..."],
            ["GUARDGONE", "Having nowhere else to go, you follow the large, cheerful looking bear across a field and onto a road."],
            [None, "The two of you climb up a hill and he turns back to look at you."],
            ["Mysterious Bear", "Bear N. Steen, at your service. I'm sure you have questions, but now isn't the time to ask them."],
            [None, "SELECTION"],
            [None, "What are you doing here?"],
            [None, "Who are you?"]
        ], "intro_3", "intro_3"]

        self.intro_3 = [[
            [None, "N. Steen walks away and puts his head in his hands, then shakes it around. He wanders back towards you."],
            ["N. Steen", "Didn't I just ask you not to ask any questions? I know I'm a forgetful bear, but that was approximately... ten seconds ago."],
            ["N. Steen", "That is, unless you lingered unnecessarily staring at me on this hill before your pointless attempt at querying me. I wasn't really paying attention."],
            [None, "He chuckles to himself as he continues walking, expecting you to follow him."],
            ["N. Steen", "All you need to know about me is that I come from far away, and I'm here to help you."],
            ["N. Steen", "I know all about your situation. Your parents just died and you presumably just got kicked out of your own castle by a wily fox with a twirly moustache."],
            ["N. Steen", "No need to worry about that right now. All solutions will come in due time, my friend!"],
            [None, "You cross what feels like an endless number of hills until you come upon a single building in a clearing."],
            ["N. Steen", "Ah, yes. Here we are! Welcome to Habbitt."],
            [None, "You look around, quite puzzled by the lack of city in front of you. Is Habbitt the name of the region? You've studied many maps in your isolation, but Habbitt was not a name that comes to your mind."],
            [p, "There's... just an inn. Is the inn called 'Habbitt'? Does someone live inside named 'Habbitt'?"],
            ["N. Steen", "Oh, I can understand your confusion, especially since I just revealed to you that I have a somewhat unreliable memory. But do not worry."],
            ["N. Steen", "This area is going to become a town named Habbitt. Does that make more sense?"],
            [p, "So, let me get this straight. An armored bear picked me up from certain doom, chastised me for asking a question, and then took me to a construction site?"],
            ["N. Steen", "You know as well as me that there's more nuance to this situation than that. Besides, I have a name! I have it for a reason!"],
            [p, "Can I at least stay in this inn until I find somewhere to go?"],
            ["N. Steen", "Friend, you're thinking too small. You've been raised to be a ruler in the event of your parents' demise, correct?"],
            [None, "The little wires in your head representing logic finally connect. This bear wants you to do your job!"],
            [p, "You want me to rule over this inn? That seems a little... short-sighted. And tyrannical, to be honest."],
            ["N. Steen", "I suppose you'll get better at the whole ruling thing after you get some experience."],
            ["N. Steen", "Additionally, I hate to tell you this, but we don't actually have anyone to run the inn."],
            [None, "You stare blankly back at the bear. Nobody running the inn? What kind of city has only one abandoned building?"],
            [p, "What kind of city has only one abandoned building?"],
            [None, "N. Steen scoffs at you."],
            ["N. Steen", "Now now, you can't possibly think I don't have a plan here. I just built this inn myself with some help. We just have to find someone to run it."],
            [p, "Do you know any innkeepers? Surely where you come from, there must have been someone. What about the help you had?"],
            ["N. Steen", "Ah, well, actually, they aren't much of an innkeeper. They gave me a hard time about having to come here and build it, too."],
            ["N. Steen", "But, fear not, I have some reports of an adventurous tavernkeeper who gave up their innkeeping job to be... an adventurer, as it sounds."],
            [p, "So your plan is to tear them away from their new adventurous life and thrust them back into the fold?"],
            ["N. Steen", "I don't think I've ever heard someone refer to innkeeping as 'the fold'. How exciting do you think innkeeping is?"],
            [p, "Look, Bear, I've been cooped up in a castle for a long time. I don't think I've ever even met an innkeeper."],
            ["N. Steen", "Well, rest assured that I will teach you what it takes to find this innkeeper, and I will help you with this new town."],
            ["N. Steen", "Follow me. I know where they are."],
            [None, "He wanders off in a direction, away from the inn. You quickly step into the inn, drop off what belongings you have, and follow the bear."],
            [None, "You eventually come upon the entrance to a dangerous looking cave."],
            ["N. Steen", "Let me guess. They never taught you how to fight in the castle?"],
            [None, "You shake your head dejectedly."],
            [p, "Not a whole lot to fight in a castle that is constantly cleaned by attendants. I'm guessing you know how to?"],
            ["N. Steen", "Of course."],
            [None, "N. Steen tosses you a stick."],
            ["N. Steen", "Just wave this around and we'll see what happens."],
            [p, "Wave it around? What, do you think some fireballs are going to come out of this piece of wood?"],
            ["N. Steen", "Us sophisticated folk call that a stick, friend."],
            [p, "That doesn't make it any better!"],
            ["N. Steen", "If anything threatening comes near you, just whack it with the stick and hopefully it'll go away."],
            [p, "Go away? You mean we aren't going to kill anything?"],
            ["N. Steen", "No. Why would we? These creatures have lives of their own. We're just persuading them to leave us alone."],
            [p, "Why are they going to bother us in the first place?"],
            ["N. Steen", "Wouldn't you want to defend your home? We are intruding on their domicile."],
            [p, "That is... a resoundingly good point. I suppose this stick will have to do."],
            ["N. Steen", "Oh, and I'll have you lead the way. It should be good practice for leading."],
            [p, "What? I've never navigated a dungeon before."],
            ["N. Steen", "A dungeon? You've been playing too many fantasy games. Who calls a cave a dungeon?"],
            ["N. Steen", "Just imagine it this way. The cave is made up of sections. Look around if you'd like, and then move on to the next section."],
            ["N. Steen", "I'll be with you in case any creatures need persuading. Maybe we'll find something fun in here other than our new friend."],
            [p, "Fun? What kind of demented bear are you?"],
            ["N. Steen", "Now, now, no need for name calling. I mean, maybe we'll find you a better weapon than a stick."],
            ["N. Steen", "Or, even better, we'll find some materials for making you a better weapon."],
            ["N. Steen", "Although, we don't have a blacksmith, so that might have to wait. Better collect stuff just in case."],
            [None, "You nod and walk forward into the dark cave."],
            [None, "[Dungeon CAVE]"]
        ], "cave", "recruit_keeper"]

        self.intro_3_quick = [[
            [None, "You nod and walk forward into the dark cave."],
            [None, "[Dungeon CAVE]"]
        ], "cave", "recruit_keeper", 2]

        self.intro_cave_loss = [[
            [p, "Ouch..."],
            ["N. Steen", "Well, that could've gone better."],
            ["N. Steen", "Turns out we were persuaded to leave instead of them."],
            ["N. Steen", "Oh well. Muster your courage, we will try again. Here we go!"],
            [None, "[Dungeon CAVE]"]
        ], "cave", "recruit_keeper", 2]

        self.recruit_keeper = [[
            [None, "You appear to be in the deepest part of the cave."],
            [p, "Well, looks like we're here."],
            ["N. Steen", "Look! There's someone in a cage over there!"],
            [None, "There is a figure collapsed in a cage in the far corner of the room. You approach the cage carefully."],
            [p, "It's a good thing we were here to save them when we... huh?"],
            [None, "Upon closer inspection, the cage is unlocked and the door is slightly ajar."],
            ["N. Steen", "What's the matter? ... Huh. The cage is not locked. This person is not a captive."],
            [None, "Your bear companion squints at the figure, pulls out a drawing on a scroll, then returns the illustration to his possessions pocket."],
            ["N. Steen", "This appears to be who we are searching for, and it appears that they are fast asleep."],
            [p, "Should we wake them up?"],
            ["N. Steen", "No, we should leave them here after coming all this way. After all, they appear to require rest."],
            [None, "N. Steen pinches the bridge of his snout."],
            ["N. Steen", "Yes, of course we should wake them up."],
            [p, "No need to be so snappy with me, it was just a question."],
            ["N. Steen", "Yes, yes, no stupid questions."],
            [None, "He pulls a tiny gong out of his posessions pocket and hits it with a tiny mallet."],
            [p, "You have a tiny gong? Do you need to wake people up often?"],
            [None, "Before you can bicker further with Mr. Steen, the hippo in the cage appears to yawn silently."],
            ["N. Steen", "Stand back, your highness."],
            [p, "What? You've never seen a hippo yawn before when you wake them up with your tiny gong?"],
            ["N. Steen", "Hippos don't really yawn. Usually that mouth motion means they're ready to fight you for being in their space."],
            [None, "The hippo glares at N. Steen."],
            ["Hippo", "I say, you're not correct, Mr. Bear. Although I don't appreciate you waking me from my restful reprieve!"],
            [None, "She stands up and daintily progresses across the room towards the two of you."],
            ["Hippo", "Can I help you gentlemen with something? Can't you let a lady sleep?"],
            ["N. Steen", "Are you Henrietta? I've come to find you so you can run the inn in Habbitt."],
            ["Henrietta", "That's all? Oh, well, let me pack my bags and get right on that."],
            [None, "She scoffs and turns back towards the cage."],
            ["Henrietta", "I told you I would only run that dingy old place if you found someone to run that 'town' of yours."],
            [p, "Are you blind, or are you equating me to chopped liver?"],
            [None, "N. Steen disapprovingly grips the bridge of his nose and sighs."],
            ["Henrietta", "So you DID find the little squirt! I am amazed that your intel was correct, Mr. Bear."],
            ["N. Steen", "My name is Bear N. Steen, ma'am. This is the ejected ruler of " + self.og_town + "."],
            [None, "Henrietta does a little courtsey, looks down, and then arches her head up at you before returning to her original position."],
            ["Henrietta", "How do you do, your highness at your lowest lowness?"],
            [p, "My parents are dead and my kingdom has been taken over by a fox. How do you think I'm doing?"],
            ["Henrietta", "There, there. We'll figure out how to get your kingdom back. In the meantime, we have a city to create."],
            ["Henrietta", "I was actually in here looking for my husband. It's hard to lose him, but he has a... temper."],
            [p, "Am I safe to assume that it's another hippo?"],
            ["N. Steen", "You really haven't been outside of your room for a while, have you?"],
            [p, "What? I can't even assume that?"],
            ["N. Steen", "Listen. Some nations on the continent are okay with marriage. Most nations only allow for what we call 'bonding'."],
            ["N. Steen", "Two animals 'bond' when they want to always stick with each other."],
            [p, "I didn't crawl out from under a rock, you know. I've read about this before."],
            ["N. Steen", "In nations that support marriage, you can sign up with the Science Department to receive children."],
            ["N. Steen", "So, if you think a bit further, doesn't it make sense that both animals don't have to be the same species?"],
            [p, "I suppose so. How does the Science Department make children?"],
            ["N. Steen", "Do I look like a scientist to you? I know a lot, but that's not something I'm privy to."],
            ["Henrietta", "I love my children. They stay by my side at all times and they're very active fellows."],
            ["Henrietta", "Anyway, my husband is a gorilla. His name is... Grilla."],
            ["Henrietta", "He told me not to tell people if that's his real name or not."],
            [p, "Is he around here somewhere?"],
            ["Henrietta", "I think I would've seen him by now. This cave system isn't particularly large."],
            ["N. Steen", "I promise that we'll look for him if you come back to Habbitt with us and run the inn."],
            ["Henrietta", "Why, thank you, Mr. Bear. That would be delightful."],
            [None, "The three of you start walking out of the cave when you stop in your tracks."],
            [p, "Henrietta, what about the cage you were sleeping in? What's the point of that?"],
            ["Henrietta", "Beats me. I just figured if I looked captive that the other creatures in here would leave me alone."],
            [p, "So... it's not yours?"],
            ["Henrietta", "What use does an innkeeper have for a cage that large?"],
            [p, "You tell me... I'm not an innkeeper, nor have I ever met one."],
            ["Henrietta", "Fine. I don't have any use for a cage that large. Any beast that's that size is too much for me to take back by myself."],
            [None, "You shrug and continue out of the cave."],
            [None, "The three of you arrive at Habbitt, in front of the familiar inn."],
            ["Henrietta", "I'll keep myself busy in here. You two can let me know if you need anything, and feel free to sit and chat in here."],
            ["HENRIETTAGONE", "Henrietta walks away into the inn. N. Steen turns towards you and holds out his hand gesturing for you to wait."],
            ["N. Steen", p + ", one moment, please."],
            [p, "Hmm?"],
            ["N. Steen", "If you need to 'advance' your relationship with anyone living in Habbitt, the inn is the place to do it."],
            ["N. Steen", "All you need to do is go inside and call one of us, and we can have a friendly chat."],
            [p, "I can't just come find you in the village?"],
            ["N. Steen", "I mean, you could, but it's easier to just call us from the central location, right?"],
            [p, "I don't think I can shout loud enough to summon anyone from here, especially if this town gets bigger."],
            ["N. Steen", "That's the magic of this inn. I've infused it with the ability to 'message' anyone within the city limits."],
            [p, "What? How did you manage that?"],
            ["N. Steen", "Don't underestimate me, " + p + ". I'm a lot more capable than you might think."],
            [p, "Okay... I don't suppose you're just going to tell me about yourself?"],
            ["N. Steen", "Not out here. Maybe in the inn I will. Depending on our relationship, anyway."],
            ["N. Steen", "If you see hearts while we're out in a dungeon, you can 'match' them to improve relationships."],
            [p, "Match... them?"],
            ["N. Steen", "That's what the government calls it where I'm from."],
            ["N. Steen", "Realistically, spending time with others in a dungeon builds relationships."],
            [p, "Okay... what should I be doing right now?"],
            ["N. Steen", "Once she's all set up, go ask Henrietta about the last place she saw her husband."],
            ["N. Steen", "I'll be working on building another building according to my blueprints. Call me from the inn if you need anything."],
            [None, "He smiles at you and waddles away."],
            [None, "To Town"]
            ]]
        
        ################
        # BOND DIALOGS #
        ################
        
        self.mc_bear_bond_dialog = [
            # Rank 1
            [[
            [p, "So he just wanted me to ring this bell, huh?"],
            [None, "You ring the bell in the inn. Like magic, Bear wanders in and sits down at a table. He beckons you to come over, which you do."],
            ["N. Steen", "Hmm? Oh, your highness."],
            [None, "He looks around as if he wasn't expecting you to walk up."],
            ["N. Steen", "Is there anything I can do for you?"],
            [p, "Well, you did say you wanted me to test out the inn system to see how it works."],
            ["N. Steen", "Ah! Yes, that I did, that I did. Do you find it to your liking?"],
            [p, "I suppose I do. It certainly got you in here fast."],
            ["N. Steen", "Like I said, it's magic. You hear a little jingle in your head and that way you know you should come over here."],
            [p, "A jingle? Is it pleasant?"],
            ["N. Steen", "Um... well, that's really in the eye of the beholder, I think. Here, let me ring the bell for you."],
            [None, "He walks up to the bell at the counter and rings it..."],
            [None, "Deep in your mind, you hear something. It's hard to make out, but it sounds like... bees?"],
            [None, "You instinctively swat at your ear trying to get the noise to go away, but it just disappears after some time."],
            [p, "Bees? Really?!"],
            ["N. Steen", "Ah, yes. So, the noise you hear is relevant to who rings the bell looking for you."],
            ["N. Steen", "As I am a bear, you hear bees, as bees like honey, and this bell's creation must be some kind of sick joke."],
            [p, "What, you don't like honey or something?"],
            ["N. Steen", "Not especially. But I do not choose the 'ringtone' of the bell. It's some kind of magic that I don't quite understand."],
            [p, "Well, you are quite... martial. I wouldn't really expect you to understand magic."],
            ["N. Steen", "What is that supposed to mean? Where I come from, we must study all topics to achieve some sort of understanding in our work."],
            [p, "Where exactly is it that you're from?"],
            ["N. Steen", "Now, now, that is not important. I'm from Habbitt now. My past is something we can explore in the future, perhaps, but not now."],
            [None, "Bear's response is abrupt and leaves you wondering what he's hiding."],
            [p, "Well, as long as you aren't here to kill me, you're an improvement from the last creature I worked with."],
            ["N. Steen", "Killing you is not in my best interests. You are much more valuable to all of us alive."],
            [p, "Lovely, just what I want to hear."],
            ["N. Steen", "So you're acclimatizing well to your new digs?"],
            [p, "My new what? I haven't really been around here for long enough to have an answer to that."],
            ["N. Steen", "Ah, well. It will come in time. Now, if you'll excuse me, I need to go back to building."],
            [None, "Bear acts like he's tipping a hat to you, despite the fact that his helmet doesn't really come off. He waddles back out of the inn."],
            [None, "END INN DIALOG"]
            ]],
            # Rank 2
            [[[None, "END INN DIALOG"]]],
            # Rank 3
            [[[None, "END INN DIALOG"]]],
            # Rank 4
            [[[None, "END INN DIALOG"]]],
            # Rank 5
            [[[None, "END INN DIALOG"]]],
            # Rank 6
            [[[None, "END INN DIALOG"]]],
            # Rank 7
            [[[None, "END INN DIALOG"]]],
            # Rank 8
            [[[None, "END INN DIALOG"]]],
            # Rank 9
            [[[None, "END INN DIALOG"]]],
            # Rank 10
            [[[None, "END INN DIALOG"]]]
        ]

        self.mc_henrietta_bond_dialog = [
            [[
            [p, "Ringing the bell for Henrietta, then..."],
            ["Henrietta", "Excuse me, your highness?"],
            [p, "Huh? What?"],
            ["Henrietta", "I couldn't help but overhear, given that I'm standing right next to you."],
            ["Henrietta", "Were you about to ring the bell to summon me?"],
            [p, "Um... yes. Yes, I was."],
            ["Henrietta", "You do realize I've been standing next to you this whole time right? The bell is at the counter and this is my inn."],
            [p, "Then why are you an option on the directory?"],
            ["Henrietta", "That bear insisted upon it. He said, 'if you are ever out of the inn, we need a means to contact you! Huh huh huh!'"],
            [p, "Yeah, that sounds like him."],
            [None, "You ring the bell for Henrietta. In your head, you hear some kind of muddy squishy sound."],
            ["Henrietta", "For the sake of the life giver! I can't believe you just rang that despite the conversation we're having here."],
            [None, "She waddles around the bar and out in front of you. She lets out a loud sigh."],
            ["Henrietta", "... You rang?"],
            [p, "Yeah, hi, I called you. I was hoping you would pick up."],
            ["Henrietta", "Get on with it..."],
            [p, "Touchy, huh? I take it you don't like the muddy squishy ringtone you have on here either."],
            ["Henrietta", "Can we please talk about the reason you called me over here?"],
            [p, "You said you were going to give me more information about your missing husband."],
            ["Henrietta", "Yes, well, he's not so much missing as he is absent from his duties as the inn's chef and cook."],
            ["Henrietta", "You see, he has a garage to the east of here a ways. It's actually pretty close to town."],
            [p, "A garage? What's that?"],
            ["Henrietta", "It's a large metal facility where he builds his robots."],
            [p, "Robots? Building? I thought he was a chef."],
            ["Henrietta", "He likes machines, like ovens and grills, but also mechanical parts. He built our cooking system in the inn himself."],
            [p, "Impressive. And what do you do here?"],
            ["Henrietta", "What sort of question is that? I run the inn. I also clean all of the rooms, including where you're staying."],
            [p, "Oh, I see."],
            ["Henrietta", "Bear is already aware of the location of the garage. Just tell him you want to 'Venture Out' and he will take you there."],
            [p, "Alright. Anything else I should know?"],
            ["Henrietta", "My husband is somewhat... eccentric. He also considers himself quite the musician. Be aware that he might ask strange things of you when you find him."],
            [p, "Yeah, that's definitely not concerning at all. Alright, we'll go find him. See you later."],
            [None, "Henrietta waddles back behind the counter and goes back to polishing a cup, as innkeepers do."],
            [None, "END INN DIALOG"]
            ]],
            [[
            [None, "Henrietta dialog 2."],
            [None, "END INN DIALOG"]
            ]],
            [[
            [None, "Henrietta dialog 3."],
            [None, "END INN DIALOG"]
            ]],
            [[
            [None, "Henrietta dialog 4."],
            [None, "END INN DIALOG"]
            ]],
            [[
            [None, "Henrietta dialog 5."],
            [None, "END INN DIALOG"]
            ]],
            [[
            [None, "Henrietta dialog 6."],
            [None, "END INN DIALOG"]
            ]],
            [[
            [None, "Henrietta dialog 7."],
            [None, "END INN DIALOG"]
            ]],
            [[
            [None, "Henrietta dialog 8."],
            [None, "END INN DIALOG"]
            ]],
            [[
            [None, "Henrietta dialog 9."],
            [None, "END INN DIALOG"]
            ]],
            [[
            [None, "Henrietta dialog 10."],
            [None, "END INN DIALOG"]
            ]]
            ]

        self.bear_henrietta_bond_dialog = [
            [[
            [None, "Bear + Henrietta dialog 1."],
            [None, "END INN DIALOG"]
            ]],
            [[
            [None, "Bear + Henrietta dialog 2."],
            [None, "END INN DIALOG"]
            ]],
            [[
            [None, "Bear + Henrietta dialog 3."],
            [None, "END INN DIALOG"]
            ]],
            [[
            [None, "Bear + Henrietta dialog 4."],
            [None, "END INN DIALOG"]
            ]],
            [[
            [None, "Bear + Henrietta dialog 5."],
            [None, "END INN DIALOG"]
            ]],
            [[
            [None, "Bear + Henrietta dialog 6."],
            [None, "END INN DIALOG"]
            ]],
            [[
            [None, "Bear + Henrietta dialog 7."],
            [None, "END INN DIALOG"]
            ]],
            [[
            [None, "Bear + Henrietta dialog 8."],
            [None, "END INN DIALOG"]
            ]],
            [[
            [None, "Bear + Henrietta dialog 9."],
            [None, "END INN DIALOG"]
            ]],
            [[
            [None, "Bear + Henrietta dialog 10."],
            [None, "END INN DIALOG"]
            ]],
            ]
        
        #########
        # SKIPS #
        #########
        self.intro_skip_to_town = [[
            [None, "[Character creation]"]
        ], "to_town"]

        self.to_town = [[
            [None, "To Town"]
        ]]

    def determine_dialog(self, target, progress, name="Default"):
        match target:
            case "inn":
                if progress < 2:
                    return self.inn_dialog_1
                else:
                    return self.outside_cave_1
            case "town":
                return [[[None, "[Returning to town.]"]]]
            case "nsteen":
                if progress >= 2:
                    return self.nsteen_neutral
            case "radish":
                if progress >= 2:
                    return self.radish_neutral
            case "intro_2":
                return self.intro_2
            case "intro_3":
                return self.intro_3
            case "intro_3_quick":
                return self.intro_3_quick
            case "intro_skip":
                return self.intro_skip_to_town
            case "to_town":
                return self.to_town
            case "mc_bear_rank_1":
                return self.mc_bear_bond_dialog[1]
                

    def process_state(self, dungeon, state):
        if dungeon == "cave":
            if state == "FINISHED":
                return self.recruit_keeper
            elif state == "DEAD":
                return self.intro_cave_loss   

    def get_dialog_description(self, name1, name2, mc_name, active_rank, r_active_rank):
        if name1 == mc_name or name2 == mc_name:
            if name1 == "N. Steen" or name2 == "N. Steen":
                descriptions = [
                    "N. Steen has shown you the ropes on how to communicate via the inn. You also learned that he has a past he won't share with you, and he dislikes honey, unlike other bears (according to him).",
                    "MC BEAR Rank 2",
                    "MC BEAR Rank 3",
                    "MC BEAR Rank 4",
                    "MC BEAR Rank 5",
                    "MC BEAR Rank 6",
                    "MC BEAR Rank 7",
                    "MC BEAR Rank 8",
                    "MC BEAR Rank 9",
                    "MC BEAR Rank 10",
                    "MC BEAR ROM Rank 1",
                    "MC BEAR ROM Rank 2",
                    "MC BEAR ROM Rank 3",
                    "MC BEAR ROM Rank 4",
                    "MC BEAR ROM Rank 5"
                ]
            if name1 == "Henrietta" or name2 == "Henrietta":
                descriptions = [
                    "Henrietta has confided in you her concerns about her husband's wellbeing. You decided to go rescue him from his own... devices.",
                    "MC HENRIETTA Rank 2",
                    "MC HENRIETTA Rank 3",
                    "MC HENRIETTA Rank 4",
                    "MC HENRIETTA Rank 5",
                    "MC HENRIETTA Rank 6",
                    "MC HENRIETTA Rank 7",
                    "MC HENRIETTA Rank 8",
                    "MC HENRIETTA Rank 9",
                    "MC HENRIETTA Rank 10",
                    None, None, None, None, None
                ]
        elif name1 == "N. Steen" or name2 == "N. Steen":
            if name1 == "Henrietta" or name2 == "Henrietta":
                descriptions = [
                    "N. Steen has shown you the ropes on how to communicate via the inn. You also learned that he has a past he won't share with you, and he dislikes honey, unlike other bears (according to him).",
                    "BEAR HENRIETTA Rank 2",
                    "BEAR HENRIETTA Rank 3",
                    "BEAR HENRIETTA Rank 4",
                    "BEAR HENRIETTA Rank 5",
                    "BEAR HENRIETTA Rank 6",
                    "BEAR HENRIETTA Rank 7",
                    "BEAR HENRIETTA Rank 8",
                    "BEAR HENRIETTA Rank 9",
                    "BEAR HENRIETTA Rank 10",
                    None, None, None, None, None
                ]
        if active_rank != None:
            return descriptions[active_rank]
        else:
            return descriptions[r_active_rank]