import frappe
from frappe.utils import getdate, today

@frappe.whitelist()
def calculate_values(record):
    doc = frappe.get_doc('Inpatient Record', record)
    discharge_date = today()
    total_paid = 0
    if doc.discharge_datetime:
        discharge_date = getdate(doc.discharge_datetime)
    
    pe_details = frappe.get_all('Payment Entry', {"posting_date": (
        "between",
		[doc.admission_ordered_for, discharge_date]), 
        'party': doc.customer}, ['name', 'posting_date', 'mode_of_payment', 'total_allocated_amount', 'unallocated_amount', 'reference_no'])
    si_details = frappe.get_all('Sales Invoice', {"posting_date": (
        "between",
		[doc.admission_ordered_for, discharge_date]), 
        'customer': doc.customer}, ['name'])

    item_group_wise_amt = {}
    total_bill = 0

    for pe in pe_details:
        total_paid += pe.total_allocated_amount

    for si in si_details:
       si_doc =  frappe.get_doc('Sales Invoice' , si['name'])
       total_bill += si_doc.grand_total
       for row in si_doc.items:
            if row.item_group not in item_group_wise_amt:
                item_group_wise_amt[row.item_group] = row.amount
            else:
                item_group_wise_amt[row.item_group] += row.amount
   
    return pe_details, item_group_wise_amt, total_bill, total_paid