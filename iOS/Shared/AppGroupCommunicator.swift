import Foundation

/// Handles communication between the main app and keyboard extension via App Groups
class AppGroupCommunicator {
    static let shared = AppGroupCommunicator()
    
    private let suiteName = "group.ai.flirrt.shared"
    private let photoRequestKey = "photoSelectionRequested"
    private let photoRequestTimeKey = "photoSelectionRequestTime"
    private let selectedPhotoKey = "selectedPhotoData"
    private let aiSuggestionsKey = "aiSuggestions"
    
    private var sharedDefaults: UserDefaults? {
        return UserDefaults(suiteName: suiteName)
    }
    
    private init() {}
    
    // MARK: - Photo Selection Request (Keyboard → Main App)
    
    /// Send a photo selection request from keyboard to main app
    func sendPhotoSelectionRequest() {
        guard let defaults = sharedDefaults else {
            print("❌ Failed to access shared UserDefaults")
            return
        }
        
        defaults.set(true, forKey: photoRequestKey)
        defaults.set(Date(), forKey: photoRequestTimeKey)
        defaults.synchronize()
        
        print("📡 Photo selection request sent via App Groups")
    }
    
    /// Check if there's a pending photo selection request (Main App)
    func hasPendingPhotoRequest() -> Bool {
        guard let defaults = sharedDefaults else { return false }
        return defaults.bool(forKey: photoRequestKey)
    }
    
    /// Clear the photo selection request (Main App)
    func clearPhotoRequest() {
        guard let defaults = sharedDefaults else { return }
        defaults.removeObject(forKey: photoRequestKey)
        defaults.removeObject(forKey: photoRequestTimeKey)
        defaults.synchronize()
        
        print("🧹 Photo selection request cleared")
    }
    
    // MARK: - Photo Data Sharing (Main App → Keyboard)
    
    /// Store selected photo data for keyboard access (Main App)
    func storeSelectedPhoto(data: Data) {
        guard let defaults = sharedDefaults else {
            print("❌ Failed to store photo data")
            return
        }
        
        defaults.set(data, forKey: selectedPhotoKey)
        defaults.synchronize()
        
        print("📸 Photo data stored in App Groups (size: \(data.count) bytes)")
    }
    
    /// Retrieve selected photo data (Keyboard)
    func getSelectedPhotoData() -> Data? {
        guard let defaults = sharedDefaults else { return nil }
        return defaults.data(forKey: selectedPhotoKey)
    }
    
    /// Clear stored photo data
    func clearSelectedPhoto() {
        guard let defaults = sharedDefaults else { return }
        defaults.removeObject(forKey: selectedPhotoKey)
        defaults.synchronize()
        
        print("🧹 Photo data cleared from App Groups")
    }
    
    // MARK: - AI Suggestions Sharing (Main App → Keyboard)
    
    /// Store AI suggestions for keyboard display (Main App)
    func storeAISuggestions(_ suggestions: [String]) {
        guard let defaults = sharedDefaults else {
            print("❌ Failed to store AI suggestions")
            return
        }
        
        defaults.set(suggestions, forKey: aiSuggestionsKey)
        defaults.synchronize()
        
        print("🤖 AI suggestions stored in App Groups: \(suggestions)")
    }
    
    /// Retrieve AI suggestions (Keyboard)
    func getAISuggestions() -> [String] {
        guard let defaults = sharedDefaults else { return [] }
        return defaults.stringArray(forKey: aiSuggestionsKey) ?? []
    }
    
    /// Clear AI suggestions
    func clearAISuggestions() {
        guard let defaults = sharedDefaults else { return }
        defaults.removeObject(forKey: aiSuggestionsKey)
        defaults.synchronize()
        
        print("🧹 AI suggestions cleared from App Groups")
    }
    
    // MARK: - Debugging
    
    /// Print current state of all shared data
    func debugPrintState() {
        guard let defaults = sharedDefaults else {
            print("❌ Cannot access shared UserDefaults")
            return
        }
        
        print("🔍 App Groups State:")
        print("  - Photo Request: \(defaults.bool(forKey: photoRequestKey))")
        print("  - Photo Request Time: \(defaults.object(forKey: photoRequestTimeKey) ?? "nil")")
        print("  - Photo Data Size: \(defaults.data(forKey: selectedPhotoKey)?.count ?? 0) bytes")
        print("  - AI Suggestions: \(defaults.stringArray(forKey: aiSuggestionsKey) ?? [])")
    }
}

