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

from app.user_management import bp
from app.user_management import views as v


bp.add_url_rule("/list", view_func=v.list_)
bp.add_url_rule("/add", view_func=v.add_user, methods=['GET', 'POST'])
bp.add_url_rule("/<int:id>/profile", view_func=v.profile)
bp.add_url_rule("/<int:id>/logout_all_sessions", view_func=v.logout_all_sessions)
bp.add_url_rule("/<int:id>/edit_profile", view_func=v.edit_profile, methods=['GET', 'POST'])
bp.add_url_rule("/<int:id>/changepwd", view_func=v.change_password, methods=['GET', 'POST'])
bp.add_url_rule("/<int:id>/suspend", view_func=v.suspend_user)
bp.add_url_rule("/<int:id>/activate", view_func=v.activate_user)
bp.add_url_rule("/<int:id>/delete", view_func=v.delete_user)
bp.add_url_rule("/<int:id>/impersonate", view_func=v.impersonate_user)

bp.add_url_rule("/<int:id>/roles/list", view_func=v.list_roles)
bp.add_url_rule("/<int:id>/roles/add", view_func=v.add_roles, methods=['GET', 'POST'])
bp.add_url_rule("/<int:user_id>/roles/edit/<int:role_id>", view_func=v.edit_role, methods=['GET', 'POST'])
bp.add_url_rule("/<int:user_id>/roles/delete/<int:role_id>", view_func=v.delete_role)

bp.add_url_rule("/_utilities/confirm", view_func=v.confirmation_page)