from flask import Flask, request, jsonify
from huggingface_hub import snapshot_download      
from flask_cors import CORS     
snapshot_download("llmware/slim-sql-tool", local_dir="/models/", local_dir_use_symlinks=False)
from llmware.agents import LLMfx

import mysql.connector

# 创建数据库连接
conn = mysql.connector.connect(
    host='localhost',         # 数据库主机
    user='root',      # 数据库用户名
    password='root',  # 数据库密码
    database='nba'   # 需要连接的数据库名
)


app = Flask(__name__)
CORS(app)  # 允许所有来源的跨域请求

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    query = data['question']
    
    # 调用你的语言模型
    schema = "CREATE TABLE player (ID text, name text, team text, score integer)"
    agent = LLMfx(verbose=True)
    answer = agent.sql(query, schema)

    # 创建一个游标对象
    cursor = conn.cursor()

    # 执行 SQL 查询
    cursor.execute(answer['llm_response'])

    # 获取结果
    results = cursor.fetchall()
    answer['sql_response'] = results
    for row in results:
        print(row)

    # 关闭游标和连接
    cursor.close()
    
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(port=5000)
