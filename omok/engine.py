class Engine:

    DIRECTIONS = ((1, 0), (1, 1), (0, 1), (-1, 1))
    COLOR_MAP = {-1:"Black", 1:"White"}

    def check_valid_place(
            plate: list[list[int]],
            color: int,
            pos: tuple[int, int],
            ) -> bool:
        
        '''
        Determines if a move is invalid based on Renju rules.

        Parameters:
         * plate: 15x15 matrix representing the game board
         * color: int: -1 for black; 1 for white
         * pos: tuple[int, int]: (x, y) coordinates of the move

        Returns:
         bool: True if the move is valid, False otherwise
        '''

        if (plate[pos[1]][pos[0]] != 0): return False # Already occupied
        if (color == 1): return True # No restrictions for White in Renju

        sequences = [
            Engine._check_sequence(plate, color, pos, vec) # Evaluate sequence length for the given direction
            for vec in Engine.DIRECTIONS
        ]
        
        CountThree = sequences.count(3) # Count of three-length-sequence
        CountFour = sequences.count(4) # Count of four-length-sequence

        if (CountThree + CountFour >= 2): return False

        return True

    def _check_sequence_one_way(
            plate: list[list[int]],
            color: int,
            pos: tuple[int, int],
            vector: tuple[int, int],
            count:int = 1,
            way:int = 1,
            ) -> tuple[int, int]:
        '''
        Recursively counts the number of consecutive stones of the same color in one direction.

        Parameters:
         * plate: 15x15 matrix representing the game board
         * color: int: -1 for black; 1 for white
         * pos: tuple[int, int]: (x, y) coordinates of the starting stone
         * vector: tuple[int, int]: (x, y) direction vector
         * count: int = 1: current count of consecutive stones
         * way: int: direction multiplier (1 for forward, -1 for backward)

        Returns:
         int: The count of consecutive stones in the specified direction
        '''

        newX, newY = pos[0] + vector[0] * way, pos[1] + vector[1] * way  # Calculate new position

        if not (0 <= newX < 15 and 0 <= newY < 15):  # Check if the new position is within bounds
            return count

        next = plate[newY][newX]
        
        if (next != color): return count # Stop counting if a different color is encountered

        return Engine._check_sequence_one_way(plate, color, (newX, newY), vector, count+1, way)
    
    def _check_sequence(
            plate: list[list[int]],
            color: int,
            pos: tuple[int, int],
            vector: tuple[int, int],
            ) -> tuple[int, int]:
        '''
        Counts the total number of consecutive stones in both directions of the given vector.

        Parameters:
         * plate: 15x15 matrix representing the game board
         * color: int: -1 for black; 1 for white
         * pos: tuple[int, int]: (x, y) coordinates of the starting stone
         * vector: tuple[int, int]: (x, y) direction vector

        Returns:
         int: The total count of consecutive stones in both directions
        '''

        sequence = Engine._check_sequence_one_way(plate, color, pos, vector, 1, 1)  # Count forward
        sequence += Engine._check_sequence_one_way(plate, color, pos, vector, 0, -1)  # Count backward

        return sequence

    def check_win(
            plate:list[list[int]],
            last:tuple[int, int]
            ) -> bool:
        
        '''
        Evaluates whether the last move resulted in a win.

        Parameters:
         * plate: 15x15 matrix representing the game board
         * last: tuple[int, int]: (x, y) coordinates of the last-placed stone

        Returns:
         bool: True if the last move resulted in a win, False otherwise
        '''

        assert isinstance(plate, (tuple, list)), "Invalid 'plate' type. Must be a tuple or list."
        assert isinstance(last, (tuple, list)), "Invalid 'last' type. Must be a tuple or list."
        assert len(last) == 2, "Invalid length of 'last', must be (x, y)."
        
        turn: int = plate[last[1]][last[0]]  # Determine the color of the last-placed stone

        assert turn != 0, f"Position {last} is not occupied."

        maximum = max([  # Calculate the maximum sequence length for each direction
            Engine._check_sequence(plate, turn, last, vec)  # Evaluate sequence length for the given direction
            for vec in Engine.DIRECTIONS
        ])

        # In Renju, Black cannot have a sequence longer than 5.
        # If the sequence length is 5 or greater, return True.
        if (maximum >= 5): return True

        return False