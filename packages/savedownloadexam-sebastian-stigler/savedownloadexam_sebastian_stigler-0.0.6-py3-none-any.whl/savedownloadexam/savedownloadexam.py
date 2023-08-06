import os
import unicodedata
from IPython.display import display, Javascript, clear_output
from ipywidgets import widgets


def js_rename_save_notebook(prefix):
    """
    creates javascript to rename, save and opens a new tab to download a jupyter notebook

    :param prefix: Prefix od the new name of the notebook
    """
    return """
function save_me() {

    var baseurl = location.protocol+"//"+location.host;
    var path = location.pathname.replace('/notebooks/', '/nbconvert/notebook/', 1)+"?download=true";
    var url = baseurl + path;
    var w = window.open('', IPython._target);
    if (Jupyter.notebook.dirty && Jupyter.notebook.writable) {
        Jupyter.notebook.save_notebook().then(function() {
            w.location = url;
        });
    } else {
        w.location = url;
    }
};

function rename_save(prefix) {
    var current_name = Jupyter.notebook.notebook_name;
    let base_name = Jupyter.notebook.metadata.savedownload?.base_name || "Exam";
    let new_name = prefix + "_" + base_name;
    Jupyter.notebook.metadata.submission = {'new_name': new_name};
    
    if (current_name.substring(0, current_name.length - 6) != new_name) {
        Jupyter.notebook.rename(new_name).then(function() {
            save_me();}
        );
    } else {
        save_me();
    }
};

rename_save('%s');
""" % (
        prefix
    )


def strip_accents(s):
    """remove accents from string"""
    umlautfree = (
        s.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    )
    umlautfree = umlautfree.replace("Ä", "Ae").replace("Ö", "Oe").replace("Ü", "Ue")
    return "".join(
        c
        for c in unicodedata.normalize("NFD", umlautfree)
        if unicodedata.category(c) != "Mn"
    )


class SaveDownloadExam:
    def __init__(self, *args, **kwargs):
        try:
            self.login_name = os.getlogin()
        except OSError:
            if "JUPYTERHUB_USER" in os.environ and os.environ["JUPYTERHUB_USER"]:
                self.login_name = os.environ["JUPYTERHUB_USER"]
            elif "USER" in os.environ and os.environ["USER"]:
                self.login_name = os.environ["USER"]
            else:
                self.login_name = "user"
        self.student_name = ""
        self.js = ""

    def _display_js(self, _=None):
        clear_output()
        display(Javascript(self.js))

    def build_notebook_prefix(self):
        student_name = self.student_name.title().replace(" ", "").replace("_", "")
        return "_".join(("Submission", self.login_name, strip_accents(student_name)))

    def run(self):

        output = widgets.Output(layout={"border": "1px solid black"})

        label1 = widgets.HTML(
            value="<h3>Please enter your full name and hit ENTER</h3>"
        )

        text = widgets.Text(
            value=self.student_name,
            placeholder="Type your first and last name here",
            disabled=False,
            layout=widgets.Layout(width="auto"),
        )

        button_edit = widgets.Button(
            tooltip="Edit Name",
            button_style="warning",
            icon="fa-edit",
            disabled=True,
            layout=widgets.Layout(width="40px"),
        )

        text_edit_button = widgets.GridBox(
            [text],
            layout=widgets.Layout(grid_template_columns="auto auto"),
        )

        label2_text = (
            "<p>Your name will be used in the filename as following:</p>"
            "<p><b>{}</b></p>"
        )

        label2 = widgets.HTML(value=label2_text.format(self.student_name))
        label3 = widgets.HTML(
            value=(
                "<h3>Are you ready to download this notebook for submission?</h3>"
                "<p>You can edit your name by clicking the edit button alongside the textbox for your name.</p>"
                "<p>If your name is correct and you want to download this notebook for submission, "
                "press the submit button below.</p>"
            )
        )

        layout = widgets.Layout(width="auto", height="40px")  # set width and height
        button_submit = widgets.Button(
            description="Save and Download Exam",
            icon="fa-download",
            button_style="success",
            display="flex",
            flex_flow="column",
            align_items="stretch",
            layout=layout,
        )

        def on_name_changed(change):
            self.student_name = strip_accents(change.new)
            notebook_name = self.build_notebook_prefix()
            self.js = js_rename_save_notebook(notebook_name)
            label2.value = label2_text.format(self.student_name)

        def on_submit_text(instance):
            text.disabled = True
            button_edit.disabled = False
            text_edit_button.children = text, button_edit
            with output:
                display(label3, button_submit)

        def on_edit(edit=None):
            output.clear_output()
            text.disabled = False
            button_edit.disabled = True
            text_edit_button.children = text,
            with output:
                display(label1, text_edit_button, label2)

        text.observe(on_name_changed, names="value")
        text.on_submit(on_submit_text)
        button_edit.on_click(on_edit)
        button_submit.on_click(self._display_js)

        clear_output()
        display(output)
        on_edit()
