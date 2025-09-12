import SwiftUI
import PhotosUI
import UIKit

/// Manages photo selection and processing for the main app
class PhotoPickerManager: ObservableObject {
    @Published var selectedImage: UIImage?
    @Published var isShowingPhotoPicker = false
    @Published var isProcessingPhoto = false
    
    private let communicator = AppGroupCommunicator.shared
    
    /// Handle photo selection from PHPickerViewController
    func handlePhotoSelection(_ result: Result<[PHPickerResult], Error>) {
        switch result {
        case .success(let results):
            guard let firstResult = results.first else { return }
            
            isProcessingPhoto = true
            
            // Load the image data
            firstResult.itemProvider.loadObject(ofClass: UIImage.self) { [weak self] object, error in
                DispatchQueue.main.async {
                    self?.isProcessingPhoto = false
                    
                    if let error = error {
                        print("❌ Error loading image: \(error)")
                        return
                    }
                    
                    guard let image = object as? UIImage else {
                        print("❌ Failed to cast object to UIImage")
                        return
                    }
                    
                    self?.selectedImage = image
                    self?.processSelectedImage(image)
                }
            }
            
        case .failure(let error):
            print("❌ Photo picker error: \(error)")
            isProcessingPhoto = false
        }
    }
    
    /// Process the selected image and store it for keyboard access
    private func processSelectedImage(_ image: UIImage) {
        print("📸 Processing selected image...")
        
        // Convert image to data for storage
        guard let imageData = image.jpegData(compressionQuality: 0.8) else {
            print("❌ Failed to convert image to data")
            return
        }
        
        // Store image data in App Groups for keyboard access
        communicator.storeSelectedPhoto(data: imageData)
        
        // Clear the photo selection request
        communicator.clearPhotoRequest()
        
        print("✅ Image processed and stored for keyboard access")
        
        // Trigger AI analysis
        triggerAIAnalysis(imageData: imageData)
    }
    
    /// Trigger AI analysis of the selected image
    private func triggerAIAnalysis(imageData: Data) {
        print("🤖 Triggering AI analysis...")
        
        // For now, simulate AI analysis with mock suggestions
        // This will be replaced with actual AI integration in Phase 5
        DispatchQueue.main.asyncAfter(deadline: .now() + 2.0) { [weak self] in
            let mockSuggestions = [
                "Hey! I love your style 😍",
                "That photo is amazing! Where was it taken?",
                "You seem like someone I'd love to get to know better ✨"
            ]
            
            self?.communicator.storeAISuggestions(mockSuggestions)
            print("✅ Mock AI suggestions stored")
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
    }
}

