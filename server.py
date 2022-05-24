from flask import Flask, render_template, url_for, request, redirect, session
import csv


app = Flask(__name__)
app.secret_key = 'SUPER_SECRET'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_pages(page_name):
    return render_template(page_name)


def write_to_csv(data):
    with open('database.csv', mode='a') as database:
        person = data['person']
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([person, email, subject, message])
        



@app.route('/submit_form', methods=['POST','GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()           
            session['data'] = data
            write_to_csv(data)
            return redirect(url_for('thankyou',data=data))
        except:
            return 'did not save to database'
    else:
        return "something came up"


# @app.route('/thankyou/<client>')
# def thankyou(client):
#     return render_template('thankyou.html', name=client)

@app.route('/thankyou')
def thankyou():
    data = request.args['data']
    data = session['data']['person']
    return render_template('thankyou.html', name=data)



# @app.route('/<username>/<int:post_id>')
# def web_pages(username='J', post_id=0):
#     return render_template("hi.html", name=username, idd=post_id)

if __name__ == "__main__":
    app.run(debug=True)