# Tutorial 3 - Creating the Field View

In this tutorial we will cover creating a new route for viewing a field in more depth and how to connect to an external API to collect and then process data about rainfall from DEFRA's weather service.

## Creating the Page

The code for the page can be found in `view.html` in this folder. It is currently populated with dummy data but we will populate it with real data later on in this series of classes. We will also be filling in the data for the chart later on in this tutorial.

## Creating the Route

We will create a route so we can actually see this page by appending this to the `main.py` file we created previously:

```python
@app.route('/field/<field_id>')
def field_view(field_id):
    context = {"title": "North Field"}
    return render_template('view.html', context=context)
```

We can see that here we have a URL parameter called `field_id`, which is a unique identifier for the field we are displaying which can be looked up in the database once we have created it. This identifier will have the format F-XXXX where X is a digit between 1 and 9. 

## Connecting to the API

Let's now look at how we can actually put a graph where the graph is supposed to be.

First, append the following to *view.html*:

```
{% block scripts %}
<script src="{{ url_for('static', filename='rainfall_chart.js') }}"></script>
{% endblock %}
```

And create the relevant js file, called `rainfall_chart.js` in *static*, the code for which can be found in `rainfall_chart.js` in this folder.

How this file's code works will be covered in depth in the in-person session but, in brief, it does the following:
 - It calculates the date as of 14 days ago from now and then queries a URL which responds with data about rainfall from a weather station from that date until now,
 - The data, which comes in 15-minute intervals, is grouped by day into a data structure to get a list of days and the corresponding amount of rainfall they had,
 - That data structure is then passed to an object called `Chart` which creates the chart and puts it into the HTML element with the ID `fieldChart`

## Conclusion

In this tutorial we have covered how to create a page to display a wide variety of information about a field, and how to query an external API for information about rainfall. In the next tutorial we will cover the basic principles of designing and using a database.
