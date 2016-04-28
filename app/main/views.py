from flask import request, render_template, session, redirect, url_for, flash, make_response, send_file
from flask.ext.login import login_user, logout_user, current_user, login_required
from google.appengine.ext import ndb

from . import main
from ..models import User, PostText, DatastoreAvator, DatastoreFile
# from .. import db

import math

@main.route('/', methods = ['GET'])
def index():
	if request.method == 'GET':
		user = current_user
		posts = ndb.gql("SELECT * FROM DatastoreFile WHERE haveExchange=false ORDER BY time_stamp DESC LIMIT 8").fetch()

		qryExchange = "SELECT * FROM DatastoreFile WHERE haveExchange=false AND eOrd='exchange' ORDER BY time_stamp DESC LIMIT 8"
		postsExchange = ndb.gql(qryExchange).fetch()
		qryDonate = "SELECT * FROM DatastoreFile WHERE haveExchange=false AND eOrd='donate' ORDER BY time_stamp DESC LIMIT 8"
		postsDonate = ndb.gql(qryDonate).fetch()

		avatorQry = "SELECT user_email FROM DatastoreAvator"
		Result = ndb.gql(avatorQry).fetch()
		avatorResult = [item.user_email.encode("utf-8") for item in Result]

		return render_template('index.html', user=user, posts=posts, postsExchange=postsExchange, postsDonate=postsDonate, avatorResult=avatorResult)

@main.route('/user_account/<username>', methods = ['GET'])
def user_account(username):
	result = User.query(User.name == username).fetch()
	if result is None:
		abort(404)
	else:
		user = result[0]
	posts = ndb.gql("SELECT * FROM DatastoreFile WHERE user_email =:user_email ORDER BY time_stamp DESC", user_email = user.email).fetch()

	avatorQry = "SELECT user_email FROM DatastoreAvator"
	avatorQryResult = ndb.gql(avatorQry).fetch()
	avatorResult = [item.user_email.encode("utf-8") for item in avatorQryResult]

	buyerQry = "SELECT buyer_email FROM DatastoreFile WHERE user_email='%s'" % (user.email)
	buyerQryResult = ndb.gql(buyerQry).fetch()
	buyerResult = [item.buyer_email.encode("utf-8") for item in buyerQryResult]

	return render_template('userAccount.html', user=user, posts=posts, avatorResult=avatorResult, buyerResult=buyerResult)

# @main.route('/user_account', methods = ['GET'])
# def user_account():
# 	return render_template('userAccount.html')

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
	if request.method == 'POST':
		post_image = request.files.get("itemImage")
		header = post_image.headers['Content-Type']
		data = post_image.read()
		imageName = post_image.filename

		itemName = request.form.get("itmeName")
		estimateValue = request.form.get("estimateValue")
		description = request.form.get("description")
		category = request.form.get("categoryOptions")
		eOrd = request.form.get("eOrdOptions")

		post = DatastoreFile()
		post.image = data
		post.imagename = imageName
		post.minetype = header

		post.itemName = itemName
		post.estimateValue = estimateValue
		post.description = description
		post.user_email = current_user.email
		post.user_name = current_user.name
		post.user_avator_link = current_user.avator_link
		post.category = category
		post.eOrd = eOrd
		post.put()
		image_link = url_for('main.itemImage', id=post.key.id(), _external=True)
		post.image_link = image_link
		post.put()

		current_user.postItem.append(post)
		current_user.put()
		# return redirect(url_for('main.upload'))
		return redirect(url_for('main.product', id = post.key.id()))
	return render_template('upload.html')

@main.route('/itemImage/<id>', methods = ['GET'])
def itemImage(id):
	result = DatastoreFile.get_by_id(int(id))
	if result:
		entity = result
		response = make_response(entity.image)
		response.headers['Content-Type'] = entity.minetype
		response.headers['Content-Disposition'] = "attachment; filename='%s'" % (entity.imagename)
		return response
	else:
		return abort(404)
	# return result

@main.route('/upload/avator', methods = ['POST'])
@login_required
def upload_avator():
	upload_image = request.files.get('avator')
	user_email = current_user.email

	header = upload_image.headers['Content-Type']
	data = upload_image.read()
	filename = upload_image.filename

	entity = DatastoreAvator(key = ndb.Key(DatastoreAvator, user_email))
	entity.data = data
	entity.filename = filename
	entity.minetype = header
	entity.user_email = user_email
	entity.put()
	image_url = url_for('main.image', useremail=current_user.email, _external=True)
	entity.avator_link = image_url
	entity.put()

	current_user.avator = entity
	current_user.avator_link = image_url
	current_user.put()
	return redirect(url_for('main.user_account', username=current_user.name))

@main.route('/image/<useremail>', methods = ['GET'])
def image(useremail):
	result = DatastoreAvator.query(DatastoreAvator.user_email == useremail).fetch()
	if result:
		entity = result[0]
		response = make_response(entity.data)
		response.headers['Content-Type'] = entity.minetype
		response.headers['Content-Disposition'] = "attachment; filename='%s'" % (entity.filename)
		return response
	else:
		return "no such image"

