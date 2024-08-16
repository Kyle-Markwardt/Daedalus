import random
from collections import deque
from board import Board, Tile

# Define Player class
class Player:
    def __init__(self, id, start_position, cards):
        self.id = id
        self.position = start_position
        self.cards = deque(cards)  # Use deque for easy card management
        self.current_card = self.cards[0] if self.cards else None

    def rotate_excess_tile(self, tile, rotation):
        tile.orientation = (tile.orientation + rotation) % 360
        return tile

    def select_push_location(self, direction, push_position):
        return push_position

    def move_piece(self, new_position):
        self.position = new_position

    def collect_token(self, token):
        # If the token matches the player's current card, collect it
        if token == self.current_card:
            print(f"Player {self.id} collected token: {token}")
            self.cards.popleft()  # Discard the current card
            # Flip to the next card in the player's hand
            self.current_card = self.cards[0] if self.cards else None

    def __repr__(self):
        return f"Player({self.id}, Position: {self.position}, Current Card: {self.current_card}, Remaining Cards: {list(self.cards)})"

# Define Environment
class LabyrinthEnv:
    def __init__(self, board):
        self.board = board
        self.player = None
        self.last_exit_position = None  # Track the last exit position
        self.reset()

    def reset(self):
        # Create the deck of 24 tokens
        all_tokens = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']

        # Shuffle the deck
        random.shuffle(all_tokens)

        # Split the deck evenly among the four players
        cards_player_1 = all_tokens[:6]
        cards_player_2 = all_tokens[6:12]
        cards_player_3 = all_tokens[12:18]
        cards_player_4 = all_tokens[18:]

        # Initialize the players with their starting positions and cards
        player_1 = Player(id=1, start_position=(0, 0), cards=cards_player_1)
        player_2 = Player(id=2, start_position=(0, 6), cards=cards_player_2)
        player_3 = Player(id=3, start_position=(6, 0), cards=cards_player_3)
        player_4 = Player(id=4, start_position=(6, 6), cards=cards_player_4)

        # Store players in the environment
        self.players = [player_1, player_2, player_3, player_4]
        self.last_exit_position = None

    def add_player(self, player):
        self.players.append(player)

    def step(self, player_id, action):
        # Handle the action (push tile, move player)
        if action['type'] == 'push':
            self.handle_push(action)
        elif action['type'] == 'move':
            self.handle_move(action)

    def handle_push(self, action):
        direction = action['direction']
        push_position = action['position']

        # Check if the push is valid
        if self.is_invalid_push(direction, push_position):
            raise ValueError("Invalid push location: No pushback allowed.")

        # Perform the push and update the last exit position
        exit_position = self.board.push_tile(direction, push_position)
        self.last_exit_position = (direction, exit_position)

    def is_invalid_push(self, direction, push_position):
    # Check if the push is at the last exit position
        if self.last_exit_position:
            last_direction, last_position = self.last_exit_position
            if last_position == push_position:
                if (last_direction == 'left' and direction == 'right') or \
                (last_direction == 'right' and direction == 'left') or \
                (last_direction == 'up' and direction == 'down') or \
                (last_direction == 'down' and direction == 'up'):
                    return True
        return False

    def handle_move(self, action):
        new_position = action['new_position']
        player = self.get_player_by_id(action['player_id'])
        if player and self.is_valid_move(player.position, new_position):
            player.move_piece(new_position)
            tile = self.board.tiles[new_position[0]][new_position[1]]
            if tile.token:
                player.collect_token(tile.token)

    def get_valid_moves(self, start_position):
        def in_bounds(position):
            return 0 <= position[0] < self.board.size and 0 <= position[1] < self.board.size

        def has_open_path(from_tile, to_tile, direction):
            opposite_direction = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
            return from_tile.get_open_paths()[direction] and to_tile.get_open_paths()[opposite_direction[direction]]

        # Directions for movement
        directions = {
            (-1, 0): 'up',
            (1, 0): 'down',
            (0, -1): 'left',
            (0, 1): 'right'
        }

        valid_moves = set()
        stack = [start_position]
        visited = set()

        while stack:
            current_row, current_col = stack.pop()
            if (current_row, current_col) in visited:
                continue

            visited.add((current_row, current_col))
            valid_moves.add((current_row, current_col))

            # Explore neighbors
            for move_vector, direction in directions.items():
                next_row, next_col = current_row + move_vector[0], current_col + move_vector[1]

                if not in_bounds((next_row, next_col)):
                    continue

                if (next_row, next_col) in visited:
                    continue

                if has_open_path(self.board.tiles[current_row][current_col], self.board.tiles[next_row][next_col], direction):
                    stack.append((next_row, next_col))

        return valid_moves

    def is_valid_move(self, current_position, target_position):
        valid_moves = self.get_valid_moves(current_position)
        return target_position in valid_moves


    def get_player_by_id(self, player_id):
        for player in self.players:
            if player.id == player_id:
                return player
        return None
    
    def render(self):
        self.board.visualize_board(self.players) 
        for player in self.players:
            print(f"Player {player.id} Location: {player.position}")
            print(f"Player {player.id}'s current card: {player.current_card if player.current_card else 'No more cards'}")

    def is_done(self):
        return all(len(player.cards) == 0 for player in self.players)

