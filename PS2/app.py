from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Retrieve the name from the form
        name = request.form.get('name', '')
        # Check if the name is not empty
        if name:
            # Render the personalized greeting page
            return render_template('greeting.html', name=name)
    # Render the initial content page with the form
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
