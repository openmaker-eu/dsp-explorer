import * as _ from 'lodash'
import * as d3 from 'd3';

let template = `
    <form class="col-md-12">
        <div class="col-md-6 col-md-offset-3">
            <div class="form-group">
                <div class="col-lg-4 col-lg-offset-4 col-md-6 col-md-offset-3 col-xs-6 col-xs-offset-3 text-center" >

                    <button class="btn custom-button margin-bottom-10" ng-click="profileImageUpload();">Choose Image</button>

                    <div ng-if="image_model.src" class="thumbnail" id="profile-image-div" >
                        <img ng-src="{$ image_model.src $}"/>
                    </div>

                    <input id="profile-image-input"
                            class="hidden"
                            input_file_model="image_model.src"
                            type="file"
                            name="profile_img"
                            onchange="angular.element(this).scope().load_file_data(this.files)"
                            ng-model="data.project_image"/>
                </div>
            </div>
        <div class="form-group">
            <input type="text" class="form-control" id="project_name" placeholder="Insert project name" ng-model="data.project_name" required>
        </div>
        <div class="form-group">
            <textarea type="text" rows="10" class="form-control" id="description" placeholder="Insert a description" ng-model="data.project_description" required></textarea>
        </div>
        <div class="form-group">
            <p>Start date</p>
            <input type="date" ng-model="data.project_start_date" required/>
            <div ng-if="!data.project_ongoing">
                <p class="margin-top-10">End date</p>
                <input type="date" ng-model="data.project_end_date" required/>
            </div>
            <p class="margin-top-10">Ongoing?</p>
            <input type="checkbox" aria-label="Ongoing" ng-model="data.project_ongoing" ng-click="push_bottom();">
        </div>
        <div class="form-group">
            <input type="text" class="form-control" id="role" placeholder="Insert your role" ng-model="data.project_creator_role" required/>
        </div>
        <div class="form-group">
            <input type="text" class="form-control" id="project_url" placeholder="Insert your project url" ng-model="data.project_url" required/>
        </div>
        <div class="form-group">
            <p>Enter up to 5 keywords about your project</p>
            <ui-select
                       multiple tagging
                       tagging-label="" tagging-tokens="SPACE|ENTER|,|/|<|>|{|}|^"
                       sortable="true"
                       spinner-enabled="true"
                       ng-class="{'form-control':true}"
                       ng-model="data.project_av_tags"
                       title="Choose a tag *" limit="5"
            >

                <ui-select-match placeholder="Type a tag and press enter">
                    {$ $item $}
                </ui-select-match>

                <ui-select-choices repeat="tag in av_tags.available | filter:$select.search track by $index">
                    <div ng-bind-html="tag | highlight: $select.search"></div>
                </ui-select-choices>

            </ui-select><br/>
            <input type="hidden" name="tags" ng-value="data.project_av_tags" required/>
        </div>
        <p class="small">* All the fields are required</p>
        <button type="submit" class="btn custom-button margin-bottom-10 pull-right margin-left-10" ng-click="create_or_update_project()">
            <span ng-if="method == 'PUT'">Create</span>
            <span ng-if="method == 'POST'">Update</span>
        </button>
        <a class="btn custom-button margin-bottom-10 pull-right" href="/profile">Back</a>
    </form>
`

export default [function(){
    return {
        template:template,
        scope: { projectid : '=', tags: '=' },
        controller : ['$scope', '$http', '$sce', function($scope, $http, $sce){

        // form data
        $scope.data = {}

        // action based on create or update
        if ($scope.projectid) {
            $scope.method = 'POST'
            $scope.url = '/api/v1.3/project/' + $scope.projectid
            // fill the template form with project information
        } else {
            $scope.method = 'PUT'
            $scope.url = '/api/v1.3/project/'
            // new project insert
        }

        $scope.load_file_data = function (files) {
            $scope.data.project_image = files
        };

        $scope.create_or_update_project = () => {
            $http({method: $scope.method, url: $scope.url, data: $scope.data}).then(function(response) {
                //
            }, function(response) {
                //
            });
        }

        // project image
        $scope.profileImageUpload = n=>$('#profile-image-input').trigger('click')

        // tags
        $scope.av_tags={ available:  $scope.tags  }

        // keep pushed
        $scope.push_bottom = () => {
            $scope.re_render
        }
 
        }]
    }
}]



