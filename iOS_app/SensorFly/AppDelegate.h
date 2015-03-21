//
//  AppDelegate.h
//  SensorFly
//
//  Created by Juan Sebastian on 2/13/15.
//  Copyright (c) 2015 Juan Sebastian. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <CoreMotion/CoreMotion.h>
#import "GroundTruthViewController.h"
#import "RotationViewController.h"
#import "DisplacementViewController.h"
#import "RegisterViewController.h"
#import "WaitingViewController.h"
#import "ApiHelper.h"

typedef enum {
    REGISTER,
    GROUND_TRUTH,
    WAITING,
    ROTATION,
    DISPLACEMENT
} State;

@interface AppDelegate : UIResponder <UIApplicationDelegate>

@property (strong, nonatomic) UIWindow *window;
@property (strong, nonatomic) RegisterViewController *registerViewController;
@property (strong, nonatomic) GroundTruthViewController *groundTruthViewController;
@property (strong, nonatomic) WaitingViewController *waitingViewController;
@property (strong, nonatomic) RotationViewController *rotationViewController;
@property (strong, nonatomic) DisplacementViewController *displacementViewController;
@property (strong, nonatomic) ApiHelper *apiHelper;
@property (strong, nonatomic) NSString *clientId;
@property (strong, nonatomic) NSString *groundTruthX;
@property (strong, nonatomic) NSString *groundTruthY;


@property State state;

-(void) showNextViewControllerWithMessage: (NSString*) message;
-(void)setServerAddr:(NSString *)serverAddr;

@end

