//
//  ApiHelper.m
//  SensorFly
//
//  Created by Juan Sebastian on 2/16/15.
//  Copyright (c) 2015 Juan Sebastian. All rights reserved.
//

#import "ApiHelper.h"
#import "AppDelegate.h"

@implementation ApiHelper
- (NSDictionary*)sendGroundTruth:(NSString*)groundTruth withError:(NSError*)error {
    NSDictionary *data = [[NSDictionary alloc] initWithObjects:@[@"groundTruth",groundTruth] forKeys:@[@"type", @"data"]];
    
    return [self postData:data withError:error];
}

- (void)sendStop {
    NSDictionary *data = [[NSDictionary alloc] initWithObjects:@[@"stop"] forKeys:@[@"type"]];
    [self postData:data withError:nil];
    return;
}

- (void)sendMotionData:(CMDeviceMotion*)motion {
    NSDictionary *accelerometerData = [[NSDictionary alloc] initWithObjects:@[[[NSNumber alloc]initWithDouble:motion.userAcceleration.x],
                                                                              [[NSNumber alloc]initWithDouble:motion.userAcceleration.y],
                                                                              [[NSNumber alloc]initWithDouble:motion.userAcceleration.z]] forKeys:@[@"x", @"y", @"z"]];
    
    NSDictionary *magnetometerData = [[NSDictionary alloc] initWithObjects:@[[[NSNumber alloc]initWithDouble:motion.attitude.roll],
                                                                             [[NSNumber alloc]initWithDouble:motion.attitude.pitch],
                                                                             [[NSNumber alloc]initWithDouble:motion.attitude.yaw]] forKeys:@[@"roll", @"pitch", @"yaw"]];
    
    NSDictionary *gyroData = [[NSDictionary alloc] initWithObjects:@[[[NSNumber alloc]initWithDouble:motion.rotationRate.x],
                                                                     [[NSNumber alloc]initWithDouble:motion.rotationRate.y],
                                                                     [[NSNumber alloc]initWithDouble:motion.rotationRate.z]] forKeys:@[@"x", @"y", @"z"]];
    
    NSDictionary *bodyDictionary = [[NSDictionary alloc] initWithObjects:@[accelerometerData, magnetometerData, gyroData] forKeys:@[@"accelerometerData", @"magnetometerData", @"gyroData"]];
    
    NSDictionary *data = [[NSDictionary alloc] initWithObjects:@[@"update",bodyDictionary] forKeys:@[@"type", @"data"]];
    
    [self postData:data withError:nil];
    return;
}

- (NSString*)postToEndpoint:(NSString*)endpoint withData:(NSDictionary*)data {
    AppDelegate *appDeletate = [UIApplication sharedApplication].delegate;

    NSMutableURLRequest *request = [[NSMutableURLRequest alloc] initWithURL: [[[NSURL URLWithString:API_URL]URLByAppendingPathComponent:endpoint] URLByAppendingPathComponent:appDeletate.clientId]];
    NSData *jsonData = [NSJSONSerialization dataWithJSONObject:data options:NSJSONWritingPrettyPrinted error:nil];
    
    [request setHTTPMethod:@"POST"];
    [request setHTTPBody: jsonData];
    [request setValue:@"application/json" forHTTPHeaderField:@"Content-Type"];
    
    NSLog(@"Sending request to %@ with contents: %@", [[[NSURL URLWithString:API_URL]URLByAppendingPathComponent:endpoint] URLByAppendingPathComponent:appDeletate.clientId],[[NSString alloc] initWithData:jsonData encoding:NSUTF8StringEncoding]);
    
    NSData* result = [NSURLConnection sendSynchronousRequest:request returningResponse:nil error:nil];
    
    if (result) {
        NSString* resultString = [[NSString alloc] initWithData:result encoding:NSASCIIStringEncoding];
        return resultString;
    } else {
        return @"No result";
    }
}

- (NSString*)getToEndpoint:(NSString*)endpoint{
    AppDelegate *appDeletate = [UIApplication sharedApplication].delegate;

    NSMutableURLRequest *request = [[NSMutableURLRequest alloc] initWithURL: [[[NSURL URLWithString:API_URL]URLByAppendingPathComponent:endpoint] URLByAppendingPathComponent:appDeletate.clientId]];
    
    [request setHTTPMethod:@"GET"];
    
    NSLog(@"Sending request to %@", [[[NSURL URLWithString:API_URL]URLByAppendingPathComponent:endpoint] URLByAppendingPathComponent:appDeletate.clientId]);
    
    NSData* result = [NSURLConnection sendSynchronousRequest:request returningResponse:nil error:nil];
    
    if (result) {
        NSString* resultString = [[NSString alloc] initWithData:result encoding:NSASCIIStringEncoding];
        return resultString;
    } else {
        return @"No result";
    }
}

- (NSDictionary*)getToEndpointAsDictionary:(NSString*)endpoint{
    AppDelegate *appDeletate = [UIApplication sharedApplication].delegate;
    
    NSMutableURLRequest *request = [[NSMutableURLRequest alloc] initWithURL: [[[NSURL URLWithString:API_URL]URLByAppendingPathComponent:endpoint] URLByAppendingPathComponent:appDeletate.clientId]];
    
    [request setHTTPMethod:@"GET"];
    
    NSLog(@"Sending request to %@", [[[NSURL URLWithString:API_URL]URLByAppendingPathComponent:endpoint] URLByAppendingPathComponent:appDeletate.clientId]);
    
    NSData* result = [NSURLConnection sendSynchronousRequest:request returningResponse:nil error:nil];
        
    if (result) {
        return [NSJSONSerialization JSONObjectWithData:result options:NSJSONReadingAllowFragments error:nil];
    } else {
        return Nil;
    }
}

- (NSDictionary*)postData:(NSDictionary*)data withError:(NSError*) error {
    if (TESTING) {
        NSData *jsonData = [NSJSONSerialization dataWithJSONObject:data options:NSJSONWritingPrettyPrinted error:nil];
        //NSLog(@"Sending request with contents: %@", [[NSString alloc] initWithData:jsonData encoding:NSUTF8StringEncoding]);
        return [[NSDictionary alloc] initWithObjects:@[@"rotation", @"displacement"] forKeys:@[@"rotation", @"displacement"]];
    } else {
        NSMutableURLRequest *request = [[NSMutableURLRequest alloc] initWithURL: [NSURL URLWithString:API_URL]];
        NSData *jsonData = [NSJSONSerialization dataWithJSONObject:data options:NSJSONWritingPrettyPrinted error:nil];
        
        [request setHTTPMethod:@"POST"];
        [request setHTTPBody: jsonData];
        [request setValue:@"application/json" forHTTPHeaderField:@"Content-Type"];
        
        //NSLog(@"Sending request with contents: %@", [[NSString alloc] initWithData:jsonData encoding:NSUTF8StringEncoding]);
        
        NSData* result = [NSURLConnection sendSynchronousRequest:request returningResponse:nil error:&error];
        
        if (result) {
            return [NSJSONSerialization JSONObjectWithData:result options:NSJSONReadingAllowFragments error:nil];
        } else {
            return Nil;
        }
    }
}
@end
