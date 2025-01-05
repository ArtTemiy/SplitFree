//
//  Caches.swift
//  SplitFreeIOS
//
//  Created by Artemiy Shvedov on 04.01.25.
//

import Foundation

@Observable
class Caches {
    var userCache = UsersCache();
    var groupsCache = GroupsCache();
    var splitsCache = SplitsCache();
}
