from Games.Game import *


class Game_Title(Game):
    def __init__(self, host_id):
        super().__init__(host_id)

    def process_how_to_play(self):
        how_to_play = super().process_how_to_play()
        list_how_to_play = how_to_play.split('-')
        header_how_to_play = list_how_to_play[0]
        footer_how_to_play = list_how_to_play[1]

        body_how_to_play = (
            'rule 1: \n'
            'rule 2: '
        )

        return header_how_to_play + body_how_to_play + footer_how_to_play
    
    def process_game(self):
        return super().process_game()
