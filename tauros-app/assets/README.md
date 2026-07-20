# TAUROS App Assets

This directory should contain the following image assets:

## Required Files

### icon.png
- **Size**: 1024x1024 pixels
- **Format**: PNG
- **Purpose**: App icon for iOS, Android, and web
- **Recommended**: Use the TAUROS/DibTauroS branding

### splash.png
- **Size**: 1242x2436 pixels (or similar)
- **Format**: PNG
- **Purpose**: Splash screen shown while app loads
- **Background**: Should use `#000000` (black) to match theme

## Generating Assets

You can use the following methods to create assets:

### Option 1: Create manually
Create PNG images with your preferred design tool (Figma, Photoshop, etc.)

### Option 2: Use Expo's asset generator
```bash
npx expo install expo-asset
# Then create base assets and use expo to generate different sizes
```

### Option 3: Use a placeholder generator
For development, you can use placeholder images:
- https://placeholder.com/
- https://placeholderart.com/

## Asset Guidelines

- Icons should be square with no transparency
- Splash should match the app's dark theme (#0d1117 background)
- Use the TAUROS teal accent color (#33cc99) for branding elements
