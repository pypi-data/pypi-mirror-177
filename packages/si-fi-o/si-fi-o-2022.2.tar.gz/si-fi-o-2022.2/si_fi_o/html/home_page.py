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

from typing import Callable

import dominate.tags as html
from flask import render_template as RenderHTML
from si_fi_o.html.session import SessionManagementAsHTML
from si_fi_o.session.form import form_t
from si_fi_o.session.session import session_t


def HomePage(
    session_id: str,
    /,
    *,
    session: session_t = None,
    form: form_t = None,
    html_template: str = "main.html",
    name: str = "Missing Name",
    name_meaning: str = "Missing Name Meaning",
    about: html.html_tag = None,
    SessionInputsAsHTML: Callable[[session_t, str], html.html_tag],
    max_file_size: int = 1,
    SessionOutputsAsHTML: Callable[[session_t], html.html_tag],
) -> str:
    """"""
    return RenderHTML(
        html_template,
        name=name,
        name_meaning=name_meaning,
        about=about,
        session=SessionInputsAsHTML(session, session_id),
        form=form,
        max_file_size=max_file_size,
        outputs=SessionOutputsAsHTML(session),
        data_management=SessionManagementAsHTML(session, session_id),
    )
