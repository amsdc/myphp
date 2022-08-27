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


from app import create_app, db
from app.models import User

# revision identifiers, used by Alembic.
revision = '4f1349b7b3e3'
down_revision = '197662c2765c'

print("Upgrading to changeable ids")

app = create_app()

with app.app_context():
    for usr in User.query.all():
        usr.generate_uid()
        print("Upgraded: ", usr)
        db.session.commit()