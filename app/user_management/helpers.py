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

from app.user_management import views as v

ACTION_MAPPING = {
    "roles:delete": "user_management.delete_role",
    "user_management:suspend_user": "user_management.suspend_user",
    "user_management:delete_user": "user_management.delete_user"
}

MESSAGE_MAPPING = {
    "roles:delete": "Are you sure you want to delete the role?",
    "user_management:suspend_user": ("Are you sure you want to "
                                     "suspend this user?"),
    "user_management:delete_user": "Delete user?"
}