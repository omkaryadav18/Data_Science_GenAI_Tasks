from flask import Flask, render_template, request
import re

app=Flask(__name__)

@app.route("/", methods=['GET','POST'])
def index():
    results=None
    test_string=""
    regex_pattern=""
    error=None

    if request.method == 'POST':
        test_string=request.form.get('test_string', '')
        regex_pattern=request.form.get('regex_pattern','')
    
        if regex_pattern:
            try:
                results=re.findall(regex_pattern,test_string)
            except re.error as e:
                error = f"Invalid Regex: {e}"
        else:
            error="Please enter a regular expression"
    
    return render_template('index.html',
                           results=results,
                           test_string=test_string,
                           regex_pattern=regex_pattern,
                           error=error)

if __name__=='__main__':
    app.run(debug=True)