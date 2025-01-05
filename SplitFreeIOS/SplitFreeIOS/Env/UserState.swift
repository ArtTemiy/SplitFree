//
//  UserState.swift
//  SplitFreeIOS
//
//  Created by Artemiy Shvedov on 04.01.25.
//

import Foundation

@Observable
class UserState {
    var user: User = User(
        id: UUID(uuid: (
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0
        )),
        name: "ArtTemiy");
}
