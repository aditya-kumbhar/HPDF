import requests,sys
from flask import Flask,json,jsonify,redirect,request,render_template,send_file,flash,session


app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route('/')
def index():
	return "Hello World- Aditya"

@app.route('/authors')
def fetch_auth():
	#fetch json data
	author_users= json.loads(requests.get('https://jsonplaceholder.typicode.com/users').content)
	author_posts= json.loads(requests.get('https://jsonplaceholder.typicode.com/posts').content)
	
	p_cnt = {}		#empty dictionary to store id: postcount
	resp_list='<h3>Author Name: Number of posts</h3><br>'	
	
	for a in author_posts:
		if a['userId'] in p_cnt:
			p_cnt[a['userId']]+=1		#increment count
		else:
			p_cnt[a['userId']]=1		#initialise dictionary key
	for a in author_users:
		resp_list+='<b>'+a['name']+'</b>: '+str(p_cnt[a['id']])+'<br>'
	return resp_list

@app.route('/setcookie')
def set_cookie():
	redirect_to_index = redirect('/')
	response = app.make_response(redirect_to_index)

	if 'name' not in request.cookies:
		response.set_cookie('name','Aditya')

	if 'age' not in request.cookies:
		response.set_cookie('age','20')
	
	return response

@app.route('/getcookies')
def get_cookies():
	if 'name' in request.cookies and 'age' in request.cookies:
		name= request.cookies.get('name')
		age= request.cookies.get('age')
		return "Name: "+name+"<br>Age: "+age
	else:
		return "No cookies set"
@app.route('/robots.txt')
def deny_req():
	return send_file('denied.txt')

@app.route('/html')
def static_doc():
	return render_template('hi.html')

@app.route('/image')
def ret_img():
	return send_file('change.png', mimetype='image/png')

@app.route('/input')
def input():
	# htmlbody='<form action="/logInput" method="post">Enter input: '
	# htmlbody+='<input type=text name="t1"><br>'
	# htmlbody+='<button type=submit>Submit</button></form>'
	return render_template('input.html')

@app.route('/logInput',methods=['POST','GET'])
def logInput():
	if(request.method=='POST'):
		inp=request.form['t1']
		print(inp, file=sys.stdout)
		flash('Input has been logged')
	return redirect('/input')


if(__name__=='__main__'):
	app.run(host='0.0.0.0',debug=False,port=8080)
