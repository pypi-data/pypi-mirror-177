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
from pathlib import Path as path_t
from typing import Any
from typing import NamedTuple as named_tuple_t

import wtforms as wtfm
from flask_wtf import FlaskForm as flask_form_t
from werkzeug.utils import secure_filename as SecureFilenameVersion


validators_t = wtfm.validators


class file_t(named_tuple_t):
    name: str
    path: path_t


class form_t(flask_form_t):
    """"""

    submit = wtfm.SubmitField(label="Launch Processing")

    @property
    def fields_to_labels(self) -> dict[str, str]:
        """"""
        output = {}

        for name in self.__dict__:
            attribute = getattr(self, name)
            if _ElementIsInputField(attribute):  # Not all elements are fields
                # Fields might not have a label (at least it does not cost much to check)
                if hasattr(attribute, "label"):
                    output[name] = attribute.label.text
                else:
                    output[name] = name

        return output

    @property
    def file_fields(self) -> tuple[str, ...]:
        """"""
        output = []

        for name in self.__dict__:
            if isinstance(getattr(self, name), wtfm.FileField):
                output.append(name)

        return tuple(output)

    def Update(self, session: dict[str, Any], /) -> None:
        """"""
        for field, value in session.items():
            if not isinstance(value, file_t):
                getattr(self, field).process_formdata((value,))

    def Submission(
        self,
        upload_folder: str | path_t,
        /,
    ) -> dict[str, Any]:
        """"""
        output = {}

        if isinstance(upload_folder, str):
            upload_folder = path_t(upload_folder)
        upload_folder.mkdir(exist_ok=True)
        time_stamp = (
            dttm.datetime.now()
            .isoformat(timespec="microseconds")
            .translate(str.maketrans(":.", "--"))
        )

        for name in self.__dict__:
            attribute = getattr(self, name)

            if _ElementIsInputField(attribute):
                data = attribute.data
                if isinstance(attribute, wtfm.FileField):
                    if (filename := data.filename) == "":
                        output[name] = None
                    else:
                        secure = SecureFilenameVersion(filename)
                        path = upload_folder / f"{time_stamp}-{secure}"
                        data.save(path)
                        output[name] = file_t(name=filename, path=path)
                else:
                    output[name] = data

        return output


def _ElementIsInputField(element: Any, /) -> bool:
    """"""
    return isinstance(element, wtfm.Field) and not isinstance(
        element, (wtfm.HiddenField, wtfm.SubmitField)
    )
