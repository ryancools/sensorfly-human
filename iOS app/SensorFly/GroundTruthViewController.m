//
//  GroundTruthViewController.m
//  SensorFly
//
//  Created by Juan Sebastian on 2/16/15.
//  Copyright (c) 2015 Juan Sebastian. All rights reserved.
//

#import "GroundTruthViewController.h"
#import "RotationViewController.h"
#import "AppDelegate.h"

@interface GroundTruthViewController ()

@end

@implementation GroundTruthViewController

- (instancetype)init
{
    self = [super init];
    if (self) {
        self = [self initWithNibName:@"GroundTruthView" bundle:nil];
    }
    return self;
}

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
    [self.inputFieldX becomeFirstResponder];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

/*
#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
}
*/

- (IBAction)tappedSend:(id)sender {
    // Send ground truth to server    
    AppDelegate *appDeletate = [UIApplication sharedApplication].delegate;
    appDeletate.groundTruthX = self.inputFieldX.text;
    appDeletate.groundTruthY = self.inputFieldY.text;
    [appDeletate showNextViewControllerWithMessage:nil];
}
@end
