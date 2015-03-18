//
//  DisplacementViewController.h
//  SensorFly
//
//  Created by Juan Sebastian on 2/16/15.
//  Copyright (c) 2015 Juan Sebastian. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface DisplacementViewController : UIViewController
- (instancetype)initWithMessage: (NSString*)message;
@property (strong, nonatomic) NSString* message;
@property (strong, nonatomic) IBOutlet UILabel *messageLabel;
@end
