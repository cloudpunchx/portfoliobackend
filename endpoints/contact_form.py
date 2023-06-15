from app import app
from flask import make_response, jsonify, request
from helpers.dbhelpers import run_statement
from helpers.helpers import check_data

@app.post('/api/contact')
def contact_form():
    """
    Expects: name, email, message.
    Optional: company
    """
    required_data = ['name', 'email', 'message']
    check_result = check_data(request.json, required_data)
    if check_result != None:
        return check_result
    name = request.json.get('name')
    email = request.json.get('email')
    company = request.json.get('company')
    message = request.json.get('message')
    result = run_statement("CALL send_contact_form(?,?,?,?)", [name, email, company, message])
    if (type(result) == list):
        if result[0][0] == 1:
            return make_response(jsonify("Your message has been received and will be responded to shortly, thank you!"), 200)
        elif result[0][0] == 0:
            return make_response(jsonify("Something went wrong, please try again."), 500)
    else:
        return make_response(jsonify(result), 500)