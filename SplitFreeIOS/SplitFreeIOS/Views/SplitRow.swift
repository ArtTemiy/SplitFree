//
//  SplitRow.swift
//  SplitFreeIOS
//
//  Created by Artemiy Shvedov on 03.01.25.
//

import SwiftUI

struct SplitRow: View {
    @Environment(UserState.self) var userState;
    @Environment(Caches.self) var caches;
    
    var split: Split;
    
    var body: some View {
        HStack() {
            Circle()
                .frame(width: 50, height: 50)
            VStack(alignment: .leading) {
                Text(split.title).font(.headline)
                Text(
                    split.created.formatted(.dateTime
                        .day(.twoDigits)
                        .month(.twoDigits)
                        .year(.twoDigits)
                    )
                ).font(.subheadline)
            
            }
            Spacer()
            VStack(alignment: .trailing) {
                let userBalance = split.getUserBalance(uid: userState.user.id)
                if (userBalance != nil) {
                    let color: Color = userBalance! < 0 ? Color.red : Color.green;
                    Text("$ " + String(abs(userBalance!)))
                        .font(.title3)
                        .foregroundStyle(color)
                    
                } else {
                    Text("-")
                        .font(.title3)
                        .foregroundStyle(.gray)
                }
                Text("\(split.getPayerName(userState: userState, caches: caches)) paid $" + String(split.total_sum))
                    .font(.caption)
            }
        }
    }
}

#Preview {
    List {
        SplitRow(split: SplitsCache().splits[0])
            .environment(UserState())
            .environment(Caches())
        
        SplitRow(split: SplitsCache().splits[1])
            .environment(UserState())
            .environment(Caches())
    
        SplitRow(split: SplitsCache().splits[2])
            .environment(UserState())
            .environment(Caches())
    }
}
