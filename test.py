from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):

    def test_board_load(self):
        """Testing the homapage HTML is displayed and board is set"""
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn("board", session)
            self.assertIn('<h1>Boggle Game</h1>', html)
            self.assertIn('<tr id="4">', html)


    
    def test_check_word(self):
        """By setting up board srom session, we are testing /check-word route"""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['board'] = [['H', 'N', 'K', 'A', 'B'], 
                                 ['B', 'E', 'D', 'Z', 'L'], 
                                 ['H', 'E', 'L', 'L', 'O'], 
                                 ['U', 'W', 'T', 'J', 'Q'], 
                                 ['G', 'A', 'V', 'K', 'A']]
        response = client.get('/check-word?word=hello')
        self.assertEqual(response.json['result'], 'ok')   

        res = client.get('/check-word?word=wall')
        self.assertEqual(res.json['result'], 'not-on-board')   

        res = client.get('/check-word?word=hnkab')
        self.assertEqual(res.json['result'], 'not-word')  

