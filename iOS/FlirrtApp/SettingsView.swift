import SwiftUI

struct SettingsView: View {
    @StateObject private var photoPickerManager = PhotoPickerManager()
    @State private var showingDebugView = false
    
    var body: some View {
        NavigationView {
            List {
                // App Information
                Section("App Information") {
                    HStack {
                        Image(systemName: "heart.fill")
                            .foregroundColor(.pink)
                        VStack(alignment: .leading) {
                            Text("Flirrt.ai")
                                .font(.headline)
                            Text("Version 1.0.0")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                    }
                }
                
                // Keyboard Setup
                Section("Keyboard Setup") {
                    Button(action: {
                        if let settingsUrl = URL(string: UIApplication.openSettingsURLString) {
                            UIApplication.shared.open(settingsUrl)
                        }
                    }) {
                        HStack {
                            Image(systemName: "gear")
                                .foregroundColor(.blue)
                            Text("Open iOS Settings")
                            Spacer()
                            Image(systemName: "arrow.up.right")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                    }
                    
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Setup Instructions:")
                            .font(.subheadline)
                            .fontWeight(.medium)
                        
                        VStack(alignment: .leading, spacing: 4) {
                            Text("1. Go to Settings > General > Keyboard")
                            Text("2. Tap 'Keyboards' > 'Add New Keyboard'")
                            Text("3. Select 'Flirrt' from the list")
                            Text("4. Enable 'Allow Full Access'")
                        }
                        .font(.caption)
                        .foregroundColor(.secondary)
                    }
                    .padding(.vertical, 4)
                }
                
                // Testing
                Section("Testing & Debug") {
                    Button(action: {
                        photoPickerManager.isShowingPhotoPicker = true
                    }) {
                        HStack {
                            Image(systemName: "photo")
                                .foregroundColor(.green)
                            Text("Test Photo Picker")
                        }
                    }
                    
                    Button(action: {
                        showingDebugView = true
                    }) {
                        HStack {
                            Image(systemName: "ladybug")
                                .foregroundColor(.orange)
                            Text("App Groups Debug")
                        }
                    }
                    
                    Button(action: {
                        AppGroupCommunicator.shared.debugPrintState()
                    }) {
                        HStack {
                            Image(systemName: "terminal")
                                .foregroundColor(.purple)
                            Text("Print Debug to Console")
                        }
                    }
                }
                
                // Privacy & Permissions
                Section("Privacy & Permissions") {
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Photo Library Access")
                            .font(.subheadline)
                            .fontWeight(.medium)
                        
                        Text("Flirrt.ai needs access to your photo library to analyze screenshots and provide personalized flirting suggestions. Your photos are processed locally and never stored permanently.")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                    .padding(.vertical, 4)
                    
                    VStack(alignment: .leading, spacing: 8) {
                        Text("App Groups Communication")
                            .font(.subheadline)
                            .fontWeight(.medium)
                        
                        Text("The keyboard extension communicates with the main app using secure App Groups to coordinate photo selection and AI suggestions.")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                    .padding(.vertical, 4)
                }
                
                // Support
                Section("Support") {
                    Link(destination: URL(string: "https://flirrt.ai/support")!) {
                        HStack {
                            Image(systemName: "questionmark.circle")
                                .foregroundColor(.blue)
                            Text("Help & Support")
                            Spacer()
                            Image(systemName: "arrow.up.right")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                    }
                    
                    Link(destination: URL(string: "https://flirrt.ai/privacy")!) {
                        HStack {
                            Image(systemName: "hand.raised")
                                .foregroundColor(.blue)
                            Text("Privacy Policy")
                            Spacer()
                            Image(systemName: "arrow.up.right")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                    }
                }
            }
            .navigationTitle("Settings")
            .sheet(isPresented: $photoPickerManager.isShowingPhotoPicker) {
                PhotoPickerView { result in
                    photoPickerManager.handlePhotoSelection(result)
                    photoPickerManager.isShowingPhotoPicker = false
                }
            }
            .sheet(isPresented: $showingDebugView) {
                AppGroupsDebugView()
            }
        }
    }
}

#Preview {
    SettingsView()
}

