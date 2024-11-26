from wtforms.fields.core import Field


def disable_form_items(*obj: Field) -> None:
    for item in obj:
        if item.render_kw is None:
            item.render_kw = {}
        item.render_kw.update({"disabled": "disabled"})
