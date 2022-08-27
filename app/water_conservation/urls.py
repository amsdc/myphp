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

from app.water_conservation import bp
from app.water_conservation import views as v


bp.add_url_rule("/", view_func=v.index)
bp.add_url_rule("/evaluate/new", view_func=v.new_evaluation, methods=['GET', 'POST'])
bp.add_url_rule("/leaderboard", view_func=v.leaderboard)