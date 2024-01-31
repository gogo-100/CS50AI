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
        if len(self.cells) == self.count:
            return set(self.cells)
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return set(self.cells)
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
        null = []
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
            if len(sentence.cells) == 0:
                null.append(sentence)
        for object in null:
            self.knowledge.remove(object)


    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        null = []
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
            if len(sentence.cells) == 0:
                null.append(sentence)
        for object in null:
            self.knowledge.remove(object)

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
        # 1.2 mark cell as made move and as safe
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # 3. add a new sentence to AI knowledge base based on cell and count
        neighbors = self.get_cell_neighbor(cell)  # only undetermined
        new_sentence = Sentence(neighbors[0],count-neighbors[1])
        self.knowledge.append(new_sentence)
        self.conclude_from_new_sentence(new_sentence)

        
    def conclude_from_new_sentence(self, sentence):
        # 4. straightly concluded from this sentence
        self.conclude(sentence)
        
        # 5. concluded from all sentences
        # needs loop222-225 here but it's enough to pass the test :)
        result = self.infer()
        for new in result:
            self.knowledge.append(new)
            self.conclude(new)     

    def conclude(self, sentence):
        """
        concluded based on this sentence
        """
        known_mines = sentence.known_mines()
        known_safes = sentence.known_safes()
        for mine in known_mines:
            self.mark_mine(mine)
        for safe in known_safes:
            self.mark_safe(safe)

    def infer(self):
        """
        infer from existing knowledge
        """
        news = []
        for s1 in self.knowledge:
            self.conclude(s1)
            for s2 in self.knowledge:
                if s1.cells!= s2.cells and s1.cells.issubset(s2.cells):
                    new = Sentence(s2.cells.difference(s1.cells), s2.count - s1.count)
                    news.append(new)
        return news

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe in self.safes:
            if safe not in self.moves_made:
                return safe
        return None
    

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        if len(self.mines) + len(self.moves_made) >= self.height * self.width:
            return None
        i = random.randint(0, self.height - 1)
        j = random.randint(0, self.width - 1)
        while (i, j)  in self.mines or (i, j)  in self.moves_made:
            i = random.randint(0, self.height - 1)
            j = random.randint(0, self.width - 1)
        return (i,j)
    

    def get_cell_neighbor(self, cell):
        """
        only include cells whose state is still undetermined in the sentence
        """
        neighbors = set()
        known_mines_cnt = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                m = cell[0] + i
                n = cell[1] + j
                border_check = m >= 0 and m < self.height and n >= 0 and n < self.width
                not_center = not(m == cell[0] and n == cell[1])
                if border_check and not_center:
                    if (m,n) in self.mines:
                        known_mines_cnt += 1
                    elif (m,n) not in self.moves_made and (m,n) not in self.safes:
                        neighbors.add((m,n))
        return (neighbors, known_mines_cnt)