//
//  ApiHelper.h
//  SensorFly
//
//  Created by Juan Sebastian on 2/16/15.
//  Copyright (c) 2015 Juan Sebastian. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <CoreMotion/CoreMotion.h>
#define API_URL @"http://10.0.23.151:5001/"
#define TESTING true

@interface ApiHelper : NSObject
- (NSDictionary*)sendGroundTruth:(NSString*)groundTruth withError:(NSError*)error;
- (void)sendStop;
- (void)sendMotionData:(CMDeviceMotion*)motion;
- (NSString*)getToEndpoint:(NSString*)endpoint;
- (NSString*)postToEndpoint:(NSString*)endpoint withData:(NSDictionary*)data;
- (NSDictionary*)getToEndpointAsDictionary:(NSString*)endpoint;
@end
