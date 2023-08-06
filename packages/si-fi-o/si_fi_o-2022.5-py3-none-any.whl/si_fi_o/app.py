# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2022)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import datetime as dttm
import secrets as scrt
from pathlib import Path as path_t
from typing import Any, Callable

from flask import Flask as flask_app_t
from flask_bootstrap import Bootstrap as BootstrapFlask
from flask_session import Session as flask_session_t

from si_fi_o.routes import routes_t
from si_fi_o.session.session import session_t


# def FlaskApp(html_folder: str, /) -> flask_app_t:
#     """
#     Just for reference. The app must be created within the specific project in order to set the template folder.
#     """
#     return flask_app_t(__name__, template_folder=html_folder)


def ConfigureApp(
    app: flask_app_t,
    home_page_details: dict[str, Any],
    form_type: type,
    max_upload_size: int,
    ProcessSession: Callable[
        [session_t, str, path_t], tuple[tuple[Any, ...], path_t | None]
    ],
    ini_section: str,
    /,
    *,
    base_folder: str = "static",
) -> None:
    """
    max_upload_size: in megabytes
    """
    routes = routes_t(
        home_page_details=home_page_details,
        form_type=form_type,
        ProcessSession=ProcessSession,
        ini_section=ini_section,
        base_folder=base_folder,
    )
    routes.Configure(app)

    app.config.from_mapping(
        PREFERRED_URL_SCHEME="https",
        SESSION_TYPE="filesystem",
        PERMANENT_SESSION_LIFETIME=dttm.timedelta(hours=1),
        SESSION_FILE_DIR=routes.session_folder,
        SECRET_KEY=scrt.token_bytes(),
        MAX_CONTENT_LENGTH=max_upload_size * 1024 * 1024,
    )
    flask_session_t(app)

    BootstrapFlask(app)
