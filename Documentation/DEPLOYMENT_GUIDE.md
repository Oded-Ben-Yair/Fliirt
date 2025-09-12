# Flirrt.ai Deployment Guide

## Overview
This guide covers deploying the complete Flirrt.ai system including the iOS app and AI backend service.

## System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   iOS Main App  │    │ Keyboard Extension│    │  AI Backend     │
│                 │    │                  │    │                 │
│ • Photo Picker  │◄──►│ • Heart Button   │───►│ • GPT-4o        │
│ • App Groups    │    │ • AI Suggestions │    │ • Grok (future) │
│ • Settings      │    │ • Text Input     │    │ • Gemini        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────▼──────────────┐
                    │      App Groups            │
                    │ • Photo Requests           │
                    │ • Selected Images          │
                    │ • AI Suggestions           │
                    │ • Text Context             │
                    └────────────────────────────┘
```

## Prerequisites

### Development Environment
- macOS with Xcode 16.x
- iOS 18.6+ target devices/simulators
- Python 3.11+ for backend
- Git for version control

### API Keys Required
- OpenAI API key (GPT-4o)
- xAI API key (Grok) - optional
- Google Gemini API key - optional

## Backend Deployment

### Local Development
```bash
cd Backend/flirrt-ai-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your_openai_key"
export XAI_API_KEY="your_xai_key"
export GEMINI_API_KEY="your_gemini_key"

# Run development server
python src/main.py
```

### Production Deployment
```bash
# Using Manus deployment service
cd Backend/flirrt-ai-service
manus-deploy-backend --framework flask --project-dir .
```

The backend will be deployed to a permanent public URL for iOS app integration.

### API Endpoints
- `GET /api/status` - Service status
- `GET /api/ai/health` - AI models health check
- `POST /api/ai/analyze-screenshot` - Main analysis endpoint
- `POST /api/ai/test-suggestions` - Testing endpoint

## iOS App Deployment

### Development Setup
1. Open `iOS/FlirrtApp.xcodeproj` in Xcode
2. Configure App Groups:
   - Main App: `group.ai.flirrt.shared`
   - Keyboard Extension: `group.ai.flirrt.shared`
3. Update backend URL in `AIService.swift`
4. Configure signing certificates

### App Store Preparation
1. **Privacy Policy Required**: Keyboard extensions must have privacy policy
2. **App Store Review**: 
   - Demonstrate keyboard functionality
   - Show photo access permissions
   - Explain AI processing
3. **Entitlements**:
   - App Groups capability
   - Photo library access (keyboard extension)

### Testing Checklist
- [ ] Main app launches successfully
- [ ] Keyboard can be enabled in Settings
- [ ] Heart button appears in keyboard
- [ ] Photo picker opens when heart button tapped
- [ ] AI suggestions appear after photo selection
- [ ] Suggestions can be inserted into text fields
- [ ] App Groups communication working
- [ ] Error handling for network issues

## Configuration

### Backend Configuration
```python
# src/main.py
BASE_URL = "https://your-deployed-backend.com"  # Update for production
DEBUG = False  # Set to False for production
```

### iOS Configuration
```swift
// iOS/Shared/AIService.swift
private let baseURL = "https://your-deployed-backend.com/api/ai"  // Update URL
```

### App Groups Setup
1. In Apple Developer Portal:
   - Create App Group: `group.ai.flirrt.shared`
   - Add to both app identifiers
2. In Xcode:
   - Enable App Groups capability
   - Select the created group

## Security Considerations

### API Security
- Use HTTPS for all communications
- Implement rate limiting
- Validate all input data
- Sanitize image data

### iOS Security
- Photo access only with user permission
- Secure App Groups communication
- No sensitive data in keyboard extension
- Proper error handling

### Privacy Compliance
- Clear privacy policy
- User consent for photo access
- Data retention policies
- GDPR/CCPA compliance

## Monitoring and Analytics

### Backend Monitoring
```python
# Add to Flask app
import logging
logging.basicConfig(level=logging.INFO)

# Monitor key metrics:
# - API response times
# - Error rates
# - AI model usage
# - User engagement
```

### iOS Analytics
```swift
// Add analytics for:
// - Keyboard usage frequency
// - Photo selection rates
// - Suggestion selection rates
// - User retention
```

## Troubleshooting

### Common Issues

#### Keyboard Not Appearing
1. Check if keyboard is enabled in Settings
2. Verify App Groups configuration
3. Check entitlements file
4. Restart device/simulator

#### Photo Picker Not Opening
1. Verify photo library permissions
2. Check App Groups communication
3. Review console logs for errors
4. Test with different photo sources

#### AI Suggestions Not Loading
1. Check backend URL configuration
2. Verify API keys are set
3. Test backend endpoints directly
4. Check network connectivity

#### App Groups Communication Issues
1. Verify group identifier matches
2. Check entitlements on both targets
3. Test with UserDefaults directly
4. Review synchronization calls

### Debug Commands
```bash
# Test backend health
curl http://localhost:5000/api/ai/health

# Test suggestions
curl -X POST -H "Content-Type: application/json" \
  -d '{"context": "test"}' \
  http://localhost:5000/api/ai/test-suggestions

# Monitor iOS logs
xcrun simctl spawn booted log stream --predicate 'subsystem contains "ai.flirrt"'
```

## Performance Optimization

### Backend Optimization
- Implement response caching
- Optimize image processing
- Use connection pooling
- Monitor memory usage

### iOS Optimization
- Lazy load AI service
- Cache suggestions locally
- Optimize image compression
- Minimize App Groups writes

## Scaling Considerations

### Backend Scaling
- Horizontal scaling with load balancer
- Database for user preferences
- Redis for caching
- CDN for static assets

### iOS Scaling
- A/B testing framework
- Feature flags
- Crash reporting
- User feedback system

## Support and Maintenance

### Regular Tasks
- Monitor API usage and costs
- Update AI models as available
- Review user feedback
- Update privacy policies
- Security audits

### Version Updates
- Coordinate iOS and backend updates
- Maintain backward compatibility
- Test on multiple iOS versions
- Update documentation

## Success Metrics

### Technical Metrics
- API response time < 2 seconds
- 99.9% uptime
- Error rate < 1%
- Keyboard activation rate > 80%

### User Metrics
- Daily active users
- Suggestion selection rate
- User retention
- App Store ratings

## Contact and Support

For deployment issues or questions:
- Check GitHub repository issues
- Review documentation
- Contact development team
- Submit feedback through app

---

**Last Updated**: September 12, 2025  
**Version**: 1.0.0  
**Status**: Ready for Production

