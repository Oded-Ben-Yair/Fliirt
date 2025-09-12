import SwiftUI
import PhotosUI
import UIKit

/// Manages photo selection and processing for the main app
class PhotoPickerManager: ObservableObject {
    @Published var selectedImage: UIImage?
    @Published var isShowingPhotoPicker = false
    @Published var isProcessingPhoto = false
    @Published var lastAnalysisResult: AIAnalysisResponse?
    @Published var errorMessage: String?
    
    private let communicator = AppGroupCommunicator.shared
    private let aiService = AIService.shared
    
    /// Handle photo selection from PHPickerViewController
    func handlePhotoSelection(_ result: Result<[PHPickerResult], Error>) {
        switch result {
        case .success(let results):
            guard let firstResult = results.first else { return }
            
            isProcessingPhoto = true
            errorMessage = nil
            
            // Load the image data
            firstResult.itemProvider.loadObject(ofClass: UIImage.self) { [weak self] object, error in
                DispatchQueue.main.async {
                    if let error = error {
                        print("❌ Error loading image: \(error)")
                        self?.isProcessingPhoto = false
                        self?.errorMessage = "Failed to load image"
                        return
                    }
                    
                    guard let image = object as? UIImage else {
                        print("❌ Failed to cast object to UIImage")
                        self?.isProcessingPhoto = false
                        self?.errorMessage = "Invalid image format"
                        return
                    }
                    
                    self?.selectedImage = image
                    self?.processSelectedImage(image)
                }
            }
            
        case .failure(let error):
            print("❌ Photo picker error: \(error)")
            isProcessingPhoto = false
            errorMessage = "Photo selection failed"
        }
    }
    
    /// Process the selected image and store it for keyboard access
    private func processSelectedImage(_ image: UIImage) {
        print("📸 Processing selected image...")
        
        // Convert image to data for storage
        guard let imageData = image.jpegData(compressionQuality: 0.8) else {
            print("❌ Failed to convert image to data")
            isProcessingPhoto = false
            errorMessage = "Failed to process image"
            return
        }
        
        // Store image data in App Groups for keyboard access
        communicator.storeSelectedPhoto(data: imageData)
        
        // Clear the photo selection request
        communicator.clearPhotoRequest()
        
        print("✅ Image processed and stored for keyboard access")
        
        // Trigger AI analysis
        Task {
            await performAIAnalysis(image: image)
        }
    }
    
    /// Perform AI analysis of the selected image
    private func performAIAnalysis(image: UIImage) async {
        print("🤖 Starting AI analysis...")
        
        do {
            // Get current text context from App Groups if available
            let currentText = communicator.getCurrentText() ?? ""
            
            // Perform AI analysis
            let analysisResult = try await aiService.analyzeScreenshot(
                image: image,
                currentText: currentText,
                context: "dating_app_screenshot"
            )
            
            await MainActor.run {
                self.lastAnalysisResult = analysisResult
                self.isProcessingPhoto = false
                
                // Store AI suggestions in App Groups for keyboard access
                self.communicator.storeAISuggestions(analysisResult.suggestions)
                
                print("✅ AI analysis complete: \(analysisResult.suggestions.count) suggestions")
                print("📝 Suggestions: \(analysisResult.suggestions)")
            }
            
        } catch {
            print("❌ AI analysis failed: \(error)")
            
            await MainActor.run {
                self.isProcessingPhoto = false
                self.errorMessage = "AI analysis failed: \(error.localizedDescription)"
                
                // Fallback to mock suggestions
                let fallbackSuggestions = [
                    "Hey! I love your style 😍",
                    "That photo is amazing! Where was it taken?",
                    "You seem like someone I'd love to get to know better ✨"
                ]
                
                self.communicator.storeAISuggestions(fallbackSuggestions)
                print("🔄 Using fallback suggestions")
            }
        }
    }
    
    /// Test AI service with mock data
    func testAIService() async {
        isProcessingPhoto = true
        errorMessage = nil
        
        do {
            let suggestions = try await aiService.testSuggestions(context: "test")
            
            await MainActor.run {
                self.isProcessingPhoto = false
                self.communicator.storeAISuggestions(suggestions)
                print("✅ AI test successful: \(suggestions)")
            }
            
        } catch {
            await MainActor.run {
                self.isProcessingPhoto = false
                self.errorMessage = "AI test failed: \(error.localizedDescription)"
                print("❌ AI test failed: \(error)")
            }
        }
    }
    
    /// Check for pending photo requests and show picker if needed
    func checkForPhotoRequests() {
        if communicator.hasPendingPhotoRequest() {
            print("📱 Photo request detected, showing picker...")
            isShowingPhotoPicker = true
        }
    }
    
    /// Reset the photo picker state
    func resetState() {
        selectedImage = nil
        isShowingPhotoPicker = false
        isProcessingPhoto = false
        lastAnalysisResult = nil
        errorMessage = nil
    }
    
    /// Get the last analysis summary for display
    func getAnalysisSummary() -> String? {
        guard let result = lastAnalysisResult else { return nil }
        
        return """
        Analysis: \(result.visualAnalysis.prefix(100))...
        Suggestions: \(result.suggestions.count)
        Models: \(result.modelUsed.visual) + \(result.modelUsed.flirting)
        """
    }
}

