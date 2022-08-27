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

"""user_management module

This module deals with the user management of MyPHP.

It includes features such as:
#. Creating Users
#. Editing user profiles
#. Logging out all users
#. Role Management
and much more."""

from flask import Blueprint

# This is auth blueprint
bp = Blueprint('user_management', __name__)

from app.user_management import urls