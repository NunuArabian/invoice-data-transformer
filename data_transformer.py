import pandas as pd
import pickle

with open('invoices_new.pkl', 'rb') as f:
    invoices_data = pickle.load(f)

def convert_type(type_id):
    type_conversion = {0: 'Material', 1: 'Equipment', 2: 'Service', 3: 'Other'}
    return type_conversion.get(type_id, 'Unknown')

data = []
for invoice in invoices_data:
    invoice_id = invoice['id']
    try:
        invoice_id = int(invoice_id)
    except ValueError:
        pass  
    try:
        created_on = pd.to_datetime(invoice['created_on'])
    except (ValueError, pd.errors.ParserError):
        continue  
    items = invoice.get('items', [])  
    for item in items:
        invoiceitem_id = item['item']['id']
        invoiceitem_name = item['item']['name']
        type_id = item['item']['type']
        invoiceitem_type = convert_type(type_id)
        unit_price = item['item']['unit_price']
        try:
            quantity = int(item['quantity'])
        except (ValueError, TypeError):
            continue  
        total_price = unit_price * quantity
        quantities = [int(item['quantity']) for item in items if isinstance(item.get('quantity'), int)]
        if quantities:
            percentage_in_invoice = total_price / sum(item['item']['unit_price'] * quantity for item, quantity in zip(items, quantities))
        else:
            percentage_in_invoice = 0  
        data.append([invoice_id, created_on, invoiceitem_id, invoiceitem_name, invoiceitem_type, unit_price, total_price, percentage_in_invoice])

columns = ['invoice_id', 'created_on', 'invoiceitem_id', 'invoiceitem_name', 'type', 'unit_price', 'total_price', 'percentage_in_invoice']
df = pd.DataFrame(data, columns=columns)

df.to_csv('output_invoices.csv', index=False)

print("Data transformation completed. Output saved to 'output_invoices.csv'.")
