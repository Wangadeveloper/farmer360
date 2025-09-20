from flask import render_template, request, redirect, url_for, flash
from . import records_bp
from .forms import FarmRecordForm

# For now, store records in memory (later connect DB)
farm_records = []

@records_bp.route("/records", methods=["GET", "POST"])
def records():
    form = FarmRecordForm()
    if form.validate_on_submit():
        record = {
            "farm_type": form.farm_type.data,
            "name": form.name.data,
            "quantity": form.quantity.data,
            "notes": form.notes.data
        }
        farm_records.append(record)
        flash("Record saved!", "success")
        return redirect(url_for("records.records"))
    return render_template("records/records.html", form=form, records=farm_records)
