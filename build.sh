#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "--- Installing Python Dependencies ---"
pip install -r requirements.txt

echo "--- Installing FFmpeg ---"
# Create a directory for ffmpeg
mkdir -p ffmpeg

# Download static build of ffmpeg (Linux amd64)
# Using a reliable source for static builds (johnvansickle or similar)
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz

# Extract
tar -xvf ffmpeg-release-amd64-static.tar.xz -C ffmpeg --strip-components=1

# Add to PATH (This only affects this script, but helpful for debug)
export PATH=$PWD/ffmpeg:$PATH

echo "FFmpeg installed to $PWD/ffmpeg"
./ffmpeg/ffmpeg -version

echo "--- Installing Node.js ---"
# Install Node.js (using static binary for simplicity and speed)
NODE_VERSION="v20.11.0"
NODE_DIST="node-$NODE_VERSION-linux-x64"

wget https://nodejs.org/dist/$NODE_VERSION/$NODE_DIST.tar.xz
tar -xJf $NODE_DIST.tar.xz
rm $NODE_DIST.tar.xz

# Add to PATH
export PATH=$PWD/$NODE_DIST/bin:$PATH
echo "Node.js installed version: $(node -v)"

echo "--- Build Complete ---"
