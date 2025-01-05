//
//  Datetime.swift
//  SplitFreeIOS
//
//  Created by Artemiy Shvedov on 05.01.25.
//

import Foundation

func FormatDate(date: Date) -> String {
    return date.formatted(.dateTime
        .day(.twoDigits)
        .month(.wide)
        .year(.defaultDigits))
}
