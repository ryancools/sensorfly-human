//
//  GroundTruthViewController.h
//  SensorFly
//
//  Created by Juan Sebastian on 2/16/15.
//  Copyright (c) 2015 Juan Sebastian. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface RegisterViewController : UIViewController
- (IBAction)tappedSend:(id)sender;
@property (strong, nonatomic) IBOutlet UITextField *ipField;
@property (strong, nonatomic) IBOutlet UITextField *idNumField;
@end
