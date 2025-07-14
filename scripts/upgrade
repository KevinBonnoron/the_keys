#!/usr/bin/env bash

echo "🚀 Starting Python dependencies update"
echo "=================================================="

# Check if pip is available
if ! command -v pip >/dev/null 2>&1; then
    echo "[ERROR] pip is not installed or not in PATH"
    exit 1
fi

echo "[INFO] Checking for outdated packages..."

# Get outdated packages (skip header lines)
outdated_packages=$(pip list --outdated --format=columns | tail -n +3 | awk '{print $1}')

if [ -z "$outdated_packages" ]; then
    echo "[SUCCESS] No outdated packages found!"
    exit 0
fi

echo "[INFO] Found packages to update:"
for package in $outdated_packages; do
    echo "  - $package"
done

echo ""
echo "=================================================="

# Ask for confirmation
printf "Do you want to update all these packages? (y/N): "
read response

case "$response" in
    y|Y|yes|YES)
        ;;
    *)
        echo "[WARNING] Update cancelled"
        exit 0
        ;;
esac

# Update each package
for package in $outdated_packages; do
    echo "[INFO] Updating $package..."
    if pip install --upgrade "$package" >/dev/null 2>&1; then
        echo "[SUCCESS] $package updated successfully"
    else
        echo "[ERROR] Failed to update $package"
    fi
    echo ""
done

# Update requirements.txt
echo "[INFO] Updating requirements.txt file..."
pip freeze > requirements.txt

echo ""
echo "[SUCCESS] Update completed!"
