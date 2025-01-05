//
//  GroupView.swift
//  SplitFreeIOS
//
//  Created by Artemiy Shvedov on 05.01.25.
//

import SwiftUI

struct GroupView: View {
    @Environment(Caches.self) var caches;

    var group: Group;

    var body: some View {
        NavigationSplitView {
            VStack {
                VStack() {
                    Text(group.title)
                        .font(.title)
                    Divider()
                }.padding()
                List {
                    ForEach(caches.splitsCache.getSplits(groupId: group.id)) {split in
                        NavigationLink {
                            SplitDetail(split: split)
                        } label: {
                            SplitRow(split: split)
                        }
                    }
                }
                    .listStyle(.plain)
                Spacer()
                Button {
                    //
                } label: {
                    Label("Add expence", systemImage: "plus.circle")
                }

            }
        } detail: {
            Text("Group view")
        }
    }
}

#Preview {
    GroupView(group: GroupsCache().groups.first!)
        .environment(Caches())
        .environment(UserState())
}
