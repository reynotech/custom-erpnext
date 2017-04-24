cur_frm.cscript['Make Sales Order'] = function() {
	frappe.model.open_mapped_doc({
		method: "reynotech.reynotech.saleorders.get_context",
		frm: cur_frm
	})
}