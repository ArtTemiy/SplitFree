//
//  ContentView.swift
//  SplitFreeIOS
//
//  Created by Artemiy Shvedov on 28.12.24.
//

import SwiftUI

struct ContentView: View {
    var body: some View {
        VStack(spacing: 0) {
            Text("Hello!")
            Spacer()
            HStack(alignment: .center) {
                Text("a")
                Spacer()
                
                Text("asd")
                
                Spacer()
                Text("a")
            }
            .background(Color(.red))
        }
//        .padding()
    }
}

#Preview {
    ContentView()
}
