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

from app.auth import bp
from app.auth import routes as r


bp.add_url_rule("/login", view_func=r.login, methods=['GET', 'POST'])
bp.add_url_rule("/changepwd", view_func=r.changepwd, methods=['GET', 'POST'])
bp.add_url_rule("/logout", view_func=r.logout)
bp.add_url_rule("/register", view_func=r.public_registration, methods=["GET", "POST"])
bp.add_url_rule("/register/<token>", view_func=r.register, methods=['GET', 'POST'])
bp.add_url_rule("/relogin", view_func=r.reauth, methods=['GET', 'POST'])
bp.add_url_rule("/resetpwd", view_func=r.reset_password_request, methods=['GET', 'POST'])
bp.add_url_rule("/resetpwd/<token>", view_func=r.reset_password, methods=['GET', 'POST'])