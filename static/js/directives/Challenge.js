import * as _ from 'lodash'
import * as d3 from 'd3';

let template = `
    <style> .liked{color:red;} </style>
    <div class="col-md-12" style="background: #f5f5f5; padding:2% 1%; margin-bottom:2%; border-radius: 3px;">
        <div class="col-md-6">
            <img style="width:100%;"
                ng-src="{$ challenge.challenge_picture $}"
                alt=""
            >
        </div>
        <div class="col-md-6">
            <!--Header-->
            <h2>
                <span>{$ challenge.title $}</span>
                &nbsp;
                <span style="font-size: 120%;"
                        class="fa fa-star pointer"
                        ng-class="{ 'text-danger': is_interested(challenge) }"
                        ng-click="click_interest(challenge)"
                ></span>
                <span class="pull-right">
                        <button class="btn login-button-active no-pointer" ng-if="!challenge.closed">Open</button>
                        <button class="btn login-button-active disabled" ng-if="challenge.closed">Closed</button>
                </span>
            </h2>
            <br>
            <!--Description-->
            <h4><i>{$ challenge.description $}</i></h4>
            <br>
            <!--Date-->
            <span>
                <p ng-if="challenge.start_date"><strong>Start:</strong>&nbsp;&nbsp;{$ challenge.start_date | date:'dd MMMM yyyy' $}</p>
                <p ng-if="challenge.end_date"><strong>End:</strong>&nbsp;&nbsp;{$ challenge.end_date | date:'dd MMMM yyyy' $}</p>
            </span>
            <br>
            <!--Tags-->
            <span>
                <span
                    class="btn login-button-active no-pointer"
                    ng-repeat="tag in challenge.tags"
                    style="margin-right: 1%;"
                >{$ tag.name $}</span>
            </span>
        </div>

    </div>
    
    <!--<div class="col-md-12"><br><br><br></div>-->
    
    <!--Challenge details-->
    <div class="col-md-12">
        <div class="col-md-12">
            <br>
            <div ng-bind-html="challenge.details"></div>
        </div>
    </div>
    
    <div class="col-md-12"><br><br></div>

    <!--Interested users-->
    <div class="col-md-12 margin-top-25" ng-if="challenge.interested.length > 0">
        <div class="well-red">{$ challenge.interested.length $} Interested users</div>
        
        <a href="/profile/{$ profile.id $}" ng-repeat="profile in challenge.interested | limitTo:20">
            <div class="row">
                <div class="col-md-1 col-xs-4">
                    <circle-image src="{$ profile.picture $}"
                        href="/profile/{$ profile.id $}"
                    ></circle-image>
                </div>
                <div class="col-md-10 col-xs-8">
                    <strong>{$ profile.user.first_name+' '+profile.user.last_name $}</strong>
                    <br><span>{$ profile.city $}</span><br>
                    <span ng-repeat="profile_tag in profile.tags">{$ profile_tag.name $}&nbsp;&nbsp;</span>
                </div>
            </div>
        </a>
        
    </div>

    
`

export default [function(){
    return {
        template:template,
        scope: { id : '=' },
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
                            $scope.$apply(()=>$(window).trigger('resize'))
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
            
            $scope.is_interested = (challenge)=>$scope.interested_ids && $scope.interested_ids.indexOf(challenge.id) > -1
 
        }]
    }
}]



