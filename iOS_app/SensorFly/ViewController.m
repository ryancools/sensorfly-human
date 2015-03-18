//
//  ViewController.m
//  SensorFly
//
//  Created by Juan Sebastian on 2/13/15.
//  Copyright (c) 2015 Juan Sebastian. All rights reserved.
//

#import "ViewController.h"
#import <CoreMotion/CoreMotion.h>
#import <dispatch/dispatch.h>
#define SEND_INTERVAL_SECS 1

@interface ViewController ()
@property (strong, nonatomic) CMMotionManager* motionManager;
@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    NSLog(@"Loaded that view");
    
    self.motionManager = [[CMMotionManager alloc]init];
    
    [self.motionManager startAccelerometerUpdates];
    [self.motionManager startGyroUpdates];
    [self.motionManager startMagnetometerUpdates];
    
    dispatch_async(dispatch_get_global_queue(QOS_CLASS_UTILITY, 0), ^(void) {
        while (true) {
            //[self postData];
            sleep(SEND_INTERVAL_SECS);
        }
    });
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

/*- (void)postData {
    NSLog(@"Tryin to post data, %@, %@, %@", self.motionManager.accelerometerData, self.motionManager.magnetometerData, self.motionManager.gyroData);
    if (self.motionManager.accelerometerData &&
        self.motionManager.magnetometerData &&
        self.motionManager.gyroData) {
        
        NSDictionary *accelerometerData = [[NSDictionary alloc] initWithObjects:@[[[NSNumber alloc]initWithDouble:self.motionManager.accelerometerData.acceleration.x],
                                                                                  [[NSNumber alloc]initWithDouble:self.motionManager.accelerometerData.acceleration.y],
                                                                                  [[NSNumber alloc]initWithDouble:self.motionManager.accelerometerData.acceleration.z]] forKeys:@[@"x", @"y", @"z"]];
        
        NSDictionary *magnetometerData = [[NSDictionary alloc] initWithObjects:@[[[NSNumber alloc]initWithDouble:self.motionManager.magnetometerData.magneticField.x],
                                                                                 [[NSNumber alloc]initWithDouble:self.motionManager.magnetometerData.magneticField.y],
                                                                                 [[NSNumber alloc]initWithDouble:self.motionManager.magnetometerData.magneticField.z]] forKeys:@[@"x", @"y", @"z"]];
        
        NSDictionary *gyroData = [[NSDictionary alloc] initWithObjects:@[[[NSNumber alloc]initWithDouble:self.motionManager.gyroData.rotationRate.x],
                                                                         [[NSNumber alloc]initWithDouble:self.motionManager.gyroData.rotationRate.y],
                                                                         [[NSNumber alloc]initWithDouble:self.motionManager.gyroData.rotationRate.z]] forKeys:@[@"x", @"y", @"z"]];
        
        NSDictionary *bodyDictionary = [[NSDictionary alloc] initWithObjects:@[accelerometerData, magnetometerData, gyroData] forKeys:@[@"accelerometerData", @"magnetometerData", @"gyroData"]];
        
        NSMutableURLRequest *request = [[NSMutableURLRequest alloc] initWithURL: [NSURL URLWithString:API_URL]];
        NSData *jsonData = [NSJSONSerialization dataWithJSONObject:bodyDictionary options:NSJSONWritingPrettyPrinted error:nil];
        
        [request setHTTPMethod:@"POST"];
        [request setHTTPBody: jsonData];
        [request setValue:@"application/json" forHTTPHeaderField:@"Content-Type"];
        
        NSLog(@"Sending request with contents: %@", [[NSString alloc] initWithData:jsonData encoding:NSUTF8StringEncoding]);
        
        NSError* error;
        
        [NSURLConnection sendSynchronousRequest:request returningResponse:nil error:&error];
        
        if (error) {
            NSLog(@"There was an error: %@", error);
        }
    }
}*/

@end
