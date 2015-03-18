//
//  GroundTruthViewController.h
//  SensorFly
//
//  Created by Juan Sebastian on 2/16/15.
//  Copyright (c) 2015 Juan Sebastian. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface GroundTruthViewController : UIViewController
- (IBAction)tappedSend:(id)sender;
@property (strong, nonatomic) IBOutlet UITextField *inputFieldX;
@property (strong, nonatomic) IBOutlet UITextField *inputFieldY;
@end
