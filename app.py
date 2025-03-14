from flask import Flask, render_template, request, jsonify
from neo_db.query_graph import query, get_KGQA_answer, get_answer_profile
from KGQA.ltp import get_target_array

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index(name=None):
    return render_template('index.html', name=name)


@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')


@app.route('/KGQA', methods=['GET', 'POST'])
def KGQA():
    return render_template('KGQA.html')


@app.route('/get_profile', methods=['GET', 'POST'])
def get_profile():
    name = request.args.get('character_name')
    json_data = get_answer_profile(name)
    return jsonify(json_data)


@app.route('/KGQA_answer', methods=['GET', 'POST'])
def KGQA_answer():
    try:
        question = request.args.get('name')
        if not question:
            return jsonify({"error": "问题参数缺失"}), 400

        # 获取目标数组
        target_array = get_target_array(str(question))
        if not target_array:
            return jsonify({"error": "无法解析问题"}), 400

        # 获取 KGQA 答案
        json_data = get_KGQA_answer(target_array)
        if not json_data:
            return jsonify({"error": "未找到相关数据"}), 404

        return jsonify(json_data)
    except Exception as e:
        return jsonify({"error": f"处理问题时发生错误: {str(e)}"}), 500


@app.route('/search_name', methods=['GET', 'POST'])
def search_name():
    name = request.args.get('name')
    json_data = query(str(name))
    return jsonify(json_data)


@app.route('/get_all_relation', methods=['GET', 'POST'])
def get_all_relation():
    return render_template('all_relation.html')


if __name__ == '__main__':
    app.debug = True
    app.run()