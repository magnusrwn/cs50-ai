import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # NOTE: MOST LIKELY ERRS HERE ARE USES OF MOTHODS... as opposed to logical/ large scale logical
        # mark the move made
        self.moves_made.add(cell)
        
        # mark as safe
        self.mark_safe(cell)

    # PREPING FOR EVALUATIONS (removing the selected cell, createing a set of neighbours, forming and addin the sentence to the kb)
        # update all sentences that have the cell in it to remove it (as it is safe if gotten this far)
        for k in self.knowledge:
            if cell in k.cells:
                k.cells.remove(cell)

        # find neighbours
        n_cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            
            # check if the height is within board limits to ensure no redundant loops
            if i >= 0 and i < self.height:

                # itterating for width    
                for j in range(cell[1] - 1, cell[1] + 2):
                    
                    # ensuring width is within the grid
                    if j >= 0 and j < self.width:
                        # of it is the cell in question, skip it... as we cant have that as part of the sentence
                        if (i, j) == cell:
                            continue
                    
                        # add the cell to the set if it's known to not be a mine, or b safe
                        if (i, j) in self.safes or (i, j) in self.mines:
                            continue

                        n_cells.add((i, j))
                
        # create the sentence of neighbours
        s = Sentence(n_cells, count)
        # adding the sentence to the kb
        self.knowledge.append(s)


    # EVALUATION OF THE SENTENCES IN THE, AND DRAWING CONCLUSIONS
        # itterating all sentences in kb
        for s in self.knowledge: # sentence in kb
            # if the len of the sentence is equal to the count of the mines, then they are all mines...
            if len(s.cells) == s.count: # if they are mines
                for c in s.cells:
                    # marking as mines
                    self.mark_mine(c)
            
            if s.count == 0:
                # mark things as safe...
                for c in s.cells:
                    self.mark_safe(c)
        
        # check if s1 subSet of s2... if is, then s3 = s2 - s1... etc...
        # O(n)^2 
        # Pseudocode ok
        for i1, s1 in enumerate(self.knowledge):
            for i2, s2 in enumerate(self.knowledge):
                if s1.cells <= s2.cells and s1.cells != s2.cells:
                    s3cells = s2.cells - s1.cells
                    s3count = s2.count - s1.count
                    
                    # create new sentence
                    s3 = Sentence(s3cells, s3count)

                    # rempve old ones
                    

                    self.knowledge.append(s3)



        
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        raise NotImplementedError
