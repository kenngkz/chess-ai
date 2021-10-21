# Chess AI

## About
This project aims to build a chess application that allows both 2 player (PvP : Player vs Player) and 1 player (PvB : Player vs Bot). The chess AI used will be trained using reinforcement learning (RL), specifically self-play. This project also aims to showcase and develop API building knowledge as well as familiarity and proficiency with RL techniques involving multiple neural networks. Finally, this project was inspired by Deepmind's AlphaGo.


## Components
1. Chess rules implementation: legal move generation, editing board state based on moves, determining if (for a given position) checkmate or stalemate has occured
2. Application API
3. Application Frontend
4. AI training and integration with API


## Chess rules implementation
### Legal move generation
Legal move generation was done in multiple steps:
1. get the prelegal moves of a particular piece
2. for each prelegal move, determine if making the move will result in the king being put under check

Further information can be found in the chess module.

### Editing board state based on moves
Board information and Move information is stored as a custom datatype class. When a move is made, a Board object must first be initialized. Then, the Move object is passed into the board.move() function, editing the information stored in the Board object.

### Determining Checkmate/Stalemate
Checkmate and stalemate status is called game state in this project. A is_under_check (chess.indicator.check()) function is used to determine if a side is under check, then legal move generation is used to determine if that side has any legal moves to make. If there are no legal moves left, then the side under check has been checkmated.

A stalemate counter is also implemented as part of the Board dataclass. We use the 50 move rule: if no capture has been made or no pawn has been moved for 50 moves, stalemate occurs. 


## Application API backend
The API framework used is Flask. 

### Persistence
Board data (position, castle_status: whether the rook/king of either side has been moved, stalemate_counter) is saved as a tuple in a .txt file. This way, the board information can persist between API calls and beyond the game shutting down or crashing. Saving is done after every move, and the save file can be reset with an API call.

