import SwiftUI

/// Debug view for monitoring App Groups communication
struct AppGroupsDebugView: View {
    @State private var debugInfo: String = "Loading..."
    @State private var refreshTimer: Timer?
    
    private let communicator = AppGroupCommunicator.shared
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    // Header
                    VStack(alignment: .leading, spacing: 8) {
                        Text("App Groups Debug")
                            .font(.title2)
                            .fontWeight(.bold)
                        
                        Text("Real-time monitoring of communication between main app and keyboard extension")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                    
                    // Debug info display
                    VStack(alignment: .leading, spacing: 12) {
                        Text("Current State:")
                            .font(.headline)
                        
                        Text(debugInfo)
                            .font(.system(.caption, design: .monospaced))
                            .padding()
                            .background(Color(.systemGray6))
                            .cornerRadius(8)
                    }
                    
                    // Test buttons
                    VStack(spacing: 12) {
                        Text("Test Actions:")
                            .font(.headline)
                        
                        Button("Simulate Photo Request") {
                            communicator.sendPhotoSelectionRequest()
                            refreshDebugInfo()
                        }
                        .buttonStyle(.borderedProminent)
                        
                        Button("Clear All Data") {
                            communicator.clearPhotoRequest()
                            communicator.clearSelectedPhoto()
                            communicator.clearAISuggestions()
                            refreshDebugInfo()
                        }
                        .buttonStyle(.bordered)
                        
                        Button("Add Mock AI Suggestions") {
                            let mockSuggestions = [
                                "Hey! I love your style 😍",
                                "That photo is amazing! Where was it taken?",
                                "You seem like someone I'd love to get to know better ✨"
                            ]
                            communicator.storeAISuggestions(mockSuggestions)
                            refreshDebugInfo()
                        }
                        .buttonStyle(.bordered)
                    }
                    
                    Spacer()
                }
                .padding()
            }
            .navigationTitle("Debug")
            .navigationBarTitleDisplayMode(.inline)
            .onAppear {
                startAutoRefresh()
            }
            .onDisappear {
                stopAutoRefresh()
            }
        }
    }
    
    private func startAutoRefresh() {
        refreshDebugInfo()
        refreshTimer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { _ in
            refreshDebugInfo()
        }
    }
    
    private func stopAutoRefresh() {
        refreshTimer?.invalidate()
        refreshTimer = nil
    }
    
    private func refreshDebugInfo() {
        let timestamp = DateFormatter.localizedString(from: Date(), dateStyle: .none, timeStyle: .medium)
        
        guard let sharedDefaults = UserDefaults(suiteName: "group.ai.flirrt.shared") else {
            debugInfo = "❌ Cannot access App Groups UserDefaults"
            return
        }
        
        let photoRequest = sharedDefaults.bool(forKey: "photoSelectionRequested")
        let photoRequestTime = sharedDefaults.object(forKey: "photoSelectionRequestTime") as? Date
        let photoDataSize = sharedDefaults.data(forKey: "selectedPhotoData")?.count ?? 0
        let aiSuggestions = sharedDefaults.stringArray(forKey: "aiSuggestions") ?? []
        
        debugInfo = """
        Last Updated: \(timestamp)
        
        📡 Photo Request: \(photoRequest ? "✅ Active" : "❌ None")
        ⏰ Request Time: \(photoRequestTime?.formatted() ?? "None")
        📸 Photo Data: \(photoDataSize) bytes
        🤖 AI Suggestions: \(aiSuggestions.count) items
        
        Suggestions:
        \(aiSuggestions.isEmpty ? "None" : aiSuggestions.enumerated().map { "  \($0.offset + 1). \($0.element)" }.joined(separator: "\n"))
        
        Raw UserDefaults:
        \(sharedDefaults.dictionaryRepresentation().filter { $0.key.contains("flirrt") || $0.key.contains("photo") || $0.key.contains("ai") })
        """
    }
}

#Preview {
    AppGroupsDebugView()
}

