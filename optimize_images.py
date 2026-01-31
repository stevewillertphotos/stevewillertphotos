#!/usr/bin/env python3
"""
Image Optimizer for Aurora Borealis Landing Page
Optimizes photos for web while maintaining quality
"""

from PIL import Image
import os
from pathlib import Path

def optimize_image(input_path, output_path, max_width, quality=85):
    """
    Optimize an image for web use
    
    Args:
        input_path: Path to original image
        output_path: Path to save optimized image
        max_width: Maximum width in pixels
        quality: JPEG quality (1-95, recommend 85)
    """
    try:
        # Open the image
        img = Image.open(input_path)
        
        # Convert RGBA to RGB if necessary (for JPEG)
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        # Get original dimensions
        original_width, original_height = img.size
        
        # Calculate new dimensions maintaining aspect ratio
        if original_width > max_width:
            ratio = max_width / original_width
            new_height = int(original_height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            print(f"  Resized: {original_width}x{original_height} → {max_width}x{new_height}")
        else:
            print(f"  No resize needed (already {original_width}px wide)")
        
        # Get file size before
        original_size = os.path.getsize(input_path) / 1024  # KB
        
        # Save optimized image
        img.save(output_path, 'JPEG', quality=quality, optimize=True)
        
        # Get file size after
        new_size = os.path.getsize(output_path) / 1024  # KB
        reduction = ((original_size - new_size) / original_size) * 100
        
        print(f"  Size: {original_size:.1f}KB → {new_size:.1f}KB (saved {reduction:.1f}%)")
        
        return True
    
    except Exception as e:
        print(f"  Error: {str(e)}")
        return False

def main():
    """Main optimization process"""
    
    print("=" * 60)
    print("Aurora Borealis Landing Page - Image Optimizer")
    print("=" * 60)
    print()
    
    # Define image categories and their settings
    images_config = {
        "Le Dun enhanced Normal.jpg": {
            "max_width": 1920,
            "quality": 85,
            "category": "Main Featured Photo"
        },
        "Le Dun Stars Light.jpg": {
            "max_width": 800,
            "quality": 85,
            "category": "Gallery"
        },
        "Le Dun Stars Red Light.jpg": {
            "max_width": 800,
            "quality": 85,
            "category": "Gallery"
        },
        "Northern Lights Swirl Middle.jpg": {
            "max_width": 800,
            "quality": 85,
            "category": "Gallery"
        },
        "Northern Lights Swirl Right.jpg": {
            "max_width": 800,
            "quality": 85,
            "category": "Gallery"
        },
        "Cotton Candy Skies Normal.jpg": {
            "max_width": 800,
            "quality": 85,
            "category": "Gallery"
        },
        "Star Burst.jpg": {
            "max_width": 800,
            "quality": 85,
            "category": "Gallery"
        }
    }
    
    # Check for images directory
    images_dir = Path("images")
    if not images_dir.exists():
        print("❌ Error: 'images' directory not found!")
        print("   Please run this script from your repository root.")
        return
    
    # Create output directory for optimized images
    optimized_dir = Path("images_optimized")
    optimized_dir.mkdir(exist_ok=True)
    print(f"✓ Output directory: {optimized_dir}/")
    print()
    
    # Process each image
    success_count = 0
    total_count = len(images_config)
    
    for filename, config in images_config.items():
        input_path = images_dir / filename
        output_path = optimized_dir / filename
        
        print(f"Processing: {filename}")
        print(f"  Category: {config['category']}")
        
        if not input_path.exists():
            print(f"  ⚠ Warning: File not found, skipping...")
            print()
            continue
        
        if optimize_image(
            input_path, 
            output_path, 
            config['max_width'], 
            config['quality']
        ):
            success_count += 1
            print(f"  ✓ Success!")
        
        print()
    
    # Summary
    print("=" * 60)
    print(f"Optimization Complete: {success_count}/{total_count} images processed")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Review optimized images in 'images_optimized/' folder")
    print("2. If satisfied, replace original images:")
    print("   cp images_optimized/* images/")
    print("3. Commit and push to GitHub:")
    print("   git add images/")
    print("   git commit -m 'Optimize images for web'")
    print("   git push")
    print()
    print("💡 Tip: Keep backups of original high-res files elsewhere!")

if __name__ == "__main__":
    # Check if PIL is installed
    try:
        from PIL import Image
    except ImportError:
        print("❌ Error: Pillow library not installed")
        print()
        print("Install with: pip install Pillow")
        print("Or: pip3 install Pillow")
        exit(1)
    
    main()
