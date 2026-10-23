# Practice task: save the revised dashboard with the updated title.
from flight_delay import app
app.layout.children[0].children = 'Flight Details Statistics Dashboard'
app.layout.children[0].style['fontSize'] = 35
if __name__ == '__main__':
    app.run(debug=False)
