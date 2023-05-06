# Creatures of Habbitt
Match 3 game where you have a party of up to 4 characters who fight enemies like an RPG, in coordination with your matches.  
Will include dialog between party members a la Fire Emblem.  
  
1/27/2023  
Allows you to name your character, select a class (supports Fighter and Paladin at the moment), and roll stats.  
Can select from rerolling 1s, 1s and 2s (my house rule), or no rerolls.  
Adds all statistics to an encapsulated class in a separate file.  
Demonstrates proficiency in Strategy Design Pattern, having encapsulated individual pieces  
  
2/6/2023  
Added two more classes (Wizard/Ranger) and added spread function that designates which stats are supposed to be prioritized by each class based on your rolls.  
Added stat allocating function to Character super class.  
  
2/7/2023  
Added stat priorities to this README. This project may be morphed for a fantasy game I'm going to make, just noting that down now.  
  
2/18/2023  
Converted dnd generator to fully fledged game.
Added:  
- Match 3 gameplay, very rudimentary and needs fine tuning
- Bear N. Steen as a party member
- Radish Rabbit as a party member
- Connected existing dialog system and map to match 3 game, which reflects which party members you have
- Added who is talking to the dialog system, which also can pull up pictures based on who is talking
- Added background choosing utility  
  
2/19/2023  
Added many more features, including:  
- Full party combat integrated into match 3, with enemies and PCs having turns  
- Overhauled UI
- Further connected match 3 segment to dialog segment  
  
Current Bugs:  
- Game majorly lags whenever a match is made due to enemy turns being taken  
  
Would like to implement:
- Better match 3 system. Preferably with clicking and dragging like an actual modern game instead of this horizontal stuff.
- More characters. I need at least 4 to have a functional party but plan to have a solid number more for "support conversations".
- Actual story. This can wait until the match 3 system is perfected.  
  
2/20 - 2/27 /2023
Overhaul. Found that it was impossible to keep the game running smoothly using just pygame, as pygame uses the RAM and CPU and not the GPU. Switched to PyOpenGL, which uses OpenGL (using C) but translated into Python for my ease of use, thankfully. 
- Created half of the UI in PyOpenGL. Have not made it to inserting proper text yet, nor have I got the "jewels" rendering and following the cursor yet. That is next on the list.  
  
=======  
  
5/2/2023
Significant progress since last update. Features:
- Dungeon crawling gameplay. Run into enemies and it takes you into a match 3 battle. Taking any party member works and leveling up is implemented. No abilities yet.
- Dialog completely in OpenGL. In fact, whole game is in OpenGL now.
- Inn dialog functions, only MCxBear and MCxHenrietta, both rank 1, are implemented, but system is set up for 10 ranks per and 5 romance ranks for relevant characters
- Menu options for Smithy and Haberdasher implemented, though the actual systems are not.
- Intro complete (not proofread though), from MC being kicked out to Bear taking them in and going through the first dungeon, recruiting Henrietta and leaving off for free roam.
- Classes overhauled. Each character has their own class while MC will be able to swap classes. Maybe future where other party members can as well.

TO-DO:
- Smithy and Haberdasher. Both involve using enemy drops to craft better equipment, so both basically use the same system.
- Enemy drops that are relevant to Smithy/Haberdasher crafting requirements
- Crawler cannot use tilesets and is currently restricted to tiny rooms. Attempted to fix, but did not take.
- Less than half of the characters are implemented. Create classes for the remaining ones that I have assets for.
- Voice acting system. Don't need actual voice clips yet, but need to framework to insert them.
- More story once all the frameworks are in place.
- Ranch. Need to speak to Ally about this

5/3/2023
Fixed match.py not working since player attacks would return instead of checking for dead enemies.

TO-DO:
- Enemy rect for collision is not positionally correct w/ the image being shown

5/4/2023
Added Lam'baste, Sunny, and Hollow as playable characters.

TO-DO:
For the new additions:
Stats pictures are not aligned. Dialog pictures are not implemented.

5/5/2023
Retroactively updated yesterday's additions to this document

5/6/2023
