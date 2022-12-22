
import json

print("Calculator Service running")

while True:
    new_request = False
    request_breakdown = None
    product_info = []
    material_cost = 0
    labor_cost = 0

    while new_request is False:
        with open("acctnotif.txt", "r+") as infile:
            request = infile.readline()
            if request.strip("\n") == "calculate":
                request_breakdown = json.loads(infile.readline())
                print(request_breakdown)
                infile.seek(0)
                infile.truncate(0)
                new_request = True
            if request.strip() == "terminate":
                infile.seek(0)
                infile.truncate(0)
                quit()

    for product in request_breakdown:
        product_info = request_breakdown[product]

    product_materials = product_info[0]["materials"]

    for material in product_materials:
        material_cost += float(product_materials[material])

    product_labor = product_info[1]["labor"]

    for labor in product_labor:
        labor_hours = float(labor)
        labor_wage = float(product_labor[labor])
        labor_cost += labor_hours * labor_wage

    product_markup = product_info[2]["percent_markup"]
    markup_modifier = (100 + float(product_markup)) / 100

    retail_price = (material_cost + labor_cost) * markup_modifier

    with open("acctnotif.txt", "w") as outfile:
        outfile.write(f"{retail_price}")

