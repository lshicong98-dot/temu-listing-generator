from flask import Flask, render_template, request, jsonify, send_file
from listing_generator import AIListingGenerator
import os
import csv
import io
import zipfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

generator = AIListingGenerator()
api_key = os.getenv('DEEPSEEK_API_KEY')
if api_key:
    generator.set_api_key(api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_listing():
    data = request.get_json()
    
    product_name = data.get('product_name', '')
    selling_points = data.get('selling_points', '')
    target_market = data.get('target_market', '')
    
    if not product_name:
        return jsonify({'error': '请输入商品名称'}), 400
    
    try:
        listing = generator.generate_listing(product_name, selling_points, target_market)
        
        return jsonify({
            'success': True,
            'title': listing.get('title', ''),
            'bullets': listing.get('bullets', []),
            'description': listing.get('description', '')
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/batch_generate', methods=['POST'])
def batch_generate():
    if 'file' not in request.files:
        return jsonify({'error': '请选择CSV文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '请选择CSV文件'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': '请上传CSV格式的文件'}), 400
    
    try:
        
        csv_content = file.read().decode('utf-8-sig')
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        
        required_columns = ['product_name', 'selling_points', 'target_market']
        if not all(col in csv_reader.fieldnames for col in required_columns):
            return jsonify({'error': 'CSV文件必须包含列: product_name, selling_points, target_market'}), 400
        
        results = []
        for row in csv_reader:
            product_name = row.get('product_name', '').strip()
            selling_points = row.get('selling_points', '').strip()
            target_market = row.get('target_market', '').strip()
            
            if not product_name:
                continue
            
            try:
                listing = generator.generate_listing(product_name, selling_points, target_market)
                results.append({
                    'product_name': product_name,
                    'title': listing.get('title', ''),
                    'bullets': listing.get('bullets', []),
                    'description': listing.get('description', '')
                })
            except Exception as e:
                results.append({
                    'product_name': product_name,
                    'error': str(e)
                })
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for i, result in enumerate(results, 1):
                if 'error' in result:
                    content = f"Product: {result['product_name']}\nError: {result['error']}"
                else:
                    content = f"Product: {result['product_name']}\n\n"
                    content += f"Title: {result['title']}\n\n"
                    content += "Bullet Points:\n"
                    for j, bullet in enumerate(result['bullets'], 1):
                        content += f"{j}. {bullet}\n"
                    content += f"\nDescription:\n{result['description']}"
                
                zip_file.writestr(f'listing_{i}_{result["product_name"][:20]}.txt', content)
        
        csv_output = io.StringIO()
        writer = csv.writer(csv_output)
        writer.writerow(['product_name', 'title', 'bullet_1', 'bullet_2', 'bullet_3', 'bullet_4', 'bullet_5', 'description'])
        for result in results:
            if 'error' not in result:
                bullets = result['bullets'] + [''] * (5 - len(result['bullets']))
                writer.writerow([
                    result['product_name'],
                    result['title'],
                    bullets[0],
                    bullets[1],
                    bullets[2],
                    bullets[3],
                    bullets[4],
                    result['description']
                ])
        zip_buffer.seek(0)
        zip_buffer_with_csv = io.BytesIO()
        with zipfile.ZipFile(zip_buffer_with_csv, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr('listings_summary.csv', csv_output.getvalue())
            zip_buffer.seek(0)
            with zipfile.ZipFile(zip_buffer, 'r') as inner_zip:
                for name in inner_zip.namelist():
                    zip_file.writestr(name, inner_zip.read(name))
        
        zip_buffer_with_csv.seek(0)
        
        return send_file(
            zip_buffer_with_csv,
            mimetype='application/zip',
            as_attachment=True,
            download_name='listings.zip'
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)