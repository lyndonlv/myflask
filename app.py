from importlib.resources import contents
from multiprocessing import context
import re
from flask import Flask, jsonify, url_for, request, redirect
from flask import render_template
import config

app = Flask(__name__)
app.config.from_object(config)

books = [
    {"id": 1, "name": "水浒传"},
    {"id": 2, "name": "西厢记"},
    {"id": 3, "name": "三国演义"},
    {"id": 4, "name": "红楼梦"},
]

# string: 默认的数据类型，接受没有任何斜杠/的字符串。
# int: 整形
# float: 浮点型。
# path： 和string类似，但是可以传递斜杠/。
# uuid： uuid类型的字符串。
# any：可以指定多种路径，这个通过一个例子来进行说明:


@app.route("/book/<int:book_id>", methods=["POST"])  # int string float
def book_detail(book_id):
    for book in books:
        if book_id == book["id"]:
            return book
    return "没有找到ID为{}的图书！".format(book_id)


@app.route("/book/list")
def book_list():
    for book in books:
        book["url"] = url_for("book_detail", book_id=book["id"])
    return jsonify(books)   # jsonify相当于 json.dumps()


@app.route('/')
def index():
    return render_template('/index.html')


@app.route("/profile")
def profile():
    # 参数传递的两种方式 1、 book/1  2、book?id=1
    user_id = request.args.get("id")
    if user_id:
        return "用户个人中心"
    else:
        return redirect(url_for("index"))


@app.route("/about")
def about():
    context = {
        "username": "李佳琪",
        "age": 18,
        "books": ["红楼梦", "水浒传", "三国演义", "西游记"],
        "person":{"name":"lisi", "age":19}
    }
    return render_template("about.html", **context)
    

if __name__ == '__main__':
    app.run(debug=True)  # 修改模板路径 template_folder="模板路径"
