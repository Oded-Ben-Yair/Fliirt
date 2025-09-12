import SwiftUI
import PhotosUI

/// SwiftUI wrapper for PHPickerViewController
struct PhotoPickerView: UIViewControllerRepresentable {
    let onCompletion: (Result<[PHPickerResult], Error>) -> Void
    
    func makeUIViewController(context: Context) -> PHPickerViewController {
        var configuration = PHPickerConfiguration()
        configuration.filter = .images
        configuration.selectionLimit = 1
        configuration.preferredAssetRepresentationMode = .current
        
        let picker = PHPickerViewController(configuration: configuration)
        picker.delegate = context.coordinator
        return picker
    }
    
    func updateUIViewController(_ uiViewController: PHPickerViewController, context: Context) {
        // No updates needed
    }
    
    func makeCoordinator() -> Coordinator {
        Coordinator(onCompletion: onCompletion)
    }
    
    class Coordinator: NSObject, PHPickerViewControllerDelegate {
        let onCompletion: (Result<[PHPickerResult], Error>) -> Void
        
        init(onCompletion: @escaping (Result<[PHPickerResult], Error>) -> Void) {
            self.onCompletion = onCompletion
        }
        
        func picker(_ picker: PHPickerViewController, didFinishPicking results: [PHPickerResult]) {
            onCompletion(.success(results))
        }
    }
}

