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

from flask_principal import Permission, RoleNeed

add_users = Permission(RoleNeed('admin.user_mgmt:add_users'))
view_profile = Permission(RoleNeed('admin.user_mgmt:view_user_profile'))
logout_user = Permission(RoleNeed('admin.user_mgmt:logout_user'))
change_user_pwd = Permission(RoleNeed('admin.user_mgmt:change_user_passwd'))
edit_profile = Permission(RoleNeed('admin.user_mgmt:edit_user_profile'))
list_users = Permission(RoleNeed('admin.user_mgmt:list_users'))
suspend_user = Permission(RoleNeed('admin.user_mgmt:suspend_user'))
activate_user = Permission(RoleNeed('admin.user_mgmt:activate_user'))
delete_user = Permission(RoleNeed('admin.user_mgmt:delete_user'))
impersonate_user = Permission(RoleNeed('admin.user_mgmt:impersonate_user'))

list_roles = Permission(RoleNeed('admin.user_mgmt:list_roles'))
add_roles = Permission(RoleNeed('admin.user_mgmt:add_roles'))
edit_roles = Permission(RoleNeed('admin.user_mgmt:edit_roles'))
delete_roles = Permission(RoleNeed('admin.user_mgmt:delete_roles'))