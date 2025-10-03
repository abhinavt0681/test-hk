#!/usr/bin/env python3
"""
Image Download Speed Test
A simple tool to test download speed by downloading an image from a URL.
"""

import requests
import time
import sys
import argparse
from urllib.parse import urlparse
import os

def format_bytes(bytes_value):
    """Convert bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} TB"

def format_speed(bytes_per_second):
    """Convert bytes per second to human readable format."""
    for unit in ['B/s', 'KB/s', 'MB/s', 'GB/s']:
        if bytes_per_second < 1024.0:
            return f"{bytes_per_second:.2f} {unit}"
        bytes_per_second /= 1024.0
    return f"{bytes_per_second:.2f} TB/s"

def test_image_download_speed(url, timeout=30):
    """
    Test download speed by downloading an image from the given URL.
    
    Args:
        url (str): URL of the image to download
        timeout (int): Request timeout in seconds
    
    Returns:
        dict: Test results including speed, size, and duration
    """
    print(f"Testing download speed for: {url}")
    print("-" * 50)
    
    try:
        # Start timing
        start_time = time.time()
        
        # Make the request with streaming to get real-time progress
        response = requests.get(url, stream=True, timeout=timeout)
        response.raise_for_status()
        
        # Get content length if available
        content_length = response.headers.get('content-length')
        if content_length:
            total_size = int(content_length)
            print(f"File size: {format_bytes(total_size)}")
        else:
            total_size = None
            print("File size: Unknown (streaming)")
        
        # Download the content
        downloaded_bytes = 0
        chunk_size = 8192  # 8KB chunks
        
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                downloaded_bytes += len(chunk)
                
                # Show progress if we know the total size
                if total_size:
                    progress = (downloaded_bytes / total_size) * 100
                    print(f"\rProgress: {progress:.1f}% ({format_bytes(downloaded_bytes)}/{format_bytes(total_size)})", end='', flush=True)
        
        # End timing
        end_time = time.time()
        duration = end_time - start_time
        
        print()  # New line after progress
        
        # Calculate results
        speed_bps = downloaded_bytes / duration if duration > 0 else 0
        
        results = {
            'url': url,
            'size_bytes': downloaded_bytes,
            'size_formatted': format_bytes(downloaded_bytes),
            'duration_seconds': duration,
            'speed_bps': speed_bps,
            'speed_formatted': format_speed(speed_bps),
            'success': True
        }
        
        return results
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        return {
            'url': url,
            'error': str(e),
            'success': False
        }
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {
            'url': url,
            'error': str(e),
            'success': False
        }

def print_results(results):
    """Print the test results in a formatted way."""
    if not results['success']:
        print(f"❌ Test failed: {results.get('error', 'Unknown error')}")
        return
    
    print("\n" + "=" * 50)
    print("📊 DOWNLOAD SPEED TEST RESULTS")
    print("=" * 50)
    print(f"URL: {results['url']}")
    print(f"File size: {results['size_formatted']}")
    print(f"Download time: {results['duration_seconds']:.2f} seconds")
    print(f"Download speed: {results['speed_formatted']}")
    print("=" * 50)
    
    # Additional speed analysis
    speed_mbps = results['speed_bps'] / (1024 * 1024)
    if speed_mbps > 10:
        print("🚀 Excellent speed! (>10 MB/s)")
    elif speed_mbps > 5:
        print("✅ Good speed (5-10 MB/s)")
    elif speed_mbps > 1:
        print("⚠️  Moderate speed (1-5 MB/s)")
    else:
        print("🐌 Slow speed (<1 MB/s)")

def main():
    """Main function to run the speed test."""
    parser = argparse.ArgumentParser(description='Test image download speed')
    parser.add_argument('url', nargs='?', 
                       default='https://picsum.photos/1920/1080',
                       help='URL of the image to download (default: random image from Picsum)')
    parser.add_argument('--timeout', type=int, default=30,
                       help='Request timeout in seconds (default: 30)')
    parser.add_argument('--multiple', type=int, default=1,
                       help='Number of times to run the test (default: 1)')
    
    args = parser.parse_args()
    
    print("🖼️  Image Download Speed Test")
    print("=" * 50)
    
    if args.multiple > 1:
        print(f"Running {args.multiple} tests...")
        speeds = []
        
        for i in range(args.multiple):
            print(f"\n--- Test {i+1}/{args.multiple} ---")
            results = test_image_download_speed(args.url, args.timeout)
            
            if results['success']:
                speeds.append(results['speed_bps'])
                print_results(results)
            else:
                print(f"Test {i+1} failed: {results.get('error', 'Unknown error')}")
        
        if speeds:
            avg_speed = sum(speeds) / len(speeds)
            print(f"\n📈 AVERAGE SPEED: {format_speed(avg_speed)}")
            print(f"📊 Tests completed: {len(speeds)}/{args.multiple}")
    else:
        results = test_image_download_speed(args.url, args.timeout)
        print_results(results)

if __name__ == "__main__":
    main()
