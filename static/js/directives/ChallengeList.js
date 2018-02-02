import * as _ from 'lodash'
import * as d3 from 'd3';

let template = `

    <div class="col-md-12 col-xs-12" ng-repeat="challenge in challenges">
        <img class="col-md-3" ng-src="/media/{$ challenge.challenge_picture $}" alt="">
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
        controller : ['$scope', '$http', '$rootScope', function($scope, $http, $rootScope){
            $http.get('/api/v1.3/challenge/').then(
                res=>{ console.log(res); $scope.challenges = res.data.results || [] },
                err=>console.log('Error: ', err)
            )
        }]
    }
}]



