import * as _ from 'lodash'
import * as d3 from 'd3';
let template = `
    <div class="col-md-12" ng-if="projects.length == 0">
        <h2>
            No Projects
        </h2>
    </div>
    <div class="col-md-3 col-sm-3 col-xs-12"
        ng-repeat="project in projects"
        style="margin-bottom:1%; margin-top: 1%;">
        <div class="card margin-bottom-20">
            <a href="{$ '/profile/project/'+project.id+'/detail' $}" class="card-image" style="border-bottom:solid 1px rgba(160, 160, 160, 0.2);">
                <div class="card-image" style="border-bottom:solid 1px rgba(160, 160, 160, 0.2);">
                    <img style="min-width:100%;" ng-src="{$ project.picture $}" class="img-responsive">
                </div>
            </a>
            <div class="card-content"><h5>{$ project.name $}</h5></div>
            <div class="card-action" style="height: auto;">
                <div class="row">
                    <div class="col-md-12">
                        <!--<p>{$ project.description | limitTo: 60 $} {$ feed.summary.length > 60 ? '...' : '' $}</p>-->
                        <p>
                            <i ng-repeat="tag in project.tags | limitTo: 2">
                                <strong>#</strong>
                                <span>{$ tag.name $}</span>
                            </i>
                            <span ng-if="project.tags.length > 2"></span>
                        </p>
                        <p>
                            <i class="glyphicon glyphicon-thumbs-up"
                                ng-class="{ 'text-red': project.is_interested, 'text-grey': !project.is_interested }"
                                uib-tooltip="{$ project.is_interested ? 'You are interested in this project': 'Go to the detail page to show interest in this Challenge' $}"
                                tooltip-placement="right"
                            ></i>
                            Interested: {$ project.interested.length $}<br>
                        </p>
                    </div>
                    <div class="col-md-12">
                        <hr>
                    </div>
                    <div class="col-md-12 text-right">
                        <a href="{$ '/profile/project/'+project.id+'/detail' $}"><p>Read more <i class="glyphicon glyphicon-new-window"></i></p></a>
                    </div>
                </div>
            </div>
        </div>
    </div>
`

export default [function(){
    return {
        template:template,
        scope: {profileid: '=',requestprofileid: '='},
        controller : ['$scope', '$http', 'toastr', function($scope, $http, toastr) {

            let url = ''
            $scope.projects = []

            console.log('profileid: ' + $scope.profileid)
            console.log('requestprofileid: ' + $scope.requestprofileid)

            $scope.get_data = (url) => {
                $http.get(url).then(res => {

                    $scope.projects = res.data.result || []

                    console.log('projects')
                    console.log($scope.projects)

                    $scope.projects = _.map($scope.projects, el =>{
                        el.is_interested = _.filter(el.interested, {id:$scope.requestprofileid}).length > 0
                        return el
                    })

                    $scope.$apply(()=>$(window).trigger('resize'))
                })
            }

            $scope.$watch('profileid', (new_data, old_data) => {
                console.log('new data: ' + new_data);
                $scope.profileid = new_data
                url = '/api/v1.3/profile/' + $scope.profileid + '/projects/'
                $scope.get_data(url)
            })

            $scope.is_interested = (project) => $scope.interested_ids && $scope.interested_ids.indexOf(project.id) > -1
        }]
    }
}]



