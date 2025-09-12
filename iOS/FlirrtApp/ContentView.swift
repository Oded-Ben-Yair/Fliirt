import SwiftUI

struct ContentView: View {
    var body: some View {
        VStack(spacing: 30) {
            VStack(spacing: 10) {
                HStack(spacing: 0) {
                    Text("Fli")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                        .foregroundColor(.primary)
                    
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
            
            VStack(spacing: 20) {
                Image(systemName: "keyboard")
                    .font(.system(size: 60))
                    .foregroundColor(.pink)
                
                Text("Welcome to Flirrt.ai")
                    .font(.title2)
                    .fontWeight(.semibold)
                
                Text("Get AI-powered flirting suggestions right in your keyboard.")
                    .font(.body)
                    .multilineTextAlignment(.center)
                    .foregroundColor(.secondary)
                    .padding(.horizontal)
            }
            
            Spacer()
            
            Button(action: {
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
            .padding(.horizontal)
            .padding(.bottom, 30)
        }
    }
}

#Preview {
    ContentView()
}
