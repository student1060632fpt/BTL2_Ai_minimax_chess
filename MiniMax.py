from Evaluation import Evalualtion

MAX, MIN = 100000, -100000

# Returns optimal value for current player
# (Initially called for root and maximizer)
def minimax_algorithm(depth_tree, maximizing_player, alpha_value, beta_value, board_state, first_move):

    # Terminating condition. i.e
    # leaf node is reached
    if (depth_tree == 0) or (board_state.is_game_over()):

        if maximizing_player:
            evaluate = Evalualtion(board_state, "W")
        else:
            evaluate = Evalualtion(board_state, "B")

        return evaluate.result()

    # All Code from here only runs if the tree has not yet reached the leaf node

    if maximizing_player:

        best = MIN
        # Recur for left and right children
        for i in board_state.legal_moves:

            board_state.push(i)

            if checkmate(board_state) and first_move:
                return i

            val = minimax_algorithm(depth_tree - 1, False, alpha_value, beta_value, board_state, False)
            board_state.pop()

            if val > best:
                best = val
                best_move_white = i

            alpha_value = max(alpha_value, best)

            # Alpha Beta Pruning
            if beta_value <= alpha_value:
                break

        if first_move:
            print(best_move_white)
            return best_move_white
        else:
            return best

    else:

        best = MAX
        for i in board_state.legal_moves:

            board_state.push(i)

            if checkmate(board_state) and first_move:
                return i

            val = minimax_algorithm(depth_tree - 1, True, alpha_value, beta_value, board_state, False)
            board_state.pop()

            if val < best:
                best = val
                best_move_black = i

            beta_value = min(beta_value, best)

            # Alpha Beta Pruning
            if beta_value <= alpha_value:
                break

        if first_move:
            return best_move_black
        else:
            return best

def checkmate(board_state):
    if board_state.is_checkmate():
        return True
    else:
        return False




