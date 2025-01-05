//
//  GroupDetails.swift
//  SplitFreeIOS
//
//  Created by Artemiy Shvedov on 05.01.25.
//

import SwiftUI

struct GroupDetails: View {
    @Environment(Caches.self) var caches;
    var group: Group;

    var body: some View {
        VStack(alignment: .leading) {
            Text(group.title)
                .font(.title)
            Text("Created: \(group.created.formatted())").font(.caption)
            Divider().padding()
            Text("Participants:").font(.headline).padding(.leading).padding(.bottom)
            ForEach(group.users, id: \.self) {userUid in
                Text(caches.userCache.users[userUid]?.name ?? "<Unknown>")
            }
            Spacer()
        }.padding()
    }
}

#Preview {
    GroupDetails(group: GroupsCache().groups.first!)
        .environment(Caches())
}
