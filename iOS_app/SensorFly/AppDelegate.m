//
//  AppDelegate.m
//  SensorFly
//
//  Created by Juan Sebastian on 2/13/15.
//  Copyright (c) 2015 Juan Sebastian. All rights reserved.
//

#import "AppDelegate.h"

@interface AppDelegate ()
@property (strong, nonatomic) NSDictionary* serverResponse;
@end

@implementation AppDelegate


- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
    // Override point for customization after application launch.
    
    self.apiHelper = [[ApiHelper alloc] init];
    
    self.state = REGISTER;
    self.registerViewController = [[RegisterViewController alloc] init];
    self.window = [[UIWindow alloc] initWithFrame:[[UIScreen mainScreen] bounds]];
    self.window.rootViewController = self.registerViewController;
    [self.window makeKeyAndVisible];
    
    return YES;
}

- (void)setServerAddr:(NSString *)serverAddr {
    [self.apiHelper setIpAndPort:serverAddr];
}

- (void)applicationWillResignActive:(UIApplication *)application {
    // Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
    // Use this method to pause ongoing tasks, disable timers, and throttle down OpenGL ES frame rates. Games should use this method to pause the game.
}

- (void)applicationDidEnterBackground:(UIApplication *)application {
    // Use this method to release shared resources, save user data, invalidate timers, and store enough application state information to restore your application to its current state in case it is terminated later.
    // If your application supports background execution, this method is called instead of applicationWillTerminate: when the user quits.
}

- (void)applicationWillEnterForeground:(UIApplication *)application {
    // Called as part of the transition from the background to the inactive state; here you can undo many of the changes made on entering the background.
}

- (void)applicationDidBecomeActive:(UIApplication *)application {
    // Restart any tasks that were paused (or not yet started) while the application was inactive. If the application was previously in the background, optionally refresh the user interface.
}

- (void)applicationWillTerminate:(UIApplication *)application {
    // Called when the application is about to terminate. Save data if appropriate. See also applicationDidEnterBackground:.
}

-(void) showNextViewControllerWithMessage: (NSString*)message {
    NSString* result;
    NSDictionary* data;
    
    switch (self.state) {
        case REGISTER:
            result = [self.apiHelper getToEndpoint:@"register"];
            NSLog(result);
            if ([result isEqualToString:@"Success"]) {
                self.groundTruthViewController = [[GroundTruthViewController alloc] init];
                self.window.rootViewController = self.groundTruthViewController;
                self.registerViewController = nil;
                self.state = GROUND_TRUTH;
                result = nil;
            } else {
                UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Error"
                                                                message:[NSString stringWithFormat:@"%@", @":("]
                                                               delegate:nil
                                                      cancelButtonTitle:@"OK"
                                                      otherButtonTitles:nil];
                [alert show];
            }
            break;

        case GROUND_TRUTH:
            data = [[NSDictionary alloc] initWithObjects:@[self.groundTruthX,self.groundTruthY] forKeys:@[@"x", @"y"]];
            result = [self.apiHelper postToEndpoint:@"groundTruth" withData:data];
            if ([result isEqualToString:@"Success"]) {
                self.waitingViewController = [[WaitingViewController alloc] init];
                self.window.rootViewController = self.waitingViewController;
                self.groundTruthViewController = nil;
                self.state = WAITING;
                data = nil;
                result = nil;
            } else {
                UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Error"
                                                                message:[NSString stringWithFormat:@"%@", @":("]
                                                               delegate:nil
                                                      cancelButtonTitle:@"OK"
                                                      otherButtonTitles:nil];
                [alert show];
            }
            break;
        
        case WAITING:
            self.serverResponse = [self.apiHelper getToEndpointAsDictionary:@"requestDirections"];
            if (self.serverResponse && [self.serverResponse valueForKey:@"rotate"] && [self.serverResponse valueForKey:@"move"]) {
                self.rotationViewController = [[RotationViewController alloc] initWithMessage:([(NSNumber* )[self.serverResponse valueForKey:@"rotate"] stringValue])];
                self.window.rootViewController = self.rotationViewController;
                self.groundTruthViewController = nil;
                self.state = ROTATION;
                [self.apiHelper getToEndpoint:@"startRotating"];
            } else {
                UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Error"
                                                                message:[NSString stringWithFormat:@"%@", @":("]
                                                               delegate:nil
                                                      cancelButtonTitle:@"OK"
                                                      otherButtonTitles:nil];
                [alert show];
            }
            break;
            
        case ROTATION:
            [self.apiHelper getToEndpoint:@"stopRotating"];
            [self.apiHelper getToEndpoint:@"startMoving"];
            self.displacementViewController = [[DisplacementViewController alloc] initWithMessage:([(NSNumber* )[self.serverResponse valueForKey:@"move"] stringValue])];
            self.window.rootViewController = self.displacementViewController;
            self.rotationViewController = nil;
            self.state = DISPLACEMENT;
            break;
            
        case DISPLACEMENT:
            [self.apiHelper getToEndpoint:@"stopMoving"];
            self.serverResponse = nil;
            self.groundTruthViewController = [[GroundTruthViewController alloc] init];
            self.window.rootViewController = self.groundTruthViewController;
            self.displacementViewController = nil;
            self.state = GROUND_TRUTH;
            break;
    }
}


@end
