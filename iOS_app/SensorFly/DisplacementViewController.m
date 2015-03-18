//
//  DisplacementViewController.m
//  SensorFly
//
//  Created by Juan Sebastian on 2/16/15.
//  Copyright (c) 2015 Juan Sebastian. All rights reserved.
//

#import "DisplacementViewController.h"
#import "AppDelegate.h"

@interface DisplacementViewController ()
@property (strong, nonatomic) IBOutlet UILabel *displacementLabel;
@property (strong, nonatomic) NSMutableArray *accelerationsX;
@property (strong, nonatomic) NSMutableArray *accelerationsY;
@property (strong, nonatomic) NSMutableArray *accelerationsZ;
@property (strong, nonatomic) NSDate *lastStep;
@property int steps;
@property BOOL done;
//@property (strong, nonatomic) NSMutableArray *velocities;
//@property (strong, nonatomic) CMPedometer* pedometer;
@end

@implementation DisplacementViewController

- (instancetype)init
{
    self = [super init];
    if (self) {
        self = [self initWithNibName:@"DisplacementView" bundle:nil];
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

- (NSString*)formatDistanceString:(NSString*)str {
    NSUInteger maxLen = 6;  // 3 decimal positions
    return [(str.length<maxLen)? str:[str substringToIndex:maxLen] stringByAppendingString:@" m"];
}

- (void)refreshDistance:(id)object {
    AppDelegate *appDelegate = [UIApplication sharedApplication].delegate;
    
    while (!self.done) {
        NSDictionary* sensorData = [appDelegate.apiHelper getToEndpointAsDictionary:@"getSensorData"];
        if (sensorData && [sensorData valueForKey:@"distance"]) {
            NSString* newLabel = [self formatDistanceString:[[sensorData valueForKey:@"distance"] stringValue]];
            [self.displacementLabel performSelectorOnMainThread:@selector(setText:) withObject:newLabel waitUntilDone:true];
        }
        usleep(50e3);   // 50ms
    }
}

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
    self.messageLabel.text = [self formatDistanceString:[self message]];
    self.done = false;

    [self performSelectorInBackground:@selector(refreshDistance:) withObject:nil];
    /* AppDelegate *appDeletate = [UIApplication sharedApplication].delegate;
     dispatch_async(dispatch_get_global_queue(QOS_CLASS_UTILITY, 0), ^(){
        while (!self.done) {
            NSDictionary* sensorData = [appDeletate.apiHelper getToEndpointAsDictionary:@"getSensorData"];
            if (sensorData && [sensorData valueForKey:@"distance"]) {
                NSString* newLabel = [[sensorData valueForKey:@"distance"] stringValue];
                [self.displacementLabel performSelectorOnMainThread:@selector(setText:) withObject:newLabel waitUntilDone:true];
            }
            sleep(.25);
        }
     });*/
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}
- (IBAction)tappedDone:(id)sender {
    // Send ground truth to server
    self.done = true;
    AppDelegate *appDeletate = [UIApplication sharedApplication].delegate;
    
    [appDeletate showNextViewControllerWithMessage:nil];
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
