import Foundation
import UIKit

/// AI service client for communicating with Flirrt.ai backend
class AIService: ObservableObject {
    static let shared = AIService()
    
    private let baseURL = "http://localhost:5000/api/ai"
    private let session = URLSession.shared
    
    private init() {}
    
    /// Analyze a screenshot and get flirting suggestions
    func analyzeScreenshot(
        image: UIImage,
        currentText: String = "",
        context: String = ""
    ) async throws -> AIAnalysisResponse {
        
        guard let imageData = image.jpegData(compressionQuality: 0.8) else {
            throw AIServiceError.imageProcessingFailed
        }
        
        let base64Image = imageData.base64EncodedString()
        
        let requestBody = AIAnalysisRequest(
            imageData: base64Image,
            currentText: currentText,
            context: context,
            timestamp: ISO8601DateFormatter().string(from: Date())
        )
        
        guard let url = URL(string: "\(baseURL)/analyze-screenshot") else {
            throw AIServiceError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        do {
            request.httpBody = try JSONEncoder().encode(requestBody)
        } catch {
            throw AIServiceError.encodingFailed
        }
        
        print("🤖 Sending AI analysis request...")
        
        do {
            let (data, response) = try await session.data(for: request)
            
            guard let httpResponse = response as? HTTPURLResponse else {
                throw AIServiceError.invalidResponse
            }
            
            print("📡 AI service response status: \(httpResponse.statusCode)")
            
            if httpResponse.statusCode == 200 {
                let analysisResponse = try JSONDecoder().decode(AIAnalysisResponse.self, from: data)
                print("✅ AI analysis successful: \(analysisResponse.suggestions.count) suggestions")
                return analysisResponse
            } else {
                // Try to decode error response
                if let errorResponse = try? JSONDecoder().decode(AIErrorResponse.self, from: data) {
                    throw AIServiceError.serverError(errorResponse.error)
                } else {
                    throw AIServiceError.serverError("HTTP \(httpResponse.statusCode)")
                }
            }
        } catch {
            print("❌ AI service error: \(error)")
            throw error
        }
    }
    
    /// Test the AI service with mock suggestions
    func testSuggestions(context: String = "general") async throws -> [String] {
        guard let url = URL(string: "\(baseURL)/test-suggestions") else {
            throw AIServiceError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let requestBody = ["context": context]
        request.httpBody = try JSONEncoder().encode(requestBody)
        
        let (data, response) = try await session.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw AIServiceError.serverError("Test request failed")
        }
        
        let testResponse = try JSONDecoder().decode(AITestResponse.self, from: data)
        return testResponse.suggestions
    }
    
    /// Check if the AI service is healthy
    func healthCheck() async throws -> AIHealthResponse {
        guard let url = URL(string: "\(baseURL)/health") else {
            throw AIServiceError.invalidURL
        }
        
        let (data, _) = try await session.data(from: url)
        return try JSONDecoder().decode(AIHealthResponse.self, from: data)
    }
}

// MARK: - Data Models

struct AIAnalysisRequest: Codable {
    let imageData: String
    let currentText: String
    let context: String
    let timestamp: String
    
    enum CodingKeys: String, CodingKey {
        case imageData = "image_data"
        case currentText = "current_text"
        case context
        case timestamp
    }
}

struct AIAnalysisResponse: Codable {
    let success: Bool
    let visualAnalysis: String
    let suggestions: [String]
    let timestamp: String
    let modelUsed: ModelInfo
    
    enum CodingKeys: String, CodingKey {
        case success
        case visualAnalysis = "visual_analysis"
        case suggestions
        case timestamp
        case modelUsed = "model_used"
    }
}

struct ModelInfo: Codable {
    let visual: String
    let flirting: String
}

struct AITestResponse: Codable {
    let success: Bool
    let suggestions: [String]
    let context: String
    let modelUsed: String
    
    enum CodingKeys: String, CodingKey {
        case success
        case suggestions
        case context
        case modelUsed = "model_used"
    }
}

struct AIHealthResponse: Codable {
    let status: String
    let service: String
    let modelsAvailable: ModelsAvailable
    
    enum CodingKeys: String, CodingKey {
        case status
        case service
        case modelsAvailable = "models_available"
    }
}

struct ModelsAvailable: Codable {
    let openai: Bool
    let grok: Bool
    let gemini: Bool
}

struct AIErrorResponse: Codable {
    let error: String
}

// MARK: - Error Types

enum AIServiceError: Error, LocalizedError {
    case invalidURL
    case imageProcessingFailed
    case encodingFailed
    case invalidResponse
    case serverError(String)
    case networkError(Error)
    
    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid API URL"
        case .imageProcessingFailed:
            return "Failed to process image"
        case .encodingFailed:
            return "Failed to encode request"
        case .invalidResponse:
            return "Invalid server response"
        case .serverError(let message):
            return "Server error: \(message)"
        case .networkError(let error):
            return "Network error: \(error.localizedDescription)"
        }
    }
}

