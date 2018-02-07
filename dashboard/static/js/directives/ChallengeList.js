import * as _ from 'lodash'
import * as d3 from 'd3';

let template = `
    <div class="col-md-12" ng-if="filtered_challenges.length == 0">
        <h2>
            No Challenges
        </h2>
    </div>
    <div class="col-md-3 col-sm-3 col-xs-12"
        ng-repeat="challenge in challenges | filter:{published:true} as filtered_challenges"
        ng-if="filtered_challenges.length > 0"
        style="margin-bottom:1%; margin-top: 1%;"
    >
        <div class="card margin-bottom-20">
            <a href="{$ '/challenge/'+challenge.id+'/' $}">
                <div class="card-image" style="border-bottom:solid 1px rgba(160, 160, 160, 0.2);">
                    <img style="min-width:100%;" ng-src="{$ challenge.picture $}" class="img-responsive">
                </div>
                <div class="card-content"><h5>{$ challenge.title $}</h5></div>
                <div class="card-action" style="height: auto;">
                    <p>{$ challenge.description | limitTo: 50 $}{$ challenge.description > 50 ? '...' : '' $}</p>
                    <p>
                        <i class="glyphicon glyphicon-time"></i> Dates: <br> {$ challenge.start_date | date:'dd MMMM yyyy' $} - {$ challenge.end_date | date:'dd MMMM yyyy' $}<br>
                    </p>
                    <p>
                        <span ng-hide="challenge.interested.length < 0"><i class="glyphicon glyphicon-heart"></i> Interested: {$ challenge.interested.length $}</span><br>
                    </p>
                    <p ng-if="!challenge.closed">
                        <i class="fa fa-unlock-alt" uib-tooltip="Challenge is Open"></i> Status:
                        Open<br>
                    </p>
                    <p ng-if="challenge.closed">
                        <i class="fa fa-lock text-grey disabled" uib-tooltip="Challenge is Closed"></i> Status:<br>
                        Closed<br>
                    </p>
                    <p>
                        <i ng-repeat="tag in challenge.tags">
                            <strong>#</strong>
                            <span>{$ tag.name $}</span>
                        </i>
                    </p>
                    <p>
                        <hr>
                    </p>
                    <div class="row">
                        <div class="col-md-6 col-sm-6 col-xs-6">
                            <p>Sponsor by: <strong>{$ challenge.company.name $}</strong></p>
                        </div>
                        <div class="col-md-6 col-sm-6 col-xs-6">
                            <img class="img-thumbnail img-responsive" ng-src="{$ challenge.company.logo $}" alt="">
                        </div>
                    </div>
                </div>
            </a>
        </div>
    </div>
`

export default [function(){
    return {
        template:template,
        scope: {
            profileid : '='
        },
        controller : ['$scope', '$http', function($scope, $http ) {
    
            $scope.challenges = []
            $scope.interested_ids = []
            
            $scope.$watch('profileid', (new_data, old_data) => {
                if(!$scope.profileid){
                    Promise
                        .all([$http.get('/api/v1.3/challenge/'), $http.get('/api/v1.3/interest_ids/')])
                        .then(
                            res => {
                                $scope.challenges = res[0].data || []
                                $scope.interested_ids = res[1].data || []
                                $scope.$apply(()=>$(window).trigger('resize'))
                            },
                            err => console.log('Error: ', err)
                        )
                }
                else {
                    $http.get('/api/v1.3/profile/' + $scope.profileid + '/challenge/').then(res => {
                        console.log(res);
                        $scope.challenges = res.data || []
                        $scope.$apply(()=>$(window).trigger('resize'))
                    })
                }
            })
            
            $scope.is_interested = challenge =>
                $scope.interested_ids && $scope.interested_ids.indexOf(challenge.id) > -1
 
        }]
    }
}]



