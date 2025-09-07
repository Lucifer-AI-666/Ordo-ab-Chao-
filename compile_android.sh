#!/bin/bash
# Manual Android compilation script for Ordo-ab-Chao
# Since Gradle can't download dependencies due to network restrictions,
# we'll use Android SDK tools directly

set -e

ANDROID_SDK="/usr/local/lib/android/sdk"
BUILD_TOOLS="$ANDROID_SDK/build-tools/34.0.0"
PLATFORM="$ANDROID_SDK/platforms/android-34"
APP_DIR="$(pwd)/app"
BUILD_DIR="$APP_DIR/build"
SRC_DIR="$APP_DIR/src/main"

echo "🔨 Starting manual Android compilation..."
echo "Using Android SDK: $ANDROID_SDK"
echo "Build tools: $BUILD_TOOLS"
echo "Platform: $PLATFORM"

# Create build directories
mkdir -p "$BUILD_DIR/gen"
mkdir -p "$BUILD_DIR/obj"
mkdir -p "$BUILD_DIR/classes"

# Step 1: Generate R.java from resources
echo "📝 Generating R.java from resources..."
"$BUILD_TOOLS/aapt" package -f -m \
    -S "$SRC_DIR/res" \
    -M "$SRC_DIR/AndroidManifest.xml" \
    -I "$PLATFORM/android.jar" \
    -J "$BUILD_DIR/gen"

# Step 2: Compile Java sources
echo "☕ Compiling Java sources..."
find "$SRC_DIR/java" -name "*.java" > "$BUILD_DIR/sources.txt"
echo "$BUILD_DIR/gen/com/lucifer/ordoabchao/R.java" >> "$BUILD_DIR/sources.txt"

javac -d "$BUILD_DIR/classes" \
    -classpath "$PLATFORM/android.jar" \
    -sourcepath "$SRC_DIR/java:$BUILD_DIR/gen" \
    @"$BUILD_DIR/sources.txt"

# Step 3: Convert Java bytecode to DEX
echo "🔄 Converting to DEX format..."
"$BUILD_TOOLS/d8" --output "$BUILD_DIR/" \
    --classpath "$PLATFORM/android.jar" \
    "$BUILD_DIR/classes/com/lucifer/ordoabchao/"*.class

# Step 4: Package resources
echo "📦 Packaging resources..."
"$BUILD_TOOLS/aapt" package -f \
    -S "$SRC_DIR/res" \
    -M "$SRC_DIR/AndroidManifest.xml" \
    -A "$SRC_DIR/assets" \
    -I "$PLATFORM/android.jar" \
    -F "$BUILD_DIR/unsigned.apk"

# Step 5: Add DEX to APK
echo "➕ Adding DEX to APK..."
cd "$BUILD_DIR"
zip -u unsigned.apk classes.dex

# Step 6: Align APK
echo "📐 Aligning APK..."
"$BUILD_TOOLS/zipalign" -f 4 unsigned.apk aligned.apk

echo "✅ Compilation completed!"
echo "📁 Output APK: $BUILD_DIR/aligned.apk"
echo ""
echo "Note: APK is unsigned. For testing purposes only."