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

from flask import escape
from flask_principal import PermissionDenied

from app.errors import bp

@bp.app_errorhandler(PermissionDenied)
def permission_denied_error(e):
    exc = []
    for need in e.args[0].needs:
        exc.append((need.method.title(), need.value))

    op = "<h1>403 Permission denied!!</h1>"
    op += "<p>The following permissions are required:</p><ul>"
    for ex in exc:
        op+=f"<li>{ex[0]}, {ex[1]}</li>"
    op+="</ul>"
    return op, 403

# @bp.app_errorhandler(404)
# def permission_denied_error(e):
#     return f"<h1>Error</h1><hr>{e}<br>{dir(e)}", 404