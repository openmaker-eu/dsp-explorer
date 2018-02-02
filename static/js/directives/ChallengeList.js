import * as _ from 'lodash'
import * as d3 from 'd3';

let template = `
    <style> .liked{ color:red;} </style>
    <!--<div class="col-md-12 col-xs-12">{$ challenges $}</div>-->
    <div class="col-md-12 col-xs-12" ng-repeat="challenge in challenges track by challenge.id">
        <img class="col-md-1" ng-src="{$ challenge.challenge_picture || challenge.company.company_picture $}" alt="">
        
        <div class="col-md-1">
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
    </div>
    <style></style>
`

export default [function(){
    return {
        template:template,
        scope: {},
        controller : ['$scope', '$http', function($scope, $http){
            
            $scope.challenges = []
            $scope.interested_ids = []
            
            $scope.get_data = ()=> Promise
                    .all([ $http.get('/api/v1.3/challenge/'), $http.get('/api/v1.3/interest_ids/') ])
                    .then(
                        res=>{
                            $scope.challenges = res[0].data || []
                            $scope.interested_ids = res[1].data || []
                            $scope.$apply()
                        },
                        err=>console.log('Error: ', err)
                    )
    
            $scope.get_data()
            
            $scope.click_interest = (challenge) =>
                ($scope.is_interested(challenge) ?
                    $http.delete('/api/v1.3/interest/challenge/'+challenge.id+'/') :
                    $http.post('/api/v1.3/interest/challenge/'+challenge.id+'/')
                )
                .then(res=>$scope.get_data(),err=>console.log(err))
            
            $scope.is_interested = (challenge)=>$scope.interested_ids.indexOf(challenge.id) > -1
 
        }]
    }
}]



