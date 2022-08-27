from flask_principal import Permission, RoleNeed

view_homepage = Permission(RoleNeed('admin.dashboard:view'))