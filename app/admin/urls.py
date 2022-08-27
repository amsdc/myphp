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

from app.admin import bp
from app.admin import routes as r


# bp.add_url_rule("/", view_func=r.determine_home)
bp.add_url_rule("/dashboard", view_func=r.index)
bp.add_url_rule("/", view_func=r.index)
# bp.add_url_rule("/ft", view_func=r.flash_test)