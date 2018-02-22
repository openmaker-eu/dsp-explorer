import * as _ from 'lodash'
import * as d3 from 'd3';


let template = `
    <div class="col-md-10 col-md-offset-1 col-sm-10 col-sm-offset-1 col-xs-12 margin-top-20 margin-bottom-30">
        <h1>
            {$ project.name $}
            <button ng-if="profileid == project.profile.id" class="btn custom-button pull-right margin-left-10" data-toggle="modal" data-target="#deleteProjectModal">Delete</button>
            <a ng-if="profileid == project.profile.id" href="{$ '/profile/project/'+project.id $}" class="btn custom-button pull-right margin-left-10">Edit</a>
            <a href="/profile" class="btn custom-button pull-right">Back</a>
        </h1>
        <div class="row Aligner">
            <div class="col-sm-6 col-sm-offset-0 col-md-6 col-md-offset-0 col-xs-12">
                <div class="col-md-8 col-md-offset-4">
                <circle-image src="{$ project.picture $}"></circle-image>
                </div>
            </div>
            <div class="col-md-6 col-sm-6 col-xs-12">
                <div style="padding-left:5%;">
                    <p><i class="glyphicon glyphicon-globe"></i>&nbsp;<a ng-href="https://{$ project.project_url $}" target="_blank">{{ project.project_url }}</a></p>
                    <p><i class="glyphicon glyphicon-time"></i>&nbsp;{{ project.start_date | date:'yyyy-MM-dd' }}</p>
                    <p ng-if="project.end_date"><i class="glyphicon glyphicon-time"></i>&nbsp;{{ project.end_date | date:'yyyy-MM-dd' }}</p>
                    <p ng-if="!project.end_date"><i class="glyphicon glyphicon-time"></i>&nbsp;Ongoing project</p>
                    <p>
                        <i class="fa fa-fw fa-hashtag"></i>&nbsp;
                        <i ng-repeat="tag in project.tags"><span>{{ tag.name }}</span>&nbsp;&nbsp;</i>
                    </p>
                </div>
            </div>
        </div>
        <div class="row margin-top-30">
            <div class="col-md-12">
                <div class="well-red">Description</div>
            </div>
            <div class="col-md-12">
                <p style="margin-bottom:20px;">{{ project.description }}</p>
            </div>
            <div class="col-md-6">
                <div class="well-red">Owner</div>
            </div>
            <div class="col-md-6">
                <div class="well-red">Collaborators</div>
            </div>
            <div class="col-md-6">
                <div class="col-md-6">
                    <circle-image src="{$ project.profile.picture $}" style="width:40%;"></circle-image>
                </div>
                <div class="col-md-6">
                    <h4 class=""> {$ project.profile.user.first_name $} {$ project.profile.user.last_name $}</h4>
                    <p class=""> as: {{project.creator_role}} </p>
                </div>
            </div>
        </div>
    </div>
    <div class="modal fade" id="deleteProjectModal" tabindex="-1" role="dialog" aria-labelledby="deleteProjectModal">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <form ng-submit="delete_project(url)">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                        <h4 class="modal-title" id="myModalLabel">Project deletion</h4>
                    </div>
                    <div class="modal-body">
                       <p>This operation cannot be reverted, You will permanenlty loose all your project data saved to OpenMaker Explorer</p>
                       <p>Are you sure do you want to delete your project?</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-danger" data-dismiss="modal">No, Close</button>
                        <input type="submit" class="btn btn-default" value="Yes, delete my project">
                    </div>
                </form>
            </div>
        </div>
    </div>
`

export default [function(){
    return {
        template:template,
        scope: { projectid : '=', profileid : '=' },
        controller : ['$scope', '$http', '$window', function($scope, $http, $window) {

            $scope.url = '/api/v1.3/project/' + $scope.projectid
            $scope.projects = []

            console.log($scope.profileid)
            
            $scope.get_data = (url) => {
                $http.get(url).then(res => {
                    $scope.project = res.data.result[0] || ''
                    console.log($scope.project)
                    $scope.$apply(()=>$(window).trigger('resize'))
                })
            }
            $scope.delete_project = (url) => {
            console.log(url)
                $http.delete(url).then(res => {
                    console.log(res)
                    $window.location.href = '/profile';
                    $scope.$apply(()=>$(window).trigger('resize'))
                })
            }
            $scope.get_data($scope.url)
        }]
    }
}]



