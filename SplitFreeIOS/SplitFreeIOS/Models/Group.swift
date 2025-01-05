//
//  Group.swift
//  SplitFreeIOS
//
//  Created by Artemiy Shvedov on 05.01.25.
//

import Foundation

struct Group: Codable, Hashable {
    var id: UUID;
    var title: String;
    var created: Date;
    var users: [UUID];
}
