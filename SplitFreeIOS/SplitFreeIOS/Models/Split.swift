//
//  Split.swift
//  SplitFreeIOS
//
//  Created by Artemiy Shvedov on 03.01.25.
//

import Foundation

struct Split: Codable, Hashable, Identifiable {
    var id: UUID;
    var groupId: UUID;
    var title: String;
    var category: String;
    var created: Date;
    var total_sum: Int32;
    var payers: Dictionary<UUID, Int32>;
    var spenders: Dictionary<UUID, Int32>;
    
    func getUserBalance(uid: UUID) -> Int32? {
        if (payers[uid] == nil && spenders[uid] == nil) {
            return nil
        }
        return payers[uid, default: 0]  - spenders[uid, default: 0];
    }
    
    func getPayerName(userState: UserState, caches: Caches) -> String {
        if (payers.count == 1) {
            let userUid: UUID = payers.first!.key;
            if (userUid == userState.user.id) {
                return "You";
            }
            return String(caches.userCache.users[userUid]?.name ?? "<Unknown>");
        }
        return "They";
    }
}
