# Tutorial 6 - Dashboard Stats

Currently, there are still several parts of our application which only have static data in them, which we will now fix.

## The Main Page Data Card

To make the top data card on our homepage accurately reflect our fields, we need to calculate:
 - The number of fields
 - The total farmed area
 - The main crop being grown
 - The expected revenue from all the fields

### Number of Fields

Getting the number of fields can be done with a Jinja *filter* which looks like this:

```html
<li>Number of Fields: {{ context.fields | length }}</li>
```

This simply takes the array `context.fields` and returns the length of the array.

### Using List Comprehensions

First, add `from statistics import mode` to the top of your `main.py` file.

For total farmed area, expected revenue, and main crop, we will calculate this on the backend using *list comprehensions* by making our context look like this:

```python
context = {
    "title": "Home",
    "fields": fields,

    "total_area": sum([field.area for field in fields]),
    "total_value": sum([field.area * field.crop_rel.value * field.crop_rel.targetYield for field in fields]),
    "main_crop": mode([field.crop_rel.name for field in fields]),
}
```

This, in each case, used the format `[ <expression> for <variable name> in <list> ]` to create a new list from an old list. We can then sum the new list, take its mode, or pass it to any other expression or function we like. This is equivalent to the code:

```python
total_area = 0
total_value = 0
field_crops = []
for field in fields:
    total_area += field.area
    total_value += field.area * field.crop_rel.value * field.crop_rel.targetYield
    field_crops.append(field.crop_rel.name)

context = {
    "title": "Home",
    "fields": fields,
    "total_area": total_area,
    "total_value": total_value,
    "main_crop": mode(field_crops)
}
```

We can now use these new items in our HTML code on the main page:

```html
<section class="p-3 shadow col-md-6 rounded-2 mb-3">
  <div class="row">
    <h3>Basic Farm Info</h3>
    <ul class="col-8 ps-4">
      <li>Number of Fields: {{ context.fields | length }}</li>
      <li>Total Farmed Area: {{ context.total_area }} ha</li>
      <li>Main Crop: {{ context.main_crop }}</li>
      <li>Expected Revenue: £{{ "{:,.2f}".format(context.total_value) }}</li>
    </ul>
    <img src="{{ url_for('static', filename='Logo.png') }}" alt="Generica farms logo" class="logo col-4">
  </div>
</section>
```

## The Main Page Graph

We will also need to write some code to get the data of the crops we are growing for the chart section at the bottom of the main page, we will need:
 - The name of the crop,
 - The total amount of that crop which has been planted,
 - The expected yield of the crop,
 - The £/tonne value of the crop,
 - The total expected revenue of the crop

The code we will use to extract this information from the database is:

```python
# Aggregate totals by crop name across all fields.
# Structure:
# crop_totals = {
#   "Wheat": {"area": 12.5, "yield": 8.0, "value": 180.0},
#   ...
# }
crop_totals = {}
for field in fields:
    # First time we see this crop name, initialise its summary.
    if field.crop_rel.name not in crop_totals.keys():
        crop_totals[field.crop_rel.name] = {
            "area": field.area,
            "yield": field.crop_rel.targetYield,
            "value": field.crop_rel.value
        }
    else:
        # Otherwise, increment area under that crop.
        crop_totals[field.crop_rel.name]['area'] += field.area
```

We can then add that to our context dictionary as `crop_totals` and make it work with the chart we created in tutorial 2 by adding this to the top of our scripts block:

```html
<script id="fields-data" type="application/json">
  {{ context.crop_totals | tojson }}
</script>
```

Now the chart should be working, and we can make the data show up in our table with:

```html
<table class="table table-striped table-hover">
  <thead>
    <tr>
      <th>Crop</th>
      <th>Ha Sown</th>
      <th>Expected Yield</th>
      <th>£/tonne</th>
      <th>Total Revenue</th>
    </tr>
  </thead>
  <tbody>
    {% for crop, details in context.crop_totals.items() %}
      <tr>
        <td>{{ crop }}</td>
        <td>{{ details.area }} ha</td>
        <td>{{ details.yield }} T/ha</td>
        <td>£{{ "{:,.2f}".format(details.value) }}</td>
        <td>£{{ "{:,.2f}".format(details.area * details.value * details.yield) }}</td>
      </tr>
    {% endfor %}
  </tbody>
</table>
```

## Conclusion

In this session we covered how to perform some basic data processing on the data in our database using list comprehensions, sum, and mode. Next session we will cover some of the important pieces of legislation in the UK which you must adhere to when processing data. 
