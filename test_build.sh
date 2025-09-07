#!/bin/bash
# Test script for Ordo-ab-Chao compilation and functionality
# Verifies that the Android app compiles correctly and web assets are present

set -e

echo "🧪 Testing Ordo-ab-Chao build process..."
echo "=========================================="

# Test 1: Verify project structure
echo "📁 Test 1: Verifying project structure..."
REQUIRED_FILES=(
    "app/src/main/AndroidManifest.xml"
    "app/src/main/java/com/lucifer/ordoabchao/MainActivity.java" 
    "app/src/main/res/layout/activity_main.xml"
    "app/src/main/assets/index.html"
    "web/index.html"
    "build.gradle"
    "settings.gradle"
    "local.properties"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [[ -f "$file" ]]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (missing)"
        exit 1
    fi
done

# Test 2: Verify Android compilation
echo ""
echo "🔨 Test 2: Testing Android compilation..."
if [[ -x "./compile_android.sh" ]]; then
    ./compile_android.sh
    if [[ -f "app/build/aligned.apk" ]]; then
        APK_SIZE=$(stat -c%s "app/build/aligned.apk")
        echo "  ✅ APK generated successfully (${APK_SIZE} bytes)"
    else
        echo "  ❌ APK generation failed"
        exit 1
    fi
else
    echo "  ❌ compile_android.sh not executable"
    exit 1
fi

# Test 3: Verify APK contents
echo ""
echo "📦 Test 3: Verifying APK contents..."
EXPECTED_APK_FILES=(
    "AndroidManifest.xml"
    "assets/index.html"
    "res/layout/activity_main.xml"
    "resources.arsc"
    "classes.dex"
)

unzip -l app/build/aligned.apk > /tmp/apk_contents.txt
for expected_file in "${EXPECTED_APK_FILES[@]}"; do
    if grep -q "$expected_file" /tmp/apk_contents.txt; then
        echo "  ✅ $expected_file found in APK"
    else
        echo "  ❌ $expected_file missing from APK"
        exit 1
    fi
done

# Test 4: Verify web assets
echo ""
echo "🌐 Test 4: Verifying web assets..."
if grep -q "Ordo ab Chao" app/src/main/assets/index.html; then
    echo "  ✅ Assets HTML contains expected content"
else
    echo "  ❌ Assets HTML missing expected content"
    exit 1
fi

if grep -q "Ordo ab Chao" web/index.html; then
    echo "  ✅ Web HTML contains expected content"
else
    echo "  ❌ Web HTML missing expected content"
    exit 1
fi

# Test 5: Verify MainActivity compilation
echo ""
echo "☕ Test 5: Verifying MainActivity..."
if [[ -f "app/build/classes/com/lucifer/ordoabchao/MainActivity.class" ]]; then
    echo "  ✅ MainActivity compiled successfully"
else
    echo "  ❌ MainActivity compilation failed"
    exit 1
fi

# Test 6: Verify R.java generation
echo ""
echo "📝 Test 6: Verifying R.java generation..."
if [[ -f "app/build/gen/com/lucifer/ordoabchao/R.java" ]]; then
    if grep -q "btn_open_browser" app/build/gen/com/lucifer/ordoabchao/R.java; then
        echo "  ✅ R.java generated with expected IDs"
    else
        echo "  ❌ R.java missing expected resource IDs"
        exit 1
    fi
else
    echo "  ❌ R.java not generated"
    exit 1
fi

echo ""
echo "🎉 All tests passed successfully!"
echo ""
echo "📋 Summary:"
echo "  - Android project structure: ✅ Complete"
echo "  - Android compilation: ✅ Working"  
echo "  - APK generation: ✅ Working"
echo "  - Web assets: ✅ Present"
echo "  - All components: ✅ Functional"
echo ""
echo "📁 Generated files:"
echo "  - APK: app/build/aligned.apk ($(stat -c%s app/build/aligned.apk) bytes)"
echo "  - Web: web/index.html (standalone version)"
echo "  - Assets: app/src/main/assets/index.html (APK integrated)"