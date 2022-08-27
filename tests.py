# This file is part of MyPHP.

# MyPHP is free software: you can redistribute it and/or modify it under 
# the terms of the GNU General Public License as published by the Free 
# Software Foundation, either version 3 of the License, or (at your 
# option) any later version.

# MyPHP is distributed in the hope that it will be useful, but WITHOUT 
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License 
# for more details.

# You should have received a copy of the GNU General Public License along
# with MyPHP. If not, see <https://www.gnu.org/licenses/>. 

from datetime import datetime, timedelta
import unittest
import time

from app import create_app
from app import db
from app.models import User, Announcement, ReloginToken, Role
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class Trait():
    def setUp(self):
        """setUp 
        
        This method sets up environment for each test.
        """
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

class UserModelCase(unittest.TestCase, Trait):
    def setUp(self):
        """setUp 
        
        This method sets up environment for each test.
        """
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        """test_password_hashing 
        
        Test Werkezug Password Hashing
        """
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_password_reset(self):
        """test_password_reset 
        
        Test Werkezug Password Reset
        """
        u = User(username='susan')
        u.set_password('cat')
        self.assertTrue(u.change_password("cat", "dog"))
        self.assertFalse(u.change_password("bat", "dogh"))

        self.assertTrue(u.check_password('dog'))
        self.assertFalse(u.check_password('cat'))
        self.assertFalse(u.check_password('dogh'))

    def test_random_uids(self):
        u = User(username='susan')
        u.set_password('cat')
        u.generate_uid()
        uid = u.unique_id

        db.session.add(u)
        db.session.commit()

        self.assertTrue(User.query.filter_by(unique_id="unique").first() == None)
        self.assertTrue(User.query.filter_by(unique_id=uid).first() == u)

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_empty_gravatar(self):
        u = User(username='john')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'default?d=identicon&s=128'))

    def test_user_roles(self):
        u = User(username='ss')
        db.session.add(u)
        db.session.commit()
        r = Role(category="us", scope="ss", user=u)
        r = Role(category="ts", scope="st", user=u)
        db.session.add(r)
        db.session.commit()
        self.assertEqual(["us:ss", "ts:st"], u.get_roles())
        self.assertNotEqual(["us:ss", "ts:st"][::-1], u.get_roles())
    
    def test_user_suspended(self):
        u = User(username='__system')
        db.session.add(u)
        db.session.commit()
        u2 = User(username='system')
        db.session.add(u2)
        db.session.commit()
        u3 = User(username='_system')
        db.session.add(u2)
        db.session.commit()
        self.assertTrue(u.is_suspended())
        self.assertFalse(u2.is_suspended())
        self.assertFalse(u3.is_suspended())


class AnnouncementModelCase(unittest.TestCase, Trait):
    def setUp(self):
        """setUp 
        
        This method sets up environment for each test.
        """
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_chronological_annc(self):
        """test_chronological_annc 
        
        Tests if announcements are arranged chronologically.
        """
        a1 = Announcement(title="Dummy", body="ss")
        db.session.add(a1)
        db.session.commit()
        time.sleep(0.05)
        a2 = Announcement(title="Dummy2", body="ss")
        db.session.add(a2)
        db.session.commit()
        self.assertTrue(Announcement.get_all()[0] == a2)
        self.assertTrue(Announcement.get_all()[1] == a1)


class TestRLToken(unittest.TestCase, Trait):
    def setUp(self):
        """setUp 
        
        This method sets up environment for each test.
        """
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_rlt_generation(self): 
        rlt = ReloginToken()
        self.assertNotEqual(rlt.token, None)

    def test_rlt_validitychk(self):
        rlt = ReloginToken(
            ipaddr = "123.122.12.12",
            user_agent = "birefos"
        )
        db.session.add(rlt)
        db.session.commit()
        self.assertTrue(rlt.check("123.122.12.12", "birefos"))
        self.assertFalse(rlt.check("123.122.1.12", "birefos"))
        self.assertFalse(rlt.check("123.122.1.12", "firefox"))
        self.assertFalse(rlt.check("123.122.12.12", "firefox"))
        

    def test_rlt_timevc(self):
        future = datetime.utcnow() - timedelta(minutes=55)
        # breakpoint()
        rlt = ReloginToken(
            ipaddr = "123.122.12.12",
            user_agent = "birefos",
            created_on=future
        )
        self.assertFalse(rlt.check("123.122.1.12", "birefos"))

if __name__ == '__main__':
    unittest.main(verbosity=2)