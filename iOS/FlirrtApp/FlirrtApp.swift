import SwiftUI

@main
struct FlirrtApp: App {
    @StateObject private var photoPickerManager = PhotoPickerManager()
    
    var body: some Scene {
        WindowGroup {
            TabView {
                ContentView()
                    .environmentObject(photoPickerManager)
                    .tabItem {
                        Image(systemName: "heart.fill")
                        Text("Home")
                    }
                
                SettingsView()
                    .tabItem {
                        Image(systemName: "gear")
                        Text("Settings")
                    }
            }
            .onAppear {
                setupBackgroundMonitoring()
            }
        }
    }
    
    private func setupBackgroundMonitoring() {
        // Start monitoring for photo requests from keyboard extension
        Timer.scheduledTimer(withTimeInterval: 0.5, repeats: true) { _ in
            photoPickerManager.checkForPhotoRequests()
        }
        
        print("✅ Background monitoring started for keyboard requests")
    }
}

