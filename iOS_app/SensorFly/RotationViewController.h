//
//  RotationViewController.h
//  SensorFly
//
//  Created by Juan Sebastian on 2/16/15.
//  Copyright (c) 2015 Juan Sebastian. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface RotationViewController : UIViewController
@property (strong, nonatomic) IBOutlet UILabel *messageLabel;
@property (strong, nonatomic) NSString* message;
- (instancetype)initWithMessage: (NSString*)message;
- (IBAction)tappedRefreshUI:(id)sender;
@end
