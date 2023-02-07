# DND-Generator-Python-
A rudimentary DND character generator in a Python terminal. Will expand to actual GUI later.  
Project exists for practicing OOP principles, with polymorphism and encapsulation already implemented.  
  
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
  
=======  
  
STAT PRIORITIES:  
Fighter - STR, CON, DEX, WIS, CHA, INT  
Paladin - CHA, STR, CON, DEX, WIS, INT  
Wizard - INT, CON, DEX, WIS, CHA, STR  
Ranger - DEX, WIS, CON, STR, CHA, INT  
