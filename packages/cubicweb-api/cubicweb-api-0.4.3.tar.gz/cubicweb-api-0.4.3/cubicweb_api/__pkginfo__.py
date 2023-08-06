# pylint: disable=W0622
# -*- coding: utf-8 -*-
# copyright 2022 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""cubicweb-api application packaging information"""


modname = "cubicweb_api"
distname = "cubicweb-api"

numversion = (0, 4, 3)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "This cube is the new api which will be integrated in CubicWeb 4."
web = "https://forge.extranet.logilab.fr/cubicweb/cubes/api"

__depends__ = {
    "cubicweb": ">= 3.36.0",
    "PyJWT": ">= 2.4.0",
    "pyramid-openapi3": ">= 0.14",
    # force openapi-spec-validator to be in 0.4.x since the 0.5 breaks the API
    # and "pyramid-openapi3" is not (yet) compatible
    # TODO: update pyramid-openapi3 to be compatible with openapi-spec-validator@v0.5.x
    "openapi-spec-validator": ">= 0.4, < 0.5",
}
__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python :: 3",
    "Programming Language :: JavaScript",
]
