import SwiftUI
import PhotosUI

struct ContentView: View {
    @EnvironmentObject var photoPickerManager: PhotoPickerManager
    @State private var isMonitoringRequests = false
    
    var body: some View {
        VStack(spacing: 30) {
            // Flirrt.ai Logo with heart-shaped 'rr'
            VStack(spacing: 10) {
                HStack(spacing: 0) {
                    Text("Fli")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                        .foregroundColor(.primary)
                    
                    // Heart-shaped 'rr' logo
                    ZStack {
                        Text("❤️")
                            .font(.title)
                        Text("rr")
                            .font(.caption)
                            .fontWeight(.bold)
                            .foregroundColor(.white)
                            .offset(y: -2)
                    }
                    
                    Text("t.ai")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                        .foregroundColor(.primary)
                }
                
                Text("AI-Powered Dating Assistant")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }
            .padding(.top, 50)
            
            Spacer()
            
            // Main content
            VStack(spacing: 20) {
                Image(systemName: "keyboard")
                    .font(.system(size: 60))
                    .foregroundColor(.pink)
                
                Text("Welcome to Flirrt.ai")
                    .font(.title2)
                    .fontWeight(.semibold)
                
                Text("Get AI-powered flirting suggestions right in your keyboard, across all dating apps.")
                    .font(.body)
                    .multilineTextAlignment(.center)
                    .foregroundColor(.secondary)
                    .padding(.horizontal)
                
                VStack(alignment: .leading, spacing: 10) {
                    HStack {
                        Image(systemName: "checkmark.circle.fill")
                            .foregroundColor(.green)
                        Text("Works in Tinder, Bumble, Hinge & more")
                    }
                    
                    HStack {
                        Image(systemName: "checkmark.circle.fill")
                            .foregroundColor(.green)
                        Text("AI analyzes screenshots for context")
                    }
                    
                    HStack {
                        Image(systemName: "checkmark.circle.fill")
                            .foregroundColor(.green)
                        Text("Never leave your dating app")
                    }
                    
                    HStack {
                        Image(systemName: isMonitoringRequests ? "checkmark.circle.fill" : "circle")
                            .foregroundColor(isMonitoringRequests ? .green : .gray)
                        Text("App Groups communication active")
                    }
                }
                .font(.subheadline)
                .padding(.horizontal)
            }
            
            Spacer()
            
            // Setup instructions and status
            VStack(spacing: 15) {
                if photoPickerManager.isProcessingPhoto {
                    HStack {
                        ProgressView()
                            .scaleEffect(0.8)
                        Text("Processing photo...")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }
                    .padding()
                    .background(Color(.systemGray6))
                    .cornerRadius(12)
                }
                
                Button(action: {
                    // Open Settings app to keyboard settings
                    if let settingsUrl = URL(string: UIApplication.openSettingsURLString) {
                        UIApplication.shared.open(settingsUrl)
                    }
                }) {
                    HStack {
                        Image(systemName: "gear")
                        Text("Enable Flirrt Keyboard")
                    }
                    .font(.headline)
                    .foregroundColor(.white)
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.pink)
                    .cornerRadius(12)
                }
                
                Text("Go to Settings > General > Keyboard > Keyboards > Add New Keyboard")
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
            }
            .padding(.horizontal)
            .padding(.bottom, 30)
        }
        .onAppear {
            isMonitoringRequests = true
            print("✅ ContentView monitoring active")
        }
        .sheet(isPresented: $photoPickerManager.isShowingPhotoPicker) {
            PhotoPickerView { result in
                photoPickerManager.handlePhotoSelection(result)
                photoPickerManager.isShowingPhotoPicker = false
            }
        }
    }
}

#Preview {
    ContentView()
        .environmentObject(PhotoPickerManager())
}

