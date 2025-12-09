#!/bin/bash

# Advent of Code Input Downloader
# This script downloads puzzle inputs for all years and days
# 
# SETUP:
# 1. Get your session cookie from adventofcode.com:
#    - Log in to adventofcode.com
#    - Open browser DevTools (F12)
#    - Go to Application/Storage > Cookies
#    - Copy the value of the 'session' cookie
# 2. Replace YOUR_SESSION_COOKIE below with your actual session cookie

SESSION_COOKIE="53616c7465645f5f9d31888b3fd507c3fff2b11c780dadd7e743bd3ec1a81818d4fbcf3ca0a4252b3091c48abd62639cd6f9691ed1d15d987003f7127f358cde"

if [ "$SESSION_COOKIE" = "YOUR_SESSION_COOKIE" ]; then
    echo "❌ Error: Please set your session cookie first!"
    echo ""
    echo "To get your session cookie:"
    echo "1. Log in to https://adventofcode.com"
    echo "2. Open browser DevTools (F12)"
    echo "3. Go to Application/Storage > Cookies"
    echo "4. Copy the value of the 'session' cookie"
    echo "5. Edit this script and replace YOUR_SESSION_COOKIE with your value"
    exit 1
fi

BASE_DIR="/Users/michaeljezt/Library/CloudStorage/ProtonDrive-9808673@proton.me-folder/proton_repos"

echo "🎄 Downloading Advent of Code inputs..."
echo ""

for year in {2015..2024}; do
    echo "Year $year:"
    
    for day in {1..25}; do
        dir="$BASE_DIR/adventofcode$year/day$day"
        
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
        fi
        
        output_file="$dir/input.txt"
        
        # Skip if already downloaded
        if [ -f "$output_file" ] && [ -s "$output_file" ]; then
            echo "  Day $day: ✓ (already exists)"
            continue
        fi
        
        # Download the input
        url="https://adventofcode.com/$year/day/$day/input"
        
        curl -s -b "session=$SESSION_COOKIE" "$url" -o "$output_file"
        
        # Check if download was successful
        if [ -s "$output_file" ]; then
            # Check if it's an error page
            if grep -q "Please log in" "$output_file" 2>/dev/null; then
                echo "  Day $day: ❌ (authentication failed)"
                rm "$output_file"
            elif grep -q "404 Not Found" "$output_file" 2>/dev/null; then
                echo "  Day $day: ⏭️  (not available yet)"
                rm "$output_file"
            else
                echo "  Day $day: ✅ (downloaded)"
            fi
        else
            echo "  Day $day: ❌ (download failed)"
        fi
        
        # Be nice to the server
        sleep 0.5
    done
    
    echo ""
done

echo "✨ Done!"
