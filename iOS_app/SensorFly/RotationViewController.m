//
//  RotationViewController.m
//  SensorFly
//
//  Created by Juan Sebastian on 2/16/15.
//  Copyright (c) 2015 Juan Sebastian. All rights reserved.
//

#import "RotationViewController.h"
#import "AppDelegate.h"

@interface RotationViewController ()
@property (strong, nonatomic) IBOutlet UILabel *rotationLabel;
@property double baseRotation;
@property BOOL done;
@end

@implementation RotationViewController

- (instancetype)init
{
    self = [super init];
    if (self) {
        self = [self initWithNibName:@"RotationView" bundle:nil];
    }
    return self;
}

- (instancetype)initWithMessage: (NSString*)message
{
    self = [self init];
    if (self) {
        self.message = message;
    }
    return self;
}

- (NSString*)formatDegreeString:(NSString*)str {
    NSUInteger maxLen = 6;  // 2 decimal positions
    return [(str.length<maxLen)? str:[str substringToIndex:maxLen] stringByAppendingString:@"º"];
}

- (void)refreshRotation {
    AppDelegate *appDelegate = [UIApplication sharedApplication].delegate;
    
    while (!self.done) {
        NSDictionary* sensorData = [appDelegate.apiHelper getToEndpointAsDictionary:@"getSensorData"];
        if (sensorData && [sensorData valueForKey:@"rotation"]) {
            NSString* newLabel = [self formatDegreeString:[[sensorData valueForKey:@"rotation"] stringValue]];
            [self.rotationLabel performSelectorOnMainThread:@selector(setText:) withObject:newLabel waitUntilDone:true];
        }
        usleep(50e3);   // 50ms
    }
    NSLog(@"Done");
}

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
    self.messageLabel.text = [self formatDegreeString:[self message]];
    self.done = false;
    
    [self performSelectorInBackground:@selector(refreshRotation) withObject:nil];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}
- (IBAction)tappedDone:(id)sender {
    // Send ground truth to server
    self.done = true;
    AppDelegate *appDeletate = [UIApplication sharedApplication].delegate;
    
    [appDeletate showNextViewControllerWithMessage:@"0 (m)"];
}
- (IBAction)tappedRefreshUI:(id)sender {
    [self performSelectorInBackground:@selector(refreshRotation) withObject:nil];
}

/*
#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
}
*/

@end
