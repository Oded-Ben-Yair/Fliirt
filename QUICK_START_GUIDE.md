# Flirrt.ai - Quick Start Guide

## 🚀 Get Started in 5 Minutes

This guide will get you up and running with Flirrt.ai for immediate testing.

## Prerequisites

- macOS with Xcode 16.x installed
- iOS 18.6+ Simulator or device
- Git access to the repository

## Step 1: Clone and Open Project

```bash
git clone https://github.com/Oded-Ben-Yair/Fliirt.git
cd Fliirt/iOS
open FlirrtApp.xcodeproj
```

## Step 2: Configure Xcode Project

1. **Select Development Team**:
   - Click on "FlirrtApp" project in navigator
   - Select "FlirrtApp" target
   - Go to "Signing & Capabilities"
   - Choose your development team

2. **Repeat for Keyboard Extension**:
   - Select "FlirrtKeyboard" target
   - Configure same development team
   - Ensure App Groups capability is enabled

## Step 3: Build and Install

1. **Select Target Device**:
   - Choose iOS Simulator (iPhone 15 Pro recommended)
   - Or connect physical iOS device

2. **Build and Run**:
   - Press `Cmd + R` or click the play button
   - Wait for app to install and launch

## Step 4: Enable Keyboard

1. **Open iOS Settings** (in Simulator or device)
2. **Navigate to**: Settings > General > Keyboard > Keyboards
3. **Add New Keyboard**: Tap "Add New Keyboard..."
4. **Select Flirrt**: Find and tap "Flirrt" in the list
5. **Enable Full Access**: 
   - Tap on "Flirrt" in keyboard list
   - Toggle "Allow Full Access" to ON
   - Confirm when prompted

## Step 5: Test the Heart Button

1. **Open Messages App** (or any app with text input)
2. **Tap in text field** to bring up keyboard
3. **Switch to Flirrt Keyboard**:
   - Tap the globe icon to cycle keyboards
   - Or long-press globe and select "Flirrt"
4. **Look for Heart Button**: You should see a pink heart (♥) button
5. **Tap Heart Button**: This should trigger the photo picker

## Step 6: Test Photo Selection

1. **Photo Picker Opens**: After tapping heart, photo picker should appear
2. **Select Any Photo**: Choose any image from your photo library
3. **Wait for Processing**: AI will analyze the image
4. **View Suggestions**: Three flirting suggestions should appear
5. **Select Suggestion**: Tap one to insert it into the text field

## 🔧 Troubleshooting

### Keyboard Not Appearing
- Restart the app and try again
- Check that keyboard is enabled in Settings
- Verify App Groups are configured correctly

### Heart Button Not Visible
- Ensure you're using the Flirrt keyboard (not default)
- Check console logs in Xcode for errors
- Verify keyboard extension built successfully

### Photo Picker Not Opening
- Confirm "Allow Full Access" is enabled
- Check photo library permissions
- Review Xcode console for error messages

### No AI Suggestions
- Verify backend service is running (see Backend Setup below)
- Check network connectivity
- Review API endpoint configuration

## 🖥️ Backend Setup (Optional for Full Testing)

To test with real AI suggestions:

```bash
cd Backend/flirrt-ai-service

# Install dependencies
pip install flask flask-cors

# Set environment variables (optional - will use mock data if not set)
export OPENAI_API_KEY="your_openai_key"

# Run backend service
python app.py
```

The backend will run on `http://localhost:5000`

## 📱 Expected Behavior

### Successful Test Flow
1. ✅ App launches without crashes
2. ✅ Keyboard appears in Settings > Keyboards
3. ✅ Heart button visible in Flirrt keyboard
4. ✅ Photo picker opens when heart button tapped
5. ✅ Suggestions appear after photo selection
6. ✅ Selected suggestion inserts into text field

### Console Log Messages
Look for these messages in Xcode console:
- `🔥 HEART BUTTON TOUCH DOWN`
- `📡 Sending photo selection request`
- `🎯 Photo request detected`
- `📸 Presenting photo picker`

## 📋 Testing Checklist

- [ ] Project builds without errors
- [ ] Main app launches successfully
- [ ] Keyboard can be enabled in Settings
- [ ] Heart button appears in keyboard
- [ ] Photo picker opens on heart button tap
- [ ] AI suggestions appear (mock or real)
- [ ] Suggestions can be inserted into text

## 🆘 Need Help?

### Check Documentation
- `Documentation/DEPLOYMENT_GUIDE.md` - Complete setup guide
- `Documentation/DEVELOPMENT_PLAN.md` - Technical details
- `Tests/` - Automated test examples

### Common Issues
1. **Build Errors**: Check Xcode version and iOS deployment target
2. **Signing Issues**: Ensure valid development team selected
3. **Simulator Issues**: Try different simulator or restart Xcode
4. **Keyboard Issues**: Restart simulator and re-enable keyboard

### Debug Commands
```bash
# Check iOS logs
xcrun simctl spawn booted log stream --predicate 'subsystem contains "ai.flirrt"'

# Test backend health
curl http://localhost:5000/api/ai/health
```

## 🎯 Success Criteria

You've successfully set up Flirrt.ai when:
- Heart button appears in keyboard interface
- Photo picker opens on button tap
- Suggestions appear after photo selection
- Complete workflow functions end-to-end

## 🚀 Next Steps

Once basic functionality is confirmed:
1. Test with different dating apps (Tinder, Bumble, etc.)
2. Try various photo types and contexts
3. Evaluate suggestion quality and relevance
4. Test error scenarios (no network, invalid photos)
5. Review performance and user experience

---

**Ready to revolutionize your dating game with AI-powered flirting suggestions!** 💕

