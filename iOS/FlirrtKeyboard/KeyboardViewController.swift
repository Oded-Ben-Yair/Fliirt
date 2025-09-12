import UIKit
import SwiftUI

class KeyboardViewController: UIInputViewController {
    
    private var keyboardHeight: CGFloat = 160
    private let communicator = AppGroupCommunicator.shared
    
    override func updateViewConstraints() {
        super.updateViewConstraints()
        
        // Set keyboard height
        let heightConstraint = NSLayoutConstraint(
            item: view!,
            attribute: .height,
            relatedBy: .equal,
            toItem: nil,
            attribute: .notAnAttribute,
            multiplier: 0.0,
            constant: keyboardHeight
        )
        heightConstraint.priority = UILayoutPriority(999)
        view.addConstraint(heightConstraint)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Set up the keyboard UI
        setupKeyboardUI()
        
        // Start monitoring for AI suggestions
        startMonitoringAISuggestions()
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
        let keyboardView = KeyboardView(
            onHeartButtonTap: { [weak self] in
                self?.handleHeartButtonTap()
            },
            onSuggestionTap: { [weak self] suggestion in
                self?.handleSuggestionTap(suggestion)
            },
            suggestions: []
        )
        
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
        communicator.sendPhotoSelectionRequest()
        
        // Insert heart emoji as immediate feedback
        insertText("❤️")
        
        // Show loading state
        updateKeyboardWithLoadingState()
    }
    
    private func handleSuggestionTap(_ suggestion: String) {
        print("💬 Suggestion selected: \(suggestion)")
        
        // Replace the heart emoji with the selected suggestion
        if let documentProxy = textDocumentProxy as? UITextDocumentProxy {
            // Delete the heart emoji if it's the last character
            if let lastChar = documentProxy.documentContextBeforeInput?.last,
               String(lastChar) == "❤️" {
                documentProxy.deleteBackward()
            }
        }
        
        // Insert the selected suggestion
        insertText(suggestion)
        
        // Clear suggestions after use
        communicator.clearAISuggestions()
        updateKeyboardWithSuggestions([])
    }
    
    private func startMonitoringAISuggestions() {
        // Check for AI suggestions every 0.5 seconds
        Timer.scheduledTimer(withTimeInterval: 0.5, repeats: true) { [weak self] _ in
            self?.checkForAISuggestions()
        }
    }
    
    private func checkForAISuggestions() {
        let suggestions = communicator.getAISuggestions()
        if !suggestions.isEmpty {
            print("🤖 Received AI suggestions: \(suggestions)")
            updateKeyboardWithSuggestions(suggestions)
        }
    }
    
    private func updateKeyboardWithLoadingState() {
        // Update the keyboard UI to show loading state
        DispatchQueue.main.async { [weak self] in
            self?.setupKeyboardUIWithState(.loading)
        }
    }
    
    private func updateKeyboardWithSuggestions(_ suggestions: [String]) {
        // Update the keyboard UI to show suggestions
        DispatchQueue.main.async { [weak self] in
            self?.setupKeyboardUIWithState(.suggestions(suggestions))
        }
    }
    
    private func setupKeyboardUIWithState(_ state: KeyboardState) {
        // Remove existing child view controllers
        children.forEach { child in
            child.willMove(toParent: nil)
            child.view.removeFromSuperview()
            child.removeFromParent()
        }
        
        // Create new keyboard view with state
        let keyboardView = KeyboardView(
            onHeartButtonTap: { [weak self] in
                self?.handleHeartButtonTap()
            },
            onSuggestionTap: { [weak self] suggestion in
                self?.handleSuggestionTap(suggestion)
            },
            suggestions: state.suggestions,
            isLoading: state.isLoading
        )
        
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
    
    private func insertText(_ text: String) {
        textDocumentProxy.insertText(text)
    }
}

// MARK: - Keyboard State
enum KeyboardState {
    case initial
    case loading
    case suggestions([String])
    
    var suggestions: [String] {
        switch self {
        case .suggestions(let suggestions):
            return suggestions
        default:
            return []
        }
    }
    
    var isLoading: Bool {
        switch self {
        case .loading:
            return true
        default:
            return false
        }
    }
}

// MARK: - SwiftUI Keyboard View
struct KeyboardView: View {
    let onHeartButtonTap: () -> Void
    let onSuggestionTap: (String) -> Void
    let suggestions: [String]
    let isLoading: Bool
    
    init(onHeartButtonTap: @escaping () -> Void, 
         onSuggestionTap: @escaping (String) -> Void, 
         suggestions: [String] = [], 
         isLoading: Bool = false) {
        self.onHeartButtonTap = onHeartButtonTap
        self.onSuggestionTap = onSuggestionTap
        self.suggestions = suggestions
        self.isLoading = isLoading
    }
    
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
                        if isLoading {
                            ProgressView()
                                .scaleEffect(0.7)
                                .progressViewStyle(CircularProgressViewStyle(tint: .white))
                        } else {
                            Image(systemName: "heart.fill")
                                .foregroundColor(.white)
                        }
                        
                        Text(isLoading ? "Analyzing..." : "Add Photo")
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
                .disabled(isLoading)
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 8)
            .background(Color(.systemGray6))
            
            // Main content area
            if !suggestions.isEmpty {
                // Show AI suggestions
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 8) {
                        ForEach(Array(suggestions.enumerated()), id: \.offset) { index, suggestion in
                            Button(action: {
                                onSuggestionTap(suggestion)
                            }) {
                                Text(suggestion)
                                    .font(.caption)
                                    .foregroundColor(.primary)
                                    .padding(.horizontal, 12)
                                    .padding(.vertical, 8)
                                    .background(Color(.systemGray5))
                                    .cornerRadius(12)
                                    .lineLimit(2)
                            }
                            .buttonStyle(PlainButtonStyle())
                        }
                    }
                    .padding(.horizontal, 12)
                }
                .frame(height: 60)
                
                Text("Tap a suggestion to use it!")
                    .font(.caption2)
                    .foregroundColor(.secondary)
                    .padding(.bottom, 8)
            } else if isLoading {
                // Show loading state
                VStack(spacing: 8) {
                    ProgressView()
                        .scaleEffect(1.2)
                    
                    Text("AI is analyzing your screenshot...")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                .frame(maxHeight: .infinity)
            } else {
                // Show initial state
                VStack {
                    Text("Tap ❤️ to analyze screenshots and get flirting suggestions!")
                        .font(.caption)
                        .foregroundColor(.secondary)
                        .multilineTextAlignment(.center)
                        .padding()
                    
                    Spacer()
                }
                .frame(height: 120)
            }
        }
        .frame(height: 160)
        .background(Color(.systemBackground))
    }
}

#Preview {
    KeyboardView(
        onHeartButtonTap: {
            print("Heart button tapped in preview")
        },
        onSuggestionTap: { suggestion in
            print("Suggestion tapped: \(suggestion)")
        },
        suggestions: ["Hey! I love your style 😍", "That photo is amazing! Where was it taken?", "You seem like someone I'd love to get to know better ✨"]
    )
}

