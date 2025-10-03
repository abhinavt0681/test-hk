# Image Download Speed Test

A simple Python application to test download speed by downloading images from URLs. Perfect for testing server performance on EC2 instances.

## Features

- 🚀 Download speed testing with real-time progress
- 📊 Detailed speed analysis and reporting
- 🔄 Multiple test runs with average calculation
- 📏 Human-readable file sizes and speeds
- ⚡ Configurable timeouts and test parameters

## Installation

1. Clone or download this project to your EC2 instance
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Test download speed with a default random image:

```bash
python image_speed_test.py
```

### Custom Image URL

Test with your own image URL:

```bash
python image_speed_test.py https://example.com/image.jpg
```

### Multiple Tests

Run multiple tests to get an average speed:

```bash
python image_speed_test.py --multiple 5
```

### Custom Timeout

Set a custom timeout (in seconds):

```bash
python image_speed_test.py --timeout 60
```

### All Options

```bash
python image_speed_test.py https://example.com/image.jpg --timeout 30 --multiple 3
```

## Example Output

```
🖼️  Image Download Speed Test
==================================================
Testing download speed for: https://picsum.photos/1920/1080
--------------------------------------------------
File size: 123.45 KB
Progress: 100.0% (123.45 KB/123.45 KB)

==================================================
📊 DOWNLOAD SPEED TEST RESULTS
==================================================
URL: https://picsum.photos/1920/1080
File size: 123.45 KB
Download time: 2.34 seconds
Download speed: 52.75 KB/s
==================================================
⚠️  Moderate speed (1-5 MB/s)
```

## Speed Analysis

The application provides speed analysis:
- 🚀 Excellent speed: >10 MB/s
- ✅ Good speed: 5-10 MB/s  
- ⚠️ Moderate speed: 1-5 MB/s
- 🐌 Slow speed: <1 MB/s

## EC2 Deployment

1. Upload the files to your EC2 instance:
   ```bash
   scp -i your-key.pem image_speed_test.py requirements.txt ec2-user@your-instance:/home/ec2-user/
   ```

2. SSH into your EC2 instance:
   ```bash
   ssh -i your-key.pem ec2-user@your-instance
   ```

3. Install dependencies and run:
   ```bash
   pip install -r requirements.txt
   python image_speed_test.py
   ```

## Testing Different Image Sources

You can test with various image sources:

- **Random images**: `https://picsum.photos/1920/1080`
- **Large test images**: `https://httpbin.org/image/jpeg`
- **Your own images**: Any publicly accessible image URL

## Requirements

- Python 3.6+
- requests library
- Internet connection

## License

This project is open source and available under the MIT License.
