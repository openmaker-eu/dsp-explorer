import * as _ from 'lodash'
import * as d3 from 'd3';

let template = `
    <style> .liked{ color:red;} </style>
    <div class="col-md-12 col-xs-12">
        <div class="col-md-6">
            <img style="width:100%;"
                ng-src="{$ challenge.challenge_picture $}"
                alt=""
            >
        </div>
        <div class="col-md-6">
            <h2>
                <span>{$ challenge.title $}</span>
                <span
                    style="font-size: 120%;"
                        class="fa fa-star pointer pull-right"
                        ng-class="{ 'liked': is_interested(challenge) }"
                        ng-click="click_interest(challenge)"
                ></span>
            </h2>
            <br>
            <h4><i>{$ challenge.description $}</i></h4>
            <br>
            <span>
                <span
                    class="btn login-button-active"
                    ng-repeat="tag in challenge.tags"
                    style="margin-right: 1%;"
                >{$ tag.name $}</span>
            </span>
        </div>
    </div>
    <div class="col-md-12">
    <br><br>
        <div class="col-md-12">
            <div ng-bind-html="challenge.details"></div>
        </div>
    </div>
`

export default [function(){
    return {
        template:template,
        scope: {
            id : '='
        },
        controller : ['$scope', '$http', function($scope, $http){
            
            $scope.get_data = ()=> Promise
                    .all([
                        $http.get('/api/v1.3/challenge/'+$scope.id+'/'),
                        $http.get('/api/v1.3/interest_ids/')
                    ])
                    .then(
                        res=>{
                            $scope.challenge = res[0].data || {}
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



