#!/usr/bin/env python3
"""
Image Speed Test Server
A Flask web server that serves images and measures download speed.
"""

from flask import Flask, send_file, render_template, jsonify, request
import time
import os
import random
from PIL import Image, ImageDraw
import io
import json

app = Flask(__name__)

# Store timing data
timing_data = []

def generate_test_image(width=1920, height=1080, size_kb=None):
    """
    Generate a test image with specified dimensions and approximate size.
    
    Args:
        width (int): Image width in pixels
        height (int): Image height in pixels  
        size_kb (int): Target size in KB (approximate)
    
    Returns:
        io.BytesIO: Image data as bytes
    """
    # Create a colorful test image
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Add some patterns to make the image larger
    for i in range(0, width, 50):
        for j in range(0, height, 50):
            color = (
                random.randint(0, 255),
                random.randint(0, 255), 
                random.randint(0, 255)
            )
            draw.rectangle([i, j, i+25, j+25], fill=color)
    
    # Add some text
    try:
        from PIL import ImageFont
        # Try to use a default font
        font = ImageFont.load_default()
    except:
        font = None
    
    text = f"Speed Test Image - {width}x{height}"
    if font:
        draw.text((50, 50), text, fill='black', font=font)
    else:
        draw.text((50, 50), text, fill='black')
    
    # Convert to bytes
    img_bytes = io.BytesIO()
    
    # Adjust quality to approximate target size
    if size_kb:
        # Rough estimation: start with quality 85 and adjust
        quality = 85
        while True:
            img_bytes.seek(0)
            img_bytes.truncate(0)
            img.save(img_bytes, format='JPEG', quality=quality)
            current_size = len(img_bytes.getvalue()) / 1024  # KB
            
            if current_size <= size_kb * 1.1:  # Within 10% of target
                break
            quality -= 5
            if quality < 10:
                break
    else:
        img.save(img_bytes, format='JPEG', quality=85)
    
    img_bytes.seek(0)
    return img_bytes

@app.route('/')
def index():
    """Main page with speed test interface."""
    return render_template('index.html')

@app.route('/image/<int:width>/<int:height>')
def serve_image(width, height):
    """
    Serve a test image with specified dimensions.
    Measures download time and logs it.
    """
    start_time = time.time()
    
    # Generate the image
    img_bytes = generate_test_image(width, height)
    
    # Get client info
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    # Calculate image size
    image_size = len(img_bytes.getvalue())
    
    # Log the request start
    request_data = {
        'timestamp': time.time(),
        'client_ip': client_ip,
        'user_agent': user_agent,
        'image_size': image_size,
        'dimensions': f"{width}x{height}",
        'start_time': start_time
    }
    
    # Add to timing data
    timing_data.append(request_data)
    
    # Keep only last 100 requests
    if len(timing_data) > 100:
        timing_data.pop(0)
    
    return send_file(
        img_bytes,
        mimetype='image/jpeg',
        as_attachment=False,
        download_name=f'test_image_{width}x{height}.jpg'
    )

@app.route('/image/<int:size_kb>kb')
def serve_sized_image(size_kb):
    """
    Serve a test image with specified size in KB.
    """
    start_time = time.time()
    
    # Generate image with target size
    img_bytes = generate_test_image(size_kb=size_kb)
    
    # Get client info
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    # Calculate actual image size
    actual_size = len(img_bytes.getvalue())
    
    # Log the request
    request_data = {
        'timestamp': time.time(),
        'client_ip': client_ip,
        'user_agent': user_agent,
        'image_size': actual_size,
        'target_size_kb': size_kb,
        'start_time': start_time
    }
    
    timing_data.append(request_data)
    
    # Keep only last 100 requests
    if len(timing_data) > 100:
        timing_data.pop(0)
    
    return send_file(
        img_bytes,
        mimetype='image/jpeg',
        as_attachment=False,
        download_name=f'test_image_{size_kb}kb.jpg'
    )

@app.route('/stats')
def get_stats():
    """Get server statistics and recent requests."""
    if not timing_data:
        return jsonify({
            'message': 'No requests yet',
            'total_requests': 0
        })
    
    # Calculate some basic stats
    total_requests = len(timing_data)
    total_size = sum(req['image_size'] for req in timing_data)
    avg_size = total_size / total_requests if total_requests > 0 else 0
    
    # Recent requests (last 10)
    recent_requests = timing_data[-10:]
    
    return jsonify({
        'total_requests': total_requests,
        'total_data_served': total_size,
        'average_image_size': avg_size,
        'recent_requests': recent_requests
    })

@app.route('/clear-stats')
def clear_stats():
    """Clear all timing data."""
    global timing_data
    timing_data = []
    return jsonify({'message': 'Stats cleared'})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    print("🚀 Image Speed Test Server")
    print("=" * 50)
    print("Server will be available at: http://localhost:5000")
    print("Image endpoints:")
    print("  /image/1920/1080 - 1920x1080 image")
    print("  /image/100kb - 100KB image")
    print("  /stats - View server statistics")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
