if(cur_frm.doc.creating_from_quote) {
    cur_frm.set_value('delivery_date', frappe.datetime.add_days(new Date(), cur_frm.doc.deliver_number));
}