import UIKit
import SwiftUI

class KeyboardViewController: UIInputViewController {
    
    override func updateViewConstraints() {
        super.updateViewConstraints()
        
        // Add custom view sizing here
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Set up the keyboard UI
        setupKeyboardUI()
    }
    
    override func viewWillLayoutSubviews() {
        super.viewWillLayoutSubviews()
    }
    
    override func textWillChange(_ textInput: UITextInput?) {
        // The app is about to change the document's contents. Perform any preparation here.
    }
    
    override func textDidChange(_ textInput: UITextInput?) {
        // The app has just changed the document's contents, the document context has been updated.
    }
    
    private func setupKeyboardUI() {
        // Create the SwiftUI view for the keyboard
        let keyboardView = KeyboardView { [weak self] in
            self?.handleHeartButtonTap()
        }
        
        // Wrap in UIHostingController
        let hostingController = UIHostingController(rootView: keyboardView)
        
        // Add as child view controller
        addChild(hostingController)
        view.addSubview(hostingController.view)
        hostingController.didMove(toParent: self)
        
        // Set up constraints
        hostingController.view.translatesAutoresizingMaskIntoConstraints = false
        NSLayoutConstraint.activate([
            hostingController.view.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            hostingController.view.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            hostingController.view.topAnchor.constraint(equalTo: view.topAnchor),
            hostingController.view.bottomAnchor.constraint(equalTo: view.bottomAnchor)
        ])
    }
    
    private func handleHeartButtonTap() {
        print("🔥 HEART BUTTON TOUCH DOWN")
        
        // Check if we have full access
        guard hasFullAccess else {
            print("❌ Full access not granted")
            insertText("❤️ (Enable Full Access in Settings)")
            return
        }
        
        // Send photo selection request via App Groups
        sendPhotoSelectionRequest()
        
        // Insert heart emoji as immediate feedback
        insertText("❤️")
    }
    
    private func sendPhotoSelectionRequest() {
        print("📡 Sending photo selection request")
        
        // Use App Groups to communicate with main app
        if let sharedDefaults = UserDefaults(suiteName: "group.ai.flirrt.shared") {
            sharedDefaults.set(true, forKey: "photoSelectionRequested")
            sharedDefaults.set(Date(), forKey: "photoSelectionRequestTime")
            sharedDefaults.synchronize()
            print("✅ Photo selection request sent via App Groups")
        } else {
            print("❌ Failed to access shared UserDefaults")
        }
    }
    
    private func insertText(_ text: String) {
        textDocumentProxy.insertText(text)
    }
}

// MARK: - SwiftUI Keyboard View
struct KeyboardView: View {
    let onHeartButtonTap: () -> Void
    
    var body: some View {
        VStack(spacing: 0) {
            // Top toolbar with Flirrt.ai branding
            HStack {
                // Flirrt.ai logo
                HStack(spacing: 2) {
                    Text("Fli")
                        .font(.caption)
                        .fontWeight(.bold)
                    
                    Text("❤️")
                        .font(.caption2)
                    
                    Text("t.ai")
                        .font(.caption)
                        .fontWeight(.bold)
                }
                .foregroundColor(.primary)
                
                Spacer()
                
                // Heart button for photo selection
                Button(action: onHeartButtonTap) {
                    HStack(spacing: 4) {
                        Image(systemName: "heart.fill")
                            .foregroundColor(.white)
                        Text("Add Photo")
                            .font(.caption)
                            .fontWeight(.medium)
                            .foregroundColor(.white)
                    }
                    .padding(.horizontal, 12)
                    .padding(.vertical, 6)
                    .background(Color.pink)
                    .cornerRadius(16)
                }
                .buttonStyle(PlainButtonStyle())
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 8)
            .background(Color(.systemGray6))
            
            // Keyboard content area
            VStack {
                Text("Tap ❤️ to analyze screenshots and get flirting suggestions!")
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
                    .padding()
                
                Spacer()
            }
            .frame(height: 120)
            .background(Color(.systemBackground))
        }
        .frame(height: 160)
    }
}

#Preview {
    KeyboardView {
        print("Heart button tapped in preview")
    }
}

