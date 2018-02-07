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
            <div class="card-image" style="border-bottom:solid 1px rgba(160, 160, 160, 0.2);">
                <img style="min-width:100%;" ng-src="{$ challenge.company.logo $}" class="img-responsive">
            </div>
            <div class="card-content"><h5>{$ challenge.title $}</h5></div>
            <div class="card-action" style="height: auto;">
                <div class="row">
                    <div class="col-md-12">
                        <p>
                            <i class="glyphicon glyphicon-thumbs-up"
                                ng-class="{ 'text-red': challenge.is_interested, 'text-grey': !challenge.is_interested }"
                                uib-tooltip="{$ challenge.is_interested ? 'You are interested in this challenge': 'Go to the detail page to show interest in this Challenge' $}"
                                tooltip-placement="right"
                            ></i>
                            Interested: {$ challenge.interested.length $}<br>
                        </p>

                        <p ng-if="!challenge.closed">
                            <i class="fa fa-unlock-alt text-red" uib-tooltip="Challenge is Open" tooltip-placement="right"></i> Status:
                            Open<br>
                        </p>
                        <p ng-if="challenge.closed">
                            <i class="fa fa-lock text-grey disabled" uib-tooltip="Challenge is Closed" tooltip-placement="right"></i> Status:<br>
                            Closed<br>
                        </p>
                        <!-- <p>
                            <i ng-repeat="tag in challenge.tags">
                                <strong>#</strong>
                                <span>{$ tag.name $}</span>
                            </i>
                        </p> -->

                        <p>Sponsor by: <strong>{$ challenge.company.name $}</strong></p>
                    </div>
                    <div class="col-md-12">
                        <hr>
                    </div>
                    <div class="col-md-12 text-right">
                        <a href="{$ '/challenge/'+challenge.id+'/' $}"><p>Read more <i class="glyphicon glyphicon-new-window"></i></p></a>
                    </div>
                </div>
            </div>
        </div>
    </div>
`

export default [function(){
    return {
        template:template,
        scope: {
            profileid : '=',
            all : '='
        },
        controller : ['$scope', '$http', function($scope, $http ) {
    
            $scope.challenges = []
            $scope.interested_ids = []
            
            $scope.$watch('[profileid, all]', (new_data, old_data) => {
                console.log(new_data);
                if($scope.profileid){
                    
                    let url = new_data[1]? '/api/v1.3/challenge/': '/api/v1.3/profile/' + $scope.profileid + '/challenge/'
                    $scope.get_data(url)
                }
            })
            
            $scope.get_data = (url) =>{
                $http.get(url).then(res => {
                    $scope.challenges = res.data || []
                    $scope.challenges = _.map($scope.challenges, el =>{
                        el.is_interested = _.filter(el.interested, {id:$scope.profileid}).length > 0
                        return el
                    })
                    $scope.$apply(()=>$(window).trigger('resize'))
                })
            }
            //
            // $scope.click_interest = (challenge) =>
            //     (challenge.is_interested ?
            //         $http.delete('/api/v1.3/interest/challenge/'+challenge.id+'/') :
            //         $http.post('/api/v1.3/interest/challenge/'+challenge.id+'/')
            //     )
            //     .then(res=>$scope.get_data(),err=>console.log(err))
            
            $scope.is_interested = (challenge)=>$scope.interested_ids && $scope.interested_ids.indexOf(challenge.id) > -1
 
        }]
    }
}]