@main.route('/product/<id>', methods = ['GET', 'POST'])
def product(id):
	if request.method == 'POST':
		textBody = request.form.get("textBody")
		post = PostText()
		post.textBody = textBody
		post.author_email = current_user.email
		post.author_name = current_user.name
		post.author_avator_link = current_user.avator_link
		post.post_for_item = id
		post.put()

		current_user.postTexts.append(post)
		current_user.put()

	qry = "SELECT * FROM PostText WHERE post_for_item='%s' ORDER BY time_stamp DESC" % (id)
	postTexts = ndb.gql(qry).fetch()

	result = DatastoreFile.get_by_id(int(id))
	if result:
		postItem = result

	entity = DatastoreFile.get_by_id(int(id))
	recommendQry = "SELECT * FROM DatastoreFile WHERE category='%s' ORDER BY time_stamp DESC LIMIT 4" % (entity.category)
	recommends = ndb.gql(recommendQry).fetch()

	avatorQry = "SELECT user_email FROM DatastoreAvator"
	Result = ndb.gql(avatorQry).fetch()
	avatorResult = [item.user_email.encode("utf-8") for item in Result]

	return render_template('product.html', postItem=postItem, postTexts=postTexts, recommends=recommends, avatorResult=avatorResult)

@main.route('/productList/<pageNum>', methods=['GET'])
def productList(pageNum):
	itemSet = ndb.gql("SELECT * FROM DatastoreFile ORDER BY time_stamp DESC").fetch()
	totalItemNum = len(itemSet)
	itemPerPage = 4

	totalPage = int(math.ceil(totalItemNum/float(itemPerPage)))
	start_point = (int(pageNum)-1) * itemPerPage
	qry = "SELECT * FROM DatastoreFile ORDER BY time_stamp DESC LIMIT %d, %d" % (start_point, itemPerPage)
	postItem = ndb.gql(qry).fetch()

	avatorQry = "SELECT user_email FROM DatastoreAvator"
	Result = ndb.gql(avatorQry).fetch()
	avatorResult = [item.user_email.encode("utf-8") for item in Result]

	return render_template('productList.html', postItem=postItem, totalPage=totalPage, avatorResult=avatorResult)

@main.route('/productCategory/<category>/<pageNum>', methods = ['GET'])
def productCategory(category, pageNum):
	qryItemSet = "SELECT * FROM DatastoreFile WHERE category='%s' ORDER BY time_stamp DESC" % (category)
	itemSet = ndb.gql(qryItemSet).fetch()
	totalItemNum = len(itemSet)
	itemPerPage = 4

	totalPage = int(math.ceil(totalItemNum / float(itemPerPage)))
	start_point = (int(pageNum) - 1) * itemPerPage
	qry = "SELECT * FROM DatastoreFile WHERE haveExchange=false AND category='%s' ORDER BY time_stamp DESC LIMIT %d, %d" % (category, start_point, itemPerPage)
	postItem = ndb.gql(qry).fetch()

	avatorQry = "SELECT user_email FROM DatastoreAvator"
	Result = ndb.gql(avatorQry).fetch()
	avatorResult = [item.user_email.encode("utf-8") for item in Result]

	return render_template('productList.html', postItem=postItem, totalPage=totalPage, avatorResult=avatorResult)

@main.route('/productEorD/<eOrd>/<pageNum>', methods = ['GET'])
def productEorD(eOrd, pageNum):
	qryItemSet = "SELECT * FROM DatastoreFile WHERE eOrd='%s' ORDER BY time_stamp DESC" % (eOrd)
	itemSet = ndb.gql(qryItemSet).fetch()
	totalItemNum = len(itemSet)
	itemPerPage = 4

	totalPage = int(math.ceil(totalItemNum / float(itemPerPage)))
	start_point = (int(pageNum) - 1) * itemPerPage
	qry = "SELECT * FROM DatastoreFile WHERE haveExchange=false AND eOrd='%s' ORDER BY time_stamp DESC LIMIT %d, %d" % (eOrd, start_point, itemPerPage)
	postItem = ndb.gql(qry).fetch()

	avatorQry = "SELECT user_email FROM DatastoreAvator"
	Result = ndb.gql(avatorQry).fetch()
	avatorResult = [item.user_email.encode("utf-8") for item in Result]

	return render_template('productList.html', postItem=postItem, totalPage=totalPage, avatorResult=avatorResult)


@main.route('/userRateStatus/<useremail>', methods = ['GET'])
def userRateStatus(useremail):
	qry = User.query(User.key == ndb.Key(User, useremail))
	user = qry.fetch()[0]

	return user.rateScore


# @main.route('/about', methods = ['GET'])
# def about():
# 	return render_template('about.html')

# @main.route('/contact', methods = ['GET'])
# def contact():
# 	return render_template('contact.html')