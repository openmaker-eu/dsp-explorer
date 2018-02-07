import * as _ from 'lodash'
import * as d3 from 'd3';

let template = `
    <div class="col-md-12" style="background: #f5f5f5; padding:2% 1%; margin-bottom:2%; border-radius: 3px;">
    <div class="col-md-12">
        <div class="col-md-12">
            <h1>
                <span>{$ challenge.title $}</span>&nbsp;&nbsp;
                <small style="font-size:100%; text-align:center;" >
                     <span
                         class="fa fa-thumbs-up"
                         ng-class="{'text-red':is_interested(challenge), 'text-grey':!is_interested(challenge), 'pointer':!challenge.closed }"
                         ng-click="challenge.closed || click_interest(challenge)"
                         uib-tooltip="{$ is_interested(challenge)? 'You are interested in this challenge': 'Click to show interest in this challenge' $}"
                     ></span>
                     <small><span>{$ challenge.interested.length $}</span></small>
                </small>
            </h1>
            <br>
        </div>
        <div class="col-md-12 visible-sm visible-xs visible-sm">
            <br>
            <span
                class="btn tag-button no-pointer"
                ng-repeat="tag in challenge.tags"
                style="margin-right: 1%;"
            >#{$ tag.name $}</span>
            <br>
        </div>
        
        </div>
        <div class="col-md-6">
            <img style="width:100%;" ng-src="{$ challenge.picture $}" alt="" >
        </div>
        <div class="col-md-6">
            <br>
            <!--Description-->
            <div class="col-md-12">
                <h4><i>{$ challenge.description $}</i></h4>
            </div>
            <br>
            <!-- Spec -->
            <div class="col-md-12">
                <br>
                <!--Status-->
                <p >
                    <strong class="text-danger"><i ng-class="{'fa fa-lock disabled': challenge.closed, 'fa fa-unlock-alt': !challenge.closed}" ></i>
                     &nbsp;Challenge</strong>&nbsp;&nbsp;{$ challenge.closed ? 'Closed': 'Open' $}
                </p>
                <!--Date-->
                <p ng-if="challenge.start_date">
                    <strong class="text-danger"><i class="fa fa-calendar-check-o "></i>&nbsp;Start:</strong>&nbsp;&nbsp;
                    {$ challenge.start_date | date:'dd MMMM yyyy' $}
                </p>
                <p ng-if="challenge.end_date">
                    <strong class="text-danger"><i class="fa fa-calendar-times-o"></i>&nbsp;End:</strong>&nbsp;&nbsp;
                    {$ challenge.end_date | date:'dd MMMM yyyy' $}
                </p>
            </div>
            <!--Tags-->
            <div class="col-md-12 .hidden-sm-down">
                <br>
                <span
                    class="btn tag-button no-pointer"
                    ng-repeat="tag in challenge.tags"
                    style="margin-right: 1%;"
                >#{$ tag.name $}</span>
            </div>
           <br>
           <span class="col-md-12">
               <br>
               <div class="row Aligner">
                    <img class="col-md-2 col-xs-3" ng-src="{$ challenge.company.logo $}" alt="">
                    <h3 class="col-md-10 co-xs-8" >{$ challenge.company.name $}</h3>
               </div>
           </span>
           
        </div>
        
        <!--<div class="col-md-12" style="margin-top: 1%;">-->
            <!--<hr>-->
           <!---->
        <!--</div>-->
    </div>

    <!--Challenge details-->
    <div class="col-md-12">
        <div class="col-md-12">
            <br>
            <div ng-bind-html="challenge.details"></div>
        </div>
    </div>
    
    <div class="col-md-12"><br><br></div>

`
var template_2 = `
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
        template:template+template_2,
        scope: { id : '=' },
        controller : ['$scope', '$http', '$sce', function($scope, $http, $sce){
            $scope.get_data = ()=> Promise
                    .all([
                        $http.get('/api/v1.3/challenge/'+$scope.id+'/'),
                        $http.get('/api/v1.3/interest_ids/')
                    ])
                    .then(
                        res=>{
                            res[0].data.details = res[0].data.details && $sce.trustAsHtml(res[0].data.details)
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



