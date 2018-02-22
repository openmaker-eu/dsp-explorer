import * as _ from 'lodash'
import * as d3 from 'd3';


let template = `
    <div class="col-md-12">
        <h1>
            {$ project.name $}
            <button class="btn custom-button pull-right margin-left-10" data-toggle="modal" data-target="#deleteProjectModal">Delete</button>
            <a href="{$ '/profile/project/'+project.id $}" class="btn custom-button pull-right margin-left-10">Edit</a>
            <a href="/profile" class="btn custom-button pull-right">Back</a>
        </h1>
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
                       <p>Are you sure do you want to delete your account?</p>
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
                    // Todo move to profile page
                    $window.location.href = '/profile';
                    $scope.$apply(()=>$(window).trigger('resize'))
                })
            }
            $scope.get_data($scope.url)
        }]
    }
}]



