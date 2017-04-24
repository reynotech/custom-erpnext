from __future__ import unicode_literals
import frappe
from erpnext.selling.doctype.quotation.quotation import _make_customer
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt

@frappe.whitelist()
def get_context(source_name, target_doc=None):
    return _make_sales_order(source_name, target_doc)


def _make_sales_order(source_name, target_doc=None, ignore_permissions=False):
    customer = _make_customer(source_name, ignore_permissions)

    def set_missing_values(source, target):
        if customer:
            target.customer = customer.name
            target.customer_name = customer.customer_name
        target.ignore_pricing_rule = 1
        target.flags.ignore_permissions = ignore_permissions
        target.run_method("set_missing_values")
        target.run_method("calculate_taxes_and_totals")

    def update_item(obj, target, source_parent):
        target.stock_qty = flt(obj.qty) * flt(obj.conversion_factor)

    quote = frappe.get_doc("Quotation", source_name).as_dict()

    doclist = get_mapped_doc("Quotation", source_name, {
            "Quotation": {
                "doctype": "Sales Order",
                "validation": {
                    "docstatus": ["=", 1]
                }
            },
            "Quotation Item": {
                "doctype": "Sales Order Item",
                "field_map": {
                    "parent": "prevdoc_docname"
                },
                "postprocess": update_item
            },
            "Sales Taxes and Charges": {
                "doctype": "Sales Taxes and Charges",
                "add_if_empty": True
            },
            "Sales Team": {
                "doctype": "Sales Team",
                "add_if_empty": True
            }
        }, target_doc, set_missing_values, ignore_permissions=ignore_permissions)

    list = doclist.as_dict()

    list['source_name'] = source_name
    list['deliver_unit'] = quote['deliver_unit']
    list['deliver_number'] = quote['deliver_number']
    list['creating_from_quote'] = True

    return list