# api/submit.py
import os
import csv
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# 创建 Flask app
app = Flask(__name__)
CORS(app)

# CSV 文件路径（Vercel 支持写入 /tmp 目录）
CSV_PATH = "/tmp/feedback.csv"

def init_csv():
    """初始化 CSV 文件（如果不存在）"""
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['时间', '姓名', '意见内容', '类型'])

@app.route('/api/submit', methods=['POST'])
def submit_feedback():
    try:
        init_csv()
        
        data = request.json
        name = data.get('name', '')
        content = data.get('content', '')
        category = data.get('category', '建议')
        
        if not content.strip():
            return jsonify({"error": "意见内容不能为空"}), 400
        
        # 写入 CSV
        with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), name, content, category])
        
        return jsonify({"message": "提交成功！"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/download')
def download_csv():
    """提供 CSV 下载（方便你导出数据）"""
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, 'r', encoding='utf-8') as f:
            csv_data = f.read()
        return csv_data, 200, {'Content-Type': 'text/csv', 'Content-Disposition': 'attachment; filename=bluefield_feedback.csv'}
    return "暂无数据", 404

# Vercel 需要这个 handler
def handler(event, context):
    return app(event, context)

# 增加 Web Server 启动逻辑
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))