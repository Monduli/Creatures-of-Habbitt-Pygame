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
  
=======  
  
STAT PRIORITIES:  
Fighter - STR, CON, DEX, WIS, CHA, INT  
Paladin - CHA, STR, CON, DEX, WIS, INT  
Wizard - INT, CON, DEX, WIS, CHA, STR  
Ranger - DEX, WIS, CON, STR, CHA, INT  
