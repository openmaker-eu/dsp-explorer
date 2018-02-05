import * as _ from 'lodash'
import * as d3 from 'd3';

let template = `
    <style> .liked{ color:red;} </style>
    <a  href="{$ '/challenge/'+challenge.id+'/' $}"
        class="col-md-12 col-xs-12"
        ng-repeat="challenge in challenges track by challenge.id"
        ng-if="challenges.length > 0"
    >
        <img class="col-md-1"
            ng-src="{$ challenge.challenge_picture || challenge.company.company_picture $}"
            alt=""
        >
        
        <div class="col-md-1" ng-if="!profileid">
                <span class="fa fa-star pointer"
                    style="font-size:300%;"
                    ng-class="{ 'liked': is_interested(challenge) }"
                    ng-click="click_interest(challenge)"
                ></span>
        </div>

        <div class="col-md-9">
            <p>{$ challenge.title $}</p>
        </div>

        <div class="col-md-12">&nbsp;</div>
    </a>
    <div class="col-md-12" ng-if="challenges.length == 0">
        <h3>No challenges</h3>
    </div>
    <style></style>
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
                
                console.log(new_data, old_data, $scope.profileid);
                
                if(!$scope.profileid){
                    console.log('all')
                    Promise
                        .all([$http.get('/api/v1.3/challenge/'), $http.get('/api/v1.3/interest_ids/')])
                        .then(
                            res => {
                                $scope.challenges = res[0].data || []
                                $scope.interested_ids = res[1].data || []
                                $scope.$apply()
                            },
                            err => console.log('Error: ', err)
                        )
                }
                else {
                    console.log('filtered')
                    $http.get('/api/v1.3/profile/' + $scope.profileid + '/challenge/').then(res => {
                        console.log(res);
                        $scope.challenges = res.data || []

                    })
                }
            })
            
            $scope.is_interested = challenge =>
                $scope.interested_ids && $scope.interested_ids.indexOf(challenge.id) > -1
 
        }]
    }
}]



