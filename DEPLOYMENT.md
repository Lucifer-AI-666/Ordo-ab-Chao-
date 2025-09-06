# Neo Cleopatra Viva - Deployment Guide

## 🚀 Vercel Deployment

### Quick Deploy
1. Connect your GitHub repository to Vercel
2. Set the build settings:
   - **Build Command**: `echo "Static site - no build needed"`
   - **Output Directory**: `public`
   - **Install Command**: `npm install` (optional)

### Manual Deploy
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy to Vercel
vercel --prod

# Follow the prompts:
# Set up and deploy "~/Ordo-ab-Chao-"? [Y/n] y
# Which scope do you want to deploy to? [Select your account]
# Link to existing project? [N/y] n
# What's your project's name? neo-cleopatra-viva
# In which directory is your code located? ./public
```

### Environment Configuration
The interface automatically detects deployment environments:
- **Local Development** (`localhost`): Attempts API calls to CopilotPrivateAgent
- **Production Deployment**: Switches to simulation mode

### Build Settings
- **Framework Preset**: None (Static Site)
- **Build Command**: Not needed
- **Output Directory**: `public`
- **Node.js Version**: 18.x

## 🏗️ Project Structure

```
/
├── vercel.json          # Vercel configuration
├── package.json         # Node.js metadata
├── public/              # Static website files
│   ├── index.html       # Main interface
│   ├── css/
│   │   └── neo-cleopatra.css
│   ├── js/
│   │   ├── copilot-agent.js
│   │   └── neo-cleopatra.js
│   └── README.md        # Interface documentation
└── DEPLOYMENT.md        # This file
```

## 🔧 Configuration Files

### vercel.json
- Configures static file serving
- Sets security headers
- Handles routing for SPA behavior

### package.json
- Defines project metadata
- Lists development dependencies
- Provides build scripts

## 🌐 Custom Domain (Optional)

To use a custom domain:
1. Go to Vercel dashboard → Project → Settings → Domains
2. Add your custom domain
3. Configure DNS records as instructed
4. SSL certificate is automatically provisioned

## 🔒 Security Features

### Headers
- X-Frame-Options: SAMEORIGIN
- X-Content-Type-Options: nosniff
- Referrer-Policy: strict-origin-when-cross-origin

### Privacy
- No external CDN dependencies
- No analytics or tracking
- Local-only data processing
- Client-side simulation mode

## 🚨 Troubleshooting

### Common Issues

**Build Fails**
- Ensure `public/` directory exists
- Check file permissions
- Verify `vercel.json` syntax

**Interface Not Loading**
- Check browser console for errors
- Verify all CSS/JS files are accessible
- Test with different browsers

**Styling Issues**
- Clear browser cache
- Check CSS file paths
- Verify viewport meta tag

### Debug Mode
Enable debug logging in browser console:
```javascript
// In browser console
window.neoCleopatraInterface.copilotAgent.enableLogging = true;
```

## 📊 Performance

### Optimization Features
- Pure CSS (no framework overhead)
- Minimal JavaScript bundle
- Optimized images and assets
- Efficient DOM manipulation

### Loading Speed
- Static files served from CDN
- Compressed CSS/JS delivery
- Progressive enhancement
- Mobile-optimized design

---

**Framework**: DibTauroS/Ordo-ab-Chao  
**Owner**: Dib Anouar  
**License**: LUP v1.0 (Personal & Non-Commercial Use Only)