//
//  SplitDetails.swift
//  SplitFreeIOS
//
//  Created by Artemiy Shvedov on 04.01.25.
//

import SwiftUI

struct SplitDetail: View {
    var split: Split;
    @Environment(Caches.self) var caches;
    
    var body: some View {
        VStack(alignment: .leading) {
            HStack {
                Text(split.title).font(.title)
                Spacer()
                Text("$ \(String(split.total_sum))").font(.title)
            }
            HStack {
                Text("Created: " + split.created.formatted(.dateTime
                    .day(.twoDigits)
                    .month(.wide)
                    .year(.defaultDigits)
                )).font(.caption)
            }
            
            HStack {
                Circle().frame(width: 50, height: 50)
                VStack(alignment: .leading) {
                    Text("Restaurant").font(.title2)
                    Text("Food").font(.caption)
                }
            }
            Divider().padding()
            Text("Payed:")
                .font(.headline)
                .padding(.bottom)
            ForEach(split.payers.sorted(by: >), id: \.value) { userUid, value in
                HStack {
                    Text(caches.userCache.users[userUid]?.name ?? "<Unknown>");
                    Spacer()
                    Text("$ \(String(value))")
                        .foregroundStyle(.green)
                }
            }

            Text("Borrowed:")
                .font(.headline)
                .padding([.top, .bottom])
            ForEach(split.spenders.sorted(by: >), id: \.value) { userUid, value in
                HStack {
                    Text(caches.userCache.users[userUid]?.name ?? "<Unknown>");
                    Spacer()
                    Text("$ \(String(value))")
                        .foregroundStyle(.red)
                }
            }
            Spacer()
        }
        .padding()
    }
}

#Preview {
    SplitDetail(split: SplitsCache().splits[0])
        .environment(UserState())
        .environment(Caches())
}
