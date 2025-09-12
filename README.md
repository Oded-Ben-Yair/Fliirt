# Flirrt.ai - AI-Powered Dating Assistant

Flirrt.ai is an innovative iOS keyboard extension that provides AI-generated flirting suggestions based on visual analysis of dating app screenshots. The app helps users craft engaging, personalized messages without ever leaving their dating apps.

## 🎯 Core Features

- **Seamless Integration**: Works across all dating apps (Tinder, Bumble, Hinge, etc.)
- **AI-Powered Analysis**: Uses advanced AI models to analyze screenshots and conversation context
- **Smart Suggestions**: Provides 3 personalized flirting options based on profile analysis
- **Privacy-First**: Minimal data retention, secure processing
- **Never Leave the App**: Complete workflow within the keyboard extension

## 🏗️ Architecture

### iOS Components
- **Main App (FlirrtApp)**: User onboarding, settings, photo picker handler
- **Keyboard Extension (FlirrtKeyboard)**: Core user interface and AI integration
- **App Groups**: Secure communication between main app and keyboard extension

### AI Model Strategy
- **Visual Analysis**: OpenAI GPT-5 (superior multimodal understanding)
- **Flirting Generation**: xAI Grok 4 (personality-driven, engaging suggestions)
- **Fallback**: Google Gemini 2.5 Pro (speed and reliability)

### Backend Services
- **API Gateway**: Request routing and authentication
- **AI Service**: Model integration and hybrid processing
- **User Service**: Account and subscription management
- **Caching Layer**: Redis for performance optimization

## 🛠️ Technology Stack

- **iOS**: Swift 6.0, SwiftUI, Xcode 16.x
- **Backend**: Python 3.11, FastAPI, PostgreSQL, Redis
- **AI Models**: GPT-5, Grok 4, Gemini 2.5 Pro
- **Deployment**: AWS, Docker, GitHub Actions

## 🚀 Development Status

Currently in active development following a systematic TDD approach:

1. ✅ Research and Architecture Design
2. 🔄 Environment Setup and Repository Initialization
3. ⏳ iOS Project Structure Setup
4. ⏳ Keyboard Extension Development
5. ⏳ Main App Development
6. ⏳ AI Integration
7. ⏳ Testing and Deployment

## 📱 User Flow

1. User enables Flirrt keyboard in iOS Settings
2. While chatting in any dating app, user taps the heart button
3. User selects a screenshot of the conversation/profile
4. AI analyzes the image and generates 3 flirting suggestions
5. User selects and sends their preferred suggestion

## 🔒 Privacy & Security

- End-to-end encryption for all data transmission
- Immediate deletion of screenshots after processing
- GDPR and CCPA compliant
- Minimal data collection and storage

## 📄 License

Proprietary - All rights reserved

## 👥 Team

Developed by the Flirrt.ai team with AI assistance from Manus.

---

*Making dating conversations effortless, one suggestion at a time.*

