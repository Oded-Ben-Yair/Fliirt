# 🎯 **Claude-Code Integration Prompt for Flirrt.ai Backend Connection**

## **Mission: Connect Perfected AI Backend to Working iOS App**

You are tasked with integrating a world-class, production-ready AI backend with an existing iOS Flirrt.ai application. The backend has been thoroughly tested and optimized to deliver exceptional flirting suggestions based on dating app screenshot analysis.

## **📋 Current Status**
- ✅ **iOS App**: Complete working flow with heart button keyboard extension
- ✅ **AI Backend**: Perfected multi-model system (GPT-4o, Grok, Gemini) with 8.5/10 quality score
- ✅ **Testing**: 1,500+ automated tests, 96.3% success rate under heavy load
- 🔗 **Missing**: Connection between iOS app and AI backend

## **🚀 Your Task**
Seamlessly integrate the perfected AI backend with the existing iOS application to create a complete, production-ready Flirrt.ai system.

## **📁 Repository Information**
- **Repository**: https://github.com/Oded-Ben-Yair/Fliirt
- **Backend Location**: `/Backend/advanced_ai_service.py`
- **iOS App Location**: `/iOS/FlirrtApp.xcodeproj`
- **Integration Guide**: `/BACKEND_INTEGRATION_GUIDE.md`

## **🔧 Backend API Details**

### **Main Endpoint**
```
POST http://localhost:5000/api/ai/analyze-screenshot
Content-Type: application/json

Request:
{
  "image_data": "base64_encoded_screenshot",
  "context": {
    "user_gender": "male",
    "target_gender": "female",
    "app_type": "tinder",
    "current_text": "Hey there!",
    "conversation_history": []
  }
}

Response:
{
  "success": true,
  "suggestions": [
    {
      "text": "I see you're into hiking! What's the most breathtaking view you've discovered?",
      "confidence": 0.92,
      "reasoning": "References hiking interest from profile photo"
    }
    // ... 2 more suggestions
  ],
  "processing_time": 8.2,
  "models_used": ["gpt-4o", "grok"]
}
```

### **Starting the Backend**
```bash
cd Backend
pip install flask flask-cors openai xai-sdk google-generativeai
python advanced_ai_service.py
# Server starts on http://localhost:5000
```

## **📱 iOS Integration Points**

### **Key Files to Modify**
1. **`iOS/Shared/AIService.swift`** - Update to call real backend API
2. **`iOS/FlirrtApp/ContentView.swift`** - Handle photo picker and API responses
3. **`iOS/Shared/AppGroupCommunicator.swift`** - Pass suggestions between apps

### **Current Flow (Working)**
1. User taps heart button in keyboard extension
2. Keyboard sends request via App Groups to main app
3. Main app opens photo picker and gets screenshot
4. **[YOUR TASK]** Main app calls backend API with screenshot
5. **[YOUR TASK]** Backend returns 3 AI-generated suggestions
6. **[YOUR TASK]** Main app sends suggestions back to keyboard
7. Keyboard displays suggestions for user selection

## **🎯 Specific Integration Requirements**

### **1. Update AIService.swift**
- Replace mock responses with real API calls to `http://localhost:5000/api/ai/analyze-screenshot`
- Handle base64 image encoding
- Parse JSON response and extract suggestions
- Implement proper error handling and loading states

### **2. Enhance Photo Picker Integration**
- Ensure selected screenshots are properly encoded as base64
- Add context information (user gender, target gender, app type)
- Handle API response timing (8-12 second processing time)

### **3. Improve User Experience**
- Add loading indicators during AI processing
- Display confidence scores with suggestions
- Handle network errors gracefully
- Optimize for production use

## **✅ Success Criteria**
- [ ] Backend starts successfully and responds to health checks
- [ ] iOS app can select photos and send them to backend
- [ ] Backend returns 3 high-quality, contextual flirting suggestions
- [ ] Suggestions appear in keyboard extension for user selection
- [ ] Complete flow works end-to-end without errors
- [ ] User experience is smooth and professional

## **🔍 Testing Instructions**
1. **Start Backend**: `cd Backend && python advanced_ai_service.py`
2. **Test Health**: `curl http://localhost:5000/api/ai/health`
3. **Build iOS App**: Open `iOS/FlirrtApp.xcodeproj` in Xcode
4. **Test Flow**: Heart button → Photo picker → AI suggestions → Display
5. **Verify Quality**: Ensure suggestions are relevant and high-quality

## **📊 Expected Performance**
- **Response Time**: 8-12 seconds for AI processing
- **Success Rate**: 96%+ under normal conditions
- **Quality Score**: 8.5/10 average suggestion quality
- **Scalability**: Tested with 100+ concurrent users

## **🎉 Final Deliverable**
A complete, working Flirrt.ai application where users can:
1. Tap the heart button in any dating app
2. Select a screenshot of a profile or conversation
3. Receive 3 AI-generated, contextual flirting suggestions
4. Use those suggestions to improve their dating conversations

The backend is production-ready and thoroughly tested. Your job is to connect it seamlessly with the existing iOS app to create the complete Flirrt.ai experience.

**Repository**: https://github.com/Oded-Ben-Yair/Fliirt
**Integration Guide**: `/BACKEND_INTEGRATION_GUIDE.md`

Good luck building the future of AI-powered dating assistance! 🚀💕

