# Tic-Tac-Toe
This produces a generic tic-tac-toe game with an AI that uses a look up table to determine the best option to play against the user. 
It is not yet a smart AI that learns to recognize the best options by anticipating an opponents next move but that is the next step I will be working on. 
More often that not whoever goes first will win. 
I have included many DocStrings and comments that hopefully explain in sufficient detail the structure and inner workings of the setup and logic. 
Please reach out with any recommendations. This is a simple personal project to practice good programming techniques and dip in to ML and AI. 
Otherwise, Enjoy the game!

Recent changes: 
12/28/23:
  - GUI to improve UX (tkinter), which contains the ability to play against mutliple difficulties of the CPU, or against another user on the same device. Restructured the logic module. Also included record management using a csv file for user stats -- Works well, but will be working to reduce the need for duplicated information. I plan on adding other record systems using JSON, and eventually SQLite as demonstrations of use.
  - The GUI application needs rework. There is an instance where you can have multiple frames open at the same time that is visually unappealing, and might lead to a crash when trying to switch from CPU game play to 1v1. My aim is to incorporate classes within the GUI application codespace, I have only been learning tkinter for a week and was practicing creating all of the components vice optmization to increase muscle memory. This has a high potential for requiring a more thorough change to the base structure of all modules. This is needed though to be rid of circular referencing and overall control and readability of the code. More to come. 
