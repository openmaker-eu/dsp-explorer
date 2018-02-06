import * as _ from 'lodash'
import * as d3 from 'd3';

let template = `
    <div class="col-md-12 col-xs-12"
        ng-repeat="challenge in challenges | filter:{published:true} as filtered_challenges"
        ng-if="filtered_challenges.length > 0"
        style="margin-bottom:1%; margin-top: 1%;"
    >
        <h4>
            <a href="{$ '/challenge/'+challenge.id+'/' $}" class="Aligner">
                <img class="col-md-2 col-xs-3" ng-src="{$ challenge.company.logo $}" alt="">
                <div class="col-md-2 col-xs-2" ng-if="!profileid">
                    <small style="font-size:200%; text-align: center;" >
                        <span
                            class="fa fa-star"
                            ng-class="{ 'text-red': is_interested(challenge), 'text-grey': !is_interested(challenge) }"
                            ng-click="click_interest(challenge)"
                            uib-tooltip="{$ is_interested(challenge) ? 'You are interested in this challenge': 'Go to the detail page to show interest in this Challenge' $}"
                        ></span>
                        <span class="">
                            <i class="fa fa-unlock-alt text-red"
                                ng-if="!challenge.closed"
                                uib-tooltip="Challenge is Open"
                            ></i>
                            <i class="fa fa-lock text-grey disabled"
                                ng-if="challenge.closed"
                                uib-tooltip="Challenge is Closed"
                            ></i>
                        </span>
                    </small>
                </div>
                <span class="col-md-8 col-xs-12">
                    <span>{$ challenge.title $}</span><br>
                    <span><small><i>{$ challenge.description $}</i></small></span>
                </span>
            </a>
        </h4>
    </div>
    <div class="col-md-12" ng-if="filtered_challenges.length == 0">
        <h3>No challenges</h3>
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



