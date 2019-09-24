
 
import unittest
from app.models import Pitch, User, Comment
from app import db



class PitchTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the Movie class
    '''

    def setUp(self):
        '''
        Set up method that will run before every Test
        '''

        self.user_Sophy = User(username = 'Sophy', password = 'potato', email = 'sophy@ms.com')
        self.new_comment = Comment(comment_content = 'Awesome stuff', pitch_id = 12345, user_id=self.user_Sophy)
        self.new_pitch = Pitch(id=12345,pitch_title="First Pitch", content='Awesome pitch for stuff',category='Interview Pitch',author = self.user_Sophy,comments = self.new_comment)

    def tearDown(self):
        Pitch.query.delete()
        User.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_pitch.id,12345)
        self.assertEquals(self.new_pitch.pitch_title,'First Pitch')
        self.assertEquals(self.new_pitch.content,'Awesome pitch for stuff')
        self.assertEquals(self.new_pitch.category,"Interview Pitch")
        self.assertEquals(self.new_pitch.author,self.user_Sophy)
        self.assertEquals(self.new_pitch.comments,self.new_comment)

    def test_save_pitch(self):
        self.new_pitch.save_pitch()
        self.assertTrue(len(Pitch.query.all())>0)

    def test_get_pitch_by_id(self):

        self.new_pitch.save_pitch()
        got_pitches = Pitch.get_pitch(12345)
        self.assertTrue(len(got_pitches) == 1)