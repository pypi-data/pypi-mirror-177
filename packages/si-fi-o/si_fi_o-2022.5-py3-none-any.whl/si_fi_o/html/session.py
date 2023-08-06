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

import dominate.tags as html
import flask as flsk

from si_fi_o.generic import URLOfPath
from si_fi_o.session.form import file_t, form_t
from si_fi_o.session.session import session_t


def SessionInputsAsHTML(
    session: session_t | None,
    session_id: str,
    /,
    *,
    save_fname: str = "SaveSession",
    load_fname: str = "LoadSession",
) -> html.html_tag:
    """"""
    output = html.div(_class="container")

    empty_form = form_t()
    file_fields = empty_form.file_fields
    field_names_to_labels = empty_form.fields_to_labels

    if (is_none := (session is None)) or session.is_empty:
        if is_none:
            session = {}
        save = None
    else:
        save = html.a(
            html.button(
                "Save Session",
                _class="btn btn-primary",
                style="margin-right:24pt; margin-top: 12pt; margin-bottom: 24pt",
            ),
            href=flsk.url_for("." + save_fname, session_id=session_id),
        )
    load = _SessionLoadingForm(session_id, load_fname)

    row = None
    for idx, (name, label) in enumerate(field_names_to_labels.items()):
        value = session.get(name, "")
        if isinstance(value, file_t):
            value = value.name
        elif isinstance(value, str) and (value.__len__() > 0) and (name in file_fields):
            # The value has been assigned by a session loading, which does not produce valid form file fields
            value = html.span(
                f"{value} (must be re-uploaded)",
                style="color:Crimson; font-weight:bold",
            )

        if idx % 2 == 0:
            if row is not None:
                output.add(row)
            row = html.div(_class="row")
        row.add(html.div(f"{label}: ", value, _class="col"))

    if row is not None:
        output.add(row)

    table = html.table()
    with table:
        with html.tr():
            if save is not None:
                html.td(save)
            html.td(load)
    output.add(table)

    return output


def SessionOutputsAsHTML(session: session_t, /) -> html.html_tag | None:
    """
    Dummy version. Actual version is specific to the project.
    Needs to be kept in sync with the processing function since it assigns the outputs.
    """
    if session.outputs is None:
        return None

    return None


def SessionManagementAsHTML(
    session: session_t,
    session_id: str,
    /,
    *,
    delete_fname: str = "DeleteSession",
) -> html.html_tag | None:
    """"""
    if session is None:
        return None

    if (path := session.outputs_path) is None:
        output_url = None
    else:
        # URLOfPath(path) -> str(path)
        output_url = str(path)

    output = html.div()
    with output:
        if output_url is not None:
            html.a(
                html.button(
                    "Download Result",
                    type="button",
                    _class="btn btn-primary",
                    style="margin-top: 8pt; margin-bottom: 12pt",
                ),
                href=output_url,
                download="",
            )
            html.span(style="margin-right:48pt")
        html.a(
            html.button(
                html.b("Clear All Data"),
                type="button",
                _class="btn btn-primary",
                style="margin-top: 8pt; margin-bottom: 12pt",
            ),
            href=flsk.url_for("." + delete_fname, session_id=session_id),
        )

    return output


def _SessionLoadingForm(session_id: str, load_fname: str, /) -> html.form:
    """"""
    output = html.form(
        role="form",
        method="post",
        enctype="multipart/form-data",
        action=flsk.url_for("." + load_fname, session_id=session_id),
        style="margin-bottom: 12pt",
    )

    with output:
        html.label("Load Session")
        html.input_(
            type="file",
            name="session",
            required=True,
            _class="btn btn-primary",
            style="margin-top: 12pt; margin-bottom: 12pt",
        )
        html.input_(
            type="submit",
            name="submit",
            value="Validate",
            _class="btn btn-primary",
            style="margin-top: 12pt; margin-bottom: 12pt",
        )

    return output
